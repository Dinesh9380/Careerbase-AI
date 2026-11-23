from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_active_student
from app.models.models import StudentProfile, LearningResource
from app.schemas.schemas import LearningRoadmapOut
from app.services.roadmap_service import roadmap_service

router = APIRouter(prefix="/roadmap", tags=["Learning Roadmap"])

@router.get("", response_model=LearningRoadmapOut)
def get_roadmap(
    career_id: Optional[int] = Query(None),
    profile: StudentProfile = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    try:
        return roadmap_service.generate_or_get_roadmap(db, profile, career_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/items/{id}/complete")
def toggle_item_completion(
    id: int,
    profile: StudentProfile = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    try:
        return roadmap_service.complete_roadmap_item(db, id, profile)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/resources")
def list_learning_resources(
    skill: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(LearningResource)
    if skill:
        query = query.filter(LearningResource.skill_name.ilike(f"%{skill}%"))
    if difficulty:
        query = query.filter(LearningResource.difficulty.ilike(difficulty))
    resources = query.all()
    return [
        {
            "id": r.id,
            "skill_name": r.skill_name,
            "title": r.title,
            "resource_type": r.resource_type,
            "provider": r.provider,
            "url": r.url,
            "estimated_hours": r.estimated_hours,
            "rating": r.rating,
            "description": r.description,
            "difficulty": r.difficulty
        } for r in resources
    ]
