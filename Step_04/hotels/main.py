from fastapi import Body, FastAPI, Query
import uvicorn

# Создаем приложение FastAPI
app = FastAPI()

# Тестовый список отелей
hotels = [
    {"id": 1, "title": "Moscow"},
    {"id": 2, "title": "Khabarovsk"}
]

# Стартовая страница
@app.get("/")
def start():
    return hotels

# Получаем список всех отелей
@app.get("/hotels")
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
@app.delete("/hotels/{hotel_id}")
def delete_hotel(
        hotel_id: int,
        hotel_titel: str | None = Query(description="Название отеля", default=None) # В метод delete можно добавлять параметры фильтрации
    ):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

# Создание нового отеля
@app.post("/hotels")
def create_hotel(
        hotel_title: str = Body(description="Название отеля", embed=True)
    ):
    global hotels
    hotels.append({"id": hotels[-1]["id"] + 1, "title": hotel_title})
    return {"status": "OK"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8001)