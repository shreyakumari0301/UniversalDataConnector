
from fastapi import APIRouter, Query
from app.connectors.crm_connector import CRMConnector
from app.connectors.support_connector import SupportConnector
from app.connectors.analytics_connector import AnalyticsConnector
from app.services.business_rules import apply_voice_limits, apply_rules
from app.services.voice_optimizer import summarize_if_large
from app.services.data_identifier import identify_data_type
from app.models.common import DataResponse, Metadata
from datetime import datetime
from typing import Optional

router = APIRouter()

@router.get("/data/{source}", response_model=DataResponse)
def get_data(source: str, limit: int = Query(10)):

    connector_map = {
        "crm": CRMConnector(),
        "support": SupportConnector(),
        "analytics": AnalyticsConnector(),
    }

    connector = connector_map.get(source)
    if not connector:
        return {"data": [], "metadata": {"total_results": 0, "returned_results": 0, "data_freshness": "unknown"}}

    raw_data = connector.fetch()
    total = len(raw_data)

    filtered = apply_voice_limits(raw_data)
    optimized = summarize_if_large(filtered)

    data_type = identify_data_type(raw_data)

    metadata = Metadata(
        total_results=total,
        returned_results=len(optimized),
        data_freshness=f"Data as of {datetime.utcnow().isoformat()}",
    )

    return DataResponse(data=optimized, metadata=metadata)


@router.get("/data/crm/customers", response_model=DataResponse)
def get_crm_customers(
    customer_id: Optional[str] = Query(None, description="Filter by customer_id (acme_corp, beta_inc, gamma_ltd)"),
    top: int = Query(10, description="Number of top customers to return"),
    period: str = Query("all", description="Filter by period: week, month, or all")
):
    connector = CRMConnector()
    
    # Get all raw data (no filtering)
    raw_data = connector.get_data({"customer_id": None, "top": None, "period": "all"})
    
    # Apply business rules
    params = {
        "customer_id": customer_id,
        "top": top,
        "period": period
    }
    
    return apply_rules("crm", raw_data, params)
