import uuid

def test_user_registration_and_login(client):
    unique_email = f"student_{uuid.uuid4().hex[:6]}@test.com"
    # 1. Register new student
    reg_payload = {
        "email": unique_email,
        "password": "Password123!",
        "full_name": "Test Scholar",
        "role": "student"
    }
    res = client.post("/api/auth/register", json=reg_payload)
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["user"]["email"] == unique_email

    # 2. Duplicate registration should fail
    dup_res = client.post("/api/auth/register", json=reg_payload)
    assert dup_res.status_code == 400
    assert "already exists" in dup_res.json()["detail"]

    # 3. Successful Login
    login_res = client.post("/api/auth/login", json={
        "email": unique_email,
        "password": "Password123!"
    })
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data

    # 4. Invalid Password Login
    bad_login = client.post("/api/auth/login", json={
        "email": unique_email,
        "password": "WrongPassword!"
    })
    assert bad_login.status_code == 401
