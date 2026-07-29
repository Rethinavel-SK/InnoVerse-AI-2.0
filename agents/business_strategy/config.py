import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class BusinessStrategyConfig(BaseSettings):
    """
    Configuration settings for the Business Strategy Agent.
    """
    groq_api_key: Optional[str] = None
    # llama-3.1-8b-instant: 6K TPM free tier — keep max_tokens<=1500 so total request stays under limit
    model_name: str = "llama-3.1-8b-instant"
    temperature: float = 0.3
    max_tokens: int = 1500
    request_timeout: float = 60.0
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = BusinessStrategyConfig()
