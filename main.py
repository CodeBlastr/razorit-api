from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router, get_current_user
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import TestModel

app = FastAPI()

origins = [
    "https://www.razorit.com",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "API Ready"}

@app.get("/test-db")
async def test_db(request: Request, db: AsyncSession = Depends(get_db)):
    user = get_current_user(request)
    result = await db.execute(select(TestModel))
    items = result.scalars().all()
    return {"data": [item.name for item in items]}
