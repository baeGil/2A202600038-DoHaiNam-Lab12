"""
Rate limiting module - Redis-based sliding window
"""
import time
import redis
from fastapi import HTTPException
from app.config import settings

redis_client = None

def get_redis():
    global redis_client
    if redis_client is None:
        if not settings.redis_url:
            return None
        try:
            redis_client = redis.from_url(settings.redis_url, decode_responses=True)
            redis_client.ping()
        except Exception:
            return None
    return redis_client

def check_rate_limit(user_id: str):
    """
    Check and enforce rate limit using Redis sorted set (sliding window).
    
    Raises HTTPException(429) if rate limit exceeded.
    """
    r = get_redis()
    if r is None:
        return  # Fallback: skip rate limiting if Redis not available
    
    now = time.time()
    window_key = f"rate_limit:{user_id}"
    
    # Remove old requests (older than 60 seconds)
    r.zremrangebyscore(window_key, 0, now - 60)
    
    # Count current requests
    count = r.zcard(window_key)
    
    if count >= settings.rate_limit_per_minute:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded: {settings.rate_limit_per_minute} req/min",
            headers={"Retry-After": "60"},
        )
    
    # Add current request
    r.zadd(window_key, {str(now): now})
    r.expire(window_key, 60)
