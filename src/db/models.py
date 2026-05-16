from sqlmodel import SQLModel, Field, Relationship, Enum as PgEnum 
from sqlalchemy import Column, DateTime, func 
from fastapi_users.db import SQLAlchemyBaseUserTableUUID

from uuid import UUID 
from uuid6 import uuid7 
from datetime import datetime 
from enum import Enum 
from decimal import Decimal 
from pydantic import EmailStr

class UserRole(str, Enum): 
    ADMIN = "ADMIN",
    USER = "USER"


class Vault(SQLModel, table=True):
    __tablename__: str = "vaults"
    id: UUID = Field(default_factory=uuid7, primary_key=True)
    name: str = Field(nullable=False)
    monthly_limit: Decimal = Field(
        default=0,
        max_digits=7,
        decimal_places=2
    )


class Category(SQLModel, table=True):
    __tablename__: str = "categories"
    id: UUID = Field(default_factory=uuid7, primary_key=True)
    vault_id: UUID = Field(foreign_key="vaults.id", index=True)
    name: str = Field(nullable=False)
    monthly_limit: Decimal = Field(
        default=0,
        max_digits=7,
        decimal_places=2)
    

class Transaction(SQLModel, table=True):
    __tablename__: str = "transactions"
    id: UUID = Field(default_factory=uuid7, primary_key=True)
    category_id: UUID = Field(foreign_key="categories.id")
    vault_id: UUID = Field(foreign_key="vaults.id")
    user_id: UUID = Field(foreign_key="users.id")
    date: datetime = Field(sa_column=Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(), 
        index=True
    ))
    total: Decimal = Field(max_digits=7,
                            decimal_places=2)
    

class User(SQLModel, table=True):
    __tablename__: str = "users"
    id: UUID = Field(default_factory=uuid7, primary_key=True)
    name: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False, unique=True)
    hashed_password: str = Field(nullable=False, exclude=True, repr=False)
    is_active: bool = Field(nullable=True, default=True)
    is_superuser: bool = Field(nullable=False, default=True)
    is_verified: bool = Field(nullable=False, default=True)
    


class UserToVault(SQLModel, table=True):
    __tablename__: str = "users_to_vaults"
    user_id: UUID = Field(foreign_key="users.id", primary_key=True)
    vault_id: UUID = Field(foreign_key="vaults.id", primary_key=True, index=True)
    role: UserRole = Field(sa_column=Column(
        PgEnum(UserRole, name="user_role"),
        nullable=False,
        server_default=UserRole.USER
    ))
