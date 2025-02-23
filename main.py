from fastapi import FastAPI
import asyncpg
import os

app = FastAPI()

# Database credentials from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

async def connect_to_db():
    try:
        conn = await asyncpg.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        return str(e)

@app.get("/test-db")
async def test_db_connection():
    conn = await connect_to_db()
    if isinstance(conn, str):
        return {"error": conn}
    else:
        await conn.close()
        return {"message": "Connected to the database successfully!"}
