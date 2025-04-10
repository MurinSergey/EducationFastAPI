
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from src.config import settings

# Подключение к базе данных
# Использование асинхронного движка
engine = create_async_engine(settings.DATABASE_URL)

# Создание асинхронного сессионного объекта для работы с базой данных
# expire_on_commit=False означает, что объекты, созданные в рамках сессии, не будут автоматически удаляться после завершения транзакции
# Это позволяет сохранять объекты в памяти и использовать их в других частях приложения
# После завершения работы с объектами, их можно будет явно удалить или использовать другой механизм управления временем жизни объектов
# В данном случае, объекты будут удаляться при закрытии сессии или явном вызове метода close() на объекте сессии
# Подробнее о настройках сессии можно почитать здесь: https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

# Создание базового класса для всех моделей данных
class Base(DeclarativeBase):
    '''
    Базовый класс для всех моделей данных.
    Для создания моделей данных необходимо наследоваться от этого класса.
    '''
    pass

# Функция для тестового подключения к базе данных
async def test_engine():
    """
    Функция для тестирования подключения к базе данных и выполнения SQL-запроса.

    Функция подключается к базе данных, выполняет SQL-запрос для получения версии базы данных и выводит результат.

    Returns:
        None
    """
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT version()"))
        print(result.fetchall())
