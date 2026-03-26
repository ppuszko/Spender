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


class Vault(SQLModel, table=True):
    __tablename__: str = "vaults"
    uid: UUID = Field(default_factory=uuid7, primary_key=True)
    name: str = Field(nullable=False)
    monthly_limit: Decimal = Field(
        default=0,
        max_digits=7,
        decimal_places=2
    )


class Category(SQLModel, table=True):
    __tablename__: str = "categories"
    uid: UUID = Field(default_factory=uuid7, primary_key=True)
    vault_uid: UUID = Field(default_factory=uuid7, foreign_key="vaults.uid", index=True)
    name: str = Field(nullable=False)
    monthly_limit: Decimal = Field(
        default=0,
        max_digits=7,
        decimal_places=2)
    

class Transaction(SQLModel, table=True):
    __tablename__: str = "transactions"
    uid: UUID = Field(default_factory=uuid7, primary_key=True)
    category_uid: UUID = Field(foreign_key="categories.uid")
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
    uid: UUID = Field(default_factory=uuid7, primary_key=True)
    name: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False, unique=True)
    password_hash: str = Field(nullable=False, exclude=True)
    role: UserRole = Field(sa_column=Column(
        PgEnum(UserRole, name="user_role"),
        nullable=False,
        server_default=UserRole.USER
    ))


class UserToVault(SQLModel, table=True):
    __tablename__: str = "users_to_vaults"
    user_uid: UUID = Field(foreign_key="users.uid", primary_key=True)
    vault_uid: UUID = Field(foreign_key="vaults.uid", primary_key=True, index=True)
    
