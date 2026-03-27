from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, Request

from functools import cached_property

from src.api.user.service import UserService
from src.api.vault.service import VaultService

class UnitOfWork:
    def __init__(self, sessionmaker: async_sessionmaker):
        self._sessionmaker = sessionmaker
        self._session: AsyncSession | None = None

    async def __aenter__(self):
        self._session = self._sessionmaker()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            if exc_val:
                await self._session.rollback()
            else:
                await self._session.commit()

            await self._session.close()
            self._session = None 

    @property
    def session(self):
        if self._session is None:
            raise HTTPException(
                status_code=500, 
                detail="Unit of Work session object used out of context.")
        return self._session 
    

    @cached_property
    def vaults(self) -> VaultService:
        return VaultService(self.session)
    

    @cached_property
    def users(self) -> UserService:
        return UserService(self.session)

def get_uow(request: Request):
    return UnitOfWork(request.app.state.sessionmaker)