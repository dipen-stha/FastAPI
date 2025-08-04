from enum import Enum


class GenderEnum(str, Enum):
    MALE = "Male"
    FEMALE = "Female"


class OrderStatusEnum(str, Enum):
    RECEIVED = "received"
    ON_THE_WAY = "on_the_way"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderPaymentMethod(str, Enum):
    CASH_ON_DELIVERY = "cash_on_delivery"
    STRIPE = "stripe"
    PAYPAL = "paypal"
    WESTERN_UNION = "western_union"
    GOOGLE_PAY = "google_pay"


class PaymentStatusEnum(str, Enum):
    PENDING = "pending"
    PAID = "paid"
