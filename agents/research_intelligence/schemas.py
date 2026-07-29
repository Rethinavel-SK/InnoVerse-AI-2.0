from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class PaperDetail(BaseModel):
    """Structured details of an individual research paper."""
    title: str = Field(..., description="Title of the paper")
    authors: str = Field(..., description="Authors formatted as string")
    year: str = Field(..., description="Publication year")
    summary: str = Field(..., description="Brief summary of the paper")
    methodology: str = Field(..., description="Methodology or approach used")
    dataset: str = Field(..., description="Dataset used or referenced in the paper")
    results: str = Field(..., description="Key findings or results achieved")
    doi_or_url: Optional[str] = Field(None, description="DOI or source URL of the paper")

    @field_validator('year', mode='before')
    @classmethod
    def coerce_year_str(cls, v):
        return str(v) if v is not None else "Unknown"

    @field_validator('authors', mode='before')
    @classmethod
    def coerce_authors_str(cls, v):
        if isinstance(v, list):
            return ", ".join(v)
        return str(v) if v is not None else "Unknown"


class RawPaper(BaseModel):
    """Raw paper data collected from external academic databases."""
    title: str
    authors: List[str]
    year: str
    abstract: str
    url: Optional[str] = None
    doi: Optional[str] = None
    source: str  # e.g., 'Semantic Scholar', 'arXiv', 'CrossRef'


class ResearchAgentRequest(BaseModel):
    """Input payload for the Research Intelligence Agent."""
    problem_statement: str = Field(
        ..., 
        description="The user's problem statement or research query",
        example="Reduce food waste in restaurants using AI."
    )
    max_results: Optional[int] = Field(5, description="Maximum number of papers to summarize")


class ResearchAgentResponse(BaseModel):
    """Strict output JSON structure required for the Research Intelligence Agent."""
    research_summary: str = Field(..., description="Overall summary of research findings")
    papers: List[PaperDetail] = Field(..., description="List of structured paper analyses")
    research_gaps: List[str] = Field(..., description="Identified research gaps in current literature")
    recommended_datasets: List[str] = Field(..., description="Recommended datasets for further research/modeling")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Overall confidence score (0.0 to 1.0)")
