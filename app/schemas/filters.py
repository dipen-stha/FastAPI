from datetime import datetime

from pydantic import BaseModel, Field

from app.utils.enum.users import OrderPaymentMethod, OrderStatusEnum, PaymentStatusEnum


class BaseFilter(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)


class ProductFilter(BaseFilter):
    name: str | None = None
    price: int | None = None
    in_stock: bool | None = None


class OrderFilter(BaseFilter):
    status: OrderStatusEnum | None = None
    payment_method: OrderPaymentMethod | None = None
    payment_status: PaymentStatusEnum | None = None
    ordered_on: datetime | None = None
    product: str | None = None
