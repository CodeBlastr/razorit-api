import os
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from jose import JWTError, jwt

# Load environment variables
load_dotenv()

# Retrieve credentials from environment
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generate JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def validate_origin(request: Request):
    """Ensure request is from an allowed frontend origin"""
    allowed_origins = ["https://www.razorit.com", "http://localhost:8080", "http://localhost:8000", "https://api.razorit.com" ]
    origin = request.headers.get("origin")
    if origin not in allowed_origins:
        raise HTTPException(status_code=403, detail="Forbidden: Unauthorized origin")

@router.post("/login")
async def login(response: Response, request: Request):
    """Login and set secure HTTP-only cookie"""
    validate_origin(request)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": ADMIN_USERNAME}, expires_delta=access_token_expires)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    return {"message": "Logged in successfully"}

@router.get("/logout")
async def logout(response: Response):
    """Logout the user by clearing the authentication cookie"""
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}

def get_current_user(request: Request):
    """Get current user from Secure Cookie"""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or username != ADMIN_USERNAME:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return {"username": ADMIN_USERNAME}
