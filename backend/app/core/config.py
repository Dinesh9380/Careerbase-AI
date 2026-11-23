import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Based Skill Assessment and Career Guidance System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Environment & Security
    SECRET_KEY: str = os.getenv("JWT_SECRET", "super-secret-production-grade-key-change-in-prod-123456789")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./career_platform.db")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://localhost:8000",
        "*"
    ]
    
    # Uploads
    UPLOAD_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "uploads")
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: List[str] = ["pdf", "jpg", "jpeg", "png"]
    
    # AI / LLM
    AI_API_KEY: str = os.getenv("AI_API_KEY", "")
    
    # Blockchain
    BLOCKCHAIN_RPC_URL: str = os.getenv("BLOCKCHAIN_RPC_URL", "http://127.0.0.1:8545")
    BLOCKCHAIN_CONTRACT_ADDRESS: str = os.getenv("BLOCKCHAIN_CONTRACT_ADDRESS", "")
    BLOCKCHAIN_LEDGER_PATH: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "blockchain_ledger.json")
    
    # ML Models path
    ML_MODEL_PATH: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ml", "models", "career_classifier.joblib")

    class Config:
        case_sensitive = True

settings = Settings()
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.dirname(settings.ML_MODEL_PATH), exist_ok=True)
