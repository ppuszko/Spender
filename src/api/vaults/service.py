from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, delete 

from db.models import Vault
from src.err.exceptions import NotFoundException

class VaultService:
    def __init__(self, session: AsyncSession):
        self._session = session 

    async def get_vault(self, uid: str) -> Vault:
        vault = await self._session.exec(
            select(Vault)
            .where(Vault.uid == uid))
        
        result = vault.first()
        if result is None:
            raise NotFoundException
        
        return result 
    
    
