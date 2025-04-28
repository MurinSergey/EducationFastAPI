from sqlalchemy import func, select
from src.schemas.hotel import Hotel
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    """
    Класс репозитория для работы с отелями.

    Атрибуты:
        _model (HotelsOrm): Модель отеля.
    """

    _model = HotelsOrm
    _schema = Hotel

    # Метод получения всех отелей с параметрами поиска
    async def get_all(
            self, 
            title: str, 
            location: str, 
            limit: int, 
            offset: int
    ) -> list[Hotel]:
        """
        Получает список отелей по заданным параметрам.

        Аргументы:
            title (str): Название отеля для поиска.
            location (str): Местоположение отеля для поиска.
            limit (int): Количество отелей на странице.
            offset (int): Страница результатов.
        """
        query = select(HotelsOrm)
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.lower().strip()))

        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.lower().strip()))

        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(query)
        return [self._schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]