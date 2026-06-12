from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    action = Column(String(50), nullable=False)  # create, update, delete, login, logout, etc.
    resource = Column(String(100))  # user, analysis, api_key, etc.
    resource_id = Column(String(100))
    
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    
    status = Column(String(20))  # success, failure
    error_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")