from pydantic import BaseModel, ConfigDict
from decimal import Decimal 


class VaultPublic(BaseModel):
    

    model_config = ConfigDict(from_attributes=True)


class VaultCreate(BaseModel): 
    name: str
    monthly_limit: Decimal

    model_config = ConfigDict(from_attributes=True)
