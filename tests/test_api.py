"""API endpoint tests (health, data, OpenAPI)."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_returns_200():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "healthy"


def test_root_returns_html():
    r = client.get("/")
    assert r.status_code == 200
    assert "Universal Data Connector" in r.text
    assert "html" in r.headers.get("content-type", "").lower()


def test_openapi_schema_available():
    r = client.get("/openapi.json")
    assert r.status_code == 200
    schema = r.json()
    assert "openapi" in schema
    assert "paths" in schema


def test_data_crm_customers_returns_structured_response():
    r = client.get("/data/crm/customers?top=2")
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert "metadata" in data
    assert "total_results" in data["metadata"]
    assert "returned_results" in data["metadata"]
    assert "data_freshness" in data["metadata"]


def test_data_support_tickets_returns_structured_response():
    r = client.get("/data/support/tickets?limit=2")
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert "metadata" in data


def test_data_analytics_metrics_returns_structured_response():
    r = client.get("/data/analytics/metrics?limit=5")
    assert r.status_code == 200
    data = r.json()
    assert "data" in data
    assert "metadata" in data


def test_llm_tools_returns_openai_format():
    r = client.get("/llm/tools?format=openai")
    assert r.status_code == 200
    data = r.json()
    assert "tools" in data
    assert len(data["tools"]) >= 1
