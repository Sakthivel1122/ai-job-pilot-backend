from beanie import Document, before_event, Insert, Update, Replace
from datetime import datetime
from typing import Optional
from pydantic import Field

class TimeStampedDocument(Document):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = None

    @before_event(Insert)
    def set_created_at(self):
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    @before_event([Update, Replace])
    def set_updated_at(self):
        self.updated_at = datetime.utcnow()

    class Config:
        from_attributes = True  # For Pydantic v2
