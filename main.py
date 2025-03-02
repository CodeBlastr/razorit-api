import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from services.mail import send_email, EmailSchema
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from auth import router as auth_router, get_current_user
from database import get_db
from models import TestModel

app = FastAPI()

# Allow frontend domains to access the backend API
origins = [
    "https://www.razorit.com",  # Production frontend
    "http://www.razorit.com",  # Production frontend
    "https://api.razorit.com",  # Secure API access
    "http://api.razorit.com",  # Secure API access
    "http://localhost:8080",  # Local dev environment
    "https://localhost:8080",  # Local dev environment
    "http://localhost:5173",  # Local react dev environment
    "https://localhost:5173",  # Local react dev environment
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

@app.get("/test-smtp")
async def test_smtp():
    import smtplib
    import os

    smtp_server = os.getenv("MAIL_SERVER")
    smtp_port = int(os.getenv("MAIL_PORT"))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(os.getenv("MAIL_USERNAME"), os.getenv("MAIL_PASSWORD"))
        server.quit()
        return {"message": "SMTP Connection successful"}
    except Exception as e:
        return {"error": str(e)}


