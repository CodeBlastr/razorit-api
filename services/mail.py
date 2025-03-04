import os
import logging
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class EmailSchema(BaseModel):
    email: EmailStr  # Sender's email
    name: str  # Sender's name
    subject: str
    message: str
    reply_to: str | None = None  # ✅ Ensure reply_to is a string

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
    reply_to = email.reply_to if email.reply_to else f"{email.name} <{email.email}>"

    email_body = """\
    <html>
        <body>
            <p><strong>Sender Name:</strong> {name}</p>
            <p><strong>Sender Email:</strong> {email}</p>
            <p><strong>Message:</strong></p>
            <p>{message}</p>
        </body>
    </html>
    """.format(name=email.name, email=email.email, message=email.message.replace("\n", "<br>"))

    message = MessageSchema(
        subject=email.subject,
        recipients=[os.getenv("SALES_EMAIL", "sales@razorit.com")],
        body=email_body,
        subtype="html",
        reply_to=[reply_to]
    )

    try:
        logger.info(f"Sending email via FastMail to {message.recipients} with Reply-To: {reply_to}")
        fm = FastMail(conf)
        await fm.send_message(message)
        logger.info("Email sent successfully!")
    except Exception as e:
        logger.error(f"Email sending failed: {e}")
        raise
