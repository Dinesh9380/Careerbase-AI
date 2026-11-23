from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_active_student
from app.models.models import (
    StudentProfile, AcademicRecord, Skill, StudentSkill, StudentSoftSkill,
    StudentInterest, StudentProject, StudentCertification, CareerRecommendation,
    AssessmentAttempt, SkillGap, StudentAchievement
)
from app.schemas.schemas import ProfileUpdate
from app.services.recommendation_service import recommendation_service

router = APIRouter(prefix="/students", tags=["Student Management"])

@router.get("/me")
def get_student_profile(
    profile: StudentProfile = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    acad = profile.academic_record
    return {
        "user_id": profile.user_id,
        "full_name": profile.user.full_name,
        "email": profile.user.email,
        "phone": profile.phone,
        "date_of_birth": profile.date_of_birth,
        "location": profile.location,
        "desired_job_role": profile.desired_job_role,
        "preferred_industry": profile.preferred_industry,
        "preferred_location": profile.preferred_location,
        "higher_studies_preference": profile.higher_studies_preference,
        "job_preference": profile.job_preference,
        "profile_completeness": profile.profile_completeness,
        "points": profile.points,
        "streak_days": profile.streak_days,
        "academic": {
            "college": acad.college if acad else None,
            "degree": acad.degree if acad else None,
            "branch": acad.branch if acad else None,
            "year_of_study": acad.year_of_study if acad else None,
            "cgpa": acad.cgpa if acad else None,
            "graduation_year": acad.graduation_year if acad else None,
            "academic_subjects": acad.academic_subjects if acad else []
        } if acad else None,
        "skills": [
            {
                "id": ss.id,
                "skill_name": ss.skill.name if ss.skill else "General",
                "category": ss.skill.category if ss.skill else "General",
                "proficiency_score": ss.proficiency_score,
                "proficiency_level": ss.proficiency_level,
                "last_assessed": ss.last_assessed
            } for ss in profile.skills
        ],
        "soft_skills": [{"name": s.skill_name, "rating": s.rating} for s in profile.soft_skills],
        "interests": [{"name": i.interest_name, "preference_level": i.preference_level} for i in profile.interests],
        "projects": [
            {
                "id": p.id,
                "title": p.title,
                "description": p.description,
                "technologies": p.technologies,
                "role": p.role,
                "duration": p.duration,
                "project_url": p.project_url
            } for p in profile.projects
        ],
        "certifications": [
            {
                "id": c.id,
                "name": c.name,
                "issuer": c.issuer,
                "issue_date": c.issue_date,
                "credential_id": c.credential_id
            } for c in profile.certifications
        ]
    }

@router.put("/me")
def update_student_profile(
    update_data: ProfileUpdate,
    profile: StudentProfile = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    if update_data.phone is not None: profile.phone = update_data.phone
    if update_data.date_of_birth is not None: profile.date_of_birth = update_data.date_of_birth
    if update_data.location is not None: profile.location = update_data.location
    if update_data.desired_job_role is not None: profile.desired_job_role = update_data.desired_job_role
    if update_data.preferred_industry is not None: profile.preferred_industry = update_data.preferred_industry
    if update_data.preferred_location is not None: profile.preferred_location = update_data.preferred_location
    if update_data.higher_studies_preference is not None: profile.higher_studies_preference = update_data.higher_studies_preference
    if update_data.job_preference is not None: profile.job_preference = update_data.job_preference

    # Academic
    if update_data.academic:
        acad = profile.academic_record
        if not acad:
            acad = AcademicRecord(profile_id=profile.id)
            db.add(acad)
        acad.college = update_data.academic.college
        acad.degree = update_data.academic.degree
        acad.branch = update_data.academic.branch
        acad.year_of_study = update_data.academic.year_of_study
        acad.cgpa = update_data.academic.cgpa
        acad.graduation_year = update_data.academic.graduation_year
        acad.academic_subjects = update_data.academic.academic_subjects

    # Skills
    if update_data.skills:
        for s_in in update_data.skills:
            skill_obj = db.query(Skill).filter(Skill.name.ilike(s_in.skill_name.strip())).first()
            if not skill_obj:
                skill_obj = Skill(name=s_in.skill_name.strip().title(), category="Technical")
                db.add(skill_obj)
                db.commit()
                db.refresh(skill_obj)

            existing_ss = db.query(StudentSkill).filter(
                StudentSkill.profile_id == profile.id,
                StudentSkill.skill_id == skill_obj.id
            ).first()

            if existing_ss:
                existing_ss.proficiency_score = s_in.proficiency_score
                existing_ss.proficiency_level = s_in.proficiency_level or "Intermediate"
            else:
                db.add(StudentSkill(
                    profile_id=profile.id,
                    skill_id=skill_obj.id,
                    proficiency_score=s_in.proficiency_score,
                    proficiency_level=s_in.proficiency_level or "Intermediate"
                ))

    # Calculate profile completeness
    completeness = 30.0
    if profile.academic_record and profile.academic_record.cgpa: completeness += 20.0
    if len(profile.skills) >= 4: completeness += 25.0
    if len(profile.projects) >= 1: completeness += 15.0
    if len(profile.certifications) >= 1: completeness += 10.0
    profile.profile_completeness = min(100.0, completeness)

    db.commit()
    db.refresh(profile)

    # Re-compute recommendations in background
    recommendation_service.compute_student_recommendations(db, profile)

    return {"message": "Profile updated successfully", "profile_completeness": profile.profile_completeness}

@router.get("/me/dashboard")
def get_student_dashboard(
    profile: StudentProfile = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    # Overall skill score
    skill_scores = [s.proficiency_score for s in profile.skills]
    avg_skill = round(sum(skill_scores) / max(len(skill_scores), 1), 1) if skill_scores else 50.0

    # Assessment stats
    attempts = db.query(AssessmentAttempt).filter(
        AssessmentAttempt.profile_id == profile.id,
        AssessmentAttempt.status == "completed"
    ).order_by(AssessmentAttempt.completed_at.desc()).all()
    avg_assessment = round(sum(a.percentage for a in attempts) / max(len(attempts), 1), 1) if attempts else 75.0

    # Ensure recommendations are computed
    recs = db.query(CareerRecommendation).filter(CareerRecommendation.profile_id == profile.id).order_by(CareerRecommendation.rank.asc()).limit(4).all()
    if not recs:
        recommendation_service.compute_student_recommendations(db, profile)
        recs = db.query(CareerRecommendation).filter(CareerRecommendation.profile_id == profile.id).order_by(CareerRecommendation.rank.asc()).limit(4).all()

    top_match = recs[0].match_score if recs else 78.0

    # Learning roadmap progress
    roadmap_progress = 42.0
    if profile.roadmaps:
        roadmap_progress = profile.roadmaps[0].progress_percentage

    # Radar chart skills formatting (Top 6-8 skills)
    radar_data = [
        {"subject": ss.skill.name if ss.skill else "General", "A": ss.proficiency_score, "fullMark": 100}
        for ss in profile.skills[:7]
    ]

    # Achievements
    achievements = [
        {
            "id": sa.achievement.id,
            "title": sa.achievement.title,
            "description": sa.achievement.description,
            "badge_icon": sa.achievement.badge_icon,
            "unlocked_at": sa.unlocked_at
        } for sa in profile.achievements if sa.achievement
    ]

    # Critical gaps
    gaps = db.query(SkillGap).filter(SkillGap.profile_id == profile.id).limit(5).all()

    return {
        "student_name": profile.user.full_name,
        "desired_career": profile.desired_job_role or (recs[0].career.title if recs else "Data Scientist"),
        "metrics": {
            "overall_skill_score": avg_skill,
            "assessment_score": avg_assessment,
            "career_readiness": top_match,
            "learning_progress": roadmap_progress,
            "points": profile.points,
            "streak_days": profile.streak_days,
            "profile_completeness": profile.profile_completeness
        },
        "radar_skills": radar_data,
        "top_recommendations": [
            {
                "career_id": r.career_id,
                "title": r.career.title if r.career else "Role",
                "match_score": r.match_score,
                "industry": r.career.industry if r.career else "Technology",
                "rank": r.rank,
                "reasons": r.reasons[:2] if r.reasons else [],
                "missing_skills": r.missing_skills[:2] if r.missing_skills else []
            } for r in recs
        ],
        "critical_gaps": [
            {
                "skill_name": g.skill_name,
                "current_score": g.current_score,
                "required_score": g.required_score,
                "severity": g.gap_severity
            } for g in gaps
        ],
        "recent_assessments": [
            {
                "id": a.id,
                "title": a.assessment.title if a.assessment else "Assessment",
                "score_pct": a.percentage,
                "accuracy": a.accuracy,
                "completed_at": a.completed_at
            } for a in attempts[:4]
        ],
        "achievements": achievements
    }

@router.get("/me/skills")
def get_student_skills(profile: StudentProfile = Depends(get_current_active_student)):
    return [
        {
            "id": ss.id,
            "skill_name": ss.skill.name if ss.skill else "General",
            "category": ss.skill.category if ss.skill else "General",
            "proficiency_score": ss.proficiency_score,
            "proficiency_level": ss.proficiency_level,
            "evidence_source": ss.evidence_source,
            "last_assessed": ss.last_assessed
        } for ss in profile.skills
    ]

@router.get("/me/skill-gaps")
def get_student_skill_gaps(
    profile: StudentProfile = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    gaps = db.query(SkillGap).filter(SkillGap.profile_id == profile.id).all()
    return [
        {
            "id": g.id,
            "skill_name": g.skill_name,
            "career_id": g.career_id,
            "current_score": g.current_score,
            "required_score": g.required_score,
            "gap_severity": g.gap_severity,
            "gap_difference": round(g.required_score - g.current_score, 1)
        } for g in gaps
    ]
