from fastapi import APIRouter, HTTPException
from app.models.schemas import UserRegister, UserLogin, TokenResponse
from app.services.auth_service import hash_password, verify_password, create_access_token
from app.db.mongo import users_col
from datetime import datetime

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def register(body: UserRegister):
    existing = await users_col.find_one({"email": body.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = {
        "name": body.name,
        "email": body.email,
        "password": hash_password(body.password),
        "created_at": datetime.utcnow(),
    }
    result = await users_col.insert_one(user)
    token = create_access_token({"sub": str(result.inserted_id)})
    return {"access_token": token, "user": {"name": body.name, "email": body.email}}


@router.post("/login", response_model=TokenResponse)
async def login(body: UserLogin):
    user = await users_col.find_one({"email": body.email})
    if not user or not verify_password(body.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user["_id"])})
    return {"access_token": token, "user": {"name": user["name"], "email": user["email"]}}
