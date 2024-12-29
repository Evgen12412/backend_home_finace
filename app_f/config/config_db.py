from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Создаем подключение к базе данных
engine = create_engine("sqlite:///home_finance.db", echo=True)

# Создаем фабрику сессий
SessionLocal = sessionmaker(bind=engine)

# Базовый класс для моделей
class Base(DeclarativeBase):
    pass