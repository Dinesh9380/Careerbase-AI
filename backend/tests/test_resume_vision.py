from app.vision.resume_intelligence import resume_engine

def test_resume_nlp_and_vision_extraction():
    sample_resume_text = """
    Alex Johnson
    Email: alex.johnson@university.edu
    Phone: (555) 123-4567

    Education:
    Bachelor of Technology in Computer Science and Engineering, 2025

    Technical Skills:
    Python, SQL, React, FastAPI, Docker, Git, Machine Learning, Data Structures

    Projects:
    Developed an AI-based Career Recommendation System with scikit-learn and React.
    Built a High-Throughput Relational Database query cache.

    Certifications:
    AWS Certified Solutions Architect Associate, 2025
    """

    parsed = resume_engine.parse_resume_content(sample_resume_text, student_existing_skills=["Python"])
    assert parsed["extracted_email"] == "alex.johnson@university.edu"
    assert parsed["extracted_phone"] is not None
    assert len(parsed["extracted_skills"]) >= 5
    assert parsed["completeness_score"] > 60.0
    assert parsed["ats_keyword_coverage"] > 50.0
    assert len(parsed["suggested_improvements"]) > 0
