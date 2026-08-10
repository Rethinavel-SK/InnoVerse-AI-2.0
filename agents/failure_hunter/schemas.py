"""
Failure Hunter Agent — Pydantic Schemas
=========================================
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class FailureRisk(BaseModel):
    rank: int = 1
    risk: str
    category: str = "general"
    probability: str = "MEDIUM"   # HIGH, MEDIUM, LOW
    impact: str = "HIGH"          # CRITICAL, HIGH, MEDIUM, LOW
    evidence: str = ""
    mitigation: str = ""


class FailureHunterRequest(BaseModel):
    problem_statement: str = Field(..., min_length=10)
    context: Optional[Dict[str, Any]] = None


class FailureHunterResponse(BaseModel):
    agent: str = "Failure Hunter Agent"
    top_failure_risks: List[FailureRisk] = Field(default_factory=list)
    overall_failure_probability: str = "MEDIUM"
    critical_assumption: str = ""
    contrarian_view: str = ""
    confidence: float = 0.80
    classification: str = "INFERENCE"
    summary: str = ""
