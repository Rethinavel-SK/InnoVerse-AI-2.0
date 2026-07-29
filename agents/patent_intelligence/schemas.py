from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class PatentDetail(BaseModel):
    """Structured details of an individual prior-art patent."""
    patent_id: str = Field(..., description="Patent identifier e.g., US11234567B2")
    title: str = Field(..., description="Title of the patent")
    assignee: Optional[str] = Field("Unknown / Unassigned", description="Assignee or inventor name")
    year: str = Field(..., description="Filing or publication year")
    summary: str = Field(..., description="Brief summary of patent prior art")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Relevance score (0.0 to 1.0)")

    @field_validator('year', mode='before')
    @classmethod
    def coerce_year_str(cls, v):
        return str(v) if v is not None else "Unknown"


class PatentAgentRequest(BaseModel):
    """Input payload for the Patent Intelligence Agent."""
    problem_statement: str = Field(
        ..., 
        description="The invention description, concept, or claim to evaluate",
        example="AI system for automated food waste tracking using computer vision and edge cameras."
    )
    max_results: Optional[int] = Field(5, description="Maximum number of similar patents to analyze")


class PatentAgentResponse(BaseModel):
    """Strict JSON output required for the Patent Intelligence Agent."""
    agent: str = Field("Patent Agent", description="Agent name identifier")
    similar_patents: List[PatentDetail] = Field(..., description="List of identified prior-art patents")
    novelty_score: int = Field(..., ge=0, le=100, description="Novelty score from 0 to 100")
    white_spaces: List[str] = Field(..., description="Detected unpatented white-space opportunities")
    risk: str = Field(..., description="Patent infringement risk assessment (e.g. Low, Medium, High)")

    @field_validator('novelty_score', mode='before')
    @classmethod
    def coerce_novelty_score_int(cls, v):
        try:
            return int(float(v))
        except (ValueError, TypeError):
            return 50
