

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

class User(UserBase):
    """
    Класс для представления пользователя.

    Атрибуты:
        id (int): Идентификатор пользователя.
    """
    id: int

class UserWithPassword(UserBase):
    """
    Класс пользователя с паролем

    Атрибуты:
        password (str): Пароль пользователя.
    """
    password: str

class UserWithHashPassword(UserBase):
    """
    Класс пользователя с хешированным паролем

    Атрибуты:
        hashed_password (str): Хэшированный пароль пользователя.
    """
    hash_password: str

class UserLogin(BaseModel):
    """
    Модель для входа пользователя.

    Attributes:
        email (EmailStr): Электронная почта пользователя.
        password (str): Пароль пользователя.
    """
    email: EmailStr
    password: str