from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Conversation, Message, User


class ConversationService:
    @staticmethod
    def get_all_conversations(user: User, db: Session):
        conversations = db.query(Conversation).filter(Conversation.userId == user.id).all()
        if not conversations:
            raise HTTPException(status_code=404, detail="No conversations found")

        return [
            {
                "conversationId": conv.id,
                "title": conv.title,
                "userId": conv.userId,
                "createdAt": conv.createdAt
            }
            for conv in conversations
        ]

    @staticmethod
    def get_messages(conversationId: str, user: User, db: Session):
        conversation = db.query(Conversation).filter(Conversation.id == conversationId, Conversation.userId == user.id).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        messages = db.query(Message).filter(Message.conversationId == conversationId).order_by(Message.createdAt).all()
        if not messages:
            raise HTTPException(status_code=404, detail="No messages found for this conversation")

        return [
            {
                "messageId": msg.id,
                "content": msg.content,
                "role": msg.role,
                "createdAt": msg.createdAt
            }
            for msg in messages
        ]
        
    @staticmethod
    def delete_conversation(conversationId: str, user: User, db: Session):
        conversation = db.query(Conversation).filter(Conversation.id == conversationId, Conversation.userId == user.id).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        db.query(Message).filter(Message.conversationId == conversationId).delete()
        db.delete(conversation)
        db.commit()
        return {"message": "Conversation deleted successfully"}