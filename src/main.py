from fastapi import Body, FastAPI, Query
import uvicorn

from hotels import router as hotels_router

# Создаем приложение FastAPI
app = FastAPI()

app.include_router(hotels_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8000)