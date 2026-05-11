import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Header, HTTPException

API_KEY = os.getenv("LEDGERGUARD_API_KEY", "dev-ledgerguard-key")
TOKEN_TTL_HOURS = int(os.getenv("LEDGERGUARD_TOKEN_TTL_HOURS", "8"))

DEMO_USERS = {
    "ap.manager@ledgerguard.local": {
        "password": "demo-password",
        "role": "ap_manager",
        "tenant_id": "demo-tenant"
    },
    "controller@ledgerguard.local": {
        "password": "demo-password",
        "role": "controller",
        "tenant_id": "demo-tenant"
    }
}

TOKENS = {}


def require_api_key(x_api_key: str = Header(default="")):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return {"auth_type": "api_key", "role": "system", "tenant_id": "default"}


def create_token(email: str) -> str:
    token = f"demo-token-{email}-{int(datetime.now(timezone.utc).timestamp())}"
    expires_at = datetime.now(timezone.utc) + timedelta(hours=TOKEN_TTL_HOURS)
    user = DEMO_USERS[email]
    TOKENS[token] = {
        "email": email,
        "role": user["role"],
        "tenant_id": user["tenant_id"],
        "expires_at": expires_at
    }
    return token


def verify_login(email: str, password: str) -> Optional[dict]:
    user = DEMO_USERS.get(email)
    if not user or user["password"] != password:
        return None
    token = create_token(email)
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in_hours": TOKEN_TTL_HOURS,
        "user": {
            "email": email,
            "role": user["role"],
            "tenant_id": user["tenant_id"]
        }
    }


def require_user(authorization: str = Header(default="")):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.replace("Bearer ", "", 1)
    session = TOKENS.get(token)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid token")
    if session["expires_at"] < datetime.now(timezone.utc):
        TOKENS.pop(token, None)
        raise HTTPException(status_code=401, detail="Expired token")
    return session
