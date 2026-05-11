from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from auth import require_user, verify_login

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(request: LoginRequest):
    session = verify_login(request.email, request.password)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return session


@router.get("/me")
def me(user=Depends(require_user)):
    return {
        "user": {
            "email": user["email"],
            "role": user["role"],
            "tenant_id": user["tenant_id"],
        }
    }
