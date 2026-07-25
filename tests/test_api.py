from fastapi.testclient import TestClient

from cyhelm.main import app

client = TestClient(app)


def test_policy_is_always_draft_and_contextual():
    response = client.post("/v1/policies/information-security", json={
        "name": "Example Trading", "industry": "Retail", "employees": 80,
        "cloud_services": ["Microsoft 365"], "handles_payment_cards": True
    })
    assert response.status_code == 200
    policy = response.json()
    assert policy["review_required"] is True
    assert "PCI DSS" in policy["sections"]["policy"]
    assert "Microsoft 365" in policy["sections"]["policy"]


def test_rejects_impossible_headcount():
    response = client.post("/v1/policies/information-security", json={
        "name": "Example", "industry": "Retail", "employees": 0
    })
    assert response.status_code == 422
