from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_db
from models import TestModel

app = FastAPI()

@app.get("/test-db")
async def test_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TestModel))
    items = result.scalars().all()
    return {"data": [item.name for item in items]}
