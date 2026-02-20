import json
from pathlib import Path
from typing import List, Dict, Any
from .base import BaseConnector


class SupportConnector(BaseConnector):
    def __init__(self):
        self.data_path = Path("data/support_tickets.json")

    def get_data(self, params: dict) -> List[Dict[str, Any]]:
        with open(self.data_path) as f:
            tickets = json.load(f)
        customer_id = params.get("customer_id")
        if customer_id is not None:
            tickets = [t for t in tickets if t.get("customer_id") == customer_id]
        status = params.get("status")
        if status is not None:
            tickets = [t for t in tickets if t.get("status") == status]
        priority = params.get("priority")
        if priority is not None:
            tickets = [t for t in tickets if t.get("priority") == priority]
        return tickets

    def fetch(self, **kwargs):
        with open(self.data_path) as f:
            return json.load(f)
