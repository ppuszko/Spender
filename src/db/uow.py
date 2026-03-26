from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, Request


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
    

def get_uow(request: Request):
    return UnitOfWork(request.app.state.sessionmaker)