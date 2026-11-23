from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_active_student
from app.models.models import StudentProfile
from app.schemas.schemas import AIChatRequest, AIChatResponse
from app.services.ai_service import career_ai_service

router = APIRouter(prefix="/ai", tags=["CareerAI Chat Assistant"])

@router.post("/chat", response_model=AIChatResponse)
def chat_with_career_ai(
    req: AIChatRequest,
    profile: StudentProfile = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")
    return career_ai_service.generate_chat_response(db, profile, req.message)
