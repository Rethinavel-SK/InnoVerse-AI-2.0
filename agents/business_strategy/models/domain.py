from datetime import datetime, timezone
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class ExecutionMetadata(BaseModel):
    """Metadata tracking execution details for the Business Strategy Agent."""
    agent_name: str = "BusinessStrategyAgent"
    version: str = "1.0.0"
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    execution_time_ms: float = 0.0
    model_used: str = "llama-3.3-70b-versatile"


class BusinessStrategyResult(BaseModel):
    """Full pipeline result wrapping strategy output with execution metadata."""
    request_id: str
    metadata: ExecutionMetadata
    strategy_output: Dict[str, Any]
