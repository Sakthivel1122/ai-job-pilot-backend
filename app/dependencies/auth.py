from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from app.models.user import User  # Your beanie User model
from app.config import settings  # contains SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer
from typing import Callable
from bson import ObjectId

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = settings.JWT_SIGNATURE_KEY
ALGORITHM = "HS256"

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        

        user = await User.find_one(
            User.id == ObjectId(user_id),
            User.deleted_at == None
        )
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def role_required(*allowed_roles: str) -> Callable:
    async def checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied for role: {current_user.role}",
            )
        return current_user
    return checker
