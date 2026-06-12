from functools import wraps
from fastapi import HTTPException, Request
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, Tuple
import time

from app.core.redis_client import redis_client
from app.core.config import settings

class RateLimiter:
    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)
    
    async def check_rate_limit(self, key: str, limit: int, window: int) -> bool:
        """Check if rate limit is exceeded using Redis"""
        redis_key = f"rate_limit:{key}"
        current = time.time()
        window_start = current - window
        
        # Get current count from Redis
        count = await redis_client.get(redis_key)
        
        if count is None:
            await redis_client.setex(redis_key, window, 1)
            return True
        
        count = int(count)
        if count >= limit:
            return False
        
        await redis_client.incr(redis_key)
        return True
    
    async def get_remaining(self, key: str, limit: int, window: int) -> int:
        """Get remaining requests allowed"""
        redis_key = f"rate_limit:{key}"
        count = await redis_client.get(redis_key)
        
        if count is None:
            return limit
        
        count = int(count)
        return max(0, limit - count)

rate_limiter = RateLimiter()

def rate_limit(limit: int = 60, window: int = 60):
    """Decorator for rate limiting endpoints"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if request:
                client_ip = request.client.host
                user_id = getattr(request.state, "user_id", None)
                key = f"{user_id or client_ip}:{func.__name__}"
                
                allowed = await rate_limiter.check_rate_limit(key, limit, window)
                if not allowed:
                    raise HTTPException(
                        status_code=429,
                        detail=f"Rate limit exceeded. Limit: {limit} requests per {window} seconds"
                    )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator