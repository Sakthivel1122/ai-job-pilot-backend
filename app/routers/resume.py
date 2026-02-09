from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form, Query
from app.dependencies.auth import get_current_user, role_required
from typing import Optional
from app.services.resume import get_suggestion_for_resume, get_job_application_resumes, resume_analyzer_get_suggestion
from app.utils.response import response
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/api/v1")

@router.post("/upload-resume")
async def upload_resume(
    resume: Optional[UploadFile] = File(None),
    job_description: Optional[str] = Form(""),
    job_application_id: str = Form(""),
    resume_name: str= Form(""),
    resume_content_type: str= Form(""),
    resume_text_content: Optional[str]= Form(""),
    current_user: dict = Depends(role_required("user")),
):
    
    result = await get_suggestion_for_resume(
        resume, 
        job_description, 
        current_user, 
        job_application_id, 
        resume_name,
        resume_content_type,
        resume_text_content
    )
    return result

@router.post("/get-resume-analysis")
async def get_resume_analysis(
    resume: Optional[UploadFile] = File(None),
    job_description: Optional[str] = Form(""),
    job_application_id: str = Form(""),
    resume_content_type: str= Form(""),
    resume_text_content: Optional[str]= Form(""),
    current_user: dict = Depends(role_required("user")),
):
    
    result = await resume_analyzer_get_suggestion(
        resume=resume,
        job_description=job_description,
        job_application_id=job_application_id,
        resume_content_type=resume_content_type,
        resume_text_content=resume_text_content,
    )
    return result

@router.get("/get-resume-list")
async def upload_resume(
    job_application_id: str,
):  
    try:
        result = await get_job_application_resumes(job_application_id)
        return response(jsonable_encoder(result), "Resume Retrieved Successfully!", 200)
    except Exception as e:
        return response(None, f"Failed to retrive resumes {str(e)}", 400)
