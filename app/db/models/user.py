from enum import unique
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query

from sqlmodel import Field, Session, SQLModel, Relationship

class UserRoleLink(SQLModel, table=True):
    __tablename__ = 'user_role'

    user_id: int = Field(foreign_key='users.id', primary_key=True)
    role_id: int = Field(foreign_key='roles.id', primary_key=True)

class User(SQLModel, table=True):
    __tablename__ = 'users'

    id: int | None = Field(default=None, primary_key=True, sa_column_kwargs={'autoincrement': True})
    name: str = Field(index=True, max_length=255)
    email: str = Field(max_length=255)
    username: str = Field(max_length=255, unique=True)
    age: int | None = Field(default=None, index=True)
    hashed_password: str = Field()
    is_active: bool = Field(default=True)
    is_archived: bool = Field(default=False)
    is_superuser: bool = Field(default=False, nullable=False)
    roles: list['Role'] = Relationship(back_populates='users', link_model=UserRoleLink)


class RolePermissionLink(SQLModel, table=True):
    __tablename__ = 'role_permission'

    role_id: int = Field(foreign_key='roles.id', primary_key=True)
    permission_id: int = Field(foreign_key='permissions.id', primary_key=True)

class Role(SQLModel, table=True):
    __tablename__ = 'roles'

    id: int | None = Field(default=None, primary_key=True, sa_column_kwargs={'autoincrement': True})
    name: str = Field(max_length=100, unique=True)
    display_name: str = Field(max_length=255, default=None, nullable=True)
    users: list['User'] = Relationship(back_populates='roles', link_model=UserRoleLink)
    permissions: list['Permission'] = Relationship(back_populates='roles', link_model=RolePermissionLink)


class Permission(SQLModel, table=True):
    __tablename__ = 'permissions'

    id: int | None = Field(default=None, primary_key=True, sa_column_kwargs={'autoincrement': True})
    name: str = Field(index=True, max_length=255, unique=True)
    display_name: str = Field(max_length=255)
    roles: list['Role'] = Relationship(back_populates='permissions', link_model=RolePermissionLink)

