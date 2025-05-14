import jwt
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Body, Response
from passlib.context import CryptContext

from src.schemas.user import User, UserWithHashPassword, UserWithPassword, UserLogin
from src.database import async_session_maker 
from src.repositories.users import UsersRepository
from src.config import settings

# Инициализация контекста хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Роутер для регистрации и авторизации пользователя
router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])

SECRET_KEY = settings.AUTH_SECRET_KEY
ALGORITHM = settings.AUTH_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.AUTH_ACCESS_TOKEN_EXPIRE_MINUTES

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """
    Создает токен доступа на основе предоставленных данных.

    Args:
        data (dict): Данные, которые будут закодированы в токен.

    Returns:
        str: Сгенерированный токен доступа.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= ({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

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
    _hash_password = pwd_context.hash(user.password)
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
        user: User = await UsersRepository(session).auth_user(data, verify_password)
        access_token = create_access_token({"user_id": user.id})
        response.set_cookie(key="access_token", value=access_token)
    return {"status": "OK", "data": {"access_token": access_token}}
