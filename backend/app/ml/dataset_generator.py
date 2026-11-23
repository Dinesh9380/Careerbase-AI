import numpy as np
import pandas as pd
from typing import Tuple, List

CAREER_ROLES = [
    "Full Stack Developer",
    "Software Developer",
    "Data Scientist",
    "Machine Learning Engineer",
    "AI Engineer",
    "Data Analyst",
    "Data Engineer",
    "Big Data Engineer",
    "Cloud Engineer",
    "DevOps Engineer",
    "Cybersecurity Analyst",
    "Security Engineer",
    "Blockchain Developer",
    "Computer Vision Engineer",
    "NLP Engineer",
    "Database Administrator",
    "Business Analyst",
    "QA Automation Engineer",
    "Research Scientist",
    "Systems Architect"
]

SKILL_COLUMNS = [
    "python", "javascript", "java", "cpp", "sql", "nosql",
    "data_structures", "algorithms", "machine_learning", "deep_learning",
    "nlp", "computer_vision", "data_engineering", "spark_bigdata",
    "cloud_aws", "devops_docker", "cybersecurity", "blockchain_solidity",
    "react_frontend", "fastapi_backend", "system_design", "math_statistics",
    "problem_solving", "communication"
]

# Primary skills emphasized per career
CAREER_PROFILES = {
    "Full Stack Developer": {"react_frontend": 85, "javascript": 85, "fastapi_backend": 80, "sql": 75, "system_design": 70},
    "Software Developer": {"data_structures": 85, "algorithms": 85, "java": 80, "cpp": 75, "system_design": 70},
    "Data Scientist": {"python": 90, "math_statistics": 88, "machine_learning": 85, "sql": 80, "deep_learning": 70},
    "Machine Learning Engineer": {"python": 90, "machine_learning": 90, "deep_learning": 85, "algorithms": 80, "cloud_aws": 70},
    "AI Engineer": {"deep_learning": 90, "python": 90, "nlp": 85, "computer_vision": 85, "machine_learning": 88},
    "Data Analyst": {"sql": 88, "math_statistics": 82, "python": 75, "communication": 85, "nosql": 65},
    "Data Engineer": {"data_engineering": 90, "sql": 88, "spark_bigdata": 85, "python": 80, "cloud_aws": 75},
    "Big Data Engineer": {"spark_bigdata": 92, "data_engineering": 88, "java": 80, "cloud_aws": 80, "sql": 80},
    "Cloud Engineer": {"cloud_aws": 92, "devops_docker": 85, "system_design": 80, "cybersecurity": 70, "python": 70},
    "DevOps Engineer": {"devops_docker": 92, "cloud_aws": 85, "system_design": 80, "fastapi_backend": 70, "cybersecurity": 70},
    "Cybersecurity Analyst": {"cybersecurity": 92, "algorithms": 75, "system_design": 80, "communication": 75, "python": 70},
    "Security Engineer": {"cybersecurity": 94, "system_design": 85, "cpp": 80, "cloud_aws": 78, "algorithms": 80},
    "Blockchain Developer": {"blockchain_solidity": 94, "data_structures": 85, "algorithms": 80, "cybersecurity": 75, "javascript": 70},
    "Computer Vision Engineer": {"computer_vision": 92, "deep_learning": 88, "python": 85, "cpp": 75, "math_statistics": 80},
    "NLP Engineer": {"nlp": 92, "deep_learning": 88, "python": 88, "machine_learning": 82, "math_statistics": 80},
    "Database Administrator": {"sql": 94, "nosql": 88, "system_design": 80, "cloud_aws": 70, "cybersecurity": 70},
    "Business Analyst": {"communication": 90, "sql": 80, "math_statistics": 75, "problem_solving": 88, "python": 60},
    "QA Automation Engineer": {"python": 80, "javascript": 80, "algorithms": 75, "devops_docker": 70, "communication": 75},
    "Research Scientist": {"math_statistics": 92, "algorithms": 90, "machine_learning": 88, "deep_learning": 85, "python": 85},
    "Systems Architect": {"system_design": 95, "cloud_aws": 85, "devops_docker": 85, "data_structures": 85, "cybersecurity": 80}
}

def generate_synthetic_student_dataset(n_samples: int = 5000, random_state: int = 42) -> pd.DataFrame:
    """Generates realistic synthetic student profiles labeled with career roles for ML training."""
    np.random.seed(random_state)
    records = []
    
    samples_per_role = n_samples // len(CAREER_ROLES)
    remainder = n_samples % len(CAREER_ROLES)

    for i, role in enumerate(CAREER_ROLES):
        count = samples_per_role + (1 if i < remainder else 0)
        profile_core = CAREER_PROFILES.get(role, {})

        for _ in range(count):
            row = {}
            # Base distribution for all skills
            for col in SKILL_COLUMNS:
                # Normal distribution centered around 45 with std 15
                score = np.clip(np.random.normal(loc=45, scale=18), 10, 100)
                row[col] = round(score, 1)

            # Boost career-specific core skills
            for core_skill, target_val in profile_core.items():
                boosted = np.clip(np.random.normal(loc=target_val, scale=8), 40, 100)
                row[core_skill] = round(max(row.get(core_skill, 0), boosted), 1)

            # Contextual academic features
            row["cgpa"] = round(np.clip(np.random.normal(loc=8.0, scale=0.9), 5.5, 9.9), 2)
            row["project_count"] = int(np.clip(np.random.poisson(lam=2.5), 0, 8))
            row["certification_count"] = int(np.clip(np.random.poisson(lam=1.8), 0, 6))
            row["target_career"] = role

            records.append(row)

    df = pd.DataFrame(records)
    # Shuffle dataset
    df = df.sample(frac=1.0, random_state=random_state).reset_index(drop=True)
    return df

if __name__ == "__main__":
    df = generate_synthetic_student_dataset(5000)
    print(f"Generated {len(df)} records. Sample target distributions:")
    print(df["target_career"].value_counts().head())
