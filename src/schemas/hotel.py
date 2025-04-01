from pydantic import BaseModel, Field


class Hotel(BaseModel):
    """
    Класс Hotel представляет отель.

    Атрибуты:
    title (str): Название отеля.
    name (str): Имя отеля.
    """
    title: str
    name: str

class HotelPATCH(BaseModel):
    """
    Класс HotelPATCH представляет обновленные данные отеля.

    Атрибуты:
    title (str | None): Название отеля. Если не указано, то None.
    name (str | None): Код отеля. Если не указано, то None.
    """
    title: str | None = Field(None, description="Название отеля")
    name: str | None = Field(None, description="Код отеля")