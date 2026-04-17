from fastapi import APIRouter, Depends, Request
from app.models.user import User
from typing import List
from app.services.auth import SignupRequest, create_user, login_user, refresh_token_service
from app.schemas.user import LoginRequest
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/signup")
async def signup(data: SignupRequest, request: Request):
    result = await create_user(data=data,request=request, role="user")
    return result

@router.post("/create_admin")
async def signup(data: SignupRequest, request: Request):
    result = await create_user(data=data, request=request, role="admin")
    return result

@router.post("/login")
async def login(data: LoginRequest, request: Request):
    result = await login_user(data=data, request=request)
    return result

@router.post("/oauth")
async def login(data: LoginRequest, request: Request):
    result = await login_user(data=data, request=request)
    return result

@router.get("/refresh-token")
async def login(current_user: User = Depends(get_current_user)):
    result = await refresh_token_service(current_user)
    return result
