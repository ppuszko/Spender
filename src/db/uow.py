from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, Request, Depends

from functools import cached_property
from collections.abc import AsyncGenerator, AsyncIterator

from src.api.users.service import UserService
from src.api.vault.service import VaultService


class UnitOfWork:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]):
        self._sessionmaker = sessionmaker
        self._session: AsyncSession | None = None

    async def __aenter__(self) -> "UnitOfWork":
        self._session = self._sessionmaker()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._session:
            try:
                if exc_val:
                    await self._session.rollback()
                else:
                    await self._session.commit()
            finally:
                await self._session.close()
                self._session = None 

    @property
    def session(self) -> AsyncSession:
        if self._session is None:
            raise RuntimeError("Unit of Work session object used out of context.")
        return self._session 
    
    @property
    def vaults(self) -> VaultService:
        return VaultService(self.session)
    
    @property
    def users(self) -> UserService:
        return UserService(self.session)

async def get_uow(request: Request) -> AsyncIterator[UnitOfWork]:
    sessionmaker = getattr(request.app.state, "sessionmaker", None)
    if sessionmaker is None:
        raise RuntimeError("Sessionmaker not initialized")
    
    uow = UnitOfWork(sessionmaker)
    async with uow:
        yield uow

async def get_session_from_uow(uow: UnitOfWork = Depends(get_uow)) -> AsyncGenerator[AsyncSession, None]:
    async with uow:
        yield uow.session 