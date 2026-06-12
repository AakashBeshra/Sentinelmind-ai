from fastapi import APIRouter, Depends
from app.api.deps import get_current_active_user
from app.models.user import User
router = APIRouter()
@router.post("/analyze")
async def analyze_voice(
    current_user: User = Depends(get_current_active_user)
):
    """Analyze voice sentiment"""
    return {"message": "Voice analysis endpoint"}