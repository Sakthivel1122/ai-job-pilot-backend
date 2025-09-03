from fastapi import APIRouter, UploadFile, File, Depends, Request
from app.utils.personal_chat_bot import update_qdrant_with_txt_file, get_vectorstore, ask_question_from_vectorstore
from app.utils.response import response
from app.constants.prompts import personal_chat_bot_system_prompt
import tempfile
import shutil
import os
from app.models.personal_chat_bot import ChatSession, ChatMessage
from beanie import PydanticObjectId
from pydantic import BaseModel
from typing import Optional
from app.dependencies.personal_chat_bot_auth import verify_chat_bot_api_key
from app.services.rate_limiter import limiter
from app.services.cors import CORSEnabledRoute

router = APIRouter(route_class=CORSEnabledRoute)

class QuestionRequest(BaseModel):
    question: str
    session_id: Optional[str] = None

class GetChatMessage(BaseModel):
    session_id: str

@router.post("/update-data", description="Upload and update data to Qdrant")
async def update_qdrant_data(
    file: UploadFile = File(...),
    _: None = Depends(verify_chat_bot_api_key)
):
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name

        # Call your function with the saved file
        update_qdrant_with_txt_file(
            file_path=temp_file_path,
            collection_name="user_sakthivel"
        )

        # Clean up the temp file
        os.remove(temp_file_path)

        return response(None, "Updated Successfully!", 200)
    except Exception as e:
        return response(f'error: {str(e)}', "Failed to Update", 400)

@router.post("/ask", response_model="", description="Ask question to chat bot")
@limiter.limit("5/minute")
async def ask_chat_bot(request: Request, data: QuestionRequest, _: None = Depends(verify_chat_bot_api_key)):
    try:
        # Get vectorstore for current user
        vectorstore = get_vectorstore("user_sakthivel")

        # Session handling
        if data.session_id:
            # Existing session — fetch session & history
            session = await ChatSession.get(data.session_id)
            if not session:
                return response("Invalid session ID", "Session not found", 400)

            messages = (
                await ChatMessage.find(ChatMessage.session.id == session.id)
                .sort("-created_at")       # newest first
                .limit(5)                  # limit to 5 messages
                .to_list()
            )
            messages.reverse()
            history = []
            for msg in messages:
                sender = "Human" if msg.sender == "human" else "AI"
                history.append(f"{sender}: {msg.message}")
        else:
            # New session — create one and set empty history
            session = await ChatSession().insert()
            history = []

        # print('chat_history', history)

        # Get answer from vectorstore and LLM
        answer = ask_question_from_vectorstore(
            vectorstore=vectorstore,
            question=data.question,
            system_prompt=personal_chat_bot_system_prompt,
            chat_history=history
        )

        # Save messages to DB
        await ChatMessage(sender="human", message=data.question, session=session).insert()
        await ChatMessage(sender="bot", message=answer, session=session).insert()
        
        # Return the answer + session ID (important for client)
        return response(
            {
                "session_id": str(session.id),
                "answer": answer
            },
            "Responded Successfully!",
            200
        )

    except Exception as e:
        return response(f'error: {str(e)}', "Failed to respond", 400)

# @router.post("/chat-message", response_model="", description="Get chat messages")
# @router.api_route(
# "/chat-message",
# methods=["POST", "OPTIONS"],
# response_model=None,
# description="Get chat messages",
# )
@router.post("/chat-message", response_model="", description="Get chat messages")
async def get_chat_messages(data: GetChatMessage):
    session = await ChatSession.get(data.session_id)
    if not session:
        return response("Invalid session ID", "Session not found", 400)
    messages = (
        await ChatMessage.find(ChatMessage.session.id == session.id)
            .sort("created_at")
            .to_list()
    )
    messages = [
        {
            'sender': msg.sender,
            'message': msg.message
        }
        for msg in messages
    ]
    return response(messages, "Retrieved successfully!", 200)

"""
If you want good enough protection without login:

✅ Add a secret header (like X-API-KEY) in fetch()

✅ Rate-limit both your Next.js API route and FastAPI route

✅ Add CORS and check origin

✅ Optional: Add CAPTCHA if LLM calls are expensive
"""
