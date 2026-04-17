"""
Authentication module - API key verification
"""
from fastapi import Header, HTTPException
from app.config import settings

api_key_header = Header(..., name="X-API-Key", auto_error=False)

def verify_api_key(x_api_key: str = api_key_header) -> str:
    """
    Verify API key from header.
    
    Returns user_id (using first 8 chars of key as user identifier).
    Raises HTTPException(401) if invalid.
    """
    if not x_api_key or x_api_key != settings.agent_api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key. Include header: X-API-Key: <key>",
        )
    return x_api_key[:8]  # Use first 8 chars as user ID
