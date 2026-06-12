from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from typing import Optional, List
from datetime import datetime, timedelta

from app.models.user import User, UserRole
from app.models.analysis import Analysis
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=get_password_hash(user_data.password),
            role=UserRole.USER,
            created_at=datetime.utcnow()
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        query = select(User).where(User.username == username)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user information"""
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        
        user.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """Change user password"""
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        
        if not verify_password(old_password, user.hashed_password):
            return False
        
        user.hashed_password = get_password_hash(new_password)
        user.last_password_change = datetime.utcnow()
        await self.db.commit()
        
        return True
    
    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        query = select(User).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def delete_user(self, user_id: int) -> bool:
        """Delete a user"""
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        
        await self.db.delete(user)
        await self.db.commit()
        
        return True
    
    async def get_user_analytics(self, user_id: int) -> dict:
        """Get user analytics"""
        # Get total analyses count
        analysis_count_query = select(func.count(Analysis.id)).where(Analysis.user_id == user_id)
        total_analyses = await self.db.execute(analysis_count_query)
        
        # Get sentiment distribution
        sentiment_dist = await self.db.execute(
            select(Analysis.sentiment_label, func.count(Analysis.id))
            .where(Analysis.user_id == user_id)
            .group_by(Analysis.sentiment_label)
        )
        
        return {
            "total_analyses": total_analyses.scalar() or 0,
            "sentiment_distribution": dict(sentiment_dist.all())
        }
    
    async def increment_api_calls(self, user_id: int) -> None:
        """Increment API calls counter"""
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(api_calls_used=User.api_calls_used + 1)
        )
        await self.db.commit()