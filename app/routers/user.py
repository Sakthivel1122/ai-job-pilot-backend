from fastapi import APIRouter, Depends
from app.models.user import User
from typing import List
from app.dependencies.auth import role_required
from app.schemas.user import JobApplicationRequest, DashboardResponse, BaseResponse
from app.services.job_application import create_update_job_application, get_all_job_application, get_dashboard_data, delete_job_application

router = APIRouter()

@router.get("/", response_model=List[User], description="HII")
async def list_all_users(current_user: dict = Depends(role_required("admin", "user"))):
    print(current_user)
    users = await User.find_all().to_list()
    return users

@router.post("/api/v1/job-application")
async def create_update_job_application_api(
    data:JobApplicationRequest,
    current_user: dict = Depends(role_required("user"))
):
    result = await create_update_job_application(data, current_user)
    return result

@router.delete("/api/v1/job-application")
async def delete_job_application_api(
    id: str,
    current_user: dict = Depends(role_required("user"))
):
    result = await delete_job_application(id, current_user)
    return result


@router.get("/api/v1/dashboard", response_model = BaseResponse[DashboardResponse])
async def dashboard_data(current_user: dict = Depends(role_required("user"))):
    result = await get_dashboard_data(current_user)
    return result

