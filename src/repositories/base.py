from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Result, delete, insert, select, update
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
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

    @staticmethod        
    def scalar_one(result: Result):
        try:
            return result.scalar_one()
        except NoResultFound as e:
            raise HTTPException(status_code=404, detail="Запись не найдена")
        except MultipleResultsFound as e:
            raise HTTPException(status_code=400, detail="Найдено более одной записи")

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
    
    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> BaseModel:
        """
        Обновляет запись в базе данных.

        Args:
            data (BaseModel): Данные для обновления.
            exclude_unset (bool): Если True, не обновлять поля, которые не были изменены.
            **filter_by: Параметры фильтрации.

        Returns:
            BaseModel: Обновленная запись.

        Raises:
            HTTPException: Если запись не найдена или найдено более одной записи.
        """
        replace_hotel_statement = (
            update(self._model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset)).returning(self._model) # тут exclude_unset=True чтобы не обновлять поля которые не были изменены
        )
        result = await self._session.execute(replace_hotel_statement)
        return BaseRepository.scalar_one(result)
    
    async def delete(self, **filter_by) -> BaseModel:
        """
        Удаляет запись из базы данных, соответствующую заданным параметрам фильтрации.

        Args:
            **filter_by: Параметры фильтрации для удаления записи.

        Returns:
            BaseModel: Удаленная запись.

        Raises:
            HTTPException: Если запись не найдена или найдено более одной записи.
        """
        delete_hotel_statement = delete(self._model).filter_by(**filter_by).returning(self._model)
        result = await self._session.execute(delete_hotel_statement)
        return BaseRepository.scalar_one(result)

