from fastapi import FastAPI
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
    return "Список отелей"

# Получаем список всех отелей
@app.get("/hotels")
def get_hotels():
    return hotels


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)