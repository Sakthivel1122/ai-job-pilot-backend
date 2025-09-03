from fastapi import UploadFile, File, Form, HTTPException
from typing import Optional, Literal
from app.utils.response import response
from app.utils.pdf import extract_text_from_pdf, get_pdf_from_url
from app.utils.ai_engine import AIEngine
from app.constants.prompts import resume_coach_system_prompt
import json
import re

# async def get_ai_suggestion_for_resume(
#     resume: UploadFile = File(...),
#     job_description: str = Form(""),
#     resume_type: Literal["link", "file", "text"] = "link"
# ):
#     if not resume:
#         raise ValueError("No resume file provided")

#     # Read file contents (bytes)

#     # Use your existing PDF extractor
#     if resume_type == "link":
#         resume_bytes = await get_pdf_from_url(resume)
#         resume_text = await extract_text_from_pdf(resume_bytes)
#     elif resume_type == "file":
#         resume_bytes = await resume.read()
#         resume_text = await extract_text_from_pdf(resume_bytes)
#     elif resume_type == "text":
#         resume_text = resume
#     else:
#         raise ValueError("resume type missing")

#     # Use your existing AI engine
#     ai_engine = AIEngine(
#         model="llama3-70b-8192",
#         temperature=0.3,
#         system_prompt=resume_coach_system_prompt
#     )

#     ai_response = ai_engine.suggest_resume_improvements(resume_text, job_description)

#     response_data = {
#         'resume_text': resume_text,
#         'ai_response': ai_response,
#     }

#     return response_data


async def get_ai_suggestion_for_resume(
    resume_text: str,
    job_description: str = Form("")
):
    # if not resume:
    #     return response(None, "No resume file provided", 400)

    # Read file contents (bytes)
    # resume_bytes = await resume.read()

    # Use your existing PDF extractor
    # resume_text = await extract_text_from_pdf(resume_bytes)
    # print('resume_text', resume_text)

    # Use your existing AI engine
    ai_engine = AIEngine(
        model="llama3-70b-8192",
        temperature=0.1,
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
