"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# By inheriting from BaseSettings,
# this class automatically looks at your computer's environment variables
# and load them into Python objects.


class Settings(BaseSettings):
    """LedgerLens runtime settings."""

    app_name: str = "LedgerLens"
    environment: str = "development"
    debug: bool = False
    allowed_image_extensions: tuple[str, ...] = ("jpg", "jpeg", "png")
    allowed_document_extensions: tuple[str, ...] = ("pdf",)
    max_upload_size_mb: int = Field(
        default=10, description="Maximum upload size in megabytes", gt=0
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="LEDGERLENS_",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings instance."""

    return Settings()


settings = get_settings()
