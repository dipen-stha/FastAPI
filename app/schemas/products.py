from pydantic import BaseModel


class BaseSchema(BaseModel):
    name: str


class BaseGetSchema(BaseSchema):
    id: int
    slug: str
    price: float


class ProductInSchema(BaseSchema):
    pass


class ProductOutSchema(BaseGetSchema):
    in_stock: bool | None

    class Config:
        from_attributes = True


class CategoryInSchema(BaseSchema):
    pass


class CategoryOutSchema(BaseGetSchema):
    pass
