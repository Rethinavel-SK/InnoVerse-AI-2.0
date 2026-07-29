"""
Pydantic Schemas for MVP & Roadmap Agent.
=========================================
Defines input request models and output response models strictly adhering
to the required contract.
"""

from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field


class MvpRoadmapRequest(BaseModel):
    """
    Input schema for MVP & Roadmap Agent.
    """
    problem_statement: str = Field(
        ...,
        description="Detailed problem statement or product vision to generate MVP & Roadmap for.",
        examples=["Build an AI-powered SaaS platform for automated code reviews and security scanning."]
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional additional context such as target audience, budget constraints, or tech stack."
    )


class MvpRoadmapResponse(BaseModel):
    """
    Output schema for MVP & Roadmap Agent.
    Matches exact output specifications required:
    - mvp_features: List of core features for Minimum Viable Product.
    - future_features: List of prioritized post-MVP features.
    - roadmap: Product roadmap phases across timeline.
    - milestones: Structured breakdown of key development milestones.
    - timeline: Overall estimated delivery timeline string.
    - sprint_plan: Suggested sprint planning breakdown.
    - team_size: Recommended engineering/product team composition & size.
    - estimated_budget: Budget estimate with cost breakdown.
    - risks: Identified development & operational risks with mitigations.
    - confidence: Confidence score between 0.0 and 1.0.
    """
    mvp_features: List[Union[str, Dict[str, Any]]] = Field(
        ...,
        description="Core features included in the Minimum Viable Product."
    )
    future_features: List[Union[str, Dict[str, Any]]] = Field(
        ...,
        description="Prioritized features deferred for post-MVP releases."
    )
    roadmap: List[Union[str, Dict[str, Any]]] = Field(
        ...,
        description="Product roadmap phases outlining strategic progression."
    )
    milestones: List[Union[str, Dict[str, Any]]] = Field(
        ...,
        description="Sequential development milestones with key deliverables."
    )
    timeline: str = Field(
        ...,
        description="Estimated overall development timeline (e.g., '14 Weeks / 3.5 Months')."
    )
    sprint_plan: List[Union[str, Dict[str, Any]]] = Field(
        ...,
        description="Suggested sprint-by-sprint breakdown of development activities."
    )
    team_size: str = Field(
        ...,
        description="Recommended team size and role distribution."
    )
    estimated_budget: str = Field(
        ...,
        description="Estimated development budget and cost allocation."
    )
    risks: List[Union[str, Dict[str, Any]]] = Field(
        ...,
        description="Identified risks during development along with mitigation strategies."
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score for the generated MVP and roadmap assessment."
    )
