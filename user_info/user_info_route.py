from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.auth_utils import get_current_user
from database import get_db
from models import User

router = APIRouter(prefix="/info", tags=["User"])

#get
@router.post("/")
def get_user_info(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return {
        "id": user.id,
        "email": user.email,
    }