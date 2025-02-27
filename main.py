from fastapi import FastAPI, Depends
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
