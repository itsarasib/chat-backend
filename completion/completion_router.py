from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from completion.completion_schemas import CompletionRequest
from completion.completion_service import CompletionService
from database import get_db

router = APIRouter(prefix="/completions", tags=["Completions"])

@router.post("/")
def create_completion(request: CompletionRequest, db: Session = Depends(get_db)):
    try:
        response_generator = CompletionService.generate_completion(request, db)
        return StreamingResponse(response_generator, media_type="text/event-stream; charset=utf-8", headers={"Transfer-Encoding": "chunked","Cache-Control": "no-cache", "Connection": "keep-alive"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    