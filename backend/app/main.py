import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.db.seed import seed_database
from app.ml.train_pipeline import train_and_evaluate_model
from app.ml.inference import inference_engine

# Import Routers
from app.api.auth import router as auth_router
from app.api.students import router as students_router
from app.api.assessments import router as assessments_router
from app.api.careers import router as careers_router
from app.api.roadmap import router as roadmap_router
from app.api.resume import router as resume_router
from app.api.blockchain import router as blockchain_router
from app.api.ai_chat import router as ai_chat_router
from app.api.reports import router as reports_router
from app.api.admin import router as admin_router
from app.api.counselor import router as counselor_router
from app.api.notifications import router as notifications_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure DB tables exist and seed default accounts & dataset
    Base.metadata.create_all(bind=engine)
    seed_database()

    # Ensure ML model is trained and cached
    if not os.path.exists(settings.ML_MODEL_PATH):
        print("Training AI/ML career classification model...")
        train_and_evaluate_model(settings.ML_MODEL_PATH)
        inference_engine.load_model()
    else:
        print("Pre-trained AI/ML model loaded.")

    yield
    # Shutdown logic if any

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Production-grade AI-Based Skill Assessment and Career Guidance System aligned with UN SDG 4.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Cybersecurity & CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

# Mount static uploads
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include Routers with /api prefix
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(students_router, prefix=settings.API_V1_STR)
app.include_router(assessments_router, prefix=settings.API_V1_STR)
app.include_router(careers_router, prefix=settings.API_V1_STR)
app.include_router(roadmap_router, prefix=settings.API_V1_STR)
app.include_router(resume_router, prefix=settings.API_V1_STR)
app.include_router(blockchain_router, prefix=settings.API_V1_STR)
app.include_router(ai_chat_router, prefix=settings.API_V1_STR)
app.include_router(reports_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)
app.include_router(counselor_router, prefix=settings.API_V1_STR)
app.include_router(notifications_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "system": settings.PROJECT_NAME,
        "status": "ONLINE",
        "sdg_alignment": "SDG 4 - Quality Education",
        "documentation": "/docs",
        "api_v1": settings.API_V1_STR
    }
