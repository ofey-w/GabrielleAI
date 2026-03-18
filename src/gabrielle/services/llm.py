from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from gabrielle.config import Settings


def get_llm(settings: Settings) -> BaseChatModel:
    if settings.llm_provider == "openai":
        return ChatOpenAI(model=settings.llm_model, api_key=settings.llm_api_key)  
    if settings.llm_provider == "anthropic":
        return ChatAnthropic(model=settings.llm_model, api_key=settings.llm_api_key)  # type: ignore[call-arg]
    raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
