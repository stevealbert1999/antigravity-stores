from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI(title="LedgerGuard AI API")

AUDIT_LOG = []


class Invoice(BaseModel):
    invoice_id: str
    vendor: str
    amount: float
    due_days: int
    po_match: bool
    duplicate_detected: bool


class InvoiceBatch(BaseModel):
    invoices: List[Invoice]


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

    if len(reasons) == 0:
        reasons.append("no_critical_anomalies")

    result = {
        "invoice_id": invoice.invoice_id,
        "vendor": invoice.vendor,
        "risk": risk,
        "risk_score": score,
        "reasons": reasons,
        "recommendation": recommendation,
        "requires_human_approval": True,
        "analyzed_at": datetime.utcnow().isoformat()
    }

    AUDIT_LOG.append(result)

    return result


@app.get("/")
def root():
    return {
        "product": "LedgerGuard AI",
        "status": "running"
    }


@app.post("/invoices/analyze")
def analyze(invoice: Invoice):
    return analyze_invoice(invoice)


@app.post("/invoices/batch-analyze")
def batch_analyze(batch: InvoiceBatch):
    return {
        "results": [analyze_invoice(invoice) for invoice in batch.invoices]
    }


@app.get("/audit-log")
def audit_log():
    return {
        "entries": AUDIT_LOG,
        "count": len(AUDIT_LOG)
    }
