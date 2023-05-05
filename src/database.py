from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}' # задаем подключение к базе данным
Base = declarative_base()


engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) # type: ignore


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Функция get_async_session - это сопрограмма, которая возвращает объект асинхронного сеанса.
    Функция использует контекстный менеджер async_session_maker() для создания нового сеанса, а затем выдает его.
    Это позволяет нам использовать оператор async with в нашем коде, который автоматически закроет соединение.

    :return: Асинхронный генератор, который выдает асинхронный сеанс
    """
    async with async_session_maker() as session:
        yield session
