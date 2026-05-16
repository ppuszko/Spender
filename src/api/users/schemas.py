from fastapi_users import schemas 

from pydantic import BaseModel
from decimal import Decimal
from pydantic import EmailStr
from uuid import UUID 



class UserRead(schemas.BaseUser[UUID]):
    pass 

class UserCreate(schemas.BaseUserCreate):
    pass 

class UserUpdate(schemas.BaseUserUpdate):
    pass