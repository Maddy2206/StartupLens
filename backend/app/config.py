from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # LLM — Alibaba Cloud DashScope (Qwen)
    dashscope_api_key: str = ""
    llm_model: str = "qwen-plus"

    # Research APIs
    tavily_api_key: str = ""
    firecrawl_api_key: str = ""
    reddit_client_id: str = ""
    reddit_client_secret: str = ""
    reddit_user_agent: str = "startup-validator/1.0"

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/startup_validator"

    # API
    cors_origins: str = "http://localhost:3000"
    enable_vector_store: bool = False

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    return Settings()
