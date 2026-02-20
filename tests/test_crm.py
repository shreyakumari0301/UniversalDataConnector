import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_crm_customers_happy_path():
    """Happy path: request top customers returns data with metadata and max 10."""
    r = client.get("/data/crm/customers?top=3")
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert "metadata" in data
    meta = data["metadata"]
    assert meta["total_results"] >= 0
    assert meta["returned_results"] <= 10
    assert meta["data_freshness"] == "2 hours ago"
    assert len(data["data"]) <= 3


def test_crm_customers_limit_enforced():
    """Edge: top=100 is capped to 10 by business rules."""
    r = client.get("/data/crm/customers?top=100")
    assert r.status_code == 200
    data = r.json()
    assert len(data["data"]) <= 10
    assert data["metadata"]["returned_results"] <= 10


def test_crm_customers_filter_no_match():
    """Edge: filter by customer_id that may have no data returns valid response."""
    r = client.get("/data/crm/customers?customer_id=nonexistent_customer_xyz")
    assert r.status_code == 200
    data = r.json()
    assert data["metadata"]["returned_results"] == 0
    assert data["data"] == []
