from sqlmodel import SQLModel, Field, Relationship, Enum as PgEnum 
from sqlalchemy import Column, DateTime, func 

from uuid import UUID 
from uuid6 import uuid7 
from datetime import datetime 
from enum import Enum 
from decimal import Decimal 
from pydantic import EmailStr

class UserRole(str, Enum): 
    ADMIN = "ADMIN",
    USER = "USER"

class BaseSQLModel(SQLModel):
    uid: UUID = Field(default_factory=uuid7, primary_key=True)


class Vault(BaseSQLModel, table=True):
    __tablename__: str = "vaults"
    name: str = Field(nullable=False)
    monthly_limit: Decimal = Field(
        default=0,
        max_digits=7,
        decimal_places=2
    )


class Category(BaseSQLModel, table=True):
    __tablename__: str = "categories"
    vault_uid: UUID = Field(foreign_key="vaults.uid", index=True)
    name: str = Field(nullable=False)
    monthly_limit: Decimal = Field(
        default=0,
        max_digits=7,
        decimal_places=2)
    

class Transaction(BaseSQLModel, table=True):
    __tablename__: str = "transactions"
    category_uid: UUID = Field(foreign_key="categories.uid")
    vault_uid: UUID = Field(foreign_key="vaults.uid")
    date: datetime = Field(sa_column=Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(), 
        index=True
    ))
    total: Decimal = Field(max_digits=7,
                            decimal_places=2)
    

class User(BaseSQLModel, table=True):
    __tablename__: str = "users"
    name: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False, unique=True)
    password_hash: str = Field(nullable=False, exclude=True, repr=False)
    


class UserToVault(SQLModel, table=True):
    __tablename__: str = "users_to_vaults"
    user_uid: UUID = Field(foreign_key="users.uid", primary_key=True)
    vault_uid: UUID = Field(foreign_key="vaults.uid", primary_key=True, index=True)
    role: UserRole = Field(sa_column=Column(
        PgEnum(UserRole, name="user_role"),
        nullable=False,
        server_default=UserRole.USER
    ))
