from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ProblemAnalysis(BaseModel):
    business_problem: str = Field(..., description="Root business problem being solved")
    domain: str = Field(..., description="Primary industry domain e.g. Healthcare, Warehouse, FinTech, Agriculture")
    primary_objective: str = Field(..., description="Main system objective")
    end_users: str = Field(..., description="Target end users or 'Not Specified'")
    functional_requirements: List[str] = Field(default_factory=list, description="Extracted core functional requirements")
    non_functional_requirements: List[str] = Field(default_factory=list, description="Quality attributes or 'Not Specified'")
    expected_scale: str = Field(..., description="Target scale volume or 'Not Specified'")
    availability_requirements: str = Field(..., description="Availability SLA or 'Not Specified'")
    performance_requirements: str = Field(..., description="Latency / performance requirements or 'Not Specified'")
    security_requirements: str = Field(..., description="Security & compliance rules or 'Not Specified'")
    ai_requirements: str = Field(..., description="AI/ML needs or 'Not Specified'")
    analytics_requirements: str = Field(..., description="Reporting & analytics needs or 'Not Specified'")
    real_time_requirements: str = Field(..., description="Real-time requirements or 'Not Specified'")
    third_party_integrations: List[str] = Field(default_factory=list, description="External APIs or integrations mentioned")
    deployment_constraints: str = Field(..., description="Deployment constraints or 'Not Specified'")


class IdentifiedRequirements(BaseModel):
    real_time: bool = Field(default=False)
    ai_required: bool = Field(default=False)
    computer_vision: bool = Field(default=False)
    nlp: bool = Field(default=False)
    iot: bool = Field(default=False)
    gps_tracking: bool = Field(default=False)
    notifications: bool = Field(default=False)
    authentication: bool = Field(default=False)
    rbac: bool = Field(default=False)
    queue_processing: bool = Field(default=False)
    event_streaming: bool = Field(default=False)
    caching: bool = Field(default=False)
    analytics: bool = Field(default=False)
    monitoring: bool = Field(default=False)
    high_availability: bool = Field(default=False)
    disaster_recovery: bool = Field(default=False)


class ArchitectureSelection(BaseModel):
    type: str = Field(..., description="Architecture style: Layered Architecture | Modular Monolith | Clean Architecture | Microservices | Event Driven Architecture | Serverless | Hybrid Architecture | Edge Architecture")
    rationale: str = Field(..., description="Why this architecture style is the best choice")
    why_alternatives_were_not_selected: str = Field(..., description="Why alternative architectural styles were rejected")


class TechChoice(BaseModel):
    technology: str = Field(..., description="Recommended technology or 'Not Specified'")
    reason: str = Field(..., description="Justification based on derived requirements")
    why_alternatives_not_selected: str = Field(..., description="Why alternative technologies were not selected")


class SolutionArchitectRequest(BaseModel):
    problem_statement: str = Field(
        ...,
        min_length=10,
        description="The validated problem statement to design the technical architecture for",
        examples=["Build an AI-powered autonomous warehouse management system that optimizes inventory, predicts demand, and assigns robots to tasks."]
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional explicit constraints provided by the user"
    )


class SolutionArchitectResponse(BaseModel):
    problem_analysis: ProblemAnalysis = Field(..., description="Step 1: Architectural problem analysis")
    identified_requirements: IdentifiedRequirements = Field(..., description="Step 2: Boolean feature requirement flags derived by architect")
    architecture: ArchitectureSelection = Field(..., description="Step 3: Selected single architecture style and justification")
    technology_recommendations: Dict[str, Any] = Field(..., description="Step 4: Technology recommendations (Frontend, Backend, Database, Vector DB, Cache, Broker, Storage, Auth, Monitoring, Deployment, Cloud, AI Models, ML Frameworks, External APIs)")
    reasoning: List[str] = Field(default_factory=list, description="Step-by-step reasoning chain: Problem -> Requirements -> Architecture -> Technologies -> Cost")
    estimated_complexity: str = Field(..., description="Technical complexity: Low | Medium | High | Very High")
    development_time: str = Field(..., description="Realistic development timeline")
    team_size: str = Field(..., description="Realistic engineering team size")
    prototype_cost: str = Field(..., description="Prototype monthly infrastructure cost")
    production_cost: str = Field(..., description="Production monthly infrastructure cost")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Architectural confidence score (decreases if information is vague or missing)")
