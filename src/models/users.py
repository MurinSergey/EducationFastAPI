from src.database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    hash_password: Mapped[str] = mapped_column(String(100), nullable=False)
    nickname: Mapped[str] = mapped_column(String(100))