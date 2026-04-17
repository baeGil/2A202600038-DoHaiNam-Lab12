"""
Cost guard module - Redis-based per-user budget tracking
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

def check_budget(user_id: str):
    """
    Check if user has exceeded monthly budget.
    
    Raises HTTPException(402) if budget exceeded.
    """
    r = get_redis()
    if r is None:
        return  # Fallback: skip budget check if Redis not available
    
    current_month = time.strftime("%Y-%m")
    cost_key = f"cost:{user_id}:{current_month}"
    
    current_cost = float(r.get(cost_key) or 0)
    
    if current_cost >= settings.monthly_budget_usd:
        raise HTTPException(402, "Monthly budget exhausted. Try next month.")

def record_cost(user_id: str, input_tokens: int, output_tokens: int):
    """
    Record cost for user in Redis.
    
    Cost calculation: $0.00015 per 1K input tokens, $0.0006 per 1K output tokens.
    """
    r = get_redis()
    if r is None:
        return  # Fallback: skip recording if Redis not available
    
    current_month = time.strftime("%Y-%m")
    cost_key = f"cost:{user_id}:{current_month}"
    
    cost = (input_tokens / 1000) * 0.00015 + (output_tokens / 1000) * 0.0006
    
    r.incrbyfloat(cost_key, cost)
    r.expire(cost_key, 31 * 86400)  # 31 days

def get_user_cost(user_id: str) -> float:
    """
    Get current month's cost for user.
    """
    r = get_redis()
    if r is None:
        return 0.0
    
    current_month = time.strftime("%Y-%m")
    cost_key = f"cost:{user_id}:{current_month}"
    
    return float(r.get(cost_key) or 0)
