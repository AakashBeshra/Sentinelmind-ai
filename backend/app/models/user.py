from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from datetime import datetime
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
    
    api_calls_limit = Column(Integer, default=1000)
    api_calls_used = Column(Integer, default=0)
    
    premium_until = Column(DateTime, nullable=True)
    
    total_analyses = Column(Integer, default=0)
    last_active = Column(DateTime, default=datetime.utcnow)
    
    last_password_change = Column(DateTime, default=datetime.utcnow)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def is_premium(self):
        return self.premium_until and self.premium_until > datetime.utcnow()
    
    def set_password(self, password: str):
        salt = bcrypt.gensalt()
        self.hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.hashed_password.encode('utf-8'))