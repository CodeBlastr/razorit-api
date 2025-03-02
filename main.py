import os
import smtplib
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from auth import router as auth_router, get_current_user
from database import get_db
from models import TestModel
from services.mail import send_email, EmailSchema

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Allow frontend domains to access the backend API
origins = [
    "https://www.razorit.com",
    "http://www.razorit.com",
    "https://api.razorit.com",
    "http://api.razorit.com",
    "http://localhost:8080",
    "https://localhost:8080",
    "http://localhost:5173",
    "https://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.get("/test-db")
async def test_db(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    result = await db.execute(select(TestModel))
    items = result.scalars().all()
    return {"data": [item.name for item in items]}

@app.post("/send-test-email/")
async def send_test_email(email: EmailSchema, current_user: dict = Depends(get_current_user)):
    await send_email(email)
    return {"message": "Email sent!"}

# Debugging route for SMTP connectivity
@app.get("/test-smtp-connection")
async def test_smtp_connection():
    smtp_server = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("MAIL_PORT", 465))
    mail_username = os.getenv("MAIL_USERNAME")
    mail_password = os.getenv("MAIL_PASSWORD")
    use_ssl = os.getenv("MAIL_SSL_TLS", "False").lower() == "true"
    use_starttls = os.getenv("MAIL_STARTTLS", "False").lower() == "true"

    # Log environment values for debugging
    logger.info(f"SMTP Debugging")
    logger.info(f"Connecting to SMTP Server: {smtp_server}")
    logger.info(f"Using Port: {smtp_port}")
    logger.info(f"Using Username: {mail_username}")
    logger.info(f"Using SSL/TLS: {use_ssl}")
    logger.info(f"Using STARTTLS: {use_starttls}")

    try:
        # Select SSL or TLS based on configuration
        if use_ssl:
            logger.info("Using SMTP_SSL for secure connection")
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else:
            logger.info("Using STARTTLS for connection upgrade")
            server = smtplib.SMTP(smtp_server, smtp_port)
            if use_starttls:
                server.starttls()

        server.login(mail_username, mail_password)
        server.quit()

        logger.info("SMTP Connection successful!")
        return {"message": "SMTP Connection successful!"}

    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"Gmail Authentication Failed: {e}")
        return {"error": "Gmail Authentication Failed", "details": str(e)}

    except smtplib.SMTPConnectError as e:
        logger.error(f"AWS IP may be blocked by Google: {e}")
        return {"error": "AWS IP may be blocked by Google", "details": str(e)}

    except smtplib.SMTPException as e:
        logger.error(f"SMTP Error: {e}")
        return {"error": "SMTP Error", "details": str(e)}

    except Exception as e:
        logger.error(f"Unknown SMTP Error: {e}")
        return {"error": "Unknown SMTP Error", "details": str(e)}
