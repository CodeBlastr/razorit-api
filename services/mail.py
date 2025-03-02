from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EmailSchema(BaseModel):
    email: str
    subject: str
    message: str

# Detect environment mode
ENV = os.getenv("ENVIRONMENT", "local").lower()

# Choose MailHog for local, Gmail for production
if ENV == "production":
    print("🚀 Running in PRODUCTION mode (Using Gmail SMTP)")
else:
    print("🛠 Running in LOCAL mode (Using MailHog)")

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 1025 if ENV == "local" else 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER", "mailhog" if ENV == "local" else "smtp.gmail.com"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS", "False").lower() == "true",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS", "False").lower() == "true",
    USE_CREDENTIALS=True if ENV == "production" else False
)

async def send_email(email: EmailSchema):
    message = MessageSchema(
        subject=email.subject,
        recipients=[email.email],
        body=email.message,
        subtype="html",
    )

    fm = FastMail(conf)
    await fm.send_message(message)
