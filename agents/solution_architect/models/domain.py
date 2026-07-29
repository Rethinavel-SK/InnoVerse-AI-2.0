from datetime import datetime, timezone
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class ExecutionMetadata(BaseModel):
    agent_name: str = "SolutionArchitectAgent"
    version: str = "1.0.0"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    execution_time_ms: float = 0.0
    model_used: str = "gpt-5"


class SolutionDesignResult(BaseModel):
    request_id: str
    metadata: ExecutionMetadata
    architecture_output: Dict[str, Any]
