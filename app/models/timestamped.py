from beanie import Document, before_event, Insert, Update, Replace
from datetime import datetime, timezone
from typing import Optional
from pydantic import Field

def utc_now():
    return datetime.now(timezone.utc)

class TimeStampedDocument(Document):
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    deleted_at: Optional[datetime] = None

    @before_event(Insert)
    def set_created_at(self):
        now = utc_now()
        self.created_at = now
        self.updated_at = now

    @before_event([Update, Replace])
    def set_updated_at(self):
        self.updated_at = utc_now()

    class Config:
        from_attributes = True  # For Pydantic v2
