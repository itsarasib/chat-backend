from enum import Enum
from pydantic import BaseModel
from typing import List

class MessageRole(str, Enum):
    system = "system"
    user = "user"
    assistant = "assistant"
    
class Message(BaseModel):
    role: MessageRole
    content: str
    
class CompletionRequest(BaseModel):
    conversationId: str
    model: str
    maxTokens: int
    messages: List[Message]
    temperature: float
    topP: float
    topK: float
    repetitionPenalty: float
    minP: float
    
    
