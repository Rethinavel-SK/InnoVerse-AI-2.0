"""
InnoVerse AI 2.0 — Caspian Configuration Module
===============================================
Loads credentials and settings safely from environment variables.
"""

import os
from typing import Optional
from pydantic import BaseModel


class CaspianConfig(BaseModel):
    api_key: Optional[str] = None
    base_url: str = "https://api.trycaspianai.com"
    telegram_bot_token: Optional[str] = None
    discord_bot_token: Optional[str] = None
    webhook_secret: Optional[str] = None

    @classmethod
    def load_from_env(cls) -> "CaspianConfig":
        api_key = os.getenv("CASPIAN_API_KEY")
        # Strip dummy/placeholder keys
        if api_key and (api_key.startswith("comm_sandbox") or "demo" in api_key.lower() or "your_" in api_key.lower()):
            api_key = None

        return cls(
            api_key=api_key,
            base_url=os.getenv("CASPIAN_BASE_URL", "https://api.trycaspianai.com"),
            telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN"),
            discord_bot_token=os.getenv("DISCORD_BOT_TOKEN"),
            webhook_secret=os.getenv("CASPIAN_WEBHOOK_SECRET"),
        )

    @property
    def is_valid(self) -> bool:
        return bool(self.api_key)


def get_caspian_config() -> CaspianConfig:
    return CaspianConfig.load_from_env()
