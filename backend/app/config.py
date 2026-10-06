"""Configuration de l'application."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration globale de l'application."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    DATABASE_URL: str = "postgresql://guestbtp:guestbtp@localhost:5432/guestbtp"

    # Application
    SECRET_KEY: str = "your-secret-key-change-in-production"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # CORS
    CORS_ORIGINS: list[str] = ["*"]


settings = Settings()
