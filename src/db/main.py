from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession 

from config.db import DBConfig

def init_engine(url: str = DBConfig.DB_URL) -> AsyncEngine:
    return create_async_engine(url=url)

def init_sessionmaker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

