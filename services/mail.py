from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import os
import logging

logger = logging.getLogger(__name__)

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 465)),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS") == "True",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS") == "True",
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_email(email):
    try:
        fm = FastMail(conf)

        message = MessageSchema(
            subject=email.subject,
            recipients=[email.email],
            body=email.message,
            subtype="plain",
        )

        # Log full email details before sending
        logger.info(f"Preparing to send email")
        logger.info(f"From: {os.getenv('MAIL_FROM')}")
        logger.info(f"To: {email.email}")
        logger.info(f"Subject: {email.subject}")
        logger.info(f"Body: {email.message}")

        await fm.send_message(message)
        logger.info("Email sent successfully!")

    except Exception as e:
        logger.error(f"SMTP ERROR: {str(e)}")
        raise
