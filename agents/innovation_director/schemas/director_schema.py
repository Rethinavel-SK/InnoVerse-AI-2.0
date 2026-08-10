"""
Pydantic Schemas for Innovation Director Agent.
===============================================
Defines request and response models for orchestrating and synthesizing
all specialist AI agents (11 in v2.0) according to strict director guidelines.
"""

from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field


class InnovationDirectorRequest(BaseModel):
    """
    Input schema for the Innovation Director Agent.
    """
    problem_statement: str = Field(
        ...,
        min_length=10,
        description="Detailed problem statement or business concept to orchestrate across specialist agents.",
        examples=["Build an AI-powered automated code security review platform for enterprise DevOps teams."]
    )
    selected_agents: Optional[List[str]] = Field(
        default=None,
        description="Optional list of specific agents to invoke if problem statement is simple. Defaults to all 9 agents."
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional project parameters such as target region, budget limits, stage, or technical constraints."
    )


class ConflictResolutionItem(BaseModel):
    """
    Structured conflict resolution entry between two or more agents.
    """
    agents_involved: List[str] = Field(..., description="List of agents with conflicting recommendations.")
    conflict_description: str = Field(..., description="Description of the disagreement between agents.")
    comparison: str = Field(..., description="Comparison of both agent recommendations.")
    resolution: str = Field(..., description="Intelligent reconciled recommendation.")
    reasoning: str = Field(..., description="Strategic reasoning for the reconciled solution.")


class FinalRecommendation(BaseModel):
    """
    Final strategic recommendations for building and commercializing the project.
    """
    build_recommendation: str = Field(..., description="Should this project be built? (Yes / No / Conditional GO)")
    expected_success_probability: Optional[str] = Field(default="85%", description="Estimated probability of project success.")
    implementation_strategy: str = Field(..., description="Recommended implementation strategy.")
    suggested_deployment_phases: Optional[List[str]] = Field(
        default_factory=lambda: ["Phase 1: MVP Core", "Phase 2: Enterprise Integration", "Phase 3: Scale"],
        description="Suggested phased deployment milestones."
    )
    commercial_viability: str = Field(..., description="Commercial viability and market revenue potential.")
    investment_priority: Optional[str] = Field(default="High Priority", description="Recommended investment priority rating.")
    future_scope: List[str] = Field(default_factory=list, description="Future enhancements and long-term features.")


class DebateEntry(BaseModel):
    """A single debate entry between agents with opposing views."""
    topic: str = Field(..., description="What the agents disagree about.")
    agents_involved: List[str] = Field(default_factory=list)
    positions: Dict[str, str] = Field(default_factory=dict, description="agent_name -> position")
    evidence: List[str] = Field(default_factory=list)
    resolution: str = Field(default="", description="Director's resolution with reasoning.")
    confidence: float = Field(default=0.7)


class EvidenceItem(BaseModel):
    """Evidence with classification (FACT/INFERENCE/PREDICTION/ASSUMPTION)."""
    statement: str
    classification: str = "INFERENCE"  # FACT, INFERENCE, PREDICTION, ASSUMPTION
    source: str = "agent_analysis"
    agent: str = ""
    confidence: float = 0.7


class InnovationDirectorResponse(BaseModel):
    """
    Unified master response returned by the Innovation Director Agent.
    Contains synthesized master findings and summaries from all 11 specialist agents (v2.0).
    """
    executive_summary: str = Field(..., description="Comprehensive executive summary narrative.")
    problem_understanding: str = Field(..., description="Deep analysis and context of the input problem statement.")
    agent_status: Dict[str, str] = Field(
        default_factory=lambda: {
            "solution_architect": "Completed",
            "business_strategy": "Completed",
            "research": "Completed",
            "patent_analysis": "Completed",
            "market_analysis": "Completed",
            "trend_analysis": "Completed",
            "risk_assessment": "Completed",
            "sustainability": "Completed",
            "mvp_roadmap": "Completed",
            "failure_hunter": "Completed",
            "execution_planner": "Completed",
        },
        description="Execution status for each specialist agent ('Completed' or 'Unavailable')."
    )
    # --- Original 9 agent summaries ---
    technical_summary: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Output from Solution Architect Agent")
    business_summary: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Output from Business Strategy Agent")
    research_summary: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Output from Research Agent")
    patent_summary: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Output from Patent Analysis Agent")
    market_summary: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Output from Market Analysis Agent")
    trend_summary: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Output from Trend Analysis Agent")
    risk_summary: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Output from Risk Assessment Agent")
    sustainability_summary: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Output from Sustainability Agent")
    roadmap_summary: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Output from MVP & Roadmap Planner Agent")

    # --- 2.0: New agent summaries ---
    failure_analysis: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Output from Failure Hunter Agent")
    execution_plan: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Output from Execution Planner Agent")

    # --- 2.0: Debate, Evidence & Score ---
    debate_trace: List[Union[DebateEntry, Dict[str, Any]]] = Field(
        default_factory=list,
        description="Multi-agent debate trace with opposing positions, evidence, and resolutions."
    )
    evidence_items: List[Union[EvidenceItem, Dict[str, Any]]] = Field(
        default_factory=list,
        description="Classified evidence items (FACT/INFERENCE/PREDICTION/ASSUMPTION)."
    )
    score_breakdown: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Transparent 10-dimension innovation score breakdown."
    )

    # --- 2.0: Idea Evolution ---
    evolution_history: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Idea evolution versions with score progression."
    )

    # --- Original fields ---
    conflict_resolution: List[Union[ConflictResolutionItem, Dict[str, Any], str]] = Field(
        default_factory=list,
        description="Reconciled conflicts between agent recommendations with reasoning."
    )
    overall_innovation_score: float = Field(..., ge=0.0, le=100.0, description="Overall score out of 100 using weighted multi-agent analysis.")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score reflecting agent completion and data quality.")
    final_recommendation: Union[FinalRecommendation, Dict[str, Any]] = Field(..., description="Final build & commercial recommendations.")

    # ------------------------------------------------------------------
    # Backwards Compatibility Properties
    # ------------------------------------------------------------------
    @property
    def problem_statement(self) -> str:
        return self.problem_understanding

    @property
    def feasibility_score(self) -> float:
        return self.overall_innovation_score

    @property
    def recommendation(self) -> str:
        if isinstance(self.final_recommendation, dict):
            return self.final_recommendation.get("build_recommendation", "GO")
        return getattr(self.final_recommendation, "build_recommendation", "GO")

    @property
    def solution_architecture(self) -> Optional[Dict[str, Any]]:
        return self.technical_summary

    @property
    def mvp_roadmap(self) -> Optional[Dict[str, Any]]:
        return self.roadmap_summary

    @property
    def business_strategy(self) -> Optional[Dict[str, Any]]:
        return self.business_summary

    @property
    def risk_assessment(self) -> Optional[Dict[str, Any]]:
        return self.risk_summary

    @property
    def research_intelligence(self) -> Optional[Dict[str, Any]]:
        return self.research_summary

    @property
    def patent_intelligence(self) -> Optional[Dict[str, Any]]:
        return self.patent_summary
