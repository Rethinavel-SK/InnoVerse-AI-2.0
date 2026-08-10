"""
InnoVerse AI 2.0 — Caspian Low-Level Client Wrapper
===================================================
Manages CommClient initialization, channel setup (Telegram, Discord, Email),
proactive messaging, and error logging without exposing secrets.
"""

import asyncio
import logging
import os
import threading
from typing import Dict, Any, Optional, Callable, List

from integrations.caspian.config import get_caspian_config, CaspianConfig

logger = logging.getLogger("CaspianClient")


class InnoVerseCaspianClient:
    """
    Wrapper around installed caspian_sdk CommClient.
    """

    def __init__(self, config: Optional[CaspianConfig] = None):
        self.config = config or get_caspian_config()
        self._client = None
        self._connections: Dict[str, Dict[str, Any]] = {}
        self._message_handler: Optional[Callable] = None
        self._listener_thread: Optional[threading.Thread] = None
        self._running = False
        self._email_address: Optional[str] = None
        self._conversation_project_map: Dict[str, str] = {}

    @property
    def is_configured(self) -> bool:
        """Reload config to check if API key is present."""
        self.config = get_caspian_config()
        return self.config.is_valid

    def initialize(self, custom_client=None) -> bool:
        """Initialize the Caspian CommClient and connect active channels."""
        if custom_client:
            self._client = custom_client
            self._connect_channels()
            return True

        if not self.is_configured:
            logger.warning("CASPIAN_API_KEY is not configured or is a placeholder. Caspian integration disabled.")
            return False

        try:
            from caspian_sdk import CommClient
            self._client = CommClient(
                api_key=self.config.api_key,
                base_url=self.config.base_url,
            )
            logger.info("Caspian CommClient initialized successfully.")
        except ImportError:
            logger.warning("caspian-sdk not installed. Run: pip install caspian-sdk")
            return False
        except Exception as e:
            logger.error("Failed to initialize Caspian CommClient: %s", e)
            return False

        self._connect_channels()
        return True

    def _connect_channels(self):
        """Connect available communication channels safely."""
        if not self._client:
            return

        # 1. Email (standard channel provided by Caspian)
        try:
            inbox = self._client.connect_email()
            if isinstance(inbox, dict):
                self._connections["email"] = inbox
                self._email_address = inbox.get("address", "")
                logger.info("✅ Email channel connected: %s", self._email_address)
        except Exception as e:
            logger.warning("Failed to connect Email channel: %s", e)

        # 2. Telegram
        token = self.config.telegram_bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
        if token:
            try:
                tg = self._client.connect_telegram(bot_token=token)
                if isinstance(tg, dict):
                    self._connections["telegram"] = tg
                    logger.info("✅ Telegram channel connected (connection_id: %s)", tg.get("id", ""))
                else:
                    self._connections["telegram"] = {"status": "connected"}
                    logger.info("✅ Telegram channel connected.")
            except Exception as e:
                logger.error("Failed to connect Telegram channel: %s", e)
        else:
            logger.info("⏭️ Telegram: TELEGRAM_BOT_TOKEN not set, skipping.")

        # 3. Discord
        discord_token = self.config.discord_bot_token or os.getenv("DISCORD_BOT_TOKEN")
        if discord_token:
            try:
                dc = self._client.connect_discord(bot_token=discord_token)
                if isinstance(dc, dict):
                    self._connections["discord"] = dc
                    logger.info("✅ Discord channel connected (connection_id: %s)", dc.get("id", ""))
                else:
                    self._connections["discord"] = {"status": "connected"}
                    logger.info("✅ Discord channel connected.")
            except Exception as e:
                logger.error("Failed to connect Discord channel: %s", e)
        else:
            logger.info("⏭️ Discord: DISCORD_BOT_TOKEN not set, skipping.")

        logger.info("Connected channels: %s", list(self._connections.keys()))

    def set_message_handler(self, handler: Callable):
        """Set the message handler callback."""
        self._message_handler = handler

    def start_listener(self):
        """Start the Caspian background listener thread."""
        if not self._client or not self._message_handler:
            logger.warning("Cannot start Caspian listener: client or handler not set.")
            return

        @self._client.on_message
        def _on_message_wrapper(message):
            try:
                # Send typing indicator if client supports it
                if hasattr(self._client, "typing"):
                    try:
                        conv_id = getattr(message, "conversation_id", None)
                        if conv_id:
                            self._client.typing(conv_id)
                    except Exception:
                        pass

                # Dispatch message through async handler
                if asyncio.iscoroutinefunction(self._message_handler):
                    loop = asyncio.new_event_loop()
                    try:
                        loop.run_until_complete(self._message_handler(message))
                    finally:
                        loop.close()
                else:
                    self._message_handler(message)
            except Exception as e:
                logger.error("Error in Caspian on_message handler: %s", e, exc_info=True)

        def _listener_loop():
            logger.info("🎧 Caspian listener thread started (polling)...")
            self._running = True
            try:
                self._client.listen(ack="🧠 InnoVerse AI is processing your message...")
            except KeyboardInterrupt:
                logger.info("Caspian listener stopped by keyboard interrupt.")
            except Exception as e:
                logger.error("Caspian listener error: %s", e)
            finally:
                self._running = False

        self._listener_thread = threading.Thread(
            target=_listener_loop, daemon=True, name="caspian-listener"
        )
        self._listener_thread.start()

    def stop_listener(self):
        """Stop Caspian client polling."""
        self._running = False
        if self._client and hasattr(self._client, "close"):
            try:
                self._client.close()
            except Exception:
                pass

    def send_to_conversation(self, conversation_id: str, text: Optional[str] = None, html: Optional[str] = None) -> Optional[Dict]:
        """Proactively send a message to a conversation."""
        if not self._client:
            logger.warning("Caspian client not initialized, cannot send message.")
            return None
        try:
            return self._client.send_message(conversation_id, text=text, html=html)
        except Exception as e:
            logger.error("Failed to send message to conversation %s: %s", conversation_id, e)
            return None

    def reply_to_message(self, message, text: Optional[str] = None, html: Optional[str] = None) -> Optional[Dict]:
        """Reply directly to a Message instance."""
        try:
            return message.reply(text=text, html=html)
        except Exception as e:
            logger.error("Failed to reply to message: %s", e)
            return None

    def link_conversation_to_project(self, conversation_id: str, project_id: str):
        self._conversation_project_map[conversation_id] = project_id

    def get_project_for_conversation(self, conversation_id: str) -> Optional[str]:
        return self._conversation_project_map.get(conversation_id)

    @property
    def connected_channels(self) -> List[str]:
        return list(self._connections.keys())

    @property
    def email_address(self) -> Optional[str]:
        return self._email_address

    @property
    def is_running(self) -> bool:
        return self._running


caspian_client = InnoVerseCaspianClient()
