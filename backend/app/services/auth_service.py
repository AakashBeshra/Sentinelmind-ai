from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from jose import jwt, JWTError

from app.models.user import User
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.core.config import settings
from app.core.redis_client import redis_client

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def authenticate_user(self, email: str, password: str) -> User | None:
        """Authenticate user with email and password"""
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            user.failed_login_attempts += 1
            await self.db.commit()
            return None
        
        # Reset failed attempts on successful login
        user.failed_login_attempts = 0
        user.last_active = datetime.utcnow()
        await self.db.commit()
        
        return user
    
    async def refresh_access_token(self, refresh_token: str) -> dict | None:
        """Generate new access token from refresh token"""
        try:
            payload = jwt.decode(
                refresh_token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            
            user_id = payload.get("sub")
            token_type = payload.get("type")
            
            if not user_id or token_type != "refresh":
                return None
            
            # Check if token is blacklisted
            is_blacklisted = await redis_client.get(f"blacklist:{refresh_token}")
            if is_blacklisted:
                return None
            
            query = select(User).where(User.id == int(user_id))
            result = await self.db.execute(query)
            user = result.scalar_one_or_none()
            
            if not user or not user.is_active:
                return None
            
            # Create new tokens
            access_token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
            new_refresh_token = create_refresh_token(data={"sub": str(user.id)})
            
            # Blacklist old refresh token
            await redis_client.setex(f"blacklist:{refresh_token}", 86400, "true")
            
            return {
                "access_token": access_token,
                "refresh_token": new_refresh_token,
                "token_type": "bearer"
            }
            
        except JWTError:
            return None
    
    async def logout(self, user_id: int, token: str) -> bool:
        """Logout user by blacklisting token"""
        # Add token to blacklist
        await redis_client.setex(f"blacklist:{token}", 86400, "true")
        return True