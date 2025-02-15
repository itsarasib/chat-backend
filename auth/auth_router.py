from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth import auth_schemas
from auth.auth_bearer import JWTBearer
from auth.auth_service import AuthService
from auth.auth_utils import create_access_token, create_refresh_token, verify_password
from database import get_db
from models import User
import models

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register_user(user: auth_schemas.UserCreate, db: Session = Depends(get_db)):
    return AuthService.register_user(user, db)

@router.post("/login", response_model=auth_schemas.TokenSchema)
def login(request: auth_schemas.requestdetails, db: Session = Depends(get_db)):
    return AuthService.login_user(request, db)

@router.get("/getusers")
def getusers( dependencies=Depends(JWTBearer()),db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    return user