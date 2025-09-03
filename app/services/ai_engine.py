from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models.user import User
from typing import List
from app.services.auth import SignupRequest, create_user
from app.dependencies.auth import role_required
from typing import Optional
from app.utils.response import response
from app.utils.pdf import extract_text_from_pdf
from app.utils.ai_engine import AIEngine
from app.constants.prompts import resume_coach_system_prompt
import json
import re

async def get_ai_suggestion_for_resume(
    resume: UploadFile = File(...),
    job_description: Optional[str] = Form("")
):
    if not resume:
        return response(None, "No resume file provided", 400)

    # Read file contents (bytes)
    resume_bytes = await resume.read()

    # Use your existing PDF extractor
    resume_text = await extract_text_from_pdf(resume_bytes)
    # print('resume_text', resume_text)

    # Use your existing AI engine
    ai_engine = AIEngine(
        model="llama3-70b-8192",
        temperature=0.3,
        system_prompt=resume_coach_system_prompt
    )

    raw_response = ai_engine.suggest_resume_improvements(resume_text, job_description)

    try:
        cleaned = raw_response.strip()

        # Extract JSON block using regex
        match = re.search(r'{.*}', cleaned, re.DOTALL)
        if not match:
            raise ValueError("No valid JSON object found in response.")

        json_str = match.group()

        # Parse the extracted JSON
        parsed = json.loads(json_str)

        ai_summary = parsed.get("ai_summary")
        ai_score = parsed.get("ai_score")
        ai_feedback = parsed.get("ai_feedback")

        return {
            "summary": ai_summary,
            "score": ai_score,
            "feedback": ai_feedback
        }

    except (json.JSONDecodeError, ValueError) as e:
        raise HTTPException(status_code=500, detail=f"AI response could not be parsed as JSON: {e}")
