from sqlmodel.ext.asyncio.session import AsyncSession  
from sqlmodel import select 

from uuid import UUID

from src.db.models import Vault, UserToVault, UserRole, UserToVault
from schemas import VaultCreate, VaultGet

class VaultService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_vault(self, vault_data: VaultCreate, user_uid: UUID) -> VaultGet:
        vault = Vault(**(vault_data.model_dump()))
        self._session.add(vault)

        utv = UserToVault(user_uid=user_uid, vault_uid=vault.uid, role=UserRole.ADMIN)
        self._session.add(utv)

        return VaultGet.model_validate(vault)
    

    async def get_user_vaults(self, user_uid: UUID) -> list[VaultGet]:
        statement = (select(Vault)
                     .join(UserToVault)
                     .where(UserToVault.user_uid == user_uid))
        res = await self._session.exec(statement)
        vaults = res.all()

        return [VaultGet.model_validate(v) for v in vaults]