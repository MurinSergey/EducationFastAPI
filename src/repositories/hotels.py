from sqlalchemy import func, select
from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    """
    Класс репозитория для работы с отелями.

    Атрибуты:
        model (HotelsOrm): Модель отеля.
    """

    model = HotelsOrm

    # Метод получения всех отелей с параметрами поиска
    async def get_all(
            self, 
            title: str, 
            location: str, 
            limit: int, 
            offset: int
    ):
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
        hotels = result.scalars().all()
        # print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        return hotels