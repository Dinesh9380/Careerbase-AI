from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.models import (
    StudentProfile, CareerRole, CareerSkill, StudentSkill,
    CareerRecommendation, SkillGap, AssessmentAttempt
)
from app.ml.inference import inference_engine
from app.ml.explainability import generate_career_explanation

class RecommendationService:
    def __init__(self):
        pass

    def compute_student_recommendations(self, db: Session, profile: StudentProfile) -> List[Dict[str, Any]]:
        """Calculates hybrid recommendations for the student combining ML, rule matching, and assessment data."""
        # 1. Gather student data
        student_skills_map = {ss.skill.name.lower(): ss.proficiency_score for ss in profile.skills if ss.skill}
        interests = [si.interest_name for si in profile.interests]
        project_count = len(profile.projects)
        cert_count = len(profile.certifications)
        cgpa = profile.academic_record.cgpa if profile.academic_record and profile.academic_record.cgpa else 7.5

        # 2. Get latest assessment scores
        assessment_scores = {}
        for att in profile.attempts:
            if att.status == "completed" and att.skill_scores:
                for s_k, s_v in att.skill_scores.items():
                    assessment_scores[s_k] = max(assessment_scores.get(s_k, 0), s_v)

        # 3. ML Model prediction
        features_df = inference_engine.map_student_skills_to_features(
            student_skills=student_skills_map,
            cgpa=cgpa,
            project_count=project_count,
            certification_count=cert_count
        )
        ml_probs = inference_engine.predict_career_probabilities(features_df)

        # 4. Evaluate each career in DB
        careers = db.query(CareerRole).all()
        evaluated_careers = []

        for career in careers:
            # Rule-based skill matching
            career_skills_list = []
            skill_match_total = 0.0
            total_weight = 0.0

            for cs in career.skills:
                s_name = cs.skill.name if cs.skill else "General"
                req = cs.required_level
                cur = student_skills_map.get(s_name.lower(), 15.0) # Baseline if not recorded
                weight = cs.importance_weight
                
                # Match percentage for this skill (capped at 100%)
                s_match = min(100.0, (cur / max(req, 1.0)) * 100.0)
                skill_match_total += (s_match * weight)
                total_weight += weight

                career_skills_list.append({
                    "skill_name": s_name,
                    "required_level": req,
                    "is_mandatory": cs.is_mandatory,
                    "importance_weight": weight
                })

            rule_skill_match = (skill_match_total / max(total_weight, 1.0))

            # ML score (scaled or fallback)
            ml_score = ml_probs.get(career.title, rule_skill_match)

            # Assessment score component
            avg_assessment = sum(assessment_scores.values()) / max(len(assessment_scores), 1) if assessment_scores else 60.0

            # Interest match component
            interest_match = 85.0 if any(term in career.title.lower() for interest in interests for term in interest.lower().split()) else 50.0

            # Academic & project readiness
            academic_proj = min(100.0, (cgpa * 8.0) + (project_count * 10.0) + (cert_count * 5.0))

            # Hybrid weighted combination:
            # 35% Skill Match + 35% ML Prediction + 10% Assessment + 10% Academic/Projects + 10% Interests
            final_match = (
                (rule_skill_match * 0.35) +
                (ml_score * 0.35) +
                (avg_assessment * 0.10) +
                (academic_proj * 0.10) +
                (interest_match * 0.10)
            )
            final_match = round(min(98.5, max(15.0, final_match)), 1)

            # Generate explainability
            reasons, missing_gaps, next_steps = generate_career_explanation(
                career_title=career.title,
                student_skills=student_skills_map,
                career_skills=career_skills_list,
                interests=interests,
                project_count=project_count,
                assessment_scores=assessment_scores
            )

            component_scores = {
                "skill_match": round(rule_skill_match, 1),
                "ml_probability": round(ml_score, 1),
                "assessment_score": round(avg_assessment, 1),
                "academic_projects": round(academic_proj, 1),
                "interest_alignment": round(interest_match, 1)
            }

            evaluated_careers.append({
                "career_id": career.id,
                "career_title": career.title,
                "slug": career.slug,
                "industry": career.industry,
                "match_score": final_match,
                "reasons": reasons,
                "missing_skills": missing_gaps,
                "recommended_actions": next_steps,
                "component_scores": component_scores,
                "career_skills_list": career_skills_list
            })

        # Rank careers
        evaluated_careers.sort(key=lambda x: x["match_score"], reverse=True)
        for i, c in enumerate(evaluated_careers):
            c["rank"] = i + 1

        # Persist top recommendations & skill gaps in DB
        # Delete old recommendations
        db.query(CareerRecommendation).filter(CareerRecommendation.profile_id == profile.id).delete()
        db.query(SkillGap).filter(SkillGap.profile_id == profile.id).delete()

        for rec_data in evaluated_careers[:10]: # Store top 10
            db_rec = CareerRecommendation(
                profile_id=profile.id,
                career_id=rec_data["career_id"],
                match_score=rec_data["match_score"],
                rank=rec_data["rank"],
                reasons=rec_data["reasons"],
                missing_skills=rec_data["missing_skills"],
                recommended_actions=rec_data["recommended_actions"],
                component_scores=rec_data["component_scores"]
            )
            db.add(db_rec)

            # Store skill gaps for top recommended careers
            for gap in rec_data["missing_skills"]:
                db_gap = SkillGap(
                    profile_id=profile.id,
                    career_id=rec_data["career_id"],
                    skill_name=gap["skill_name"],
                    current_score=gap["current_score"],
                    required_score=gap["required_score"],
                    gap_severity=gap["gap_severity"]
                )
                db.add(db_gap)

        db.commit()
        return evaluated_careers

    def compare_careers(self, db: Session, profile: StudentProfile, career_ids: List[int]) -> List[Dict[str, Any]]:
        """Compares 2 or more careers side by side on required skills, readiness, salary, and learning time."""
        recommendations = self.compute_student_recommendations(db, profile)
        rec_dict = {r["career_id"]: r for r in recommendations}

        comparison = []
        for cid in career_ids:
            career = db.query(CareerRole).filter(CareerRole.id == cid).first()
            if not career:
                continue

            rec = rec_dict.get(cid, {})
            match_score = rec.get("match_score", 50.0)

            # Readiness label
            readiness = "Job Ready" if match_score >= 80 else ("Near Ready (1-2 months)" if match_score >= 65 else "Developing (3-6 months)")
            est_weeks = max(4, int((100 - match_score) * 0.4))

            comparison.append({
                "career_id": career.id,
                "title": career.title,
                "match_score": match_score,
                "readiness_level": readiness,
                "required_skills": [
                    {
                        "skill_name": cs.skill.name if cs.skill else "General",
                        "required_level": cs.required_level,
                        "is_mandatory": cs.is_mandatory
                    } for cs in career.skills
                ],
                "missing_skills": rec.get("missing_skills", []),
                "learning_time_weeks": est_weeks,
                "difficulty": career.difficulty,
                "average_salary": career.average_salary
            })

        return comparison

recommendation_service = RecommendationService()
