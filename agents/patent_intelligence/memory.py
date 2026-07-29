import time
from typing import Dict, Optional
from .schemas import PatentAgentResponse


class AgentMemory:
    """In-memory cache for Patent Intelligence Agent responses with TTL."""

    def __init__(self, ttl_seconds: int = 86400):
        self.ttl = ttl_seconds
        self._cache: Dict[str, dict] = {}

    def _normalize_key(self, query: str) -> str:
        return query.strip().lower()

    def get(self, query: str) -> Optional[PatentAgentResponse]:
        key = self._normalize_key(query)
        entry = self._cache.get(key)
        if not entry:
            return None
        
        if time.time() - entry["timestamp"] > self.ttl:
            del self._cache[key]
            return None
            
        return entry["response"]

    def set(self, query: str, response: PatentAgentResponse) -> None:
        key = self._normalize_key(query)
        self._cache[key] = {
            "timestamp": time.time(),
            "response": response
        }

    def clear(self) -> None:
        self._cache.clear()
