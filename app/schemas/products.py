from datetime import datetime

from pydantic import BaseModel


class BaseSchema(BaseModel):
    name: str


class BaseGetSchema(BaseSchema):
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime


class ProductInSchema(BaseSchema):
    pass


class ProductOutSchema(BaseGetSchema):
    pass


class CategoryInSchema(BaseSchema):
    pass


class CategoryOutSchema(BaseGetSchema):
    pass
