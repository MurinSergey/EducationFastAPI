import uvicorn
from fastapi import Body, FastAPI, Query
import sys
from pathlib import Path

# Добавляем путь к корневой директории проекта в список путей поиска модулей
# Это позволяет импортировать модули из корневой директории проекта
# В данном случае, путь к корневой директории проекта считается из текущего файла (main.py)
# И затем добавляем этот путь в список путей поиска модулей
# Это позволяет импортировать модули из папки "src", которая находится в корневой директории проекта
sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as hotels_router
from src.config import settings

from src.database import *

# Создаем приложение FastAPI
app = FastAPI()

# Включаем маршруты из файла hotels.py в основное приложение
app.include_router(hotels_router)

# Запускаем приложение при выполнении скрипта main.py
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8000)
