
from typing import List, Dict, Any
from datetime import datetime, timedelta
from app.config import settings
from app.models.common import DataResponse, Metadata

def apply_voice_limits(data: List[Dict]) -> List[Dict]:
    return data[:settings.MAX_RESULTS]


def apply_rules(data_type: str, raw_data: List[dict], params: dict) -> DataResponse:
    """
    Apply business rules based on data type.
    
    Args:
        data_type: Type of data ("crm", "support", etc.)
        raw_data: Raw list of dictionaries from connector
        params: Query parameters dict
    
    Returns:
        DataResponse with filtered data and metadata
    """
    if data_type == "crm":
        return _apply_crm_rules(raw_data, params)
    else:
        # Default: return all data with metadata
        return DataResponse(
            data=raw_data,
            metadata=Metadata(
                total_results=len(raw_data),
                returned_results=len(raw_data),
                data_freshness="unknown"
            )
        )


def _apply_crm_rules(raw_data: List[dict], params: dict) -> DataResponse:
    """Apply CRM-specific business rules."""
    total_results = len(raw_data)
    filtered_data = raw_data.copy()
    
    # Filter by customer_id if provided
    customer_id = params.get("customer_id")
    if customer_id:
        filtered_data = [c for c in filtered_data if c.get("customer_id") == customer_id]
    
    # Filter by period
    period = params.get("period", "all")
    if period != "all":
        now = datetime.now()
        if period == "week":
            cutoff = now - timedelta(days=7)
        elif period == "month":
            cutoff = now - timedelta(days=30)
        else:
            cutoff = None
        
        if cutoff:
            filtered_data = [
                c for c in filtered_data
                if datetime.fromisoformat(c["last_order_date"]) >= cutoff
            ]
    
    # Sort by revenue DESC (for top customers)
    filtered_data.sort(key=lambda x: x.get("revenue", 0), reverse=True)
    
    # Limit: min(params.top or 10, 10) - max 10
    top = params.get("top", 10)
    limit = min(top, 10)
    filtered_data = filtered_data[:limit]
    
    # Metadata with data freshness
    return DataResponse(
        data=filtered_data,
        metadata=Metadata(
            total_results=total_results,
            returned_results=len(filtered_data),
            data_freshness="2 hours ago"
        )
    )
