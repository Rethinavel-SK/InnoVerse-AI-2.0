import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class InnovationDirectorConfig(BaseSettings):
    """
    Configuration settings for the Innovation Director Agent.
    """
    groq_api_key: Optional[str] = None
    model_name: str = "llama-3.1-8b-instant"
    temperature: float = 0.3
    max_tokens: int = 3500
    request_timeout: float = 90.0
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = InnovationDirectorConfig()
