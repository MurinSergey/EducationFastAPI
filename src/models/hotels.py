from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, BigInteger

# Класс для создания таблицы БД "hotels" в соотвествии с ORM SQLAlchemy
class HotelsOrm(Base):
    """
    Класс для создания таблицы БД "hotels" в соотвествии с ORM SQLAlchemy

    Атрибуты:
        id (Mapped[int]): Идентификатор отеля
        title (Mapped[str]): Название отеля
        location (Mapped[str]): Адрес отеля
    """
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(length=100))
    location: Mapped[str]