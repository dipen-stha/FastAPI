from datetime import datetime

from pydantic import BaseModel

from app.db.models import UserOrder
from app.schemas.products import ProductOutSchema
from app.schemas.user import UserOut
from app.utils.enum.users import OrderPaymentMethod, OrderStatusEnum, PaymentStatusEnum


class UserOrderIn(BaseModel):
    user_id: int
    product_ids: list[int]
    payment_method: str = OrderPaymentMethod.CASH_ON_DELIVERY.value
    payment_status: str = PaymentStatusEnum.PENDING.value


class UserOrderOut(BaseModel):
    user: UserOut
    products: list[ProductOutSchema]
    ordered_on: datetime
    status: OrderStatusEnum | None
    payment_method: OrderPaymentMethod | None
    payment_status: PaymentStatusEnum | None

    class Config:
        from_attributes = True

    @staticmethod
    def from_orm(user_order: UserOrder):
        products_schemas = [
            ProductOutSchema.model_validate(product) for product in user_order.products
        ]
        return UserOrderOut(
            user=UserOut.model_validate(user_order.user),
            products=products_schemas,
            ordered_on=user_order.ordered_on,
            status=user_order.status,
            payment_method=user_order.payment_method,
            payment_status=user_order.payment_status,
        )
