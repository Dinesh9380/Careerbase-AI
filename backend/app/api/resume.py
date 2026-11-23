import os
import shutil
import uuid
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.core.deps import get_current_active_student
from app.models.models import StudentProfile, Resume, ResumeExtractedData, Skill, StudentSkill
from app.schemas.schemas import ResumeAnalysisOut, AcceptExtractedSkillsRequest
from app.vision.resume_intelligence import resume_engine

router = APIRouter(prefix="/resume", tags=["Resume & Document Vision Intelligence"])

@router.post("/upload", response_model=ResumeAnalysisOut)
async def upload_and_analyze_resume(
    file: UploadFile = File(...),
    profile: StudentProfile = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    # Validate extension
    ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '.{ext}'. Supported formats: PDF, JPG, JPEG, PNG."
        )

    # Save file safely
    safe_filename = f"{uuid.uuid4()}_{file.filename.replace(' ', '_')}"
    file_path = os.path.join(settings.UPLOAD_DIR, safe_filename)

    with open(file_path, "wb") as buffer:
        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File exceeds maximum size limit of 10MB.")
        buffer.write(content)

    # 1. OCR / Document Extraction
    extracted_text = resume_engine.extract_text(file_path, ext)
    existing_skills = [ss.skill.name for ss in profile.skills if ss.skill]
    analysis = resume_engine.parse_resume_content(extracted_text, existing_skills)

    # 2. Persist in Database
    resume_record = Resume(
        profile_id=profile.id,
        filename=file.filename,
        file_path=file_path,
        file_type=ext,
        file_size=len(content)
    )
    db.add(resume_record)
    db.commit()
    db.refresh(resume_record)

    extracted_record = ResumeExtractedData(
        resume_id=resume_record.id,
        extracted_name=analysis["extracted_name"],
        extracted_email=analysis["extracted_email"],
        extracted_phone=analysis["extracted_phone"],
        extracted_education=analysis["extracted_education"],
        extracted_skills=analysis["extracted_skills"],
        extracted_projects=analysis["extracted_projects"],
        extracted_certifications=analysis["extracted_certifications"],
        extracted_experience=analysis["extracted_experience"],
        completeness_score=analysis["completeness_score"],
        ats_keyword_match={"coverage": analysis["ats_keyword_coverage"]},
        raw_text=extracted_text[:4000]
    )
    db.add(extracted_record)
    db.commit()

    return {
        "resume_id": resume_record.id,
        "filename": file.filename,
        "completeness_score": analysis["completeness_score"],
        "extracted_name": analysis["extracted_name"],
        "extracted_email": analysis["extracted_email"],
        "extracted_phone": analysis["extracted_phone"],
        "extracted_education": analysis["extracted_education"],
        "extracted_skills": analysis["extracted_skills"],
        "missing_recommended_skills": ["Cloud Architecture", "Docker", "REST API Design"],
        "extracted_projects": analysis["extracted_projects"],
        "extracted_certifications": analysis["extracted_certifications"],
        "extracted_experience": analysis["extracted_experience"],
        "ats_keyword_coverage": analysis["ats_keyword_coverage"],
        "suggested_improvements": analysis["suggested_improvements"]
    }

@router.get("/latest", response_model=ResumeAnalysisOut)
def get_latest_resume_analysis(
    profile: StudentProfile = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    res = db.query(Resume).filter(Resume.profile_id == profile.id).order_by(Resume.id.desc()).first()
    if not res or not res.extracted_data:
        raise HTTPException(status_code=404, detail="No resume uploaded yet.")

    data = res.extracted_data
    return {
        "resume_id": res.id,
        "filename": res.filename,
        "completeness_score": data.completeness_score,
        "extracted_name": data.extracted_name,
        "extracted_email": data.extracted_email,
        "extracted_phone": data.extracted_phone,
        "extracted_education": data.extracted_education or [],
        "extracted_skills": data.extracted_skills or [],
        "missing_recommended_skills": ["Cloud Architecture", "Docker", "REST API Design"],
        "extracted_projects": data.extracted_projects or [],
        "extracted_certifications": data.extracted_certifications or [],
        "extracted_experience": data.extracted_experience or [],
        "ats_keyword_coverage": data.ats_keyword_match.get("coverage", 75.0) if data.ats_keyword_match else 75.0,
        "suggested_improvements": [
            "Quantify project achievements with measurable metrics (e.g. 'Improved performance by 35%')",
            "Ensure technical skills align with target career keywords"
        ]
    }

@router.post("/accept-skills")
def accept_extracted_skills(
    req: AcceptExtractedSkillsRequest,
    profile: StudentProfile = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    added_count = 0
    for s_name in req.skills:
        skill_obj = db.query(Skill).filter(Skill.name.ilike(s_name.strip())).first()
        if not skill_obj:
            skill_obj = Skill(name=s_name.strip().title(), category="Technical")
            db.add(skill_obj)
            db.commit()
            db.refresh(skill_obj)

        existing_ss = db.query(StudentSkill).filter(
            StudentSkill.profile_id == profile.id,
            StudentSkill.skill_id == skill_obj.id
        ).first()

        if not existing_ss:
            db.add(StudentSkill(
                profile_id=profile.id,
                skill_id=skill_obj.id,
                proficiency_score=60.0,
                proficiency_level="Intermediate",
                evidence_source={"source": "resume_ocr_extraction"}
            ))
            added_count += 1

    db.commit()
    return {"message": f"Successfully imported {added_count} skills into your active student profile."}
