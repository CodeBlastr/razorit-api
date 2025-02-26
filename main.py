from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import timedelta

from auth import authenticate_user, create_access_token, get_current_user
from database import get_db
from models import TestModel

app = FastAPI()

# Allow both localhost (for development) and production frontend
origins = [
    "https://www.razorit.com",
    "http://www.razorit.com",
    "https://api.razorit.com",
    "http://api.razorit.com",
    "http://localhost:8080",
    "https://localhost:8080",
]

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "API Seeder Added"}

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """ Authenticate user and return a JWT access token """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/test-db")
async def test_db(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """ Secure endpoint that requires authentication """
    result = await db.execute(select(TestModel))
    items = result.scalars().all()
    return {"data": [item.name for item in items], "user": current_user}

@app.get("/secure-data")
async def secure_data(current_user: dict = Depends(get_current_user)):
    """ Secure endpoint that requires authentication """
    return {"message": f"Hello {current_user['username']}, you have access to secure data."}
