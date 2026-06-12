from functools import lru_cache
from app.core.redis_client import redis_client
import hashlib
import json

class InferenceCache:
    def __init__(self, cache_ttl: int = 3600):
        self.cache_ttl = cache_ttl
    
    def get_cache_key(self, text: str, task: str) -> str:
        """Generate cache key from text"""
        text_hash = hashlib.md5(text.encode()).hexdigest()
        return f"{task}:{text_hash}"
    
    async def get_cached_result(self, text: str, task: str):
        """Get cached inference result"""
        cache_key = self.get_cache_key(text, task)
        cached = await redis_client.get(cache_key)
        
        if cached:
            return json.loads(cached)
        return None
    
    async def cache_result(self, text: str, task: str, result: dict):
        """Cache inference result"""
        cache_key = self.get_cache_key(text, task)
        await redis_client.setex(cache_key, self.cache_ttl, json.dumps(result))
    
    @lru_cache(maxsize=1000)
    def cache_local(self, text: str, task: str):
        """Local in-memory cache"""
        return None