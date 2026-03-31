"""Application configuration."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Core Banking System"
    database_url: str = "sqlite:///./cbs.db"
    debug: bool = False
    default_currency: str = "EUR"

    model_config = {"env_prefix": "CBS_"}


settings = Settings()
