from datetime import date

from pydantic import BaseModel, field_validator, ValidationError, EmailStr

from app.db.models import User
from app.utils.enum.users import GenderEnum


class BaseUser(BaseModel):
    id: int | None =  None
    name: str
    username: str
    email: str
    age: int | None


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
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class TokenData(BaseModel):
    username: str = None

class BasePermission(BaseModel):
    id: int | None
    display_name: str

class PermissionIn(BasePermission):
    id: int | None = None

class PermissionOut(BaseModel):
    name: str

    class Config:
        from_attributes = True


class BaseRole(BaseModel):
    id: int | None
    name: str
    display_name: str


class RoleIn(BaseRole):
    id: int | None = None
    permissions: list[int] | None


class RoleOut(BaseRole):
    permissions: list[PermissionOut] | None

    class Config:
        from_attributes = True


class UserRoleLinkSchema(BaseModel):
    user_id: int
    role_ids: list[int]

class UserRoleSchema(BaseUser):
    roles: list[RoleOut] | None = None

class UserDetailSchema(UserOut):
   permissions: list[str]

   @staticmethod
   def from_orm(user: User) -> "UserDetailSchema":
       permissions = set(
           permission.name
           for role in user.roles
           for permission in role.permissions
       )
       return UserDetailSchema(
           id=user.id,
           name=user.name,
           username=user.username,
           email=user.email,
           age=user.age,
           is_active=user.is_active,
           is_archived=user.is_archived,
           permissions=list(permissions),
       )


class BaseProfile(BaseModel):
    gender: GenderEnum | None
    dob: date | None
    address: str | None


class ProfileIn(BaseProfile):
    user: int

class ProfileInPatch(BaseProfile):
    pass


class ProfileOut(BaseProfile):
    id: int | None
    user: UserOut

    class Config:
        from_attributes = True
