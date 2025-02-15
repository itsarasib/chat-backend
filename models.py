from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class TokenTable(Base):
    __tablename__ = "tokens"
    user_id = Column(Integer)
    access_toke = Column(String(450), primary_key=True)
    refresh_toke = Column(String(450),nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.utcnow)
    
class TempMessage(Base):
    __tablename__ = "temp_messages"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)


# from sqlalchemy import Boolean, Column, DateTime, Integer, String, Float, ForeignKey, Enum, TIMESTAMP, func
# from sqlalchemy.orm import relationship, declarative_base
# from enum import Enum as PyEnum

# Base = declarative_base()

# class MessageRole(str, PyEnum):
#     assistant = "assistant"
#     user = "user"

# class MessageFeedback(str, PyEnum):
#     good = "good"
#     bad = "bad"
#     non = "non"

# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     email = Column(String, unique=True, nullable=False)
#     password = Column(String, nullable=False)

#     conversations = relationship("Conversation", back_populates="user")


# class TokenTable(Base):
#     __tablename__ = "tokens"
#     user_id = Column(Integer)
#     access_toke = Column(String(450), primary_key=True)
#     refresh_toke = Column(String(450),nullable=False)
#     status = Column(Boolean)
#     created_date = Column(DateTime, server_default=func.now())


# class Config(Base):
#     __tablename__ = 'config'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     systemPrompt = Column(String, nullable=False)
#     model = Column(String, nullable=False)
#     maxTokens = Column(Integer, nullable=False)
#     temperature = Column(Float, nullable=False)
#     topP = Column(Float, nullable=False)
#     topK = Column(Float, nullable=False)
#     repetitionPenalty = Column(Float, nullable=False)
#     minP = Column(Float, nullable=False)

#     conversations = relationship("Conversation", back_populates="config")


# class Conversation(Base):
#     __tablename__ = 'conversation'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     userId = Column(Integer, ForeignKey('users.id'), nullable=False)
#     title = Column(String, nullable=False)
#     createdAt = Column(TIMESTAMP, server_default=func.now())
#     updatedAt = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
#     configId = Column(Integer, ForeignKey('config.id'), nullable=False)

#     user = relationship("User", back_populates="conversations")
#     config = relationship("Config", back_populates="conversations")
#     messages = relationship("Message", back_populates="conversation")


# class Message(Base):
#     __tablename__ = 'message'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     conversationId = Column(Integer, ForeignKey('conversation.id'), nullable=False)
#     content = Column(String, nullable=False)
#     role = Column(Enum(MessageRole), nullable=False)
#     feedback = Column(Enum(MessageFeedback), default=MessageFeedback.non, nullable=False)
#     tokenCounter = Column(Integer, nullable=False)
#     speed = Column(Float, nullable=False)
#     createdAt = Column(TIMESTAMP, server_default=func.now())
#     updatedAt = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

#     conversation = relationship("Conversation", back_populates="messages")