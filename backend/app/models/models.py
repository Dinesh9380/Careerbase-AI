from datetime import datetime, timezone
import uuid
from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from app.core.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

# ================= USER & AUTH =================
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), default=generate_uuid, unique=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), default="student", index=True) # student, admin, counselor
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    profile = relationship("StudentProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")

# ================= STUDENT PROFILE =================
class StudentProfile(Base):
    __tablename__ = "student_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    phone = Column(String(50), nullable=True)
    date_of_birth = Column(String(50), nullable=True)
    location = Column(String(255), nullable=True)
    desired_job_role = Column(String(255), nullable=True)
    preferred_industry = Column(String(255), nullable=True)
    preferred_location = Column(String(255), nullable=True)
    higher_studies_preference = Column(String(100), nullable=True)
    job_preference = Column(String(100), nullable=True)
    profile_completeness = Column(Float, default=0.0)
    points = Column(Integer, default=50)
    streak_days = Column(Integer, default=1)
    
    user = relationship("User", back_populates="profile")
    academic_record = relationship("AcademicRecord", back_populates="profile", uselist=False, cascade="all, delete-orphan")
    skills = relationship("StudentSkill", back_populates="profile", cascade="all, delete-orphan")
    soft_skills = relationship("StudentSoftSkill", back_populates="profile", cascade="all, delete-orphan")
    interests = relationship("StudentInterest", back_populates="profile", cascade="all, delete-orphan")
    projects = relationship("StudentProject", back_populates="profile", cascade="all, delete-orphan")
    certifications = relationship("StudentCertification", back_populates="profile", cascade="all, delete-orphan")
    resumes = relationship("Resume", back_populates="profile", cascade="all, delete-orphan")
    attempts = relationship("AssessmentAttempt", back_populates="profile", cascade="all, delete-orphan")
    recommendations = relationship("CareerRecommendation", back_populates="profile", cascade="all, delete-orphan")
    roadmaps = relationship("LearningRoadmap", back_populates="profile", cascade="all, delete-orphan")
    credentials = relationship("Credential", back_populates="profile", cascade="all, delete-orphan")
    achievements = relationship("StudentAchievement", back_populates="profile", cascade="all, delete-orphan")
    counselor_notes = relationship("CounselorNote", back_populates="profile", cascade="all, delete-orphan")

class AcademicRecord(Base):
    __tablename__ = "academic_records"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    college = Column(String(255), nullable=True)
    degree = Column(String(255), nullable=True)
    branch = Column(String(255), nullable=True)
    year_of_study = Column(String(50), nullable=True)
    cgpa = Column(Float, nullable=True)
    graduation_year = Column(Integer, nullable=True)
    academic_subjects = Column(JSON, default=list)
    
    profile = relationship("StudentProfile", back_populates="academic_record")

# ================= SKILLS =================
class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    category = Column(String(100), index=True, nullable=False) # Programming, Data Science, Web, Cloud, AI/ML, etc.
    description = Column(Text, nullable=True)
    difficulty_level = Column(String(50), default="Intermediate")

class StudentSkill(Base):
    __tablename__ = "student_skills"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    proficiency_score = Column(Float, default=50.0) # 0 to 100
    proficiency_level = Column(String(50), default="Intermediate") # Beginner, Basic, Intermediate, Advanced, Expert
    evidence_source = Column(JSON, default=dict) # e.g. {"assessment": 75, "project": True, "self_rating": 4}
    last_assessed = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    profile = relationship("StudentProfile", back_populates="skills")
    skill = relationship("Skill")

class StudentSoftSkill(Base):
    __tablename__ = "student_soft_skills"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    skill_name = Column(String(100), nullable=False)
    rating = Column(Integer, default=3) # 1 to 5
    
    profile = relationship("StudentProfile", back_populates="soft_skills")

class StudentInterest(Base):
    __tablename__ = "student_interests"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    interest_name = Column(String(100), nullable=False)
    preference_level = Column(Integer, default=5) # 1 to 5
    
    profile = relationship("StudentProfile", back_populates="interests")

class StudentProject(Base):
    __tablename__ = "student_projects"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    technologies = Column(JSON, default=list)
    role = Column(String(100), nullable=True)
    duration = Column(String(100), nullable=True)
    project_url = Column(String(255), nullable=True)
    
    profile = relationship("StudentProfile", back_populates="projects")

class StudentCertification(Base):
    __tablename__ = "student_certifications"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    issuer = Column(String(255), nullable=False)
    issue_date = Column(String(100), nullable=True)
    credential_id = Column(String(255), nullable=True)
    certificate_url = Column(String(255), nullable=True)
    
    profile = relationship("StudentProfile", back_populates="certifications")

# ================= CAREERS =================
class CareerRole(Base):
    __tablename__ = "career_roles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), unique=True, index=True, nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    industry = Column(String(100), index=True, nullable=False)
    difficulty = Column(String(50), default="Intermediate")
    entry_level_suitability = Column(Boolean, default=True)
    education_requirement = Column(String(255), default="Bachelor's Degree in CS/IT/Related")
    average_salary = Column(String(100), default="$85,000 - $120,000 / ₹8-16 LPA")
    market_demand = Column(String(50), default="High")
    soft_skills = Column(JSON, default=list)
    recommended_projects = Column(JSON, default=list)
    recommended_certifications = Column(JSON, default=list)
    
    skills = relationship("CareerSkill", back_populates="career", cascade="all, delete-orphan")

class CareerSkill(Base):
    __tablename__ = "career_skills"
    
    id = Column(Integer, primary_key=True, index=True)
    career_id = Column(Integer, ForeignKey("career_roles.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    required_level = Column(Float, default=70.0) # 0 to 100
    is_mandatory = Column(Boolean, default=True)
    importance_weight = Column(Float, default=1.0)
    
    career = relationship("CareerRole", back_populates="skills")
    skill = relationship("Skill")

# ================= ASSESSMENTS =================
class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    category = Column(String(100), index=True, nullable=False)
    description = Column(Text, nullable=True)
    time_limit_minutes = Column(Integer, default=20)
    passing_percentage = Column(Float, default=60.0)
    total_questions = Column(Integer, default=10)
    role_slug = Column(String(100), nullable=True, index=True)
    is_active = Column(Boolean, default=True)
    
    questions = relationship("Question", back_populates="assessment", cascade="all, delete-orphan")
    attempts = relationship("AssessmentAttempt", back_populates="assessment")

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="SET NULL"), nullable=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), default="mcq") # mcq, multi_select, true_false, scenario, coding
    difficulty = Column(String(50), default="Intermediate") # Beginner, Intermediate, Advanced
    marks = Column(Integer, default=1)
    explanation = Column(Text, nullable=True)
    code_snippet = Column(Text, nullable=True)
    
    assessment = relationship("Assessment", back_populates="questions")
    skill = relationship("Skill")
    options = relationship("QuestionOption", back_populates="question", cascade="all, delete-orphan")

class QuestionOption(Base):
    __tablename__ = "question_options"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    option_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)
    explanation = Column(Text, nullable=True)
    
    question = relationship("Question", back_populates="options")

class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
    score = Column(Float, default=0.0)
    total_marks = Column(Float, default=0.0)
    percentage = Column(Float, default=0.0)
    status = Column(String(50), default="completed") # in_progress, completed, timed_out
    time_spent_seconds = Column(Integer, default=0)
    accuracy = Column(Float, default=0.0)
    difficulty_performance = Column(JSON, default=dict)
    skill_scores = Column(JSON, default=dict)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    profile = relationship("StudentProfile", back_populates="attempts")
    assessment = relationship("Assessment", back_populates="attempts")
    answers = relationship("AssessmentAnswer", back_populates="attempt", cascade="all, delete-orphan")

class AssessmentAnswer(Base):
    __tablename__ = "assessment_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("assessment_attempts.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    selected_options = Column(JSON, default=list)
    is_correct = Column(Boolean, default=False)
    marks_awarded = Column(Float, default=0.0)
    
    attempt = relationship("AssessmentAttempt", back_populates="answers")
    question = relationship("Question")

# ================= RECOMMENDATIONS & SKILL GAPS =================
class CareerRecommendation(Base):
    __tablename__ = "career_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    career_id = Column(Integer, ForeignKey("career_roles.id", ondelete="CASCADE"), nullable=False)
    match_score = Column(Float, nullable=False) # 0 to 100
    rank = Column(Integer, default=1)
    reasons = Column(JSON, default=list) # why recommended
    missing_skills = Column(JSON, default=list)
    recommended_actions = Column(JSON, default=list)
    component_scores = Column(JSON, default=dict) # e.g. skill_match, assessment, interest, academic, projects, soft_skills
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    profile = relationship("StudentProfile", back_populates="recommendations")
    career = relationship("CareerRole")

class SkillGap(Base):
    __tablename__ = "skill_gaps"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    career_id = Column(Integer, ForeignKey("career_roles.id", ondelete="CASCADE"), nullable=False)
    skill_name = Column(String(100), nullable=False)
    current_score = Column(Float, default=0.0)
    required_score = Column(Float, default=70.0)
    gap_severity = Column(String(50), default="Medium") # None, Low, Medium, High, Critical
    calculated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

# ================= ROADMAP & LEARNING =================
class LearningRoadmap(Base):
    __tablename__ = "learning_roadmaps"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    career_id = Column(Integer, ForeignKey("career_roles.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    total_items = Column(Integer, default=0)
    completed_items = Column(Integer, default=0)
    progress_percentage = Column(Float, default=0.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    profile = relationship("StudentProfile", back_populates="roadmaps")
    career = relationship("CareerRole")
    items = relationship("RoadmapItem", back_populates="roadmap", cascade="all, delete-orphan")

class RoadmapItem(Base):
    __tablename__ = "roadmap_items"
    
    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("learning_roadmaps.id", ondelete="CASCADE"), nullable=False)
    skill_name = Column(String(100), nullable=False)
    stage = Column(String(50), default="Beginner") # Foundation, Beginner, Intermediate, Advanced, Professional
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    estimated_hours = Column(Integer, default=10)
    prerequisites = Column(JSON, default=list)
    resource_link = Column(String(500), nullable=True)
    project_prompt = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    
    roadmap = relationship("LearningRoadmap", back_populates="items")

class LearningResource(Base):
    __tablename__ = "learning_resources"
    
    id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String(100), index=True, nullable=False)
    title = Column(String(255), nullable=False)
    resource_type = Column(String(50), default="Course") # Course, Tutorial, Documentation, Video, Book, Project, Certification
    provider = Column(String(100), nullable=False)
    url = Column(String(500), nullable=False)
    estimated_hours = Column(Integer, default=15)
    rating = Column(Float, default=4.7)
    description = Column(Text, nullable=True)
    difficulty = Column(String(50), default="Intermediate")

# ================= RESUME & VISION =================
class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_size = Column(Integer, default=0)
    upload_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    profile = relationship("StudentProfile", back_populates="resumes")
    extracted_data = relationship("ResumeExtractedData", back_populates="resume", uselist=False, cascade="all, delete-orphan")

class ResumeExtractedData(Base):
    __tablename__ = "resume_extracted_data"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), unique=True, nullable=False)
    extracted_name = Column(String(255), nullable=True)
    extracted_email = Column(String(255), nullable=True)
    extracted_phone = Column(String(100), nullable=True)
    extracted_education = Column(JSON, default=list)
    extracted_skills = Column(JSON, default=list)
    extracted_projects = Column(JSON, default=list)
    extracted_certifications = Column(JSON, default=list)
    extracted_experience = Column(JSON, default=list)
    completeness_score = Column(Float, default=0.0) # 0 to 100
    ats_keyword_match = Column(JSON, default=dict)
    raw_text = Column(Text, nullable=True)
    
    resume = relationship("Resume", back_populates="extracted_data")

# ================= BLOCKCHAIN & CREDENTIALS =================
class Credential(Base):
    __tablename__ = "credentials"
    
    id = Column(Integer, primary_key=True, index=True)
    credential_id = Column(String(64), unique=True, index=True, nullable=False) # e.g. CRED-2026-XXXXX
    profile_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    credential_type = Column(String(100), default="Skill Assessment Certificate") # Skill Assessment Certificate, Course Completion, Career Readiness
    credential_hash = Column(String(64), nullable=False) # SHA-256 hash of credential data
    issuer_address = Column(String(100), default="0x71C...EDUGUIDE_ROOT_CA")
    blockchain_tx_hash = Column(String(66), nullable=False) # 0x...
    block_number = Column(Integer, default=1042)
    verification_status = Column(String(50), default="VERIFIED")
    metadata_json = Column(JSON, default=dict)
    issued_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    profile = relationship("StudentProfile", back_populates="credentials")

# ================= COUNSELOR & NOTES =================
class CounselorNote(Base):
    __tablename__ = "counselor_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    counselor_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    profile_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    note_text = Column(Text, nullable=False)
    guidance_actions = Column(JSON, default=list)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    profile = relationship("StudentProfile", back_populates="counselor_notes")
    counselor = relationship("User")

# ================= GAMIFICATION =================
class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False) # ASSESSMENT_STARTER, SQL_EXPLORER, etc.
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    badge_icon = Column(String(100), default="Award")
    category = Column(String(50), default="Assessment")
    points = Column(Integer, default=50)

class StudentAchievement(Base):
    __tablename__ = "student_achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id", ondelete="CASCADE"), nullable=False)
    unlocked_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    profile = relationship("StudentProfile", back_populates="achievements")
    achievement = relationship("Achievement")

# ================= AUDIT LOGS & NOTIFICATIONS =================
class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String(100), index=True, nullable=False) # LOGIN, LOGOUT, SUBMIT_ASSESSMENT, CREATE_CREDENTIAL, etc.
    status = Column(String(50), default="SUCCESS")
    ip_address = Column(String(100), default="127.0.0.1")
    details = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    
    user = relationship("User", back_populates="audit_logs")

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), default="info") # info, success, warning, achievement
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    user = relationship("User", back_populates="notifications")
