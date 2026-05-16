from pydantic import BaseModel, ConfigDict
from decimal import Decimal 
from uuid import UUID 

class VaultCreate(BaseModel): 
    name: str
    monthly_limit: Decimal

    model_config = ConfigDict(from_attributes=True)


class VaultGet(BaseModel): 
    uid: UUID 
    name: str
    monthly_limit: Decimal

    model_config = ConfigDict(from_attributes=True)