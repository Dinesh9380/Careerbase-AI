from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from app.models.models import (
    Assessment, Question, QuestionOption, AssessmentAttempt,
    AssessmentAnswer, StudentProfile, StudentSkill, Skill,
    Achievement, StudentAchievement, Notification
)

class AssessmentService:
    def __init__(self):
        pass

    def start_assessment(self, db: Session, assessment_id: int, profile: StudentProfile) -> Dict[str, Any]:
        """Initializes a new assessment attempt and returns ordered questions."""
        assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
        if not assessment:
            raise ValueError("Assessment not found")

        # Create attempt
        attempt = AssessmentAttempt(
            profile_id=profile.id,
            assessment_id=assessment.id,
            status="in_progress",
            started_at=datetime.now(timezone.utc)
        )
        db.add(attempt)
        db.commit()
        db.refresh(attempt)

        # Get questions
        questions = db.query(Question).filter(Question.assessment_id == assessment.id).all()

        questions_data = []
        for q in questions:
            options_data = [
                {"id": opt.id, "option_text": opt.option_text}
                for opt in q.options
            ]
            questions_data.append({
                "id": q.id,
                "question_text": q.question_text,
                "question_type": q.question_type,
                "difficulty": q.difficulty,
                "marks": q.marks,
                "code_snippet": q.code_snippet,
                "options": options_data
            })

        return {
            "attempt_id": attempt.id,
            "assessment_id": assessment.id,
            "title": assessment.title,
            "category": assessment.category,
            "time_limit_minutes": assessment.time_limit_minutes,
            "questions": questions_data,
            "started_at": attempt.started_at
        }

    def submit_assessment(
        self,
        db: Session,
        attempt_id: int,
        answers: List[Dict[str, Any]],
        time_spent_seconds: int,
        profile: StudentProfile
    ) -> Dict[str, Any]:
        """Scores the attempt, updates student skill profile, checks achievements."""
        attempt = db.query(AssessmentAttempt).filter(
            AssessmentAttempt.id == attempt_id,
            AssessmentAttempt.profile_id == profile.id
        ).first()

        if not attempt:
            raise ValueError("Assessment attempt not found")
        if attempt.status == "completed":
            raise ValueError("Assessment already submitted")

        total_score = 0.0
        total_possible = 0.0
        correct_count = 0
        difficulty_performance = {"Beginner": {"correct": 0, "total": 0}, "Intermediate": {"correct": 0, "total": 0}, "Advanced": {"correct": 0, "total": 0}}
        skill_score_map = {} # skill_id => {"earned": 0, "total": 0}

        for ans in answers:
            q_id = ans.get("question_id")
            selected_opts = ans.get("selected_options", [])
            question = db.query(Question).filter(Question.id == q_id).first()
            if not question:
                continue

            total_possible += question.marks
            diff = question.difficulty
            if diff not in difficulty_performance:
                difficulty_performance[diff] = {"correct": 0, "total": 0}
            difficulty_performance[diff]["total"] += 1

            if question.skill_id:
                if question.skill_id not in skill_score_map:
                    skill_score_map[question.skill_id] = {"earned": 0, "total": 0}
                skill_score_map[question.skill_id]["total"] += question.marks

            # Check correctness
            correct_opts = [opt.id for opt in question.options if opt.is_correct]
            is_correct = set(selected_opts) == set(correct_opts)

            marks_awarded = question.marks if is_correct else 0.0
            if is_correct:
                total_score += marks_awarded
                correct_count += 1
                difficulty_performance[diff]["correct"] += 1
                if question.skill_id:
                    skill_score_map[question.skill_id]["earned"] += marks_awarded

            # Record answer
            db_answer = AssessmentAnswer(
                attempt_id=attempt.id,
                question_id=question.id,
                selected_options=selected_opts,
                is_correct=is_correct,
                marks_awarded=marks_awarded
            )
            db.add(db_answer)

        # Update attempt
        pct = (total_score / max(total_possible, 1.0)) * 100
        accuracy = (correct_count / max(len(answers), 1)) * 100
        attempt.score = total_score
        attempt.total_marks = total_possible
        attempt.percentage = round(pct, 1)
        attempt.accuracy = round(accuracy, 1)
        attempt.time_spent_seconds = time_spent_seconds
        attempt.difficulty_performance = difficulty_performance
        attempt.status = "completed"
        attempt.completed_at = datetime.now(timezone.utc)

        # Update Student Skills proficiency based on performance
        skill_results = {}
        for s_id, s_stats in skill_score_map.items():
            skill_obj = db.query(Skill).filter(Skill.id == s_id).first()
            if not skill_obj:
                continue
            s_pct = (s_stats["earned"] / max(s_stats["total"], 1)) * 100
            skill_results[skill_obj.name] = round(s_pct, 1)

            # Update or create student skill record
            stud_skill = db.query(StudentSkill).filter(
                StudentSkill.profile_id == profile.id,
                StudentSkill.skill_id == s_id
            ).first()

            # Level classification
            level = "Beginner"
            if s_pct >= 85: level = "Expert"
            elif s_pct >= 70: level = "Advanced"
            elif s_pct >= 50: level = "Intermediate"
            elif s_pct >= 30: level = "Basic"

            if stud_skill:
                # Weighted blend with existing score
                stud_skill.proficiency_score = round((stud_skill.proficiency_score * 0.4) + (s_pct * 0.6), 1)
                stud_skill.proficiency_level = level
                stud_skill.evidence_source = {
                    "last_assessment_id": attempt.assessment_id,
                    "assessment_score": round(s_pct, 1),
                    "assessed_date": datetime.now(timezone.utc).isoformat()
                }
                stud_skill.last_assessed = datetime.now(timezone.utc)
            else:
                stud_skill = StudentSkill(
                    profile_id=profile.id,
                    skill_id=s_id,
                    proficiency_score=round(s_pct, 1),
                    proficiency_level=level,
                    evidence_source={"assessment_score": round(s_pct, 1)}
                )
                db.add(stud_skill)

        attempt.skill_scores = skill_results

        # Gamification: check achievements
        unlocked_badges = []
        achieve_starter = db.query(Achievement).filter(Achievement.code == "ASSESSMENT_STARTER").first()
        if achieve_starter:
            has_it = db.query(StudentAchievement).filter(
                StudentAchievement.profile_id == profile.id,
                StudentAchievement.achievement_id == achieve_starter.id
            ).first()
            if not has_it:
                db.add(StudentAchievement(profile_id=profile.id, achievement_id=achieve_starter.id))
                unlocked_badges.append(achieve_starter.title)
                profile.points += achieve_starter.points

        if pct >= 80:
            achieve_high = db.query(Achievement).filter(Achievement.code == "HIGH_SCORER").first()
            if achieve_high:
                has_high = db.query(StudentAchievement).filter(
                    StudentAchievement.profile_id == profile.id,
                    StudentAchievement.achievement_id == achieve_high.id
                ).first()
                if not has_high:
                    db.add(StudentAchievement(profile_id=profile.id, achievement_id=achieve_high.id))
                    unlocked_badges.append(achieve_high.title)
                    profile.points += achieve_high.points

        # Add notification
        notif = Notification(
            user_id=profile.user_id,
            title="Assessment Completed",
            message=f"You scored {round(pct, 1)}% in '{attempt.assessment.title}'. Skill proficiencies updated.",
            notification_type="success"
        )
        db.add(notif)

        db.commit()
        db.refresh(attempt)

        return {
            "attempt_id": attempt.id,
            "score": attempt.score,
            "total_marks": attempt.total_marks,
            "percentage": attempt.percentage,
            "accuracy": attempt.accuracy,
            "passed": attempt.percentage >= attempt.assessment.passing_percentage,
            "status": attempt.status,
            "skill_scores": skill_results,
            "difficulty_performance": difficulty_performance,
            "new_achievements": unlocked_badges
        }

assessment_service = AssessmentService()
