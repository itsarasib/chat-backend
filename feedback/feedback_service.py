from sqlalchemy.orm import Session
from models import Message, User
from fastapi import HTTPException

class FeedbackService:
    @staticmethod
    def give_feedback(messageId: str, feedback: str, user: User, db: Session):
        message = db.query(Message).filter(Message.id == messageId).first()
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")

        if message.role != "assistant":
            raise HTTPException(status_code=400, detail="Feedback can only be given to assistant messages")

        if feedback not in ["good", "bad"]:
            raise HTTPException(status_code=400, detail="Invalid feedback value")

        message.feedback = feedback
        db.commit()
        return {"message": "Feedback submitted successfully"}