from sqlalchemy import select


class BaseRepository:
    """
    Базовый класс репозитория для работы с базой данных.

    Атрибуты:
        model (Any): Модель, с которой работает репозиторий.
    """

    model = None

    def __init__(self, session):
        """
        Инициализация репозитория.

        Аргументы:
            session (Any): Сессия базы данных.
        """
        self._session = session

    async def get_all(self):
        """
        Получение всех записей из таблицы.

        Возвращает:
            list: Список всех записей.
        """
        query = select(self.model)
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
        query = select(self.model).filter_by(**filter_by)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()
