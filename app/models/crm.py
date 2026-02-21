"""CRM data models."""
from pydantic import BaseModel
from typing import Optional


class CustomerRecord(BaseModel):
    """Single CRM customer record."""
    id: int
    name: str
    customer_id: str
    revenue: float
    orders: int
    last_order_date: str
