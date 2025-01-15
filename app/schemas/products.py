from datetime import datetime

from pydantic import BaseModel

class BaseSchema(BaseModel):
    name: str

    slug: str

class BaseGetSchema(BaseSchema):
    id: int
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