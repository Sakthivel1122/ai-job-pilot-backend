from fastapi import APIRouter, Depends
from app.models.user import User
from typing import List
from app.services.auth import SignupRequest, create_user, login_user, refresh_token_service
from app.schemas.user import LoginRequest
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/signup")
async def signup(data: SignupRequest):
    result = await create_user(data)
    return result

@router.post("/login")
async def login(data: LoginRequest):
    result = await login_user(data)
    return result

@router.post("/oauth")
async def login(data: LoginRequest):
    result = await login_user(data)
    return result

@router.get("/refresh-token")
async def login(current_user: User = Depends(get_current_user)):
    result = await refresh_token_service(current_user)
    return result
