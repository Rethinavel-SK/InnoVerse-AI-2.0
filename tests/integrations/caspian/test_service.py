"""
Tests for integrations.caspian.service
"""

import pytest
from unittest.mock import MagicMock
from integrations.caspian.service import InnoVerseCaspianService
from integrations.caspian.client import InnoVerseCaspianClient
from integrations.caspian.config import CaspianConfig


def test_service_connect_telegram_unconfigured(monkeypatch):
    monkeypatch.delenv("CASPIAN_API_KEY", raising=False)
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    service = InnoVerseCaspianService()
    assert not service.connect_telegram()


def test_service_connect_discord_unconfigured(monkeypatch):
    monkeypatch.delenv("CASPIAN_API_KEY", raising=False)
    monkeypatch.delenv("DISCORD_BOT_TOKEN", raising=False)
    service = InnoVerseCaspianService()
    assert not service.connect_discord()
