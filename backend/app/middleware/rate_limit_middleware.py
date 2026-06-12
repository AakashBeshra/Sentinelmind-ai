from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.redis_client import redis_client
import time

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        rate_key = f"rate_limit:{client_ip}"
        
        # Get current count
        current = await redis_client.get(rate_key)
        
        if current and int(current) > 100:  # 100 requests per minute
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        # Increment counter
        await redis_client.incr(rate_key)
        await redis_client.expire(rate_key, 60)
        
        return await call_next(request)