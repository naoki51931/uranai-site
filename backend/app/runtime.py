from app.config import get_settings
from app.services.weaviate_store import WeaviateStore


weaviate_store = WeaviateStore(get_settings().weaviate_url)
