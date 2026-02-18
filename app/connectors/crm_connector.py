import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any
from .base import BaseConnector

class CRMConnector(BaseConnector):

    def __init__(self):
        self.data_path = Path("data/customers.json")

    def get_data(self, params: dict) -> List[Dict[str, Any]]:
        with open(self.data_path) as f:
            customers = json.load(f)

        # Filter by customer_id if provided
        customer_id = params.get("customer_id")
        if customer_id is not None:
            customers = [c for c in customers if c.get("customer_id") == customer_id]

        # Filter by period if provided
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
                customers = [
                    c for c in customers
                    if datetime.fromisoformat(c["last_order_date"]) >= cutoff
                ]

        # Sort by revenue descending and apply top limit
        customers.sort(key=lambda x: x.get("revenue", 0), reverse=True)
        
        top = params.get("top")
        if top is not None:
            customers = customers[:top]

        return customers
