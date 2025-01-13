from pydantic import BaseModel

class BaseUser(BaseModel):
    id: int | None
    name: str
    username: str
    email: str
    age: int


class UserIn(BaseUser):
    hashed_password: str


class UserOut(BaseUser):
    is_active: bool
    is_archived: bool

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    hashed_password: str