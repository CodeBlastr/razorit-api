import os
import logging
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class EmailSchema(BaseModel):
    email: str
    subject: str
    message: str

# Log environment values
logger.info(f"Using SMTP Server: {os.getenv('MAIL_SERVER')}")
logger.info(f"Using SMTP Port: {os.getenv('MAIL_PORT')}")
logger.info(f"Using SMTP Username: {os.getenv('MAIL_USERNAME')}")
logger.info(f"Using MAIL_FROM: {os.getenv('MAIL_FROM')}")
logger.info(f"Using TLS: {os.getenv('MAIL_STARTTLS', 'False')}")
logger.info(f"Using SSL: {os.getenv('MAIL_SSL_TLS', 'False')}")

# Ensure credentials are passed explicitly
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER", "email-smtp.us-east-2.amazonaws.com"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS", "True").lower() == "true",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS", "False").lower() == "true",
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True  # Ensure SSL/TLS verification
)

async def send_email(email: EmailSchema):
    message = MessageSchema(
        subject=email.subject,
        recipients=[email.email],
        body=email.message,
        subtype="html",
    )

    try:
        logger.info("🚀 Sending email via FastMail")
        fm = FastMail(conf)
        await fm.send_message(message)
        logger.info("Email sent successfully!")
    except Exception as e:
        logger.error(f"Email sending failed: {e}")
        raise
