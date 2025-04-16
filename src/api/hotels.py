from fastapi import Body, Query, APIRouter
from sqlalchemy import insert, select
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
    id: int | None = Query(description="Номер отеля", default=None),
    title: str | None = Query(description="Название отеля", default=None),
):
    per_page = pagination.per_page or 5 # По умолчанию выводим 5 отелей на странице
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if id:
            query = query.filter(id=id)
        if title:
            query = query.filter(title=title)

        query = (
            query
            .limit(per_page)
            .offset((pagination.page - 1) * per_page)
        )
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels

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
            "summary": "Создание отеля London",
            "value": {
                "title": "Big Ban Hotel",
                "location": "London street 1"
            }
        },
        "2": {
            "summary": "Создание отеля Paris",
            "value": {
                "title": "Luvr Hotel",
                "location": "Paris street 1"
            }
        }
    })
):

    async with async_session_maker() as session:
        add_hotel_statement = insert(HotelsOrm).values(**hotel_data.model_dump())
        # print(add_hotel_statement.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_statement)
        await session.commit()

    return {"status": "OK"}

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
