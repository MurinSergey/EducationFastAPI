from sqlalchemy import insert, select
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
    
    async def add(self, data):
        """
        Добавление новой записи в таблицу.

        Аргументы:
            data (dict): Данные для добавления записи.

        Возвращает:
            Any: Добавленная запись.
        """
        add_hotel_statement = insert(self._model).values(**data).returning(self._model)
        # print(add_hotel_statement.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        result = await self._session.execute(add_hotel_statement)
        return result.scalar_one_or_none()

