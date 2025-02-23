from fastapi import FastAPI
import os
import asyncpg

# Load environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

app = FastAPI()

# Function to test DB connection
async def test_db_connection():
    try:
        conn = await asyncpg.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        rows = await conn.fetch("SELECT current_database();")
        await conn.close()
        return {"db_name": rows[0]["current_database"]}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def read_root():
    return {"message": "Hello from Backend API"}

@app.get("/test-db")
async def test_db():
    return await test_db_connection()
