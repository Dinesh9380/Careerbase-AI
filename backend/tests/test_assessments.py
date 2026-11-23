def test_assessment_flow(client):
    # Login as demo student
    login_res = client.post("/api/auth/login", json={
        "email": "student@demo.com",
        "password": "Demo@123456"
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. List active assessments
    list_res = client.get("/api/assessments", headers=headers)
    assert list_res.status_code == 200
    assessments = list_res.json()
    assert len(assessments) > 0
    ass_id = assessments[0]["id"]

    # 2. Start assessment
    start_res = client.post(f"/api/assessments/{ass_id}/start", headers=headers)
    assert start_res.status_code == 200
    start_data = start_res.json()
    assert "attempt_id" in start_data
    attempt_id = start_data["attempt_id"]
    questions = start_data["questions"]
    assert len(questions) > 0

    # 3. Submit answers
    answers = []
    for q in questions:
        # Pick the first option
        opt_id = q["options"][0]["id"] if q["options"] else 1
        answers.append({"question_id": q["id"], "selected_options": [opt_id]})

    submit_res = client.post(f"/api/assessments/{attempt_id}/submit", json={
        "time_spent_seconds": 120,
        "answers": answers
    }, headers=headers)
    assert submit_res.status_code == 200
    result = submit_res.json()
    assert "percentage" in result
    assert "status" in result
    assert result["status"] == "completed"
