from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import engine, async_session
from models import TestModel
import asyncio

async def seed_data():
    async with async_session() as session:
        async with session.begin():
            # Check if data already exists
            result = await session.execute(select(TestModel))
            existing_data = result.scalars().all()

            if existing_data:
                print("✅ Database already seeded. Skipping...")
                return

            print("🌱 Seeding database...")
            test_data = [
                TestModel(name="Sample Data 1"),
                TestModel(name="Sample Data 2"),
                TestModel(name="Sample Data 3"),
            ]
            session.add_all(test_data)
            await session.commit()
            print("✅ Seeding completed.")

if __name__ == "__main__":
    asyncio.run(seed_data())
