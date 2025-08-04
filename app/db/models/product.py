from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel

from .base import OrderProductLink


class BaseTimeStampSlugModel(SQLModel):
    __abstract__ = True

    slug: str | None = Field(max_length=255, unique=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # def __init__(self, **kwargs):  # Need to change this, we need save() like behavior to save slug on instance creation
    #     super().__init__()
    #     if hasattr(self, 'name') and self.name and not self.slug:
    #         self.slug = slugify(text=self.name)
    #     super().__init__()


class CategoryProductPivot(SQLModel, table=True):
    __tablename__ = "product_categories"

    category_id: int = Field(foreign_key="categories.id", primary_key=True)
    product_id: int = Field(foreign_key="products.id", primary_key=True)


class Category(BaseTimeStampSlugModel, table=True):
    __tablename__ = "categories"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    products: list["Product"] = Relationship(
        back_populates="categories", link_model=CategoryProductPivot
    )


class Product(BaseTimeStampSlugModel, table=True):
    __tablename__ = "products"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    categories: list["Category"] = Relationship(
        back_populates="products", link_model=CategoryProductPivot
    )
    price: int | None = Field(default=0)
    user_carts: list["UserCart"] = Relationship(back_populates="product")
    total_quantity: int | None = Field(default=0)
    orders: list["UserOrder"] = Relationship(
        back_populates="products", link_model=OrderProductLink
    )
