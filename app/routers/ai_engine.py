from fastapi import APIRouter, UploadFile, File, Form
from app.models.user import User
from typing import List
from app.services.auth import SignupRequest, create_user
from app.dependencies.auth import role_required
from typing import Optional
from app.utils.response import response
from app.utils.pdf import extract_text_from_pdf
from app.utils.ai_engine import AIEngine
from app.constants.prompts import resume_coach_system_prompt
# from app.services.ai_engine import get_ai_suggestion_for_resume
from app.utils.resume import get_ai_suggestion_for_resume

router = APIRouter()

@router.post("/api/v1/resume-coach")
async def resume_coach(
    resume: UploadFile = File(...),
    job_description: Optional[str] = Form("")
):
    resume_bytes = await resume.read()

    # Use your existing PDF extractor
    resume_text = await extract_text_from_pdf(resume_bytes)

    result = await get_ai_suggestion_for_resume(resume_text, job_description)
    return response(result, "Retrieved Successfully!!", 200)
