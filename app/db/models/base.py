from datetime import datetime

from sqlmodel import SQLModel, Field


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



class OrderProductLink(SQLModel, table=True):

    id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="user_orders.id")
    product_id: int = Field(foreign_key="products.id")

    created_at: datetime = Field(default=datetime.now)
    updated_at: datetime = Field(default=datetime.now)

    __tablename__ = "orders_products_link"