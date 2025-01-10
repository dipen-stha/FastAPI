from enum import unique
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query

from sqlmodel import Field, Session, SQLModel, create_engine, select

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=255)
    email: str = Field(max_length=255)
    username: str = Field(max_length=255, unique=True)
    age: int | None = Field(default=None, index=True)
    hashed_password: str = Field()
    is_active: bool = Field(default=True)
    is_archived: bool = Field(default=True)
