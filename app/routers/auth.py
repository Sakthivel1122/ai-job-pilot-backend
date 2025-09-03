from fastapi import APIRouter, HTTPException, status
from app.models.user import User
from typing import List
from app.services.auth import SignupRequest, create_user, login_user
from app.schemas.user import LoginRequest

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
