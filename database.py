"""
Эта часть программы относится к базе данных.
Мы имортируем ассинхронный движок из sqalchemy.ext.asyncio и sessionmaker
используя их для создания движка и сессии.

После чего создаем две асинхронные функции для создания таблиц и их удаления.

Также импортируем модель для создания таблиц.
"""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from models.orm_model import Base


database_irl = 'postgresql+asyncpg://postgres:11223344Qq@localhost:5432/todolist'
engine = create_async_engine(database_irl)

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
