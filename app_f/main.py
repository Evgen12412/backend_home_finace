from fastapi import FastAPI
import uvicorn
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager

from app_f.data_base.connection import conn
from app_f.routes.users import user_router

# Определяем lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Подключаемся к базе данных
    conn()  # Создает таблицы, если они еще не существуют
    yield
    # Shutdown: Здесь можно добавить логику для очистки ресурсов, если это необходимо

# Создаем приложение FastAPI с lifespan
app = FastAPI(lifespan=lifespan)

# Регистрируем маршруты
app.include_router(user_router, prefix="/user")

@app.get("/")
async def home():
    return RedirectResponse(url="/user/")

if __name__ == "__main__":
    uvicorn.run("app_f.main:app", host="127.0.0.1", port=8070, reload=True)
