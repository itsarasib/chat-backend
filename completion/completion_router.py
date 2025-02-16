from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from auth.auth_utils import get_current_user
from completion.completion_schemas import CompletionRequest
from completion.completion_service import CompletionService
from database import get_db
from models import User

router = APIRouter(prefix="/completions", tags=["Completions"])

@router.post("/")
def create_completion(request: CompletionRequest, db: Session = Depends(get_db), user: User =Depends(get_current_user)):
    try:
        response_generator = CompletionService.generate_completion(request, db, user)
        return StreamingResponse(response_generator, media_type="text/event-stream; charset=utf-8", headers={"Transfer-Encoding": "chunked","Cache-Control": "no-cache", "Connection": "keep-alive"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    