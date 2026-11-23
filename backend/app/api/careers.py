from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_active_student
from app.models.models import CareerRole, CareerSkill, StudentProfile, CareerRecommendation
from app.schemas.schemas import CareerRoleOut, CareerRecommendationOut, CareerCompareRequest, CareerCompareItem
from app.services.recommendation_service import recommendation_service

router = APIRouter(prefix="/careers", tags=["Career Guidance"])

@router.get("", response_model=List[CareerRoleOut])
def list_careers(db: Session = Depends(get_db)):
    careers = db.query(CareerRole).all()
    res = []
    for c in careers:
        skills = [
            {
                "skill_name": cs.skill.name if cs.skill else "General",
                "required_level": cs.required_level,
                "is_mandatory": cs.is_mandatory,
                "importance_weight": cs.importance_weight
            } for cs in c.skills
        ]
        res.append({
            "id": c.id,
            "title": c.title,
            "slug": c.slug,
            "description": c.description,
            "industry": c.industry,
            "difficulty": c.difficulty,
            "entry_level_suitability": c.entry_level_suitability,
            "education_requirement": c.education_requirement,
            "average_salary": c.average_salary,
            "market_demand": c.market_demand,
            "soft_skills": c.soft_skills or [],
            "recommended_projects": c.recommended_projects or [],
            "recommended_certifications": c.recommended_certifications or [],
            "skills": skills
        })
    return res

@router.get("/recommendations", response_model=List[CareerRecommendationOut])
def get_student_recommendations(
    profile: StudentProfile = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    recs = recommendation_service.compute_student_recommendations(db, profile)
    out = []
    for r in recs:
        out.append({
            "career_id": r["career_id"],
            "career_title": r["career_title"],
            "slug": r["slug"],
            "industry": r["industry"],
            "match_score": r["match_score"],
            "rank": r["rank"],
            "reasons": r["reasons"],
            "missing_skills": r["missing_skills"],
            "recommended_actions": r["recommended_actions"],
            "component_scores": r["component_scores"]
        })
    return out

@router.post("/compare", response_model=List[CareerCompareItem])
def compare_careers(
    req: CareerCompareRequest,
    profile: StudentProfile = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    if not req.career_ids or len(req.career_ids) < 1:
        raise HTTPException(status_code=400, detail="Provide at least one career ID to evaluate.")
    return recommendation_service.compare_careers(db, profile, req.career_ids)

@router.get("/{id}")
def get_career_by_id(id: int, db: Session = Depends(get_db)):
    c = db.query(CareerRole).filter(CareerRole.id == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Career role not found")

    skills = [
        {
            "skill_name": cs.skill.name if cs.skill else "General",
            "required_level": cs.required_level,
            "is_mandatory": cs.is_mandatory,
            "importance_weight": cs.importance_weight
        } for cs in c.skills
    ]

    return {
        "id": c.id,
        "title": c.title,
        "slug": c.slug,
        "description": c.description,
        "industry": c.industry,
        "difficulty": c.difficulty,
        "entry_level_suitability": c.entry_level_suitability,
        "education_requirement": c.education_requirement,
        "average_salary": c.average_salary,
        "market_demand": c.market_demand,
        "soft_skills": c.soft_skills or [],
        "recommended_projects": c.recommended_projects or [],
        "recommended_certifications": c.recommended_certifications or [],
        "skills": skills
    }
