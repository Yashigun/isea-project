from functools import lru_cache
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

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

    ALLOWED_ORIGINS: List[str] = Field(default_factory=list)
    LOG_LEVEL: str

    MAX_LOGIN_ATTEMPTS: int
    ACCOUNT_LOCK_MINUTES: int
    PASSWORD_MIN_LENGTH: int

    RATE_LIMIT_REQUESTS: int
    RATE_LIMIT_WINDOW_SECONDS: int

    REDIS_URL: Optional[str] = None   # optional

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()