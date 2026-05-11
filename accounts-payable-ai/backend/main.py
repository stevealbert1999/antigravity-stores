import csv
import io
import json
from datetime import datetime
from typing import List

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from auth import require_api_key, require_user, verify_login
from db import (
    init_db,
    upsert_invoice_result,
    list_invoice_results,
    get_invoice_result,
    insert_audit_event,
    list_audit_events,
    upsert_approval,
)

app = FastAPI(title="LedgerGuard AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


class LoginRequest(BaseModel):
    email: str
    password: str


class Invoice(BaseModel):
    invoice_id: str
    vendor: str
    amount: float
    due_days: int
    po_match: bool
    duplicate_detected: bool


class InvoiceBatch(BaseModel):
    invoices: List[Invoice]


class ApprovalRequest(BaseModel):
    comment: str = ""


def parse_bool(value):
    return str(value).strip().lower() in {"true", "1", "yes", "y", "si", "sí"}


def analyze_invoice(invoice: Invoice, actor: dict):
    risk = "low"
    score = 10
    reasons = []
    recommendation = "approve_standard"

    if invoice.duplicate_detected:
        risk = "high"
        score += 60
        reasons.append("possible_duplicate_invoice")
        recommendation = "block_and_review"

    if not invoice.po_match:
        score += 20
        reasons.append("po_mismatch")
        if risk != "high":
            risk = "medium"
            recommendation = "manual_review"

    if invoice.due_days < 0:
        score += 10
        reasons.append("invoice_overdue")

    if invoice.amount > 10000:
        score += 15
        reasons.append("high_invoice_amount")
        if risk == "low":
            risk = "medium"

    if score >= 80:
        risk = "high"
    elif score >= 35 and risk == "low":
        risk = "medium"

    if len(reasons) == 0:
        reasons.append("no_critical_anomalies")

    result = {
        "invoice_id": invoice.invoice_id,
        "vendor": invoice.vendor,
        "amount": invoice.amount,
        "risk": risk,
        "risk_score": score,
        "reasons": reasons,
        "recommendation": recommendation,
        "requires_human_approval": True,
        "approval_status": "pending",
        "analyzed_at": datetime.utcnow().isoformat()
    }

    upsert_invoice_result(result)
    insert_audit_event(
        event="invoice_analyzed",
        invoice_id=invoice.invoice_id,
        payload=json.dumps({"actor": actor, "result": result}),
        created_at=result["analyzed_at"]
    )
    return result


@app.get("/")
def root():
    return {"product": "LedgerGuard AI", "status": "running", "database": "sqlite_or_postgres", "auth": "bearer_or_api_key"}


@app.post("/auth/login")
def login(request: LoginRequest):
    session = verify_login(request.email, request.password)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return session


@app.get("/auth/me")
def me(user=Depends(require_user)):
    return {"user": {"email": user["email"], "role": user["role"], "tenant_id": user["tenant_id"]}}


@app.post("/invoices/analyze")
def analyze(invoice: Invoice, user=Depends(require_user)):
    return analyze_invoice(invoice, actor=user)


@app.post("/system/invoices/analyze")
def system_analyze(invoice: Invoice, actor=Depends(require_api_key)):
    return analyze_invoice(invoice, actor=actor)


@app.post("/invoices/batch-analyze")
def batch_analyze(batch: InvoiceBatch, user=Depends(require_user)):
    return {"results": [analyze_invoice(invoice, actor=user) for invoice in batch.invoices]}


@app.post("/invoices/upload-csv")
async def upload_csv(file: UploadFile = File(...), user=Depends(require_user)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    content = await file.read()
    text = content.decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))

    required = {"invoice_id", "vendor", "amount", "due_days", "po_match", "duplicate_detected"}
    if not required.issubset(set(reader.fieldnames or [])):
        raise HTTPException(status_code=400, detail=f"CSV must include columns: {sorted(required)}")

    results = []
    for row in reader:
        invoice = Invoice(
            invoice_id=row["invoice_id"],
            vendor=row["vendor"],
            amount=float(row["amount"]),
            due_days=int(row["due_days"]),
            po_match=parse_bool(row["po_match"]),
            duplicate_detected=parse_bool(row["duplicate_detected"]),
        )
        results.append(analyze_invoice(invoice, actor=user))

    return {"count": len(results), "results": results}


@app.get("/invoices/risk-queue")
def risk_queue(user=Depends(require_user)):
    order = {"high": 0, "medium": 1, "low": 2}
    results = sorted(list_invoice_results(), key=lambda x: (order.get(x["risk"], 9), -x["risk_score"]))
    return {"count": len(results), "results": results}


@app.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: str, user=Depends(require_user)):
    result = get_invoice_result(invoice_id)
    if not result:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return result


@app.post("/approvals/{invoice_id}/approve")
def approve_invoice(invoice_id: str, request: ApprovalRequest, user=Depends(require_user)):
    result = get_invoice_result(invoice_id)
    if not result:
        raise HTTPException(status_code=404, detail="Invoice not found")
    timestamp = datetime.utcnow().isoformat()
    approval = {"invoice_id": invoice_id, "status": "approved", "user": user["email"], "comment": request.comment, "timestamp": timestamp}
    upsert_approval(invoice_id=invoice_id, status="approved", user=user["email"], comment=request.comment, timestamp=timestamp)
    insert_audit_event(event="invoice_approved", invoice_id=invoice_id, payload=json.dumps({"actor": user, "approval": approval}), created_at=timestamp)
    return approval


@app.post("/approvals/{invoice_id}/reject")
def reject_invoice(invoice_id: str, request: ApprovalRequest, user=Depends(require_user)):
    result = get_invoice_result(invoice_id)
    if not result:
        raise HTTPException(status_code=404, detail="Invoice not found")
    timestamp = datetime.utcnow().isoformat()
    approval = {"invoice_id": invoice_id, "status": "rejected", "user": user["email"], "comment": request.comment, "timestamp": timestamp}
    upsert_approval(invoice_id=invoice_id, status="rejected", user=user["email"], comment=request.comment, timestamp=timestamp)
    insert_audit_event(event="invoice_rejected", invoice_id=invoice_id, payload=json.dumps({"actor": user, "approval": approval}), created_at=timestamp)
    return approval


@app.get("/audit-log")
def audit_log(user=Depends(require_user)):
    events = list_audit_events()
    return {"entries": events, "count": len(events)}
