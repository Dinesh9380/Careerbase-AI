from typing import Optional, Dict, Any
from fastapi import Request
from sqlalchemy.orm import Session
from app.models.models import AuditLog

def log_audit_event(
    db: Session,
    action: str,
    user_id: Optional[int] = None,
    status: str = "SUCCESS",
    ip_address: str = "127.0.0.1",
    details: Optional[Dict[str, Any]] = None
) -> AuditLog:
    """Records an immutable audit event in the database."""
    log_entry = AuditLog(
        user_id=user_id,
        action=action,
        status=status,
        ip_address=ip_address,
        details=details or {}
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry
