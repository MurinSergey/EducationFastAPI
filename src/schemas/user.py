

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """
    Базовый класс для пользователя.

    Атрибуты:
        email (str): Электронная почта пользователя.
        nickname (str): Никнейм пользователя.
    """
    email: EmailStr
    nickname: str

class UserRequestAdd(UserBase):
    """
    Класс для добавления пользователя.

    Атрибуты:
        password (str): Пароль пользователя.
    """
    password: str

class UserDatabaseAdd(UserBase):
    """
    Класс для добавления пользователя в базу данных.

    Атрибуты:
        hashed_password (str): Хэшированный пароль пользователя.
    """
    hash_password: str


class User(UserBase):
    """
    Класс для представления пользователя.

    Атрибуты:
        id (int): Идентификатор пользователя.
    """
    id: int
