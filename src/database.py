
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.config import settings

# Подключение к базе данных
# Использование асинхронного движка
engine = create_async_engine(settings.DATABASE_URL)

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