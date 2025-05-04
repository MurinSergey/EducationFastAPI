from src.database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class UsersOrm(Base):
    """
    Класс UsersOrm представляет таблицу "users" в базе данных.

    Атрибуты:
        id (int): Уникальный идентификатор пользователя. Является первичным ключом.
        email (str): Электронная почта пользователя. Не может быть пустой.
        hash_password (str): Хэш пароля пользователя. Не может быть пустым.
        nickname (str): Никнейм пользователя.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    hash_password: Mapped[str] = mapped_column(String(100), nullable=False)
    nickname: Mapped[str] = mapped_column(String(100))