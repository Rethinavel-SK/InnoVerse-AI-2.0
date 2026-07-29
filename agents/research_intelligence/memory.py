import time
from typing import Dict, Any, Optional
from .schemas import ResearchAgentResponse

class AgentMemory:
    """In-memory cache & store for problem analyses to prevent redundant API queries."""
    
    def __init__(self, ttl_seconds: int = 86400):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.ttl_seconds = ttl_seconds

    def _normalize_key(self, key: str) -> str:
        return key.strip().lower()

    def get(self, query: str) -> Optional[ResearchAgentResponse]:
        norm_key = self._normalize_key(query)
        entry = self._cache.get(norm_key)
        if not entry:
            return None
        
        # Check expiration
        if time.time() - entry["timestamp"] > self.ttl_seconds:
            del self._cache[norm_key]
            return None
            
        return entry["response"]

    def set(self, query: str, response: ResearchAgentResponse) -> None:
        norm_key = self._normalize_key(query)
        self._cache[norm_key] = {
            "timestamp": time.time(),
            "response": response
        }

    def clear(self) -> None:
        self._cache.clear()
