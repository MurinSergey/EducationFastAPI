from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    """
    Класс репозитория для работы с отелями.

    Атрибуты:
        model (HotelsOrm): Модель отеля.
    """

    model = HotelsOrm
