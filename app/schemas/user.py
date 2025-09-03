from pydantic import BaseModel, EmailStr, Field
from beanie import Document, Link, PydanticObjectId
from pydantic import EmailStr, Field, HttpUrl
from typing import Optional, Literal, List, Any, TypeVar, Generic
from datetime import datetime

class Response(BaseModel):
    status: int
    message: str

T = TypeVar("T")

class BaseResponse(BaseModel, Generic[T]):
    content: T
    response: Response

class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class JobApplicationRequest(BaseModel):
    id: Optional[str] = None
    company: str
    role: str
    location: str
    application_url: Optional[str] = Field(default=None)
    salary_min: Optional[float] = Field(default=None)
    salary_max: Optional[float] = Field(default=None)
    status: str
    notes: Optional[str] = Field(default=None)
    job_description: str

class JobApplicationResponse(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")
    company: str
    role: str
    location: str
    application_url: Optional[str] = None
    salary_min: float
    salary_max: float
    status: str
    notes: Optional[str] = None
    job_description: str

    class Config:
        from_attributes = True
        validate_by_name = True
        populate_by_name = True

class DashboardResponse(BaseModel):
    total_application_count: int
    applied_count: int
    interview_count: int
    offer_count: int
