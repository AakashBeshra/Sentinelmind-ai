from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

class Feedback(Base):
    __tablename__ = "feedbacks"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id", ondelete="CASCADE"), unique=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Feedback content
    is_correct = Column(Boolean, nullable=True)
    correct_sentiment = Column(String(20), nullable=True)
    correct_emotions = Column(String(200), nullable=True)  # Comma-separated
    
    # Rating
    rating = Column(Integer)  # 1-5 stars
    comment = Column(Text)
    
    # Used for model improvement
    included_in_training = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    analysis = relationship("Analysis", back_populates="feedback")
    user = relationship("User")