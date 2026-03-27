from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from pydantic import EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password_hash: str 


class UserLogin(BaseModel): 
    email: EmailStr
    password: str