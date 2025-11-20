from beanie import Document, Link, PydanticObjectId
from pydantic import EmailStr, Field, HttpUrl
from typing import Optional, Literal
from .timestamped import TimeStampedDocument
from datetime import datetime

class User(TimeStampedDocument):
    username: str = Field(..., max_length=100)
    email: EmailStr
    password: Optional[str] = None
    role: Literal["user", "admin"] = "user"
    provider: Optional[Literal["google"]] = None
    provider_id: Optional[str] = None

    class Settings:
        name = "users"  # MongoDB collection name

class JobApplication(TimeStampedDocument):
    user: PydanticObjectId
    company: str
    role: str
    location: Optional[str] = None
    application_url: Optional[str] = Field(default=None)
    salary_min: Optional[float] = Field(default=None)
    salary_max: Optional[float] = Field(default=None)
    status: Literal["applied", "interview_scheduled", "interviewing", "selected", "rejected", "offer_received", "withdrawn"] = "applied"
    notes: Optional[str] = Field(default=None)
    job_description: str = Field(default=None)

    class Settings:
        name = "job_applications"

class Resume(TimeStampedDocument):
    user: PydanticObjectId
    job_application: PydanticObjectId
    file_url: Optional[str] = None
    original_text: Optional[str] = None
    ai_summary: Optional[str] = None
    ai_score: Optional[float] = None
    ai_feedback: Optional[str] = None

    class Settings:
        name = "resumes"
