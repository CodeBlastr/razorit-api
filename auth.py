import os
import base64
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Form, Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Credentials from Environment
CLIENT_ID = os.getenv("CLIENT_ID", "default-client-id")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "default-client-secret")
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secure-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# FastAPI Router for Authentication
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def create_access_token(data: dict, expires_delta: timedelta):
    """Generates a JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/token")
async def generate_token(
    client_id: str = Form(None),
    client_secret: str = Form(None),
    authorization: str = Header(None),
):
    """
    Authenticate client using either:
    1. Basic Auth (Authorization Header)
    2. Form Data (client_id, client_secret)
    """
    
    # Option 1: If Authorization Header (Basic Auth) is used
    if authorization:
        try:
            scheme, credentials = authorization.split()
            if scheme.lower() != "basic":
                raise HTTPException(status_code=401, detail="Invalid authentication scheme")

            decoded = base64.b64decode(credentials).decode("utf-8")
            auth_client_id, auth_client_secret = decoded.split(":")
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid Basic Auth format")

        if auth_client_id != CLIENT_ID or auth_client_secret != CLIENT_SECRET:
            raise HTTPException(status_code=401, detail="Invalid client credentials")

    # Option 2: If Form Data is used
    elif client_id and client_secret:
        if client_id != CLIENT_ID or client_secret != CLIENT_SECRET:
            raise HTTPException(status_code=401, detail="Invalid client credentials")
    
    else:
        raise HTTPException(status_code=401, detail="Missing credentials")

    # Generate JWT Token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": CLIENT_ID}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Validate JWT Token"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        client_id: str = payload.get("sub")
        if client_id is None or client_id != CLIENT_ID:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception
    return {"client_id": CLIENT_ID}
