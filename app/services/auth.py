from app.models.user import User
from app.utils.hash import encrypt_password
from app.utils.jwt import generate_tokens
from app.schemas.user import SignupRequest, LoginRequest
from app.utils.response import response
from app.utils.hash import verify_password

async def create_user(data: SignupRequest) -> dict:
    existing_user = await User.find_one(User.email == data.email, User.deleted_at == None)
    if existing_user:
        return response (None,"User already exists!", 400)

    try:
        hashed_pwd = encrypt_password(data.password)
        user = User(
            username=data.username,
            email=data.email,
            password=hashed_pwd,
        )
        await user.insert()
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
        return response(None, f"Failed to create user: {str(e)}", 400)

async def login_user(data: LoginRequest):
    existing_user = await User.find_one(User.email == data.email, User.deleted_at == None)

    if existing_user is None:
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

        return response({
                "user_data": user_dict,
                "token": {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            }, "User Signup Successful", 200)
    else:
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
