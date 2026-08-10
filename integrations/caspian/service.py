"""
InnoVerse AI 2.0 — Caspian Standalone Service
============================================
Provides standalone command-line entrypoint and service manager for Caspian:
    python -m integrations.caspian.service
"""

import asyncio
import logging
import os
import sys
import time

from integrations.caspian.client import caspian_client, InnoVerseCaspianClient
from integrations.caspian.config import get_caspian_config
from integrations.caspian.handlers import CaspianMessageHandler
from backend.caspian.message_router import message_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("CaspianService")


class InnoVerseCaspianService:
    """
    Service wrapper for initializing and running Caspian integrations.
    """

    def __init__(self, client: Optional[InnoVerseCaspianClient] = None):
        self.client = client or caspian_client
        self.handler = CaspianMessageHandler(router=message_router)

    def connect_telegram(self, bot_token: Optional[str] = None) -> bool:
        """Connect Telegram channel using bot token."""
        token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            logger.error("Cannot connect Telegram: TELEGRAM_BOT_TOKEN not provided.")
            return False
        
        config = get_caspian_config()
        if not config.is_valid:
            logger.error("Cannot connect Telegram: CASPIAN_API_KEY is not configured.")
            return False

        logger.info("Connecting Telegram bot via Caspian SDK...")
        if not self.client._client:
            self.client.initialize()
        
        return "telegram" in self.client.connected_channels

    def connect_discord(self, bot_token: Optional[str] = None) -> bool:
        """Connect Discord channel using bot token."""
        token = bot_token or os.getenv("DISCORD_BOT_TOKEN")
        if not token:
            logger.error("Cannot connect Discord: DISCORD_BOT_TOKEN not provided.")
            return False

        config = get_caspian_config()
        if not config.is_valid:
            logger.error("Cannot connect Discord: CASPIAN_API_KEY is not configured.")
            return False

        logger.info("Connecting Discord bot via Caspian SDK...")
        if not self.client._client:
            self.client.initialize()

        return "discord" in self.client.connected_channels

    def start(self):
        """Start the Caspian communication service."""
        config = get_caspian_config()
        if not config.is_valid:
            logger.warning("CASPIAN_API_KEY is not set or invalid. Service not started.")
            return False

        if self.client.initialize():
            self.client.set_message_handler(self.handler.handle_message)
            self.client.start_listener()
            logger.info("🚀 Caspian Communication Service started successfully.")
            return True
        return False


caspian_service = InnoVerseCaspianService()


if __name__ == "__main__":
    logger.info("Starting Caspian Communication Service in standalone mode...")
    success = caspian_service.start()
    if success:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Stopping Caspian Service...")
            caspian_service.client.stop_listener()
            sys.exit(0)
    else:
        logger.error("Failed to start Caspian Service. Ensure CASPIAN_API_KEY is set in .env")
        sys.exit(1)
