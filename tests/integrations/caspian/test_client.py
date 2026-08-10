"""
Tests for integrations.caspian.client
"""

import pytest
from unittest.mock import MagicMock
from integrations.caspian.client import InnoVerseCaspianClient
from integrations.caspian.config import CaspianConfig


def test_client_init_unconfigured():
    config = CaspianConfig(api_key=None)
    client = InnoVerseCaspianClient(config=config)
    assert not client.is_configured
    assert not client.initialize()


def test_client_init_mock_sdk():
    config = CaspianConfig(
        api_key="caspian_test_key_123",
        telegram_bot_token="tg_token_123",
        discord_bot_token="dc_token_123",
    )
    client = InnoVerseCaspianClient(config=config)

    mock_comm = MagicMock()
    mock_comm.connect_email.return_value = {"address": "test@trycaspianai.com"}
    mock_comm.connect_telegram.return_value = {"id": "tg_conn_1"}
    mock_comm.connect_discord.return_value = {"id": "dc_conn_1"}

    assert client.initialize(custom_client=mock_comm)
    assert "email" in client.connected_channels
    assert "telegram" in client.connected_channels
    assert "discord" in client.connected_channels
    assert client.email_address == "test@trycaspianai.com"
