from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_active_counselor
from app.models.models import User, StudentProfile, CounselorNote, Notification

router = APIRouter(prefix="/counselor", tags=["Counselor Guidance Operations"])

@router.get("/students")
def get_assigned_students(
    counselor: User = Depends(get_current_active_counselor),
    db: Session = Depends(get_db)
):
    profiles = db.query(StudentProfile).all()
    res = []
    for p in profiles:
        u = p.user
        if not u: continue
        res.append({
            "id": p.id,
            "student_name": u.full_name,
            "email": u.email,
            "target_career": p.desired_job_role or "Data Scientist",
            "profile_completeness": p.profile_completeness,
            "points": p.points,
            "streak_days": p.streak_days,
            "notes_count": len(p.counselor_notes)
        })
    return res

@router.get("/students/{id}")
def get_student_counselor_detail(
    id: int,
    counselor: User = Depends(get_current_active_counselor),
    db: Session = Depends(get_db)
):
    p = db.query(StudentProfile).filter(StudentProfile.id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Student profile not found")

    notes = db.query(CounselorNote).filter(CounselorNote.profile_id == p.id).order_by(CounselorNote.created_at.desc()).all()
    acad = p.academic_record

    return {
        "id": p.id,
        "full_name": p.user.full_name if p.user else "Student",
        "email": p.user.email if p.user else "",
        "phone": p.phone,
        "desired_career": p.desired_job_role,
        "academic": {
            "college": acad.college if acad else "",
            "degree": acad.degree if acad else "",
            "branch": acad.branch if acad else "",
            "cgpa": acad.cgpa if acad else 0.0
        } if acad else None,
        "skills": [
            {
                "skill_name": ss.skill.name if ss.skill else "General",
                "proficiency_score": ss.proficiency_score,
                "proficiency_level": ss.proficiency_level
            } for ss in p.skills
        ],
        "recommendations": [
            {
                "career_title": r.career.title if r.career else "",
                "match_score": r.match_score,
                "reasons": r.reasons,
                "missing_skills": r.missing_skills
            } for r in p.recommendations
        ],
        "notes": [
            {
                "id": n.id,
                "counselor_name": n.counselor.full_name if n.counselor else "Counselor",
                "note_text": n.note_text,
                "guidance_actions": n.guidance_actions or [],
                "created_at": n.created_at
            } for n in notes
        ]
    }

@router.post("/students/{id}/notes")
def add_counselor_note(
    id: int,
    note_data: dict,
    counselor: User = Depends(get_current_active_counselor),
    db: Session = Depends(get_db)
):
    p = db.query(StudentProfile).filter(StudentProfile.id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Student profile not found")

    note_text = note_data.get("note_text")
    if not note_text:
        raise HTTPException(status_code=400, detail="Note text is required")

    actions = note_data.get("guidance_actions", [])
    note = CounselorNote(
        counselor_id=counselor.id,
        profile_id=p.id,
        note_text=note_text,
        guidance_actions=actions
    )
    db.add(note)

    # Notify student
    db.add(Notification(
        user_id=p.user_id,
        title="New Counselor Guidance",
        message=f"Counselor {counselor.full_name} added personalized guidance notes to your profile.",
        notification_type="info"
    ))

    db.commit()
    return {"message": "Counselor note and guidance plan recorded successfully."}
