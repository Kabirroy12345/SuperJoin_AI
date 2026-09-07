import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "endpoints" in data
    assert "Welcome" in data["message"]

def test_get_documents():
    response = client.get("/api/documents")
    assert response.status_code == 200
    docs = response.json()
    assert isinstance(docs, list)
    assert len(docs) >= 1

def test_get_facts():
    response = client.get("/api/facts")
    assert response.status_code == 200
    facts = response.json()
    assert isinstance(facts, list)
    assert len(facts) >= 1

    # Test single fact retrieval
    fact_id = facts[0]["id"]
    single_res = client.get(f"/api/facts/{fact_id}")
    assert single_res.status_code == 200
    assert single_res.json()["id"] == fact_id

def test_get_relationships():
    response = client.get("/api/relationships")
    assert response.status_code == 200
    rels = response.json()
    assert isinstance(rels, list)
    assert len(rels) >= 1

    # Test relationship type filter
    filtered_res = client.get("/api/relationships?type=corroboration")
    assert filtered_res.status_code == 200

def test_get_cases():
    response = client.get("/api/cases")
    assert response.status_code == 200
    cases = response.json()
    assert isinstance(cases, list)
    assert len(cases) >= 1
    # Check that case 1 or 4 exists
    case_numbers = [c.get("case_number") for c in cases]
    assert 1 in case_numbers or 3 in case_numbers or 4 in case_numbers

def test_get_export():
    response = client.get("/api/export")
    assert response.status_code == 200
    export_data = response.json()
    assert "summary" in export_data
    assert "facts" in export_data
    assert "relationships" in export_data
    assert export_data["summary"]["total_documents"] >= 1
