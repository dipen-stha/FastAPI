from pydantic_core.core_schema import ValidationInfo
from sqlmodel import Session

from pydantic import BaseModel, field_validator, ValidationError

from app.db.models import User


class BaseUser(BaseModel):
    id: int | None =  None
    name: str
    username: str
    email: str
    age: int


class UserIn(BaseUser):
    hashed_password: str

    class Config:
        from_attributes = True


class UserOut(BaseUser):
    is_active: bool
    is_archived: bool

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class TokenData(BaseModel):
    username: str = None

class BaseRole(BaseModel):
    id: int | None
    name: str


class RoleIn(BaseRole):
    id: int | None = None
    permissions: list[int] | None


class RoleOut(BaseRole):
    permissions: list[int] | None

    class Config:
        from_attributes = True

class BasePermission(BaseModel):
    id: int | None
    display_name: str

class PermissionIn(BasePermission):
    id: int | None = None

class PermissionOut(BaseModel):
    name: str

    class Config:
        from_attributes = True