"""Analytics/metrics data models."""
from pydantic import BaseModel
from typing import Union


class MetricRecord(BaseModel):
    """Single analytics metric record (time-series point)."""
    timestamp: str
    customer_id: str
    metric: str  # revenue | orders
    value: Union[float, int]
