from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean
from sqlalchemy.schema import UniqueConstraint
from datetime import datetime

from app.core.database import Base

class ModelMetadata(Base):
    __tablename__ = "model_metadata"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100), nullable=False)
    model_version = Column(String(50), nullable=False)
    
    # Model metrics
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    
    # Training info
    training_date = Column(DateTime)
    training_epochs = Column(Integer)
    training_samples = Column(Integer)
    validation_samples = Column(Integer)
    
    # Model config
    model_config = Column(JSON)
    model_path = Column(String(500))
    
    is_active = Column(Boolean, default=False)
    is_deployed = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint('model_name', 'model_version', name='uq_model_version'),
    )