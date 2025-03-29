from fastapi import Body, Query, APIRouter

router = APIRouter(prefix="/hotels", tags=["Отели"])

# Тестовый список отелей
hotels = [
    {"id": 1, "title": "Moscow", "name": "msc"},
    {"id": 2, "title": "Khabarovsk", "name": "khv"}
]

# Получаем список всех отелей
@router.get("", summary="Список всех отелей")
def get_hotels(
        id: int | None = Query(description="Номер отеля", default=None),
        title: str | None = Query(description="Название отеля", default=None)
    ):
    _hotels = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        _hotels.append(hotel)
    return _hotels

# Удаление выбранного отеля
@router.delete("/{hotel_id}", summary="Удаление отеля")
def delete_hotel(
        hotel_id: int,
        hotel_titel: str | None = Query(description="Название отеля", default=None) # В метод delete можно добавлять параметры фильтрации
    ):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

# Создание нового отеля
@router.post("", summary="Создание нового отеля")
def create_hotel(
        hotel_title: str = Body(description="Название отеля", embed=True),
        hotel_name: str = Body(description="Код отеля", embed=True)
    ):

    global hotels
    hotels.append({"id": hotels[-1]["id"] + 1, "title": hotel_title, "name": hotel_name})

    return {"status": "OK"}

# Изменение всего объекта
@router.put("/{hotel_id}", summary="Полное обновление данных")
def replace_hotel(
        hotel_id: int,
        hotel_title: str = Body(description="Название отеля", embed=True),
        hotel_name: str = Body(description="Код отеля", embed=True)
    ):

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_title
            hotel["name"] = hotel_name
            break

    return {"status": "OK"}

# Изменение части объекта
@router.patch("/{hotel_id}", summary="Частичное обновление данных")
def update_hotel(
        hotel_id: int,
        hotel_title: str | None = Body(default=None, description="Название отеля", embed=True),
        hotel_name: str | None = Body(default=None, description="Код отеля", embed=True)
    ):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_title:
                hotel["title"] = hotel_title
            if hotel_name:
                hotel["name"] = hotel_name
            break

    return {"status": "OK"}