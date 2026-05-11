from models.invoice import Invoice
from services.risk_engine import analyze_invoice_risk


def test_duplicate_invoice_is_high_risk():
    invoice = Invoice(
        invoice_id="INV-1",
        vendor="ACME",
        amount=12500,
        due_days=-5,
        po_match=False,
        duplicate_detected=True,
    )

    result = analyze_invoice_risk(invoice)

    assert result["risk"] == "high"
    assert result["recommendation"] == "block_and_review"
    assert "possible_duplicate_invoice" in result["reasons"]


def test_clean_invoice_is_low_risk():
    invoice = Invoice(
        invoice_id="INV-2",
        vendor="ACME",
        amount=100,
        due_days=10,
        po_match=True,
        duplicate_detected=False,
    )

    result = analyze_invoice_risk(invoice)

    assert result["risk"] == "low"
    assert result["recommendation"] == "approve_standard"
    assert result["reasons"] == ["no_critical_anomalies"]
