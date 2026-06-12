from fastapi import APIRouter, Depends
from typing import Optional
from app.api.deps import get_current_user
from app.models.user import User
router = APIRouter()
@router.get("/dashboard")
async def get_dashobard_stats(
    current_user: User = Depends(get_current_user)
):
    """Get dashobard statistics"""
    return {"message": "Dashboard stats endpoint"}
