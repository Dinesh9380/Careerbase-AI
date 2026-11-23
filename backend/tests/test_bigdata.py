from app.bigdata.analytics_engine import bigdata_engine

def test_bigdata_batch_processing(client):
    # Process batch of 1,000 records
    result = bigdata_engine.generate_and_process_dataset(record_count=1000)
    assert result["records_processed"] == 1000
    assert result["execution_time_seconds"] > 0
    assert len(result["skill_popularity"]) > 0
    assert len(result["career_interest_trends"]) > 0
    assert len(result["department_performance"]) > 0

    # Test via admin API endpoint
    login_res = client.post("/api/auth/login", json={
        "email": "admin@demo.com",
        "password": "Demo@123456"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    api_res = client.post("/api/admin/bigdata/generate", json={"record_count": 1000}, headers=headers)
    assert api_res.status_code == 200
    data = api_res.json()
    assert data["records_processed"] == 1000
