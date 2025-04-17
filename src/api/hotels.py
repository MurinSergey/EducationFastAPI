from fastapi import Body, Query, APIRouter
from sqlalchemy import func, insert, select
from src.repositories.hotels import HotelsRepository
from src.models.hotels import HotelsOrm
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from schemas.hotel import Hotel, HotelPATCH

# Создаем роутер
router = APIRouter(prefix="/hotels", tags=["Отели"])

# Получаем список всех отелей
@router.get("", summary="Список всех отелей")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(description="Название отеля", default=None),
    location: str | None = Query(description="Адрес отеля", default=None),
):
    per_page = pagination.per_page or 5  # По умолчанию выводим 5 отелей на странице
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=(pagination.page - 1) * per_page
        )
        

# Удаление выбранного отеля
@router.delete("/{hotel_id}", summary="Удаление отеля")
def delete_hotel(
    hotel_id: int,
    # В метод delete можно добавлять параметры фильтрации
    hotel_titel: str | None = Query(
        description="Название отеля", default=None)
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

# Создание нового отеля
@router.post("", summary="Создание нового отеля")
async def create_hotel(
    hotel_data: Hotel = Body(openapi_examples={
        "1": {
            "summary": "Создание отеля Big Ben",
            "value": {
                "title": "Big Ben отель",
                "location": "Лондон, ул. Трафальгар, 1"
            }
        },
        "2": {
            "summary": "Создание отеля ЛУВР",
            "value": {
                "title": "Отель ЛУВР",
                "location": "Париж, ул. Монт-Сен-Пьер, 1"
            }
        },
        "3": {
            "summary": "Создание отеля Царь",
            "value": {
                "title": "Царь-отель",
                "location": "Санкт-Петербург, ул. Царя, 1"
            }
        }
    })
):

    async with async_session_maker() as session:
        new_data = await HotelsRepository(session).add(hotel_data.model_dump())
        await session.commit()

    return {"status": "OK", "new data": new_data}

# Изменение всего объекта
@router.put("/{hotel_id}", summary="Полное обновление данных")
def replace_hotel(
    hotel_id: int,
    hotel_data: Hotel
):

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            break

    return {"status": "OK"}

# Изменение части объекта
@router.patch("/{hotel_id}", summary="Частичное обновление данных")
def update_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name
            break

    return {"status": "OK"}
