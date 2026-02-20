import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from .base import BaseConnector


class AnalyticsConnector(BaseConnector):
    def __init__(self):
        self.data_path = Path("data/analytics.json")

    def get_data(self, params: dict) -> List[Dict[str, Any]]:
        with open(self.data_path) as f:
            rows = json.load(f)
        customer_id = params.get("customer_id")
        if customer_id is not None:
            rows = [r for r in rows if r.get("customer_id") == customer_id]
        from_date = params.get("from")
        to_date = params.get("to")
        if from_date or to_date:
            def in_range(r):
                ts = r.get("timestamp") or r.get("date") or ""
                if not ts:
                    return False
                try:
                    t = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                except Exception:
                    t = datetime.min
                if from_date:
                    try:
                        fd = datetime.fromisoformat(from_date.replace("Z", "+00:00"))
                        if t < fd:
                            return False
                    except Exception:
                        pass
                if to_date:
                    try:
                        td = datetime.fromisoformat(to_date.replace("Z", "+00:00"))
                        if t > td:
                            return False
                    except Exception:
                        pass
                return True
            rows = [r for r in rows if in_range(r)]
        # Last N points (time-series order: newest first)
        rows.sort(key=lambda r: r.get("timestamp") or r.get("date") or "", reverse=True)
        limit = params.get("limit", 200)
        return rows[:limit]

    def fetch(self, **kwargs):
        with open(self.data_path) as f:
            return json.load(f)
