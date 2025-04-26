from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from src.database import engine


class BaseRepository:
    """
    Базовый класс репозитория для работы с базой данных.

    Атрибуты:
        model (Any): Модель, с которой работает репозиторий.
    """

    _model = None

    def __init__(self, session):
        """
        Инициализация репозитория.

        Аргументы:
            session (Any): Сессия базы данных.
        """
        self._session = session

    async def get_all(self, *args, **kwargs):
        """
        Получение всех записей из таблицы.

        Возвращает:
            list: Список всех записей.
        """
        query = select(self._model)
        result = await self._session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        """
        Получение одной записи из таблицы по фильтрам.

        Аргументы:
            **filter_by: Фильтры для поиска записи.

        Возвращает:
            Any: Запись, удовлетворяющая фильтрам, или None, если запись не найдена.
        """
        query = select(self._model).filter_by(**filter_by)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def add(self, data: BaseModel):
        """
        Добавляет данные в базу данных.

        Args:
            data (BaseModel): Данные, которые нужно добавить.

        Returns:
            scalar_one_or_none: Результат выполнения запроса.
        """
        add_hotel_statement = insert(self._model).values(**data.model_dump()).returning(self._model)
        # print(add_hotel_statement.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        result = await self._session.execute(add_hotel_statement)
        return result.scalar_one_or_none()
    
    async def update(self, data: BaseModel, **filter_by) -> BaseModel:
        """
        Обновляет данные в базе данных.

        Args:
            data (BaseModel): Данные, которые нужно обновить.
            **filter_by: Фильтры для поиска записи.

        Returns:
            BaseModel: Обновленная запись.
        """
        query = update(self._model).filter_by(**filter_by).values(**data.model_dump()).returning(self._model)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()
    
    async def delete(self, **filter_by) -> BaseModel:
        """
        Удаляет запись из базы данных, соответствующую заданным фильтрам.

        Args:
            **filter_by: Ключевые слова, используемые для фильтрации записей.

        Returns:
            BaseModel: Удаленная запись или None, если запись не найдена.
        """
        qery = delete(self._model).filter_by(**filter_by).returning(self._model)
        result = await self._session.execute(qery)
        return result.scalar_one_or_none()
