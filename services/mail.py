import os
import logging
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class EmailSchema(BaseModel):
    email: str
    name: str  # Added name field
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
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS", "True").lower() == "true",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS", "False").lower() == "true",
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_email(email: EmailSchema):
    reply_to = f"{email.name} <{email.email}>"  # Correctly format Reply-To
    message = MessageSchema(
        subject=email.subject,
        recipients=[os.getenv("SALES_EMAIL", "sales@example.com")],
        body=email.message,
        subtype="html",
        headers={"Reply-To": reply_to}  # Set Reply-To to "Name <email>"
    )

    try:
        logger.info(f"Sending email via FastMail to {message.recipients}")
        fm = FastMail(conf)
        await fm.send_message(message)
        logger.info("Email sent successfully!")
    except Exception as e:
        logger.error(f"Email sending failed: {e}")
        raise
