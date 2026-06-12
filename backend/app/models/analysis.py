from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text, Boolean
from datetime import datetime

from app.core.database import Base

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    original_text = Column(Text, nullable=False)
    cleaned_text = Column(Text)
    language = Column(String(10))
    
    sentiment_label = Column(String(20))
    sentiment_confidence = Column(Float)
    sentiment_scores = Column(JSON)
    
    emotions = Column(JSON)
    dominant_emotion = Column(String(20))
    
    toxicity_score = Column(Float)
    is_toxic = Column(Boolean, default=False)
    
    processing_time_ms = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)