from fastapi import HTTPException, Requests
from functools import wraps
from typing import Dict, Callable
import time
from collections import defaultdict

# Simple in-memory rate limiter for development
class RateLimiter:
    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)
    async def check_rate_limit(self, key: str, limit: int, window: int) -> bool:
        current_time = time.time()
        if key in self.requests:
            # Remove old requests
            self.requests[key] = [t for t in self.requests[key] if current_time - t < window]
            if len(self.requests[key]) >= limit:
                return False
        self.requests[key].append(current_time)
        return True
rate_limiter = RateLimiter()

def rate_limit(limit: int = 60, window: int = 60):
    """Decorator for rate limiting endpoints"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract requests from args or kwargs
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            if request:
                client_ip = request.client.host
                key = f"{client_ip}:{func.__name__}"
                if not await rate_limiter.check_rate_limit(key, limit, window):
                    raise HTTPException(
                        status_code = 429,
                        detail = f"Rate limit exceeded. Limit: {limit} requests per {window} seconds"
                    )
            return await func(*args, **kwargs)
        return wrapper
    return decorator