from fastapi import APIRouter, Depends, Query
from app.models.user import User
from typing import List
from app.dependencies.auth import role_required
from app.services.admin import admin_dashboard_api_service, admin_get_users_api_service, admin_get_job_application_list_api_service, admin_get_resume_list_api_service, admin_get_job_application_details_api_service
from typing import Optional

router = APIRouter()

@router.get("/dashboard", response_model=List[User], description="HII")
async def admin_dashboard_api(current_user: dict = Depends(role_required("admin"))):
    response = await admin_dashboard_api_service()
    return response

@router.get("/get-users", response_model=List[User], description="HII")
async def admin_get_users_api(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search_text: Optional[str] = None,
    current_user: dict = Depends(role_required("admin"))
):
    response = await admin_get_users_api_service(page=page, limit=limit, search_text=search_text)
    return response

@router.get("/get-job-application-list", response_model=List[User], description="HII")
async def admin_get_job_application_list_api(
    user_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(role_required("admin"))
):
    response = await admin_get_job_application_list_api_service(user_id=user_id, page=page, limit=limit)
    return response

@router.get("/get-resume-list", response_model=List[User], description="HII")
async def admin_get_resume_list_api(
    user_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(role_required("admin"))
):
    response = await admin_get_resume_list_api_service(user_id=user_id, page=page, limit=limit)
    return response

@router.get("/get-job-application-details", response_model=List[User], description="HII")
async def admin_get_resume_list_api(
    user_id: str,
    job_application_id: str,
    current_user: dict = Depends(role_required("admin"))
):
    response = await admin_get_job_application_details_api_service(user_id=user_id, job_application_id=job_application_id)
    return response
