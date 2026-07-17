from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[3]
ENV_FILE_PATH = ROOT_DIR / ".env"


class Settings(BaseSettings):
    environment: str = Field(
        default="development",
        validation_alias="APP_ENV",
    )

    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    openai_timeout_seconds: float = 30.0
    openai_max_retries: int = 2

    retrieval_top_k: int = 2
    rag_max_context_chars: int = 4000
    vector_store_provider: str = "in_memory"

    sqlite_db_path: str = "./backend/storage/app.db"
    session_memory_limit: int = 5

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