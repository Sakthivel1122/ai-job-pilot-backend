from beanie import Document
from pydantic import Field
from typing import Optional, Literal
from datetime import datetime
from pymongo import IndexModel
from app.models.timestamped import utc_now


class AuthLog(Document):
    user_id: Optional[str] = None  # None for failed login / signup attempts
    event: Literal["login", "signup"]
    success: bool
    ip: Optional[str] = None
    user_agent: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=utc_now)

    class Settings:
        name = "auth_logs"
        indexes = [
            IndexModel([("user_id", 1)]),
            IndexModel([("created_at", -1)]),

            # TTL index: auto-delete logs after 90 days
            IndexModel(
                [("created_at", 1)],
                expireAfterSeconds=60 * 60 * 24 * 90
            ),

            # Compound index for queries like: event + recent logs
            IndexModel([("event", 1), ("created_at", -1)])
        ]