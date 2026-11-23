from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_token
from app.core.audit import log_audit_event
from app.core.deps import get_current_user
from app.models.models import User, StudentProfile
from app.schemas.schemas import UserRegister, UserLogin, Token, UserOut

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
def register(user_in: UserRegister, request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host if request.client else "127.0.0.1"
    existing = db.query(User).filter(User.email == user_in.email.lower().strip()).first()
    if existing:
        log_audit_event(db, "REGISTRATION_FAILED", None, "FAILED", client_ip, {"email": user_in.email, "reason": "Email already registered"})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists."
        )

    user = User(
        email=user_in.email.lower().strip(),
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        role=user_in.role if user_in.role in ["student", "counselor", "admin"] else "student",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    if user.role == "student":
        profile = StudentProfile(user_id=user.id, profile_completeness=20.0)
        db.add(profile)
        db.commit()

    access_token = create_access_token(user.id, user.role)
    refresh_token = create_refresh_token(user.id, user.role)

    log_audit_event(db, "USER_REGISTER", user.id, "SUCCESS", client_ip, {"role": user.role})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role
        }
    }

@router.post("/login", response_model=Token)
def login(login_data: UserLogin, request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host if request.client else "127.0.0.1"
    user = db.query(User).filter(User.email == login_data.email.lower().strip()).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        log_audit_event(db, "LOGIN_FAILED", None, "FAILED", client_ip, {"email": login_data.email})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password."
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account is deactivated.")

    access_token = create_access_token(user.id, user.role)
    refresh_token = create_refresh_token(user.id, user.role)

    log_audit_event(db, "USER_LOGIN", user.id, "SUCCESS", client_ip, {"role": user.role})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role
        }
    }

@router.post("/refresh")
def refresh_token(token_data: dict, db: Session = Depends(get_db)):
    refresh_tok = token_data.get("refresh_token")
    if not refresh_tok:
        raise HTTPException(status_code=400, detail="Missing refresh token")
    payload = decode_token(refresh_tok)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")

    new_access_token = create_access_token(user.id, user.role)
    return {"access_token": new_access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user
