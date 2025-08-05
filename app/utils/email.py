from pydantic import EmailStr

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

from app.config import settings

config = ConnectionConfig(
    MAIL_USERNAME=settings.EMAIL_USERNAME,
    MAIL_PASSWORD=settings.EMAIL_PASSWORD,
    MAIL_FROM=settings.EMAIL_FROM,
    MAIL_SERVER=settings.EMAIL_SERVER,
    MAIL_PORT=settings.EMAIL_PORT,
    MAIL_FROM_NAME=settings.EMAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)

async def send_email(subject: str, recipients: list[EmailStr], body: str):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype=MessageType.html,
    )

    fm = FastMail(config)
    await fm.send_message(message)
