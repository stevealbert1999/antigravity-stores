from datetime import datetime


def analyze_invoice_risk(invoice):
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

    if not reasons:
        reasons.append("no_critical_anomalies")

    return {
        "invoice_id": invoice.invoice_id,
        "vendor": invoice.vendor,
        "amount": invoice.amount,
        "risk": risk,
        "risk_score": score,
        "reasons": reasons,
        "recommendation": recommendation,
        "requires_human_approval": True,
        "approval_status": "pending",
        "analyzed_at": datetime.utcnow().isoformat(),
    }
