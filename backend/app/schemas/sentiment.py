from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, List
from datetime import datetime

class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    language: Optional[str] = "auto"
    include_emotions: bool = True
    include_toxicity: bool = False
    include_entities: bool = False
    
    @validator('text')
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty or only whitespace')
        return v.strip()

class SentimentResponse(BaseModel):
    sentiment: str  # positive, negative, neutral
    confidence: float
    probabilities: Dict[str, float]
    emotions: Optional[Dict[str, float]] = None
    toxicity: Optional[Dict[str, float]] = None
    entities: Optional[List[Dict[str, str]]] = None
    language: str
    processing_time_ms: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class BatchSentimentRequest(BaseModel):
    texts: List[str] = Field(..., max_items=100)
    language: Optional[str] = "auto"
    include_emotions: bool = True
    include_toxicity: bool = False

class BatchSentimentResponse(BaseModel):
    results: List[SentimentResponse]
    batch_id: str
    total_processing_time_ms: float
    successful_count: int
    failed_count: int