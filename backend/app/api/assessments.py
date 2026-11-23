from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_active_student
from app.models.models import Assessment, AssessmentAttempt, StudentProfile
from app.schemas.schemas import AssessmentListOut, AssessmentStartOut, AssessmentSubmitRequest, AssessmentResultOut
from app.services.assessment_service import assessment_service
from app.services.recommendation_service import recommendation_service

router = APIRouter(prefix="/assessments", tags=["Skill Assessments"])

@router.get("", response_model=List[AssessmentListOut])
def list_assessments(db: Session = Depends(get_db)):
    assessments = db.query(Assessment).filter(Assessment.is_active == True).all()
    return assessments

@router.get("/{id}")
def get_assessment_details(id: int, db: Session = Depends(get_db)):
    ass = db.query(Assessment).filter(Assessment.id == id).first()
    if not ass:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return {
        "id": ass.id,
        "title": ass.title,
        "category": ass.category,
        "description": ass.description,
        "time_limit_minutes": ass.time_limit_minutes,
        "total_questions": len(ass.questions),
        "passing_percentage": ass.passing_percentage
    }

@router.post("/{id}/start")
def start_assessment(
    id: int,
    profile: StudentProfile = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    try:
        data = assessment_service.start_assessment(db, id, profile)
        return data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{attempt_id}/submit", response_model=AssessmentResultOut)
def submit_assessment(
    attempt_id: int,
    req: AssessmentSubmitRequest,
    profile: StudentProfile = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    try:
        answers_dict = [{"question_id": a.question_id, "selected_options": a.selected_options} for a in req.answers]
        result = assessment_service.submit_assessment(
            db=db,
            attempt_id=attempt_id,
            answers=answers_dict,
            time_spent_seconds=req.time_spent_seconds,
            profile=profile
        )
        # Recalculate recommendations after new test submission
        recommendation_service.compute_student_recommendations(db, profile)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/history/my-attempts")
def get_assessment_history(
    profile: StudentProfile = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    attempts = db.query(AssessmentAttempt).filter(
        AssessmentAttempt.profile_id == profile.id
    ).order_by(AssessmentAttempt.completed_at.desc()).all()

    return [
        {
            "id": a.id,
            "assessment_id": a.assessment_id,
            "title": a.assessment.title if a.assessment else "Assessment",
            "category": a.assessment.category if a.assessment else "General",
            "score": a.score,
            "total_marks": a.total_marks,
            "percentage": a.percentage,
            "accuracy": a.accuracy,
            "status": a.status,
            "time_spent_seconds": a.time_spent_seconds,
            "completed_at": a.completed_at,
            "skill_scores": a.skill_scores or {}
        } for a in attempts
    ]
