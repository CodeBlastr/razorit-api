from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db, engine
from models import TestModel
import asyncio

async def seed():
    async with AsyncSession(engine) as session:
        async with session.begin():
            # Insert test data
            test_data = [
                TestModel(name="Sample Data 1"),
                TestModel(name="Sample Data 2"),
                TestModel(name="Sample Data 3"),
            ]
            session.add(test_data)

        await session.commit()
        print("✅ Database seeded successfully!")

# Run the seeding process
if __name__ == "__main__":
    asyncio.run(seed())