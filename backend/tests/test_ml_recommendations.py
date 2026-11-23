from app.ml.inference import inference_engine
from app.ml.explainability import generate_career_explanation

def test_ml_inference_and_recommendations(client):
    # 1. Test feature mapping and inference
    student_skills = {"python": 88.0, "sql": 82.0, "machine_learning": 78.0}
    df = inference_engine.map_student_skills_to_features(student_skills, cgpa=8.8, project_count=3)
    assert len(df) == 1

    probs = inference_engine.predict_career_probabilities(df)
    assert len(probs) > 0
    assert "Data Scientist" in probs or "Machine Learning Engineer" in probs

    # 2. Test explainability engine
    reasons, missing_gaps, next_steps = generate_career_explanation(
        career_title="Data Scientist",
        student_skills=student_skills,
        career_skills=[
            {"skill_name": "Python", "required_level": 80.0, "is_mandatory": True},
            {"skill_name": "Deep Learning", "required_level": 70.0, "is_mandatory": True}
        ],
        interests=["Data Science", "AI/ML"],
        project_count=2,
        assessment_scores={"Python": 90.0}
    )

    assert len(reasons) > 0
    assert any("Deep Learning" in g["skill_name"] for g in missing_gaps)
    assert len(next_steps) > 0

    # 3. Test API recommendations endpoint
    login_res = client.post("/api/auth/login", json={
        "email": "student@demo.com",
        "password": "Demo@123456"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    rec_res = client.get("/api/careers/recommendations", headers=headers)
    assert rec_res.status_code == 200
    recs = rec_res.json()
    assert len(recs) > 0
    assert "match_score" in recs[0]
    assert "reasons" in recs[0]
