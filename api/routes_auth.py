import os

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.orm import Session

from api.auth import hash_password, verify_password, create_access_token, decode_access_token
from api.database import get_db
from api.models_auth import Token, UserCreate, UserLogin, UserResponse
from api.models_db_auth import UserDB

MOCK_CVR_URL = os.getenv("MOCK_CVR_URL", "https://pythonayd-mock-cvr.onrender.com")

router = APIRouter(prefix="/auth", tags=["auth"])
_bearer = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    db: Session = Depends(get_db),
) -> UserDB:
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Ugyldigt token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Ugyldigt token")

    user = db.query(UserDB).filter(UserDB.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Bruger ikke fundet")
    return user


@router.post("/register", response_model=UserResponse, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(UserDB).filter(UserDB.email == payload.email).first():
        raise HTTPException(status_code=409, detail="Email er allerede registreret")

    try:
        response = httpx.get(f"{MOCK_CVR_URL}/cvr/{payload.cvr}", timeout=5)
        if response.status_code == 404:
            raise HTTPException(status_code=400, detail=f"CVR-nummer {payload.cvr} ikke fundet")
        response.raise_for_status()
        cvr_data = response.json()
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Mock CVR API er utilgængeligt")

    user = UserDB(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        cvr=payload.cvr,
        firmanavn=cvr_data["firmanavn"],
        adresse=cvr_data["adresse"],
        postnummer=cvr_data["postnummer"],
        by=cvr_data["by"],
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Forkert email eller adgangskode")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def me(current_user: UserDB = Depends(get_current_user)):
    return current_user
