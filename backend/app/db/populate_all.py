from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.models import Assessment, Question, QuestionOption, CareerRole

def clean_and_link():
    db: Session = SessionLocal()
    try:
        # Map of old assessment IDs to source assessment IDs to copy questions from if count < 6
        copy_map = {
            1: 13, # Full stack
            3: 18, # SQL
            4: 15, # Data Science
            5: 16, # ML
            6: 20, # Cloud
            7: 21, # DevOps
            8: 22, # Cybersecurity
            9: 19, # Big Data
            10: 23, # Blockchain
            12: 28, # Problem solving
        }

        role_slug_map = {
            1: "full-stack-developer",
            2: "cs-fundamentals",
            3: "data-analyst",
            4: "data-scientist",
            5: "machine-learning-engineer",
            6: "cloud-engineer",
            7: "devops-engineer",
            8: "cybersecurity-analyst",
            9: "data-engineer",
            10: "blockchain-developer",
            11: "python-programming",
            12: "problem-solving"
        }

        for old_id, src_id in copy_map.items():
            old_ass = db.query(Assessment).filter(Assessment.id == old_id).first()
            src_ass = db.query(Assessment).filter(Assessment.id == src_id).first()
            if old_ass and src_ass:
                # Copy questions from src_ass if not already present
                existing_texts = {q.question_text for q in old_ass.questions}
                for src_q in src_ass.questions:
                    if src_q.question_text not in existing_texts:
                        new_q = Question(
                            assessment_id=old_ass.id,
                            skill_id=src_q.skill_id,
                            question_text=src_q.question_text,
                            question_type=src_q.question_type,
                            difficulty=src_q.difficulty,
                            marks=src_q.marks,
                            explanation=src_q.explanation,
                            code_snippet=src_q.code_snippet
                        )
                        db.add(new_q)
                        db.commit()
                        db.refresh(new_q)

                        for opt in src_q.options:
                            db.add(QuestionOption(
                                question_id=new_q.id,
                                option_text=opt.option_text,
                                is_correct=opt.is_correct
                            ))
                        db.commit()

        # Update role_slugs on old assessments
        for aid, rslug in role_slug_map.items():
            ass = db.query(Assessment).filter(Assessment.id == aid).first()
            if ass:
                ass.role_slug = rslug
                ass.total_questions = len(ass.questions)
                db.commit()

        # Update total_questions for all assessments
        for ass in db.query(Assessment).all():
            ass.total_questions = len(ass.questions)
            db.commit()

        # Also let's check which assessments are active
        print("Updated all assessments. Summary:")
        for ass in db.query(Assessment).filter(Assessment.is_active == True).all():
            print(f"ID {ass.id}: {ass.title} ({ass.category}) | Role: {ass.role_slug} | Questions: {len(ass.questions)}")

    finally:
        db.close()

if __name__ == "__main__":
    clean_and_link()
