from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from auth import authenticate_request, generate_keys
from database import get_db
from models import TestModel

app = FastAPI()

# Allow both localhost (for development) and production frontend
origins = [
    "https://www.razorit.com",  # Production frontend
    "http://www.razorit.com",  # Production frontend
    "https://api.razorit.com",  # Secure API access
    "http://api.razorit.com",  # Secure API access
    "http://localhost:8080",  # Local dev environment
    "https://localhost:8080",  # Local dev environment
]

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow requests from multiple origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def root():
    return {"message": "API Authentication"}

@app.get("/secure-data")
async def secure_data(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello {current_user['username']}, you have access to secure data."}

@app.get("/generate-keys")
async def generate_keys_endpoint():
    """ Generate new access key & secret on demand """
    new_access
