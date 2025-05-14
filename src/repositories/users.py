

from typing import Callable

from fastapi import HTTPException, status
from sqlalchemy import select
from src.schemas.user import User, UserLogin, UserWithHashPassword
from src.models.users import UsersOrm
from src.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    """
    Класс UsersRepository представляет репозиторий для работы с пользователями.

    Атрибуты:
        _model (UsersOrm): Модель ORM для работы с таблицей "users".
        _schema (User): Схема для валидации данных пользователя.
    """
    _model = UsersOrm
    _schema = User

    # Аутентификация пользователя
    async def auth_user(self, user: UserLogin, check_password: Callable[[str, str], bool]) -> User:
        """
        Аутентификация пользователя.

        Args:
            user (UserWithPassword): Объект пользователя с паролем.
            check_password (Callable[[str, str], bool]): Функция для проверки пароля.

        Returns:
            User: Объект пользователя.

        Raises:
            HTTPException: Если аутентификация не удалась.
        """
        query = select(self._model).filter_by(email=user.email)
        result = await self._session.execute(query)
        model = BaseRepository.scalar_one(result)
        auth_user = UserWithHashPassword.model_validate(model, from_attributes=True)
        if not check_password(user.password, auth_user.hash_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Ошибка аутентификации")
        return self._schema.model_validate(model, from_attributes=True)