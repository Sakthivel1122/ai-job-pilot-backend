from fastapi import FastAPI, HTTPException, Request
from app.routers import user, auth, ai_engine, personal_chat_bot, job_application, resume
from app.config import settings
from app.db.init import init_db
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.services.rate_limiter import limiter
from app.utils.response import response
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # Connect to MongoDB + init Beanie
    yield

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# Setup Limiter
app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://sakthivel-profile.vercel.app",
        "https://ai-job-pilot.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# limiter custom error handler
@app.exception_handler(RateLimitExceeded)
async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return response(None, "Too many requests, Please trying again after 1 minute", 429)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail if isinstance(exc.detail, dict) else {
            "content": {},
            "response": {
                "message": str(exc.detail),
                "status": exc.status_code
            }
        }
    )

# Include routers
app.include_router(user.router, prefix="/user", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(ai_engine.router, prefix="/ai-engine", tags=["AI Engine"])
app.include_router(personal_chat_bot.router, prefix="/personal-chat-bot", tags=["Personal Chat Bot"])
app.include_router(job_application.router, prefix="/job-application", tags=["Job Application APIs"])
app.include_router(resume.router, prefix="/resume", tags=["Resume APIs"])
