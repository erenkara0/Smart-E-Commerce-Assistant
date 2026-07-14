from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[3]
ENV_FILE_PATH = ROOT_DIR / ".env"


class Settings(BaseSettings):
    environment: str = "development"

    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

    retrieval_top_k: int = 4
    rag_max_context_chars: int = 4000
    vector_store_provider: str = "in_memory"

    session_db_path: str = "backend/app/data/sessions.db"

    langsmith_tracing: bool = False
    langsmith_api_key: str | None = None
    langsmith_project: str = "smart-e-commerce-assistant"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()