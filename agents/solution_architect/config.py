import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class SolutionArchitectConfig(BaseSettings):
    """
    Configuration settings for the Solution Architect Agent.
    """
    groq_api_key: Optional[str] = None
    # llama-3.1-8b-instant is Groq's fastest model — ideal for quick testing
    # Switch to llama-3.3-70b-versatile for best quality (but slower)
    model_name: str = "llama-3.1-8b-instant"
    temperature: float = 0.2
    max_tokens: int = 2000
    request_timeout: float = 30.0
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = SolutionArchitectConfig()
