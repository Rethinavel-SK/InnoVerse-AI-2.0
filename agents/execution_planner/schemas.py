"""
Execution Planner Agent — Pydantic Schemas
=============================================
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Milestone(BaseModel):
    milestone: str
    description: str = ""
    target_week: int = 4
    deliverables: List[str] = Field(default_factory=list)


class ExecutionTask(BaseModel):
    title: str
    description: str = ""
    category: str = "general"
    priority: str = "MEDIUM"
    estimated_days: int = 5
    suggested_owner: str = "Team"
    deadline_offset_days: int = 14
    dependencies: List[str] = Field(default_factory=list)
    success_criteria: str = ""


class ValidationExperiment(BaseModel):
    experiment: str
    hypothesis: str = ""
    success_metric: str = ""
    estimated_duration_days: int = 7


class ExecutionPlan(BaseModel):
    recommended_approach: str = ""
    total_estimated_weeks: int = 12
    milestones: List[Milestone] = Field(default_factory=list)
    tasks: List[ExecutionTask] = Field(default_factory=list)
    validation_experiments: List[ValidationExperiment] = Field(default_factory=list)
    immediate_next_steps: List[str] = Field(default_factory=list)


class ExecutionPlannerRequest(BaseModel):
    problem_statement: str = Field(..., min_length=10)
    context: Optional[Dict[str, Any]] = None
    analysis_summary: Optional[str] = None


class ExecutionPlannerResponse(BaseModel):
    agent: str = "Execution Planner Agent"
    execution_plan: ExecutionPlan = Field(default_factory=ExecutionPlan)
    confidence: float = 0.80
    classification: str = "INFERENCE"
    summary: str = ""
