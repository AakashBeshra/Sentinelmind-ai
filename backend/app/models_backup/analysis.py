from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base

class AnalysisType(str, enum.Enum):
    SENTIMENT = "sentiment"
    EMOTION = "emotion"
    TOXICITY = "toxicity"
    COMPREHENSIVE = "comprehensive"

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Input data
    original_text = Column(Text, nullable=False)
    cleaned_text = Column(Text)
    language = Column(String(10))
    
    # Analysis results
    analysis_type = Column(Enum(AnalysisType), default=AnalysisType.COMPREHENSIVE)
    sentiment_label = Column(String(20))
    sentiment_confidence = Column(Float)
    sentiment_scores = Column(JSON)  # Store probabilities
    
    # Emotion detection
    emotions = Column(JSON)  # Store emotion scores
    dominant_emotion = Column(String(20))
    emotion_confidence = Column(Float)
    
    # Additional analysis
    toxicity_score = Column(Float)
    is_toxic = Column(Boolean, default=False)
    entities = Column(JSON)  # Named entities detected
    
    # Metadata
    processing_time_ms = Column(Float)
    model_version = Column(String(50))
    batch_id = Column(String(100), index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="analyses")
    feedback = relationship("Feedback", back_populates="analysis", uselist=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "text": self.original_text,
            "sentiment": self.sentiment_label,
            "sentiment_confidence": self.sentiment_confidence,
            "emotions": self.emotions,
            "dominant_emotion": self.dominant_emotion,
            "toxicity": self.is_toxic,
            "processing_time_ms": self.processing_time_ms,
            "timestamp": self.created_at.isoformat()
        }