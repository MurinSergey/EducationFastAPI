from pydantic import BaseModel, Field


class Hotel(BaseModel):
    """
    Класс Hotel представляет отель.

    Атрибуты:
    title (str): Название отеля.
    location (str): Имя отеля.
    """
    title: str = Field(description="Название отеля")
    location: str = Field(description="Адрес отеля")

class HotelPATCH(BaseModel):
    """
    Класс HotelPATCH представляет обновленные данные отеля.

    Атрибуты:
    title (str | None): Название отеля. Если не указано, то None.
    location (str | None): Код отеля. Если не указано, то None.
    """
    title: str | None = Field(None, description="Название отеля")
    location: str | None = Field(None, description="Адрес отеля")