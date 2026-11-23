from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_active_student
from app.models.models import StudentProfile
from app.services.pdf_service import pdf_service

router = APIRouter(prefix="/reports", tags=["Career Report Generation"])

@router.get("/download-pdf")
def download_career_report_pdf(
    profile: StudentProfile = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    try:
        pdf_bytes = pdf_service.generate_career_report(db, profile)
        filename = f"Career_Intelligence_Report_{profile.user.full_name.replace(' ', '_')}.pdf"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate career report: {str(e)}")
