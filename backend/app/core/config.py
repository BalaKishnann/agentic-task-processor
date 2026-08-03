import logging
import sys
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized application configuration.
    Values are read from environment variables (or a .env file locally).
    Required fields with no default will raise a validation error at
    startup if missing, rather than failing later mid-request.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # --- Required ---
    OPENAI_API_KEY: str = Field(..., min_length=1)

    DATABASE_URL: str = Field(default="sqlite:///agent.db")

    # --- Optional, with sensible defaults ---
    ENVIRONMENT: str = Field(
        default="development"
    )  # development | staging | production
    LOG_LEVEL: str = Field(default="INFO")
    CORS_ALLOWED_ORIGINS: str = Field(default="http://localhost:5173")
    LOG_JSON: bool = Field(
        default=True
    )  # set False locally if you want human-readable logs
    RATE_LIMIT_PER_MINUTE: int = Field(default=30)
    CORS_ALLOWED_METHODS: str = Field(default="GET,POST")
    CORS_ALLOWED_HEADERS: str = Field(default="Content-Type,Authorization")

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        upper_value = value.upper()
        if upper_value not in valid_levels:
            raise ValueError(
                f"LOG_LEVEL must be one of {sorted(valid_levels)}, got '{value}'"
            )
        return upper_value

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, value: str) -> str:
        valid_envs = {"development", "staging", "production"}
        lower_value = value.lower()
        if lower_value not in valid_envs:
            raise ValueError(
                f"ENVIRONMENT must be one of {sorted(valid_envs)}, got '{value}'"
            )
        return lower_value

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ALLOWED_ORIGINS.split(",")]

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @property
    def cors_methods_list(self) -> list[str]:
        return [m.strip() for m in self.CORS_ALLOWED_METHODS.split(",")]

    @property
    def cors_headers_list(self) -> list[str]:
        return [h.strip() for h in self.CORS_ALLOWED_HEADERS.split(",")]


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance. Raises pydantic.ValidationError with a
    clear message if required env vars are missing or invalid — this
    is what makes startup fail fast instead of the app booting and
    breaking later on first real request.
    """
    try:
        return Settings()
    except Exception as exc:
        # Print directly, since logging config depends on settings we
        # don't have yet at this point.
        print(f"FATAL: Invalid configuration — {exc}", file=sys.stderr)
        raise


def configure_logging001(log_level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )
