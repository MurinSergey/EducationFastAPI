from fastapi import Body, Query, APIRouter

from schemas.hotel import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])

# Тестовый список отелей
hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

# Получаем список всех отелей
@router.get("", summary="Список всех отелей")
def get_hotels(
    id: int | None = Query(description="Номер отеля", default=None),
    title: str | None = Query(description="Название отеля", default=None),
    page: int = Query(description="Номер страницы", default=1),
    per_page: int = Query(description="Количество элементов на странице", default=3)
):
    _hotels = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        _hotels.append(hotel)
    return _hotels[(page - 1) * per_page : page * per_page]

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
def create_hotel(
    hotel_data: Hotel = Body(openapi_examples={
        "1": {
            "summary": "Создание отеля London",
            "value": {
                "title": "London",
                "name": "lnd"
            }
        },
        "2": {
            "summary": "Создание отеля Paris",
            "value": {
                "title": "Paris",
                "name": "prs"
            }
        }
    })
):

    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })

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
