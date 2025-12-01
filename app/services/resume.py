from fastapi import UploadFile, File, Form
from app.utils.resume import get_ai_suggestion_for_resume
from app.utils.response import response
from app.utils.pdf import extract_text_from_pdf
from fastapi.encoders import jsonable_encoder
from app.models.user import User, Resume, JobApplication
from bson import ObjectId
from typing import Optional
from beanie import PydanticObjectId

async def get_suggestion_for_resume(
    resume: UploadFile = File(...),
    job_description: Optional[str] = Form(""),
    current_user: User = None,
    job_application_id: str = "",
    resume_name: str = Form("")
    # file_type: str = ""
):
    try:
        job_application = await JobApplication.find_one(
            JobApplication.id == ObjectId(job_application_id),
            JobApplication.deleted_at == None
        )

        if not job_application:
            return response(None, "Job Application Not Found", 400)
        
        resume_bytes = await resume.read()

        # Use your existing PDF extractor
        resume_text = await extract_text_from_pdf(resume_bytes)

        if job_description != "":
            job_description_text = job_description
        else:
            # print('getting job_description from db', job_application.job_description)
            job_description_text = job_application.job_description
            
        # print('job_description_text', job_description_text)

        result = await get_ai_suggestion_for_resume(resume_text, job_description_text)

        resume = Resume(
            user=current_user.id,
            name=resume_name,
            job_application=job_application.id,
            original_text=resume_text,
            ai_summary=result.get("summary"),
            ai_score=result.get("score"),
            ai_feedback=result.get("feedback"),
            # file_url=resume if file_type == "link" else None
        )
        await resume.insert()
        
        return response(result, "Resume Uploaded Successfully!", 200)
    except Exception as e:
        return response({'error': str(e)}, "API Failed", 400)

async def get_job_application_resumes(job_application_id: str, ):
    resumes = await Resume.find(
        Resume.job_application == PydanticObjectId(job_application_id)
    ).sort("-created_at").limit(5).to_list()
    return resumes
