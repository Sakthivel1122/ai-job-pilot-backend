from app.models.user import User
from app.utils.hash import encrypt_password
from app.utils.jwt import generate_tokens
from app.schemas.user import SignupRequest, LoginRequest
from app.utils.response import response
from app.utils.hash import verify_password
from typing import Optional, Literal
from fastapi import APIRouter, Depends, Request
from app.models.auth_log import AuthLog

async def create_user(data: SignupRequest, request: Request, role: Literal["user" , "admin"] = "user") -> dict:
    ip = request.client.host if request else None
    user_agent = request.headers.get("user-agent") if request else None
    existing_user = await User.find_one(User.email == data.email, User.deleted_at == None)
    if existing_user:
        await AuthLog(
            user_id=str(existing_user.id),
            event="signup",
            success=False,
            ip=ip,
            user_agent=user_agent,
            notes="Email already exists"
        ).insert()
        return response (None,"User already exists!", 400)

    try:
        hashed_pwd = encrypt_password(data.password)
        user = User(
            username=data.username,
            email=data.email,
            password=hashed_pwd,
            role=role
        )
        await user.insert()
        await AuthLog(
            user_id=str(user.id),
            event="signup",
            success=True,
            ip=ip,
            user_agent=user_agent,
            notes="Signup Successfull"
        ).insert()
        user_dict = {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
        access_token, refresh_token = generate_tokens(user_dict)
        return response({
                "user_data": user_dict,
                "token": {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            }, "User Signup Successful", 200)

    except Exception as e:
        
        await AuthLog(
            user_id=None,
            event="signup",
            success=False,
            ip=ip,
            user_agent=user_agent,
            notes=f"signup failed error: {str(e)}"
        ).insert()
        return response(None, f"Failed to create user: {str(e)}", 400)

async def login_user(data: LoginRequest, request: Request):
    ip = request.client.host if request else None
    user_agent = request.headers.get("user-agent") if request else None
    existing_user = await User.find_one(User.email == data.email, User.deleted_at == None)

    if existing_user is None:
        await AuthLog(
            user_id=str(existing_user.id),
            event="signup",
            success=False,
            ip=ip,
            user_agent=user_agent,
            notes="Email already exists"
        ).insert()
        return response(None, "User Not Found", 400)
    
    is_valid = verify_password(data.password, existing_user.password)

    if is_valid:
        user_dict = {
            "id": str(existing_user.id),
            "username": existing_user.username,
            "email": existing_user.email,
            "role": existing_user.role
        }
        access_token, refresh_token = generate_tokens(user_dict)
        await AuthLog(
            user_id=str(existing_user.id),
            event="login",
            success=True,
            ip=ip,
            user_agent=user_agent,
            notes="Login Successfull"
        ).insert()

        return response({
                "user_data": user_dict,
                "token": {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            }, "User Signup Successful", 200)
    else:
        await AuthLog(
            user_id=str(existing_user.id),
            event="login",
            success=False,
            ip=ip,
            user_agent=user_agent,
            notes="Invalid Password"
        ).insert()
        return response(None, "Invalid Password", 400)

async def refresh_token_service(user: User):

    user_dict = {
        'id': str(user.id),
        'username': user.username,
        'email': user.email,
        'role': user.role,
    }
    
    try:
        access_token, refresh_token = generate_tokens(user_dict)
        return response({
            'user_data': user_dict,
            'token': {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }, "success", 200)
    except Exception as e:
        return response(None, f"Failed to generate token: {str(e)}", 400)
