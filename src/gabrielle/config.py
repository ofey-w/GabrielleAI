from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Application
    app_name: str = "gabrielle"
    debug: bool = False

    # LLM — all required, no defaults (set in .env)
    llm_provider: str  # e.g. "openai" or "anthropic"
    llm_model: str     # e.g. "gpt-4o" or "claude-3-5-sonnet-20241022"
    llm_api_key: SecretStr

    # Search
    tavily_api_key: SecretStr
