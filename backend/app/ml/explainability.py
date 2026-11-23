from typing import List, Dict, Any, Tuple

def generate_career_explanation(
    career_title: str,
    student_skills: Dict[str, float],
    career_skills: List[Dict[str, Any]],
    interests: List[str],
    project_count: int,
    assessment_scores: Dict[str, float]
) -> Tuple[List[str], List[Dict[str, Any]], List[str]]:
    """
    Generates explainable, evidence-based reasoning for why a career is recommended,
    identifies specific skill gaps with severity, and provides actionable next steps.
    """
    reasons = []
    missing_gaps = []
    next_steps = []

    strong_matches = []
    moderate_skills = []

    for cs in career_skills:
        skill_name = cs["skill_name"]
        req_level = float(cs.get("required_level", 70.0))
        cur_level = float(student_skills.get(skill_name.lower(), student_skills.get(skill_name, 0.0)))
        
        diff = req_level - cur_level

        if cur_level >= req_level:
            strong_matches.append(f"{skill_name} ({int(cur_level)}% proficiency)")
        elif cur_level >= (req_level * 0.7):
            moderate_skills.append(skill_name)
        else:
            severity = "Critical" if cs.get("is_mandatory") and diff > 30 else ("High" if diff > 25 else "Medium")
            missing_gaps.append({
                "skill_name": skill_name,
                "current_score": round(cur_level, 1),
                "required_score": round(req_level, 1),
                "gap_severity": severity,
                "is_mandatory": cs.get("is_mandatory", True)
            })

    # 1. Build reasons
    if strong_matches:
        reasons.append(f"Strong match in core competencies: {', '.join(strong_matches[:3])}.")
    if moderate_skills:
        reasons.append(f"Solid foundation in {', '.join(moderate_skills[:2])} with quick upgrade potential.")

    # Assessment evidence
    top_assessments = [k for k, v in assessment_scores.items() if v >= 75]
    if top_assessments:
        reasons.append(f"High assessment scores in {', '.join(top_assessments[:2])}.")

    # Project evidence
    if project_count >= 2:
        reasons.append(f"Demonstrated practical hands-on experience with {project_count} completed technical projects.")

    # Interest alignment
    for interest in interests:
        if any(term in career_title.lower() for term in interest.lower().split()):
            reasons.append(f"Direct alignment with declared career interest in '{interest}'.")
            break

    if not reasons:
        reasons.append(f"Good foundational aptitude aligning with entry-level {career_title} pathways.")

    # 2. Build actionable next steps
    if missing_gaps:
        top_gap = missing_gaps[0]
        next_steps.append(f"Bridge the highest priority gap in {top_gap['skill_name']} from {int(top_gap['current_score'])}% to {int(top_gap['required_score'])}%.")
        if len(missing_gaps) > 1:
            next_steps.append(f"Follow personalized roadmap modules for {missing_gaps[1]['skill_name']}.")
    else:
        next_steps.append("Complete advanced scenario-based assessments to demonstrate mastery.")

    next_steps.append(f"Build and deploy an end-to-end portfolio project showcasing {career_title} tech stack.")
    next_steps.append("Earn a blockchain-verified skill credential to validate your readiness to recruiters.")

    return reasons, missing_gaps, next_steps
