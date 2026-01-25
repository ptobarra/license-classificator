from app.core.config import settings
from app.llm.base import LLMClient
from app.llm.ollama_client import OllamaClient
from app.llm.openai_client import OpenAIClient


def get_llm_client() -> LLMClient:
    if settings.llm_provider.lower() == "openai":
        return OpenAIClient()
    return OllamaClient()
