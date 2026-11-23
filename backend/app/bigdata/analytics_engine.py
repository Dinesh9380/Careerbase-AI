import time
import numpy as np
import pandas as pd
from typing import Dict, List, Any

POPULAR_SKILLS = [
    "Python", "SQL", "Machine Learning", "Data Structures", "Algorithms",
    "React", "FastAPI", "Cloud / AWS", "DevOps / Docker", "Cybersecurity",
    "Big Data / Spark", "Deep Learning", "System Design", "NLP", "Blockchain"
]

DEPARTMENTS = ["Computer Science", "Information Technology", "Data Science & AI", "Electronics & Comm", "Software Engineering"]

CAREER_INTERESTS = [
    "Data Scientist", "Full Stack Developer", "AI Engineer", "Cloud Engineer",
    "DevOps Engineer", "Cybersecurity Analyst", "Data Engineer", "Blockchain Developer"
]

class BigDataAnalyticsEngine:
    def __init__(self):
        pass

    def generate_and_process_dataset(self, record_count: int = 10000) -> Dict[str, Any]:
        """
        Simulates large-scale student assessment and skill telemetry logs,
        executes fast vectorized aggregations, and computes multi-dimensional analytics.
        """
        start_time = time.time()
        np.random.seed(42)

        # 1. Generate Synthetic Big Data Batch
        student_ids = np.random.randint(1000, 1000 + (record_count // 5) + 1, size=record_count)
        departments = np.random.choice(DEPARTMENTS, size=record_count, p=[0.35, 0.25, 0.20, 0.10, 0.10])
        skills = np.random.choice(POPULAR_SKILLS, size=record_count)
        scores = np.clip(np.random.normal(loc=68, scale=16, size=record_count), 20, 100).round(1)
        careers = np.random.choice(CAREER_INTERESTS, size=record_count)
        time_spent = np.random.randint(300, 1800, size=record_count) # seconds

        df = pd.DataFrame({
            "student_id": student_ids,
            "department": departments,
            "skill": skills,
            "score": scores,
            "desired_career": careers,
            "time_spent": time_spent
        })

        # 2. Big Data Aggregation Operations
        # A. Skill Popularity & Average Proficiency
        skill_grp = df.groupby("skill")["score"].agg(["count", "mean"]).reset_index()
        skill_grp.columns = ["skill", "assessments_count", "average_score"]
        skill_grp["average_score"] = skill_grp["average_score"].round(1)
        skill_grp = skill_grp.sort_values(by="assessments_count", ascending=False)
        skill_popularity = skill_grp.to_dict(orient="records")

        # B. Career Interest Trends
        career_grp = df.groupby("desired_career").size().reset_index(name="student_count")
        career_grp["percentage"] = ((career_grp["student_count"] / record_count) * 100).round(1)
        career_grp = career_grp.sort_values(by="student_count", ascending=False)
        career_trends = career_grp.to_dict(orient="records")

        # C. Common Skill Gaps (records where score < 60%)
        gaps_df = df[df["score"] < 60]
        gap_grp = gaps_df.groupby("skill").size().reset_index(name="gap_count")
        gap_grp["gap_rate_pct"] = ((gap_grp["gap_count"] / df.groupby("skill").size().values) * 100).round(1)
        gap_grp = gap_grp.sort_values(by="gap_count", ascending=False)
        common_gaps = gap_grp.to_dict(orient="records")

        # D. Department-wise Performance
        dept_grp = df.groupby("department")["score"].agg(["count", "mean"]).reset_index()
        dept_grp.columns = ["department", "total_records", "mean_score"]
        dept_grp["mean_score"] = dept_grp["mean_score"].round(1)
        dept_performance = dept_grp.to_dict(orient="records")

        execution_time = round(time.time() - start_time, 3)

        return {
            "records_processed": record_count,
            "execution_time_seconds": execution_time,
            "records_per_second": int(record_count / max(execution_time, 0.001)),
            "engine_used": "Pandas Optimized In-Memory Engine (Vectorized)",
            "skill_popularity": skill_popularity[:10],
            "career_interest_trends": career_trends[:8],
            "common_skill_gaps": common_gaps[:8],
            "department_performance": dept_performance
        }

bigdata_engine = BigDataAnalyticsEngine()
