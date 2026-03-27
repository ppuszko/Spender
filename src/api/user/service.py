from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, delete 
from passlib.context import CryptContext

from uuid import UUID
from pydantic import EmailStr

from src.db.models import Vault, User, UserToVault, UserRole
from src.bases.service import BaseService
from src.err.exceptions import NotFoundException, ForbiddenException

from user.schemas import VaultCreate, UserCreate, UserLogin


hash_context = CryptContext(
    schemes = ["bcrypt"]
)


class UserService():
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_vault(self, vault_data: VaultCreate, user_uid: UUID):
        vault = Vault(**(vault_data.model_dump()))
        self._session.add(vault)

        utv = UserToVault(user_uid=user_uid, vault_uid=vault.uid, role=UserRole.ADMIN)
        self._session.add(utv)

    async def register_user(self, user_data: UserCreate): 
        user_data.password_hash = self._generate_hash(user_data.password_hash)
        user_dict = user_data.model_dump()
        user = User(**user_dict)

        self._session.add(user)
    

    async def login(self, user_data: UserLogin) -> bool:
        user = await self.__get_user_by_email(user_data.email)
        if user is not None:
            if self._verify_hash(user_data.password, user.password_hash):
                return True 
        raise ForbiddenException("E-mail and/or password incorrect")


    async def __get_user_by_uid(self, uid: UUID) -> User: 
        user = (await self._session.exec(select(User)
                                 .where(User.uid == uid))).first()
        
        if user is None:
            raise NotFoundException()
        
        return user


    async def __get_user_by_email(self, email: EmailStr) -> User:
        user = (await self._session.exec(select(User)
                                         .where(User.email == email))).first()

        if user is None: 
            raise NotFoundException()

        return user        



    def _generate_hash(self, secret: str) -> str:
        return hash_context.hash(secret)
    
    def _verify_hash(self, secret: str, secret_hash: str) -> bool:
        return hash_context.verify(secret, secret_hash)


         


    

    
    
    
