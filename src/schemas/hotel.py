from pydantic import BaseModel, Field



class HotelAdd(BaseModel):
    """
    Класс HotelAdd представляет данные для добавления нового отеля.

    Атрибуты:
    title (str): Название отеля.
    location (str): Адрес отеля.
    """

    title: str = Field(description="Название отеля")
    location: str = Field(description="Адрес отеля")

class Hotel(HotelAdd):
    """
    Класс Hotel представляет информацию об отеле.

    Атрибуты:
    id (int): Идентификатор отеля.
    title (str): Название отеля.
    location (str): Адрес отеля.
    """
    id: int = Field(description="Идентификатор отеля")


class HotelPATCH(BaseModel):
    """
    Класс HotelPATCH представляет обновленные данные отеля.

    Атрибуты:
    title (str | None): Название отеля. Если не указано, то None.
    location (str | None): Код отеля. Если не указано, то None.
    """
    title: str | None = Field(None, description="Название отеля")
    location: str | None = Field(None, description="Адрес отеля")