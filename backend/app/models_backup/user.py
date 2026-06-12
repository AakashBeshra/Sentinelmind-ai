from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
import enum
import bcrypt

from app.core.database import Base

class UserRole(str, enum.Enum):
    USER = "user"
    PREMIUM = "premium"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    full_name = Column(String(100))
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    avatar_url = Column(String(500))
    
    # Account limits
    api_calls_limit = Column(Integer, default=1000)
    api_calls_used = Column(Integer, default=0)
    
    # Premium features
    premium_until = Column(DateTime, nullable=True)
    
    # Analytics
    total_analyses = Column(Integer, default=0)
    last_active = Column(DateTime, default=datetime.utcnow)
    
    # Security
    last_password_change = Column(DateTime, default=datetime.utcnow)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    analyses = relationship("Analysis", back_populates="user", cascade="all, delete-orphan")
    api_keys = relationship("APIKey", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user")
    
    @hybrid_property
    def is_premium(self):
        return self.premium_until and self.premium_until > datetime.utcnow()
    
    @hybrid_property
    def has_api_access(self):
        return self.is_active and (self.is_premium or self.api_calls_used < self.api_calls_limit)
    
    def set_password(self, password: str):
        salt = bcrypt.gensalt()
        self.hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))
    
    def increment_api_calls(self):
        self.api_calls_used += 1
        self.total_analyses += 1
        self.last_active = datetime.utcnow()