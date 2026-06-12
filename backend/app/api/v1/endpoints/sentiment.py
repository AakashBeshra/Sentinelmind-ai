from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from pydantic import BaseModel
from app.api.deps import get_current_active_user
from app.models.user import User
from app.services.sentiment_service import SentimentService
router = APIRouter()
class SentimentRequest(BaseModel):
	text: str
	language: Optional[str] = "auto"
	include_emotions: bool = True
	include_toxicity: bool = False
@router.post("/analyze")
async def analyze_sentiment(
	request: SentimentRequest,
	current_user: User = Depends(get_current_active_user)
):
	"""Analyze sentiment of text"""
	result = await SentimentService.analyze(
		request.text,
		language=request.language,
		include_emotions=request.include_emotions,
		include_toxicity=request.include_toxicity
	)
	return result