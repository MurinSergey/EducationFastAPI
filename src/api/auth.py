from fastapi import APIRouter, Body, HTTPException
from passlib.context import CryptContext

from src.schemas.user import User, UserDatabaseAdd, UserRequestAdd
from src.database import async_session_maker 
from src.repositories.users import UsersRepository

# Инициализация контекста хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Роутер для регистрации и авторизации пользователя
router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])

# Регистрация пользователя
@router.post("/register")
async def register(
    user: UserRequestAdd = Body(openapi_examples={
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
    new_user = UserDatabaseAdd(email=user.email, hash_password=_hash_password, nickname=user.nickname)
    async with async_session_maker() as session:
        data: User = await UsersRepository(session).add(new_user)
        await session.commit()
    
    return {"status": "OK", "data": data}
