import uuid
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_active_student, get_current_user
from app.models.models import StudentProfile, Credential, Achievement, StudentAchievement, User
from app.schemas.schemas import CredentialCreateRequest, CredentialOut, VerifyCredentialResponse
from app.blockchain.blockchain_ledger import blockchain_ledger

router = APIRouter(prefix="", tags=["Blockchain Credential Verification"])

@router.post("/credentials/create", response_model=CredentialOut)
def issue_certificate(
    req: CredentialCreateRequest,
    profile: StudentProfile = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    cred_id = f"CRED-2026-{uuid.uuid4().hex[:8].upper()}"

    # Add to cryptographic blockchain ledger
    chain_info = blockchain_ledger.add_credential(
        credential_id=cred_id,
        student_id=profile.id,
        title=req.title,
        credential_type=req.credential_type,
        metadata=req.metadata,
        issuer="0x71C...EDUGUIDE_ROOT_CA"
    )

    # Persist in DB
    db_cred = Credential(
        credential_id=cred_id,
        profile_id=profile.id,
        title=req.title,
        credential_type=req.credential_type,
        credential_hash=chain_info["credential_hash"],
        issuer_address=chain_info["issuer"],
        blockchain_tx_hash=chain_info["tx_hash"],
        block_number=chain_info["block_number"],
        verification_status="VERIFIED",
        metadata_json=req.metadata
    )
    db.add(db_cred)

    # Gamification
    ach = db.query(Achievement).filter(Achievement.code == "CREDENTIAL_HOLDER").first()
    if ach:
        has_it = db.query(StudentAchievement).filter(
            StudentAchievement.profile_id == profile.id,
            StudentAchievement.achievement_id == ach.id
        ).first()
        if not has_it:
            db.add(StudentAchievement(profile_id=profile.id, achievement_id=ach.id))
            profile.points += ach.points

    db.commit()
    db.refresh(db_cred)

    return db_cred

@router.get("/credentials", response_model=List[CredentialOut])
def list_student_credentials(
    profile: StudentProfile = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    return db.query(Credential).filter(Credential.profile_id == profile.id).order_by(Credential.issued_at.desc()).all()

@router.get("/credentials/{id}", response_model=CredentialOut)
def get_credential_by_id(
    id: int,
    profile: StudentProfile = Depends(get_current_active_student),
    db: Session = Depends(get_db)
):
    cred = db.query(Credential).filter(Credential.id == id, Credential.profile_id == profile.id).first()
    if not cred:
        raise HTTPException(status_code=404, detail="Credential not found")
    return cred

# Public-style verification endpoint (No auth required for third-party recruiters!)
@router.get("/blockchain/verify/{credential_id}", response_model=VerifyCredentialResponse)
def verify_credential_public(credential_id: str, db: Session = Depends(get_db)):
    db_cred = db.query(Credential).filter(Credential.credential_id == credential_id).first()
    
    # Check ledger
    verification = blockchain_ledger.verify_credential(
        credential_id=credential_id,
        expected_hash=db_cred.credential_hash if db_cred else None
    )

    if not verification["is_valid"]:
        return {
            "is_valid": False,
            "verification_status": "TAMPERED / INVALID" if verification.get("tamper_detected") else "NOT_FOUND",
            "credential_id": credential_id,
            "title": db_cred.title if db_cred else None,
            "student_name": db_cred.profile.user.full_name if db_cred and db_cred.profile and db_cred.profile.user else None,
            "credential_hash": db_cred.credential_hash if db_cred else "N/A",
            "blockchain_tx_hash": db_cred.blockchain_tx_hash if db_cred else "N/A",
            "block_number": db_cred.block_number if db_cred else 0,
            "timestamp": db_cred.issued_at if db_cred else None,
            "tamper_detected": verification.get("tamper_detected", False),
            "details": verification.get("details", "Verification check failed.")
        }

    return {
        "is_valid": True,
        "verification_status": "VERIFIED",
        "credential_id": credential_id,
        "title": db_cred.title if db_cred else verification.get("title"),
        "student_name": db_cred.profile.user.full_name if db_cred and db_cred.profile and db_cred.profile.user else "Verified Scholar",
        "credential_hash": verification["credential_hash"],
        "blockchain_tx_hash": verification["tx_hash"],
        "block_number": verification["block_number"],
        "timestamp": db_cred.issued_at if db_cred else None,
        "tamper_detected": False,
        "details": "Credential signature cryptographically validated against immutable ledger root."
    }

@router.get("/blockchain/ledger")
def inspect_blockchain_ledger():
    """Returns the immutable blocks and hash audit trail for admin transparency."""
    return {
        "total_blocks": len(blockchain_ledger.chain),
        "difficulty": blockchain_ledger.difficulty,
        "chain": [b.to_dict() for b in blockchain_ledger.chain]
    }
