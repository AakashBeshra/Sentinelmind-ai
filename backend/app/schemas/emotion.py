from pydantic import BaseModel, Field
from typing import Dict, Optional

class EmotionRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    language: Optional[str] = "auto"

class EmotionResponse(BaseModel):
    dominant_emotion: str
    dominant_confidence: float
    all_emotions: Dict[str, float]
    intensity: str  # low, medium, high
    recommendation: Optional[str] = None

class EmotionTimeline(BaseModel):
    timestamp: float
    emotions: Dict[str, float]