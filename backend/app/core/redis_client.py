import redis.asyncio as redis
import json
from typing import Optional, Any
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self):
        self.client: Optional[redis.Redis] = None
    
    async def connect(self):
        """Establish Redis connection"""
        self.client = await redis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
            encoding="utf-8"
        )
        await self.client.ping()
        logger.info("Connected to Redis")
    
    async def disconnect(self):
        """Close Redis connection"""
        if self.client:
            await self.client.close()
            logger.info("Disconnected from Redis")
    
    async def get(self, key: str) -> Optional[str]:
        """Get value by key"""
        if not self.client:
            return None
        return await self.client.get(key)
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set key-value pair with optional TTL"""
        if not self.client:
            return False
        
        if isinstance(value, dict):
            value = json.dumps(value)
        
        if ttl:
            await self.client.setex(key, ttl, value)
        else:
            await self.client.set(key, value)
        
        return True
    
    async def setex(self, key: str, ttl: int, value: Any):
        """Set with expiration"""
        if isinstance(value, dict):
            value = json.dumps(value)
        await self.client.setex(key, ttl, value)
    
    async def delete(self, key: str) -> int:
        """Delete key"""
        if not self.client:
            return 0
        return await self.client.delete(key)
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        if not self.client:
            return False
        return await self.client.exists(key) > 0
    
    async def incr(self, key: str) -> int:
        """Increment counter"""
        if not self.client:
            return 0
        return await self.client.incr(key)
    
    async def expire(self, key: str, ttl: int) -> bool:
        """Set expiration on key"""
        if not self.client:
            return False
        return await self.client.expire(key, ttl)
    
    async def flushall(self):
        """Clear all keys"""
        if self.client:
            await self.client.flushall()
    
    async def is_healthy(self) -> bool:
        """Check Redis health"""
        try:
            if not self.client:
                return False
            await self.client.ping()
            return True
        except:
            return False

# Singleton instance
redis_client = RedisClient()