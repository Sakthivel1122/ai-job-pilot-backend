from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user, role_required
from app.services.job_application import get_job_application_details

router = APIRouter(prefix="/api/v1")

@router.get("/get-job-application-details")
async def get_job_application_details_api(
    id: str,
    current_user: dict = Depends(role_required("admin", "user"))
):
    result = await get_job_application_details(id=id, current_user=current_user)
    return result
