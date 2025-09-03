from qdrant_client import QdrantClient
from app.config import settings

qdrant_client = QdrantClient(
    host=settings.QDRANT_DB_URL,
    port=settings.QDRANT_DB_PORT,
)