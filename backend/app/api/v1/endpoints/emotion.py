from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from pydantic import BaseModel
from app.api.deps import get_current_active_user
from app.models.user import User
from app.services.emotion_service import EmotionService
router = APIRouter()
class EmotionRequest(BaseModel):
    text: str
    language: Optional[str] = "auto"

@router.post("/detect")
async def detect_emotions(
    request: EmotionRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Detect emotions in text"""
    result = await EmotionService.detect_emotions(request.text)
    return result
