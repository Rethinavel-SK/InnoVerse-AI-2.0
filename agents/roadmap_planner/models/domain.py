"""
Domain Models for MVP & Roadmap Agent.
======================================
Contains internal data models, execution metadata, and result containers.
"""

import time
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class ExecutionMetadata(BaseModel):
    """
    Metadata about the agent execution run.
    """
    agent_name: str = "MVPRoadmapAgent"
    version: str = "1.0.0"
    execution_time_ms: float
    model_used: str
    timestamp: float = Field(default_factory=time.time)


class MVPRoadmapResult(BaseModel):
    """
    Complete result container including request ID, execution metadata,
    and agent output.
    """
    request_id: str
    metadata: ExecutionMetadata
    roadmap_output: Dict[str, Any]
