from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from pydantic import EmailStr



class VaultPublic(BaseModel):
    

    model_config = ConfigDict(from_attributes=True)


class VaultCreate(BaseModel): 
    name: str
    monthly_limit: Decimal

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password_hash: str 


class UserLogin(BaseModel): 
    email: EmailStr
    password: str