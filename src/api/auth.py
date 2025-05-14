from fastapi import APIRouter, Body, Request, Response

from src.services.auth import AuthService
from src.schemas.user import User, UserWithHashPassword, UserWithPassword, UserLogin
from src.database import async_session_maker 
from src.repositories.users import UsersRepository

# Роутер для регистрации и авторизации пользователя
router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])

# Регистрация пользователя
@router.post("/register")
async def register(
    user: UserWithPassword = Body(openapi_examples={
        "1": {
            "summary": "Пример регистрации 1",
            "value": {
                "email": "Ivan@gmail.com",
                "nickname": "Ivan",
                "password": "qwerty"
            }
        },
        "2": {
            "summary": "Пример регистрации 2",
            "value": {
                "email": "Roman@gmail.com",
                "nickname": "Roman",
                "password": "qwerty123"
            }
        }
    })
):
    _hash_password = AuthService().hash_password(user.password)
    new_user = UserWithHashPassword(email=user.email, hash_password=_hash_password, nickname=user.nickname)
    async with async_session_maker() as session:
        data: User = await UsersRepository(session).add(new_user)
        await session.commit()
    
    return {"status": "OK", "data": data}

# Аутентификация пользователя
@router.post("/login")
async def login(
    response: Response,
    data: UserLogin = Body(openapi_examples={
        "1": {
            "summary": "Пример входа 1",
            "value": {
                "email": "Ivan@gmail.com",
                "password": "qwerty"
            }
        },
        "2": {
            "summary": "Пример входа 2",
            "value": {
                "email": "Roman@gmail.com",
                "password": "qwerty123"
            }
        }
    })
):
    access_token = None
    async with async_session_maker() as session:
        user: User = await AuthService().login_user(session, data)
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie(key="access_token", value=access_token)
    return {"status": "OK", "data": {"access_token": access_token}}

# Тестовый путь для проверки авторизации
@router.get("/only_auth")
async def auth_only(
    request: Request,
):
    access_token = None
    if "access_token" in request.cookies:
        access_token = request.cookies["access_token"]
        
    return {"status": "OK", "data": {"access_token": access_token}}