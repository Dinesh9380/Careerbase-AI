from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# ================= AUTH =================
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str
    role: str = "student" # student, admin, counselor

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None
    type: Optional[str] = None

class UserOut(BaseModel):
    id: int
    uuid: str
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ================= STUDENT & PROFILE =================
class AcademicRecordIn(BaseModel):
    college: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    year_of_study: Optional[str] = None
    cgpa: Optional[float] = None
    graduation_year: Optional[int] = None
    academic_subjects: List[str] = []

class SkillIn(BaseModel):
    skill_name: str
    proficiency_score: float = 50.0 # 0-100
    proficiency_level: Optional[str] = "Intermediate"

class SoftSkillIn(BaseModel):
    skill_name: str
    rating: int = 3 # 1-5

class InterestIn(BaseModel):
    interest_name: str
    preference_level: int = 5

class ProjectIn(BaseModel):
    title: str
    description: Optional[str] = None
    technologies: List[str] = []
    role: Optional[str] = None
    duration: Optional[str] = None
    project_url: Optional[str] = None

class CertificationIn(BaseModel):
    name: str
    issuer: str
    issue_date: Optional[str] = None
    credential_id: Optional[str] = None

class ProfileUpdate(BaseModel):
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    location: Optional[str] = None
    desired_job_role: Optional[str] = None
    preferred_industry: Optional[str] = None
    preferred_location: Optional[str] = None
    higher_studies_preference: Optional[str] = None
    job_preference: Optional[str] = None
    academic: Optional[AcademicRecordIn] = None
    skills: Optional[List[SkillIn]] = None
    soft_skills: Optional[List[SoftSkillIn]] = None
    interests: Optional[List[InterestIn]] = None
    projects: Optional[List[ProjectIn]] = None
    certifications: Optional[List[CertificationIn]] = None

# ================= ASSESSMENTS =================
class QuestionOptionOut(BaseModel):
    id: int
    option_text: str
    # Note: is_correct is NOT returned during taking assessment!

class QuestionOut(BaseModel):
    id: int
    question_text: str
    question_type: str
    difficulty: str
    marks: int
    code_snippet: Optional[str] = None
    options: List[QuestionOptionOut]

class AssessmentListOut(BaseModel):
    id: int
    title: str
    category: str
    description: Optional[str]
    time_limit_minutes: int
    total_questions: int
    passing_percentage: float
    role_slug: Optional[str] = None

class AssessmentStartOut(BaseModel):
    attempt_id: int
    assessment_id: int
    title: str
    category: str
    time_limit_minutes: int
    questions: List[QuestionOut]
    started_at: datetime

class SubmitAnswerItem(BaseModel):
    question_id: int
    selected_options: List[int] # option IDs

class AssessmentSubmitRequest(BaseModel):
    time_spent_seconds: int
    answers: List[SubmitAnswerItem]

class AssessmentResultOut(BaseModel):
    attempt_id: int
    score: float
    total_marks: float
    percentage: float
    accuracy: float
    passed: bool
    status: str
    skill_scores: Dict[str, float]
    difficulty_performance: Dict[str, Any]
    new_achievements: List[str] = []

# ================= CAREERS & RECOMMENDATIONS =================
class CareerSkillOut(BaseModel):
    skill_name: str
    required_level: float
    is_mandatory: bool
    importance_weight: float

class CareerRoleOut(BaseModel):
    id: int
    title: str
    slug: str
    description: str
    industry: str
    difficulty: str
    entry_level_suitability: bool
    education_requirement: str
    average_salary: str
    market_demand: str
    soft_skills: List[str]
    recommended_projects: List[str]
    recommended_certifications: List[str]
    skills: List[CareerSkillOut] = []

class CareerRecommendationOut(BaseModel):
    career_id: int
    career_title: str
    slug: str
    industry: str
    match_score: float # 0 to 100
    rank: int
    reasons: List[str] # Why recommended
    missing_skills: List[Dict[str, Any]]
    recommended_actions: List[str]
    component_scores: Dict[str, float]

class CareerCompareRequest(BaseModel):
    career_ids: List[int]

class CareerCompareItem(BaseModel):
    career_id: int
    title: str
    match_score: float
    readiness_level: str
    required_skills: List[Dict[str, Any]]
    missing_skills: List[Dict[str, Any]]
    learning_time_weeks: int
    difficulty: str
    average_salary: str

# ================= ROADMAP =================
class RoadmapItemOut(BaseModel):
    id: int
    skill_name: str
    stage: str
    title: str
    description: Optional[str]
    estimated_hours: int
    resource_link: Optional[str]
    project_prompt: Optional[str]
    is_completed: bool
    completed_at: Optional[datetime]

class LearningRoadmapOut(BaseModel):
    id: int
    career_title: str
    career_id: int
    total_items: int
    completed_items: int
    progress_percentage: float
    items: List[RoadmapItemOut]

# ================= RESUME & VISION =================
class ExtractedSkillItem(BaseModel):
    skill_name: str
    category: str
    in_profile: bool

class ResumeAnalysisOut(BaseModel):
    resume_id: int
    filename: str
    completeness_score: float
    extracted_name: Optional[str]
    extracted_email: Optional[str]
    extracted_phone: Optional[str]
    extracted_education: List[str]
    extracted_skills: List[ExtractedSkillItem]
    missing_recommended_skills: List[str]
    extracted_projects: List[str]
    extracted_certifications: List[str]
    extracted_experience: List[str]
    ats_keyword_coverage: float
    suggested_improvements: List[str]

class AcceptExtractedSkillsRequest(BaseModel):
    skills: List[str]

# ================= BLOCKCHAIN =================
class CredentialCreateRequest(BaseModel):
    title: str
    credential_type: str
    metadata: Dict[str, Any] = {}

class CredentialOut(BaseModel):
    id: int
    credential_id: str
    title: str
    credential_type: str
    credential_hash: str
    issuer_address: str
    blockchain_tx_hash: str
    block_number: int
    verification_status: str
    issued_at: datetime
    metadata_json: Dict[str, Any]

class VerifyCredentialResponse(BaseModel):
    is_valid: bool
    verification_status: str
    credential_id: str
    title: Optional[str]
    student_name: Optional[str]
    credential_hash: str
    blockchain_tx_hash: str
    block_number: int
    timestamp: Optional[datetime]
    tamper_detected: bool
    details: str

# ================= AI ASSISTANT =================
class AIChatRequest(BaseModel):
    message: str

class AIChatResponse(BaseModel):
    reply: str
    sources_used: List[str] = []
    suggested_followups: List[str] = []

# ================= BIG DATA & ADMIN =================
class BigDataGenRequest(BaseModel):
    record_count: int = 10000 # 1000, 10000, 50000, 100000

class BigDataGenResponse(BaseModel):
    records_processed: int
    execution_time_seconds: float
    records_per_second: int = 0
    engine_used: str # PySpark or Pandas Optimized Engine
    skill_popularity: List[Dict[str, Any]]
    career_interest_trends: List[Dict[str, Any]]
    common_skill_gaps: List[Dict[str, Any]]
    department_performance: List[Dict[str, Any]]
