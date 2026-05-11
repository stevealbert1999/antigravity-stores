from fastapi import APIRouter, Depends

from auth import require_user
from db import list_audit_events

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/log")
def audit_log(user=Depends(require_user)):
    events = list_audit_events()
    return {
        "entries": events,
        "count": len(events),
    }
