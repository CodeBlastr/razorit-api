from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_db
from models import TestModel

app = FastAPI()

# ✅ Allow both localhost (for development) and production frontend
origins = [
    "http://localhost:3000",  # Local dev environment
    "http://127.0.0.1:3000",  # Localhost alternative
    "https://www.razorit.com",  # Production frontend
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
