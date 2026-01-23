from fastapi import APIRouter, Depends, Query
from app.dependencies.auth import get_current_user, role_required
from app.services.job_application import get_job_application_details
from typing import List, Optional
from app.services.job_application import get_all_job_application
from app.schemas.user import JobApplicationResponse, JobApplicationResponse, BaseResponse

router = APIRouter(prefix="/api/v1")

@router.get("/get-job-application-details")
async def get_job_application_details_api(
    id: str,
    current_user: dict = Depends(role_required("admin", "user"))
):
    result = await get_job_application_details(id=id, current_user=current_user)
    return result

@router.get("/get-job-applications", response_model=BaseResponse[List[JobApplicationResponse]])
async def get_job_application(
    current_user: dict = Depends(role_required("user")),
    status: Optional[str] = "all",
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search_text: Optional[str] = None,
):
    result = await get_all_job_application(
        user=current_user,
        page=page,
        limit=limit,
        application_status=status,
        search_text=search_text
    )
    return result
