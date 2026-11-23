from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.models import (
    StudentProfile, CareerRole, LearningRoadmap, RoadmapItem,
    LearningResource, SkillGap, Notification, Achievement, StudentAchievement
)

ROADMAP_TEMPLATES = {
    "Foundation": [
        {"title": "Core Syntax & Algorithmic Foundations", "desc": "Master fundamentals, control structures, and basic computational thinking.", "hours": 15},
        {"title": "Version Control & Git Collaboration", "desc": "Learn branching, merging, GitHub workflows, and repository hygiene.", "hours": 8}
    ],
    "Beginner": [
        {"title": "Core Domain Frameworks & Tools", "desc": "Build working applications utilizing primary libraries and standard packages.", "hours": 25},
        {"title": "Database Schema Design & Querying", "desc": "Implement relational schemas, indexes, and complex analytical SQL queries.", "hours": 18}
    ],
    "Intermediate": [
        {"title": "Architectural Design & API Integration", "desc": "Develop RESTful modular micro-architectures with robust error handling.", "hours": 30},
        {"title": "Testing, Validation & Code Quality", "desc": "Write comprehensive unit and integration test suites adhering to standard patterns.", "hours": 15}
    ],
    "Advanced": [
        {"title": "System Scalability & Performance Optimization", "desc": "Implement caching, asynchronous worker queues, and bottleneck elimination.", "hours": 35},
        {"title": "Domain-Specific Advanced Specialization", "desc": "Deep dive into state-of-the-art algorithms, model tuning, or cloud infrastructure.", "hours": 40}
    ],
    "Professional": [
        {"title": "Production Deployment & Containerization", "desc": "Package containerized artifacts with automated CI/CD deployment pipelines.", "hours": 20},
        {"title": "Capstone Portfolio Engineering & Recruiter Pitch", "desc": "Deliver end-to-end demonstrable production product with documentation.", "hours": 40}
    ]
}

class RoadmapService:
    def __init__(self):
        pass

    def generate_or_get_roadmap(self, db: Session, profile: StudentProfile, career_id: Optional[int] = None) -> Dict[str, Any]:
        """Generates dynamic 5-tier roadmap tailored to student's skill gaps for their target career."""
        target_career_id = career_id or profile.target_career_id

        # Fallback to top career if not set
        if not target_career_id:
            career = db.query(CareerRole).first()
            target_career_id = career.id if career else 1

        career = db.query(CareerRole).filter(CareerRole.id == target_career_id).first()
        if not career:
            raise ValueError("Target career role not found")

        # Check existing roadmap
        roadmap = db.query(LearningRoadmap).filter(
            LearningRoadmap.profile_id == profile.id,
            LearningRoadmap.career_id == target_career_id
        ).first()

        if not roadmap:
            # Create new roadmap
            roadmap = LearningRoadmap(
                profile_id=profile.id,
                career_id=career.id,
                title=f"{career.title} Mastery Roadmap",
                total_items=0,
                completed_items=0,
                progress_percentage=0.0
            )
            db.add(roadmap)
            db.commit()
            db.refresh(roadmap)

            # Retrieve student's gaps for this career
            gaps = db.query(SkillGap).filter(
                SkillGap.profile_id == profile.id,
                SkillGap.career_id == career.id
            ).all()

            gap_skill_names = [g.skill_name for g in gaps] or [cs.skill.name for cs in career.skills if cs.skill][:4]

            # Populate roadmap items for each stage
            total_items_count = 0
            for stage, templates in ROADMAP_TEMPLATES.items():
                for idx, tpl in enumerate(templates):
                    associated_skill = gap_skill_names[idx % len(gap_skill_names)] if gap_skill_names else "Engineering"
                    
                    # Fetch matching learning resource
                    res = db.query(LearningResource).filter(
                        LearningResource.skill_name.ilike(f"%{associated_skill}%")
                    ).first()
                    res_url = res.url if res else "https://docs.python.org/3/"

                    item = RoadmapItem(
                        roadmap_id=roadmap.id,
                        skill_name=associated_skill,
                        stage=stage,
                        title=f"{associated_skill}: {tpl['title']}",
                        description=tpl["desc"],
                        estimated_hours=tpl["hours"],
                        prerequisites=["Basic computer literacy" if stage == "Foundation" else "Previous module completion"],
                        resource_link=res_url,
                        project_prompt=f"Create a mini-project demonstrating mastery of {associated_skill} in {stage.lower()} context.",
                        is_completed=False
                    )
                    db.add(item)
                    total_items_count += 1

            roadmap.total_items = total_items_count
            db.commit()
            db.refresh(roadmap)

        # Return structured roadmap
        items = db.query(RoadmapItem).filter(RoadmapItem.roadmap_id == roadmap.id).all()
        items_data = [
            {
                "id": it.id,
                "skill_name": it.skill_name,
                "stage": it.stage,
                "title": it.title,
                "description": it.description,
                "estimated_hours": it.estimated_hours,
                "resource_link": it.resource_link,
                "project_prompt": it.project_prompt,
                "is_completed": it.is_completed,
                "completed_at": it.completed_at
            }
            for it in items
        ]

        return {
            "id": roadmap.id,
            "career_title": career.title,
            "career_id": career.id,
            "total_items": roadmap.total_items,
            "completed_items": roadmap.completed_items,
            "progress_percentage": roadmap.progress_percentage,
            "items": items_data
        }

    def complete_roadmap_item(self, db: Session, item_id: int, profile: StudentProfile) -> Dict[str, Any]:
        """Toggles roadmap item completion status and updates overall progress."""
        item = db.query(RoadmapItem).filter(RoadmapItem.id == item_id).first()
        if not item:
            raise ValueError("Roadmap item not found")

        roadmap = db.query(LearningRoadmap).filter(
            LearningRoadmap.id == item.roadmap_id,
            LearningRoadmap.profile_id == profile.id
        ).first()

        if not roadmap:
            raise ValueError("Roadmap does not belong to student")

        # Toggle status
        item.is_completed = not item.is_completed
        item.completed_at = datetime.now(timezone.utc) if item.is_completed else None

        # Recompute totals
        all_items = db.query(RoadmapItem).filter(RoadmapItem.roadmap_id == roadmap.id).all()
        completed = sum(1 for it in all_items if it.is_completed)
        roadmap.completed_items = completed
        roadmap.progress_percentage = round((completed / max(len(all_items), 1)) * 100, 1)

        # Gamification: points
        if item.is_completed:
            profile.points += 25
            if roadmap.progress_percentage >= 100:
                achieve = db.query(Achievement).filter(Achievement.code == "ROADMAP_FINISHER").first()
                if achieve:
                    has_achieve = db.query(StudentAchievement).filter(
                        StudentAchievement.profile_id == profile.id,
                        StudentAchievement.achievement_id == achieve.id
                    ).first()
                    if not has_achieve:
                        db.add(StudentAchievement(profile_id=profile.id, achievement_id=achieve.id))
                        profile.points += achieve.points

        db.commit()
        db.refresh(roadmap)

        return {
            "item_id": item.id,
            "is_completed": item.is_completed,
            "completed_items": roadmap.completed_items,
            "total_items": roadmap.total_items,
            "progress_percentage": roadmap.progress_percentage
        }

roadmap_service = RoadmapService()
