from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import hashlib
import json
import base64

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    username: str
    password: str
    full_name: str = ""

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain: str, hashed: str) -> bool:
    return hash_password(plain) == hashed

def create_token(user_id: int) -> str:
    token_data = {
        "sub": user_id,
        "exp": (datetime.utcnow() + timedelta(days=1)).isoformat()
    }
    return base64.b64encode(json.dumps(token_data).encode()).decode()

@router.post("/register")
async def register(data: RegisterRequest):
    return {"message": "Registration endpoint - implement database", "data": data.dict()}

@router.post("/login")
async def login(data: LoginRequest):
    return {"access_token": create_token(1), "token_type": "bearer"}