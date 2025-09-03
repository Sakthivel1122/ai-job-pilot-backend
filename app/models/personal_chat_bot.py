from app.models.timestamped import TimeStampedDocument
from beanie import Link
from typing import Literal

class ChatSession(TimeStampedDocument):
    class Settings:
        name = "chat_sessions"  # MongoDB collection name

class ChatMessage(TimeStampedDocument):
    session: Link[ChatSession]
    sender: Literal["human", "bot"]
    message: str

    class Settings:
        name = "chat_messages"  # MongoDB collection name
