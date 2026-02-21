"""Tests for business rules engine."""
import pytest
from app.services.business_rules import apply_rules, apply_voice_limits
from app.models.common import DataResponse, Metadata


def test_apply_rules_crm_limit_and_metadata():
    raw = [
        {"customer_id": "acme_corp", "revenue": 100, "last_order_date": "2026-02-01T00:00:00"},
        {"customer_id": "acme_corp", "revenue": 200, "last_order_date": "2026-02-02T00:00:00"},
        {"customer_id": "beta_inc", "revenue": 150, "last_order_date": "2026-02-03T00:00:00"},
    ]
    result = apply_rules("crm", raw, {"customer_id": "acme_corp", "top": 1, "period": "all"})
    assert isinstance(result, DataResponse)
    assert result.metadata.total_results == 3
    assert result.metadata.returned_results <= 1
    assert result.metadata.data_freshness == "2 hours ago"
    assert all(c["customer_id"] == "acme_corp" for c in result.data)


def test_apply_rules_support_sort_and_limit():
    raw = [
        {"id": 1, "customer_id": "acme", "created_at": "2026-01-01T00:00:00", "title": "A", "status": "open", "priority": "high"},
        {"id": 2, "customer_id": "acme", "created_at": "2026-02-01T00:00:00", "title": "B", "status": "open", "priority": "low"},
    ]
    result = apply_rules("support", raw, {"limit": 1})
    assert isinstance(result, DataResponse)
    assert result.metadata.returned_results <= 1
    assert result.metadata.data_freshness == "2 hours ago"


def test_apply_rules_analytics_time_series_metadata():
    raw = [
        {"timestamp": "2026-02-01T00:00:00", "customer_id": "acme", "metric": "revenue", "value": 100.0},
    ] * 10
    result = apply_rules("analytics", raw, {"limit": 5})
    assert isinstance(result, DataResponse)
    assert result.metadata.data_type == "time-series"


def test_apply_voice_limits_respects_max():
    from app.config import settings
    data = [{"x": i} for i in range(20)]
    limited = apply_voice_limits(data)
    assert len(limited) <= settings.MAX_RESULTS
