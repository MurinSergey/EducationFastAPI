

from src.schemas.user import User
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