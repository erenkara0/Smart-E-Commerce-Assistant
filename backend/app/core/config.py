from functools import lru_cache
from pathlib import Path
from typing import Self

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[3]
ENV_FILE_PATH = ROOT_DIR / ".env"


class Settings(BaseSettings):
    environment: str = Field(
        default="development",
        validation_alias="APP_ENV",
    )
    cors_allowed_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        validation_alias="CORS_ALLOWED_ORIGINS",
    )
    cors_allow_credentials: bool = Field(
        default=False,
        validation_alias="CORS_ALLOW_CREDENTIALS",
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
    langsmith_endpoint: str = "https://api.smith.langchain.com"

    @model_validator(mode="after")
    def validate_cors_settings(self) -> Self:
        normalized_origins = [
            origin.strip().rstrip("/")
            for origin in self.cors_allowed_origins
            if origin.strip()
        ]

        self.cors_allowed_origins = list(
            dict.fromkeys(normalized_origins)
        )

        if not self.cors_allowed_origins:
            raise ValueError(
                "CORS_ALLOWED_ORIGINS must contain at least one origin."
            )

        if (
            self.environment.strip().lower() == "production"
            and "*" in self.cors_allowed_origins
        ):
            raise ValueError(
                "Wildcard CORS origin is not allowed in production."
            )

        return self

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )
    


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()