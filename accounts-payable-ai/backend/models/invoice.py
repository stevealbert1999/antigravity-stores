from pydantic import BaseModel


class Invoice(BaseModel):
    invoice_id: str
    vendor: str
    amount: float
    due_days: int
    po_match: bool
    duplicate_detected: bool


class InvoiceBatch(BaseModel):
    invoices: list[Invoice]
