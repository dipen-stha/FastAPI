from .celery import celery
from app.db.models.user import User, UserOrder
from app.utils.email import send_email

async def send_email_for_order(user: User, order: UserOrder):
    try:
        await send_email("You order was received!", ["dipenstha00@gmail.com"], f"You order id is f{order.id}")
        print("Email sent successfully")
    except Exception as e:
        print(e)