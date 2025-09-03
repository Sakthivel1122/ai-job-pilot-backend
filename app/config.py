from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI AI Job Pilot"
    JWT_SIGNATURE_KEY: str
    CHAT_BOT_API_KEY: str
    GROQ_API_KEY: str
    MONGODB_DB_NAME: str
    MONGODB_URL: str
    QDRANT_DB_URL: str
    QDRANT_DB_PORT: int

    class Config:
        env_file = ".env"

settings = Settings()
