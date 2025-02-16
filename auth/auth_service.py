from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from auth import auth_schemas
from auth.auth_utils import create_access_token, create_refresh_token, get_hashed_password, verify_password
from models import TokenTable, User


class AuthService:
    @staticmethod
    def register_user(user: auth_schemas.UserCreate, db: Session):
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        encrypted_password = get_hashed_password(user.password)

        new_user = User(email=user.email, password=encrypted_password)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "User registered successfully"}
    
    @staticmethod
    def login_user(request: auth_schemas.requestdetails, db: Session):
        user = db.query(User).filter(User.email == request.email).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")

        hashed_pass = user.password
        if not verify_password(request.password, hashed_pass):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password"
            )

        access = create_access_token(user.id)
        refresh = create_refresh_token(user.id)

        token_db = TokenTable(user_id=user.id, access_token=access, refresh_token=refresh, status=True)
        db.add(token_db)
        db.commit()
        db.refresh(token_db)

        return {
            "access_token": access,
            "refresh_token": refresh,
        }