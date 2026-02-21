"""Support ticket data models."""
from pydantic import BaseModel


class SupportTicket(BaseModel):
    """Single support ticket record."""
    id: int
    customer_id: str
    title: str
    status: str  # open | closed
    created_at: str
    priority: str  # high | low
