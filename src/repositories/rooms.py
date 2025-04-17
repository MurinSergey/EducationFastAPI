from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository


class RoomsRepository(BaseRepository):
    """
    Класс репозитория для работы с комнатами.

    Атрибуты:
        _model (RoomsOrm): Модель комнаты.
    """
    _model = RoomsOrm
