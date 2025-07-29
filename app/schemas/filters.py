from pydantic import BaseModel, Field


class BaseFilter(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)


class ProductFilter(BaseFilter):
    name: str | None = None
    price: int | None = None
    in_stock: bool | None = None
