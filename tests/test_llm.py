import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_llm_tools_openai():
    """LLM tools endpoint returns OpenAI-format tool definitions."""
    r = client.get("/llm/tools?format=openai")
    assert r.status_code == 200
    data = r.json()
    assert "tools" in data
    tools = data["tools"]
    assert len(tools) == 3
    names = {t["function"]["name"] for t in tools}
    assert names == {"get_crm_customers", "get_support_tickets", "get_analytics_metrics"}
    assert "parameters" in tools[0]["function"]


def test_llm_tools_anthropic():
    """LLM tools endpoint returns Anthropic-format tool definitions."""
    r = client.get("/llm/tools?format=anthropic")
    assert r.status_code == 200
    data = r.json()
    assert "tools" in data
    tools = data["tools"]
    assert len(tools) == 3
    names = {t["name"] for t in tools}
    assert names == {"get_crm_customers", "get_support_tickets", "get_analytics_metrics"}
    assert "input_schema" in tools[0]


def test_llm_tools_endpoints():
    """Tool-to-endpoint mapping is returned."""
    r = client.get("/llm/tools/endpoints")
    assert r.status_code == 200
    data = r.json()
    assert "tool_endpoints" in data
    eps = data["tool_endpoints"]
    assert eps["get_crm_customers"]["path"] == "/data/crm/customers"
    assert eps["get_crm_customers"]["method"] == "GET"
