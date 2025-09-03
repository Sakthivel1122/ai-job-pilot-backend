from fastapi import Header, HTTPException
from app.config import settings
from typing import Optional

API_KEY = settings.CHAT_BOT_API_KEY

async def verify_chat_bot_api_key(x_api_key: Optional[str] = Header(None)):
    return
    if x_api_key is None:
        raise HTTPException(
            status_code=401,
            detail="Missing API key. Please include 'X-API-KEY' in headers."
        )

    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key provided."
        )
