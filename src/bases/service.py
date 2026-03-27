from sqlmodel import SQLModel, select, delete
from sqlmodel.ext.asyncio.session import AsyncSession 
from typing import TypeVar, Generic, Type
from uuid import UUID

from src.err.exceptions import NotFoundException
from src.db.models import BaseSQLModel

T = TypeVar("T", bound=BaseSQLModel)

class BaseService(Generic[T]):
    """Implements basic CRUD for all generic service operations"""
    def __init__(self, session: AsyncSession, model: Type[T]):
        self._session = session
        self._model = model 

    async def _create(self, attributes: dict) -> T:
        obj = self._model(**attributes)
        self._session.add(obj)
        return obj 
    
    async def _get_by_uid(self, uid: UUID) -> T: 
        res = await self._session.exec(
            select(self._model)
            .where(self._model.uid == uid))
        res = res.first()

        if res is None: 
            raise NotFoundException()

        return res 
    
    async def _update(self, uid: UUID, attributes: dict) ->  T:
        res = await self._get_by_uid(uid)
        
        for k, v in attributes.items():
            setattr(res, k, v)
        
        return res

    async def _delete(self, uid: UUID):
        res = await self._get_by_uid(uid)

        await self._session.delete(res)