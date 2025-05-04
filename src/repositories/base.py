from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import Result, delete, insert, select, update
from sqlalchemy.exc import NoResultFound, MultipleResultsFound, IntegrityError
from src.database import engine


class BaseRepository:
    """
    Базовый класс репозитория для работы с базой данных.

    Атрибуты:
        model (Any): Модель, с которой работает репозиторий.
    """

    _model = None
    _schema: BaseModel = None

    def __init__(self, session):
        """
        Инициализация репозитория.

        Аргументы:
            session (Any): Сессия базы данных.
        """
        self._session = session

    @staticmethod        
    def scalar_one(result: Result):
        """
        Возвращает скалярное значение из результата запроса.

        Аргументы:
            result (Any): Результат запроса.

        Возвращает:
            Any: Скалярное значение из результата запроса.

        Исключения:
            HTTPException: Если запись не найдена или найдено более одной записи.
        """
        try:
            return result.scalar_one()
        except NoResultFound as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Запись не найдена")
        except MultipleResultsFound as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Найдено более одной записи")

    async def get_all(self, *args, **kwargs) -> list[BaseModel]:
        """
        Получение всех записей из таблицы.

        Возвращает:
            list: Список всех записей.
        """
        query = select(self._model)
        result = await self._session.execute(query)
        return [self._schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def get_one(self, **filter_by) -> BaseModel:
        """
        Получает один объект из базы данных, соответствующий заданным фильтрам.

        Args:
            **filter_by: Ключевые слова для фильтрации объектов.

        Returns:
            BaseModel: Найденный объект или None, если объект не найден.
        """
        query = select(self._model).filter_by(**filter_by)
        result = await self._session.execute(query)
        model = BaseRepository.scalar_one(result)
        return self._schema.model_validate(model, from_attributes=True)

    async def add(self, data: BaseModel) -> BaseModel:
        """
        Добавляет данные в базу данных.

        Args:
            data (BaseModel): Данные, которые нужно добавить.

        Returns:
            BaseModel: Добавленные данные.
        """
        add_hotel_statement = insert(self._model).values(**data.model_dump()).returning(self._model)
        # print(add_hotel_statement.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        result = await self._session.execute(add_hotel_statement)
        model =  BaseRepository.scalar_one(result)
        return self._schema.model_validate(model, from_attributes=True)

    
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
        model = BaseRepository.scalar_one(result)
        return self._schema.model_validate(model, from_attributes=True)
    
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
        model = BaseRepository.scalar_one(result)
        return self._schema.model_validate(model, from_attributes=True)

