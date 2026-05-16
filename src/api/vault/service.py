from sqlmodel.ext.asyncio.session import AsyncSession  
from sqlmodel import select 

from uuid import UUID

from src.db.models import Vault, UserToVault, UserRole, UserToVault
from schemas import VaultCreate, VaultGet

class VaultService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_vault(self, vault_data: VaultCreate, user_id: UUID) -> VaultGet:
        vault = Vault(**(vault_data.model_dump()))
        self._session.add(vault)

        utv = UserToVault(user_id=user_id, vault_id=vault.id, role=UserRole.ADMIN)
        self._session.add(utv)

        return VaultGet.model_validate(vault)
    

    async def get_user_vaults(self, user_id: UUID) -> list[VaultGet]:
        statement = (select(Vault)
                     .join(UserToVault)
                     .where(UserToVault.user_id == user_id))
        res = await self._session.exec(statement)
        vaults = res.all()

        return [VaultGet.model_validate(v) for v in vaults]