from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_db
from models import TestModel

app = FastAPI()

# ✅ Allow both localhost (for development) and production frontend
origins = [
]
origins = [
    "https://www.razorit.com", # Production frontend
    "http://www.razorit.com", # Production frontend
    "https://api.razorit.com", # ✅ Secure API access
    "http://api.razorit.com", # ✅ Secure API access
    "http://localhost:8080",  # Local dev environment
    "https://localhost:8080",  # Local dev environment
]

# ✅ Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ✅ Allow requests from multiple origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def root():
    return {"message": "API Seeder Added"}

@app.get("/test-db")
async def test_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TestModel))
    items = result.scalars().all()
    return {"data": [item.name for item in items]}
