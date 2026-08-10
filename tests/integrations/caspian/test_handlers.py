"""
Tests for integrations.caspian.handlers
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from integrations.caspian.handlers import CaspianMessageHandler


@pytest.mark.asyncio
async def test_handle_empty_message():
    handler = CaspianMessageHandler()
    message = MagicMock()
    message.text = "   "
    res = await handler.handle_message(message)
    assert res is None


@pytest.mark.asyncio
async def test_handle_valid_message_with_router():
    router = AsyncMock()
    handler = CaspianMessageHandler(router=router)

    message = MagicMock()
    message.id = "msg_123"
    message.conversation_id = "conv_456"
    message.channel = "telegram"
    message.sender = "user_789"
    message.text = "AI assistant for market research"

    res = await handler.handle_message(message)
    assert res["status"] == "success"
    assert res["message_id"] == "msg_123"
    assert res["channel"] == "telegram"
    router.handle_message.assert_called_once_with(message)


@pytest.mark.asyncio
async def test_handle_message_fallback_reply():
    handler = CaspianMessageHandler(router=None)

    message = MagicMock()
    message.id = "msg_100"
    message.channel = "discord"
    message.text = "Hello InnoVerse"
    message.reply = MagicMock()

    res = await handler.handle_message(message)
    assert res["status"] == "fallback_replied"
    message.reply.assert_called_once()
