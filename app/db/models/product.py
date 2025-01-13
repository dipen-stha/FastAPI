from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel

from slugify import slugify

class BaseTimeStampSlugModel(SQLModel):
    __abstract__ = True

    slug: str | None = Field(max_length=255, unique=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def __init__(self):
        if hasattr(self, 'name') and not self.slug:
            self.slug = slugify(self.name)


class CategoryProductPivot(SQLModel, table=True):
    __tablename__ = 'product_categories'

    category_id: int = Field(foreign_key='categories.id', primary_key=True)
    product_id: int = Field(foreign_key='products.id', primary_key=True)

class Category(BaseTimeStampSlugModel, table=True):
    __tablename__ = 'categories'

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    products: list['Product'] = Relationship(back_populates='categories', link_model=CategoryProductPivot)


class Product(BaseTimeStampSlugModel, table=True):
    __tablename__ = 'products'

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    categories: list['Category'] = Relationship(back_populates='products', link_model=CategoryProductPivot)
    price: int | None = Field(default=0)