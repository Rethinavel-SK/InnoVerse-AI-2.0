"""
Domain Models for Innovation Director Agent.
============================================
Contains metadata structures and execution result containers.
"""

import time
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class ExecutionMetadata(BaseModel):
    """
    Metadata about the Innovation Director Agent execution run.
    """
    agent_name: str = "InnovationDirectorAgent"
    version: str = "1.0.0"
    execution_time_ms: float
    model_used: str
    agents_executed: int = 6
    timestamp: float = Field(default_factory=time.time)


class InnovationDirectorResult(BaseModel):
    """
    Complete result container including request ID, execution metadata,
    and synthesized master director output.
    """
    request_id: str
    metadata: ExecutionMetadata
    director_output: Dict[str, Any]
