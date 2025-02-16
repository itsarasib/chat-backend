from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.auth_utils import get_current_user
from database import get_db
from models import User
from feedback.feedback_service import FeedbackService
from pydantic import BaseModel

class FeedbackRequest(BaseModel):
    messageId: str
    feedback: str

router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.post("/")
def give_feedback(request: FeedbackRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return FeedbackService.give_feedback(request.messageId, request.feedback, user, db)
