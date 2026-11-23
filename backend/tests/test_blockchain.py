from app.blockchain.blockchain_ledger import blockchain_ledger

def test_blockchain_ledger_and_verification(client):
    # 1. Direct ledger tests
    cred_id = "TEST-CRED-9999"
    result = blockchain_ledger.add_credential(
        credential_id=cred_id,
        student_id=1,
        title="Test Solidity Certificate",
        credential_type="Skill Assessment Certificate",
        metadata={"grade": "A+", "score": 95.0}
    )

    assert result["block_number"] > 0
    assert result["credential_hash"] is not None
    assert result["tx_hash"].startswith("0x")

    # 2. Verify legitimate credential
    verif = blockchain_ledger.verify_credential(cred_id, expected_hash=result["credential_hash"])
    assert verif["is_valid"] is True
    assert verif["tamper_detected"] is False

    # 3. Verify tampering detection
    tampered_verif = blockchain_ledger.verify_credential(cred_id, expected_hash="fake_hash_123456789")
    assert tampered_verif["is_valid"] is False
    assert tampered_verif["tamper_detected"] is True

    # 4. Public API endpoint
    pub_res = client.get(f"/api/blockchain/verify/{cred_id}")
    assert pub_res.status_code == 200
    pub_data = pub_res.json()
    assert pub_data["is_valid"] is True
    assert pub_data["verification_status"] == "VERIFIED"
