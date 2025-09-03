from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.config import settings
from app.models.user import User, JobApplication, Resume   # Import your models here
from app.models.personal_chat_bot import ChatSession, ChatMessage
async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.MONGODB_DB_NAME]
    await init_beanie(database=db, document_models=[User, JobApplication, Resume, ChatSession, ChatMessage])
    