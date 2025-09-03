from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form, Query
from app.models.user import User
from typing import List, Optional
from app.utils.response import response
from app.utils.hash import encrypt_password
from app.utils.jwt import generate_tokens
from app.schemas.user import SignupRequest
from app.dependencies.auth import get_current_user, role_required
from app.services.auth import create_user
from app.schemas.user import JobApplicationRequest, JobApplicationResponse, JobApplicationResponse, DashboardResponse, BaseResponse
from app.services.job_application import create_update_job_application, get_all_job_application, get_dashboard_data
from app.services.resume import get_suggestion_for_resume

router = APIRouter()

@router.get("/", response_model=List[User], description="HII")
async def list_all_users(current_user: dict = Depends(role_required("admin", "user"))):
    print(current_user)
    users = await User.find_all().to_list()
    return users

@router.post("/api/v1/job-application")
async def create_update_job_application(
    data:JobApplicationRequest,
    current_user: dict = Depends(role_required("user"))
):
    result = await create_update_job_application(data, current_user)
    return result

@router.get("/api/v1/job-application", response_model=BaseResponse[List[JobApplicationResponse]])
async def get_job_application(
    current_user: dict = Depends(role_required("user")),
    status: Optional[str] = Query(None, description="Filter by job status"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    job_application_id: str = Query(default=None),
):
    result = await get_all_job_application(current_user, status, page, limit)
    return result

@router.post("/api/v1/upload-resume")
async def upload_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(""),
    job_application_id: str = Form(""),
    # file_type: str = Form(""),
    current_user: dict = Depends(role_required("user"))
):
    result = await get_suggestion_for_resume(
        resume, 
        job_description, 
        current_user, 
        job_application_id, 
    )
    return result

@router.get("/api/v1/dashboard", response_model = BaseResponse[DashboardResponse])
async def dashboard_data(current_user: dict = Depends(role_required("user"))):
    result = await get_dashboard_data(current_user)
    return result
