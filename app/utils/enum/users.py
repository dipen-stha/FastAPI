from enum import Enum


class GenderEnum(str, Enum):
    MALE = "Male"
    FEMALE = "Female"


class OrderStatusEnum(str, Enum):
    RECEIVED = "Received"
    ON_THE_WAY = "On The Way"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
