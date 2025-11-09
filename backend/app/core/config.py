from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    env: str = Field("dev", env="ENV")
    port: int = Field(8000, env="PORT")
    database_url: str = Field("sqlite:///./app.db", env="DATABASE_URL")

    knot_base: str = Field("https://development.knotapi.com", env="KNOT_BASE")
    knot_client_id: str | None = Field(None, env="KNOT_CLIENT_ID")
    knot_client_secret: str | None = Field(None, env="KNOT_CLIENT_SECRET")
    knot_basic_auth: str | None = Field(None, env="KNOT_BASIC_AUTH")

    openai_api_key: str | None = Field(None, env="OPENAI_API_KEY")
    openai_org_id: str | None = Field(None, env="OPENAI_ORG_ID")

    gemini_api_key: str | None = Field(None, env="GEMINI_API_KEY")
    dedalus_api_key: str | None = Field(None, env="DEDALUS_API_KEY")

    tax_default: float = Field(0.0825, env="DEFAULT_TAX_RATE")

    class Config:
        env_file = Path(__file__).resolve().parents[2] / ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
