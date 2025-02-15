from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import users.users_service as users_service, users.users_schemas as users_schemas
from database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[users_schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return users_service.get_users(db)

@router.post("/", response_model=users_schemas.UserResponse)
def create_user(user: users_schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = users_service.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return users_service.create_user(db, user)
