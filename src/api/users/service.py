from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, delete 
from passlib.context import CryptContext

from uuid import UUID
from pydantic import EmailStr

from src.db.models import Vault, User, UserToVault, UserRole

from src.err.exceptions import NotFoundException, ForbiddenException

from users.schemas import UserCreate




class UserService():
    def __init__(self, session: AsyncSession):
        self._session = session

    async def __get_user_by_id(self, id: UUID) -> User: 
        user = (await self._session.exec(select(User)
                                 .where(User.id == id))).first()
        if user is None:
            raise NotFoundException()
        
        return user

    async def __get_user_by_email(self, email: EmailStr) -> User:
        user = (await self._session.exec(select(User)
                                         .where(User.email == email))).first()
        if user is None: 
            raise NotFoundException()

        return user        


         


    

    
    
    
