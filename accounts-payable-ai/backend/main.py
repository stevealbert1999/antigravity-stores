import csv
import io
from datetime import datetime
from typing import List, Dict

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

app = FastAPI(title="LedgerGuard AI API")

AUDIT_LOG = []
INVOICE_RESULTS: Dict[str, dict] = {}
APPROVALS: Dict[str, dict] = {}


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
    user: str
    comment: str = ""


def parse_bool(value):
    return str(value).strip().lower() in {"true", "1", "yes", "y", "si", "sí"}


def analyze_invoice(invoice: Invoice):
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

    INVOICE_RESULTS[invoice.invoice_id] = result
    AUDIT_LOG.append({"event": "invoice_analyzed", **result})

    return result


@app.get("/")
def root():
    return {"product": "LedgerGuard AI", "status": "running"}


@app.post("/invoices/analyze")
def analyze(invoice: Invoice):
    return analyze_invoice(invoice)


@app.post("/invoices/batch-analyze")
def batch_analyze(batch: InvoiceBatch):
    return {"results": [analyze_invoice(invoice) for invoice in batch.invoices]}


@app.post("/invoices/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
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
        results.append(analyze_invoice(invoice))

    return {"count": len(results), "results": results}


@app.get("/invoices/risk-queue")
def risk_queue():
    order = {"high": 0, "medium": 1, "low": 2}
    results = sorted(INVOICE_RESULTS.values(), key=lambda x: (order.get(x["risk"], 9), -x["risk_score"]))
    return {"count": len(results), "results": results}


@app.post("/approvals/{invoice_id}/approve")
def approve_invoice(invoice_id: str, request: ApprovalRequest):
    if invoice_id not in INVOICE_RESULTS:
        raise HTTPException(status_code=404, detail="Invoice not found")

    approval = {
        "invoice_id": invoice_id,
        "status": "approved",
        "user": request.user,
        "comment": request.comment,
        "timestamp": datetime.utcnow().isoformat()
    }
    APPROVALS[invoice_id] = approval
    INVOICE_RESULTS[invoice_id]["approval_status"] = "approved"
    AUDIT_LOG.append({"event": "invoice_approved", **approval})
    return approval


@app.post("/approvals/{invoice_id}/reject")
def reject_invoice(invoice_id: str, request: ApprovalRequest):
    if invoice_id not in INVOICE_RESULTS:
        raise HTTPException(status_code=404, detail="Invoice not found")

    approval = {
        "invoice_id": invoice_id,
        "status": "rejected",
        "user": request.user,
        "comment": request.comment,
        "timestamp": datetime.utcnow().isoformat()
    }
    APPROVALS[invoice_id] = approval
    INVOICE_RESULTS[invoice_id]["approval_status"] = "rejected"
    AUDIT_LOG.append({"event": "invoice_rejected", **approval})
    return approval


@app.get("/audit-log")
def audit_log():
    return {"entries": AUDIT_LOG, "count": len(AUDIT_LOG)}
