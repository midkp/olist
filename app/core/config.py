"""Configuration settings for the application."""

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    DATABASE_URL: str
    APP_NAME: str
    HOST: str
    PORT: int
    DEBUG: bool
    API_KEY: str
    OPENAI_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()
