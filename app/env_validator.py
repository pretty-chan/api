from typing import Literal
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["settings"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )

    APP_ENV: Literal["development", "production", "local"]
    SERVER_PORT: int
    OPENROUTER_API_KEY: str
    GOOGLE_SEARCH_API_KEY: str
    GOOGLE_SEARCH_ENGINE_ID: str

    @staticmethod
    @field_validator("SERVER_PORT")
    def check_port_range(value: int):
        if not 0 < value < 65536:
            raise ValueError("SERVER_PORT number must be between 1 and 65535")
        return value


settings = Settings()
