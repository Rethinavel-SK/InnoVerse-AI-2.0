"""
InnoVerse AI 2.0 — Caspian SDK Client (Backend Wrapper)
=======================================================
Maintains backward compatibility by delegating to integrations.caspian.
"""

from integrations.caspian.client import InnoVerseCaspianClient, caspian_client

__all__ = ["InnoVerseCaspianClient", "caspian_client"]

