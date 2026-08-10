"""
InnoVerse AI 2.0 — Caspian Message Handlers
===========================================
Receives Caspian Message objects, extracts attributes, validates text,
invokes the existing InnoVerse Agent Orchestrator / CaspianMessageRouter,
and sends the response back to the user over Telegram / Discord / Email.
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("CaspianHandlers")


class CaspianMessageHandler:
    """
    Message handler for Caspian SDK integrations.
    """

    def __init__(self, router=None):
        self._router = router

    def set_router(self, router):
        self._router = router

    async def handle_message(self, message: Any) -> Optional[Dict[str, Any]]:
        """
        Process an inbound Caspian message according to specifications:
        1. Extract attributes (id, conversation_id, channel, sender, text)
        2. Validate message
        3. Invoke agent pipeline via router
        4. Reply back via Caspian message.reply()
        5. Graceful exception handling
        """
        # 1. Extract message details
        msg_id = getattr(message, "id", None)
        conversation_id = getattr(message, "conversation_id", None)
        channel = getattr(message, "channel", "unknown")
        sender = getattr(message, "sender", None)
        text = getattr(message, "text", "") or ""

        logger.info(
            "[Caspian Message Received] ID: %s | Channel: %s | Conversation: %s | Sender: %s",
            msg_id, channel, conversation_id, sender
        )

        # 2. Validate empty / invalid messages
        text_clean = text.strip()
        if not text_clean:
            logger.info("Ignoring empty message ID: %s", msg_id)
            return None

        # 3. Process via backend CaspianMessageRouter
        try:
            if self._router:
                await self._router.handle_message(message)
                return {
                    "status": "success",
                    "message_id": msg_id,
                    "channel": channel,
                    "conversation_id": conversation_id,
                }
            else:
                # Direct fallback reply if router isn't attached
                reply_text = f"🧠 InnoVerse AI received your message on {channel}: {text_clean}"
                if hasattr(message, "reply") and callable(message.reply):
                    message.reply(text=reply_text)
                return {
                    "status": "fallback_replied",
                    "message_id": msg_id,
                    "channel": channel,
                }

        except Exception as exc:
            # Handle specific Caspian exception types if imported
            error_type = exc.__class__.__name__
            if error_type == "AccountRequiredError":
                logger.error("Caspian Account Required: %s", exc)
                self._safe_reply(message, "⚠️ Caspian Service Account required. Please check account billing/configuration.")
            elif error_type == "InsufficientCreditError":
                logger.error("Caspian Insufficient Credit: %s", exc)
                self._safe_reply(message, "⚠️ Caspian Service credits exhausted.")
            elif error_type == "CommError":
                logger.error("Caspian Communication Error: %s", exc)
                self._safe_reply(message, "⚠️ Communication layer error encountered.")
            else:
                logger.error("Error processing Caspian message ID %s: %s", msg_id, exc, exc_info=True)
                self._safe_reply(message, "⚠️ InnoVerse AI encountered an error processing your request.")

            return {
                "status": "error",
                "error": str(exc),
                "message_id": msg_id,
            }

    def _safe_reply(self, message: Any, text: str):
        if hasattr(message, "reply") and callable(message.reply):
            try:
                message.reply(text=text)
            except Exception as e:
                logger.error("Failed to send error reply: %s", e)
