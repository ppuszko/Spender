from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession 
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase

from config.db import DBConfig
from uow import get_session_from_uow
from models import User

def init_engine(url: str = DBConfig.DB_URL) -> AsyncEngine:
    return create_async_engine(url=url)

def init_sessionmaker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

async def get_user_db(session: AsyncSession = Depends(get_session_from_uow)):
    yield SQLAlchemyUserDatabase(session, User)
