from fastapi import APIRouter, Depends
from requests import Session

from auth.auth_utils import get_current_user
from conversation.conversation_service import ConversationService
from database import get_db
from models import User


router = APIRouter(prefix="/conversations", tags=["Conversations"])

@router.post("/")
def get_all_conversations(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ConversationService.get_all_conversations(user, db)

@router.post("/{conversationId}")
def get_messages(conversationId: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ConversationService.get_messages(conversationId, user, db)

@router.delete("/{conversationId}")
def delete_conversation(conversationId: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ConversationService.delete_conversation(conversationId, user, db)