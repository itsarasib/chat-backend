import json
import time
from uuid import uuid4
from sqlalchemy.orm import Session

from completion.completion_schemas import CompletionRequest, MessageRole
from completion.completion_utils import call_external_api
from models import Conversation, Message, User

class CompletionService:
    @staticmethod
    def generate_completion(request: CompletionRequest, db: Session, user: User):
        if not request.conversationId:
            raise ValueError("conversationId is required")
        
        #compare conversationId to db, if exists save messages of role user to db
        #if not exists, create new conversationId and save messages of role user to db
        
        
         # Check if the conversation exists
        conversation = db.query(Conversation).filter(Conversation.id == request.conversationId).first()
        if not conversation:
            # Create a new conversation
            conversation = Conversation(
                id=request.conversationId,
                userId= user.id , 
                title=request.messages[-1].content,
                systemPrompt=request.messages[0].content if request.messages and request.messages[0].role == MessageRole.system else "",
                model=request.model,
                maxTokens=request.maxTokens,
                temperature=request.temperature,
                topP=request.topP,
                topK=request.topK,
                repetitionPenalty=request.repetitionPenalty,
                minP=request.minP
            )
            db.add(conversation)
            db.commit()
            
            
        messageId = str(uuid4())    
            
        # Save messages with role user to the database
        last_user_message = next((msg for msg in reversed(request.messages) if msg.role == MessageRole.user), None)
        if last_user_message:
            new_message = Message(
                id=messageId,
                conversationId= request.conversationId,
                content=last_user_message.content,
                role=MessageRole.user,
                tokenCounter=len(last_user_message.content.split()),
                speed=0.0
            )
            db.add(new_message)
        db.commit()
        
        messages = [msg.dict() for msg in request.messages]
        model = request.model
        params = {
            "max_tokens": request.maxTokens,
            "temperature": request.temperature,
            "top_p": request.topP,
            "top_k": request.topK,
            "repetition_penalty": request.repetitionPenalty,
            "min_p": request.minP,
        }

        response = call_external_api(messages, model, params)
        
        plain_text = ""
        def stream_response():
            nonlocal plain_text
            start_time = time.time()
            token_count = 0
            
            yield f'id: {messageId}\n'
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith("data: "):
                        try:
                            json_line = json.loads(decoded_line[6:])
                            content = json_line.get("choices", [{}])[0].get("delta", {}).get("content")
                            if content is None or not content:
                                yield f'token: {token_count}\n'
                                end_time = time.time()
                                speed = round(end_time - start_time, 2)
                                yield f'speed: {speed}\n'
                                break
                            if content:
                                plain_text += content
                                token_count += len(content.split())
                            yield f"data: {content}\n"
                        except Exception as e:
                            print(f"Failed to parse line: {decoded_line}, error: {e}")
            
            end_time = time.time()
            duration = round(end_time - start_time, 2)  # Calculate duration in seconds
            
            # Save the assistant's response to the database
            assistant_message = Message(
                id=str(uuid4()),
                conversationId=request.conversationId,
                content=plain_text,
                role=MessageRole.assistant,
                tokenCounter=token_count,
                speed=duration
            )
            db.add(assistant_message)
            db.commit()

            print(f"Token count: {token_count}, Speed: {duration} seconds")
            
        return stream_response()