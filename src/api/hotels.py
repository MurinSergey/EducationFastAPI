from fastapi import Body, HTTPException, Query, APIRouter
from src.repositories.hotels import HotelsRepository
from src.api.dependencies import PaginationDep
from src.database import async_session_maker 
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
async def delete_hotel(
    hotel_id: int
):
    status = "OK"
    data = None
    async with async_session_maker() as session:
        try:
            data = await HotelsRepository(session).delete(id=hotel_id)
        except HTTPException as e:
            status = "NOT_OK"
            data = e
            await session.rollback()
        await session.commit()

    return {"status": status, "data": data}

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
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}

# Изменение всего объекта
@router.put("/{hotel_id}", summary="Полное обновление данных")
async def replace_hotel(
    hotel_id: int,
    hotel_data: Hotel
):
    status = "OK"
    data = None
    async with async_session_maker() as session:
        try:
            data = await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        except HTTPException as e:
            await session.rollback()
            status = "NOT_OK"
            data = e
        await session.commit()

    return {"status": status, "data": data}

# Изменение части объекта
@router.patch("/{hotel_id}", summary="Частичное обновление данных")
async def update_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH
):
    status = "OK"
    data = None
    async with async_session_maker() as session:
        try:
            data = await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        except HTTPException as e:
            await session.rollback()
            status = "NOT_OK"
            data = e
        await session.commit()

    return {"status": status, "data": data}
