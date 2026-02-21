"""Tests for CRM, Support, and Analytics connectors."""
import pytest
from app.connectors.crm_connector import CRMConnector
from app.connectors.support_connector import SupportConnector
from app.connectors.analytics_connector import AnalyticsConnector


def test_crm_connector_returns_list():
    connector = CRMConnector()
    data = connector.get_data({"customer_id": None, "top": None, "period": "all"})
    assert isinstance(data, list)
    if data:
        assert "customer_id" in data[0] and "revenue" in data[0]


def test_crm_connector_filters_by_customer_id():
    connector = CRMConnector()
    data = connector.get_data({"customer_id": "acme_corp", "top": 5, "period": "all"})
    assert all(c.get("customer_id") == "acme_corp" for c in data)


def test_support_connector_returns_list():
    connector = SupportConnector()
    data = connector.get_data({"customer_id": None, "status": None, "priority": None})
    assert isinstance(data, list)
    if data:
        assert "customer_id" in data[0] and "status" in data[0]


def test_support_connector_filters_by_status():
    connector = SupportConnector()
    data = connector.get_data({"customer_id": None, "status": "open", "priority": None})
    assert all(t.get("status") == "open" for t in data)


def test_analytics_connector_returns_list():
    connector = AnalyticsConnector()
    data = connector.get_data({"customer_id": None, "from": None, "to": None, "limit": 50})
    assert isinstance(data, list)
    if data:
        row = data[0]
        assert ("timestamp" in row or "date" in row) and "value" in row
