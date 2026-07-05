from functools import lru_cache
from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    ENVIRONMENT: str
    DEBUG: bool

    DATABASE_URL: str

    JWT_ACCESS_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ISSUER: str
    JWT_AUDIENCE: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    COOKIE_SECURE: bool
    COOKIE_HTTPONLY: bool
    COOKIE_SAMESITE: str

    # CORS – stored as a comma-separated string to avoid JSON parsing issues
    ALLOWED_ORIGINS_RAW: str = Field(default="", alias="ALLOWED_ORIGINS")

    LOG_LEVEL: str

    MAX_LOGIN_ATTEMPTS: int
    ACCOUNT_LOCK_MINUTES: int
    PASSWORD_MIN_LENGTH: int

    RATE_LIMIT_REQUESTS: int
    RATE_LIMIT_WINDOW_SECONDS: int

    REDIS_URL: Optional[str] = None

    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""
    CLOUDINARY_UPLOAD_PRESET: str = ""

    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        """Parse the comma-separated string into a list of origins."""
        if not self.ALLOWED_ORIGINS_RAW:
            return []
        return [origin.strip() for origin in self.ALLOWED_ORIGINS_RAW.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()