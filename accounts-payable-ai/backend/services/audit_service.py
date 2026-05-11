import json
from db import insert_audit_event


def log_event(event: str, invoice_id: str, payload: dict, created_at: str):
    insert_audit_event(
        event=event,
        invoice_id=invoice_id,
        payload=json.dumps(payload),
        created_at=created_at,
    )
