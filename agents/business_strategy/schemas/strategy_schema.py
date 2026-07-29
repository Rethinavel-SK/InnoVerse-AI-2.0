from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Request Schema
# ---------------------------------------------------------------------------

class BusinessStrategyRequest(BaseModel):
    """Input schema for the Business Strategy Agent."""
    problem_statement: str = Field(
        ...,
        min_length=10,
        description="A description of the business problem, idea, or domain to analyze.",
        examples=[
            "Build an AI-powered platform that helps small restaurants manage inventory and reduce food waste.",
            "Create a SaaS product for remote team collaboration and productivity tracking.",
        ]
    )
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional context: target region, budget, industry, company stage, etc."
    )


# ---------------------------------------------------------------------------
# Nested Output Models
# ---------------------------------------------------------------------------

class CustomerSegment(BaseModel):
    segment_name: str = Field(..., description="Name of the customer segment")
    description: str = Field(..., description="Who these customers are and their key pain points")
    size_estimate: str = Field(..., description="Approximate addressable size of this segment")
    willingness_to_pay: str = Field(..., description="Expected price sensitivity: Low | Medium | High")


class RevenueStream(BaseModel):
    stream_name: str = Field(..., description="Name of the revenue stream (e.g., Subscription, Licensing)")
    description: str = Field(..., description="How this revenue stream works")
    estimated_contribution: str = Field(..., description="Estimated percentage contribution to total revenue")


class Competitor(BaseModel):
    name: str = Field(..., description="Competitor company or product name")
    strengths: str = Field(..., description="Key strengths of this competitor")
    weaknesses: str = Field(..., description="Key weaknesses or gaps")
    differentiation: str = Field(..., description="How this startup differentiates from this competitor")


class SWOTAnalysis(BaseModel):
    strengths: List[str] = Field(default_factory=list, description="Internal strengths of the business")
    weaknesses: List[str] = Field(default_factory=list, description="Internal weaknesses or limitations")
    opportunities: List[str] = Field(default_factory=list, description="External opportunities in the market")
    threats: List[str] = Field(default_factory=list, description="External threats or risks")


class BusinessModelCanvas(BaseModel):
    key_partners: List[str] = Field(default_factory=list, description="Strategic partners and suppliers")
    key_activities: List[str] = Field(default_factory=list, description="Core activities to deliver the value proposition")
    key_resources: List[str] = Field(default_factory=list, description="Critical assets required")
    value_propositions: List[str] = Field(default_factory=list, description="Unique value delivered to customers")
    customer_relationships: List[str] = Field(default_factory=list, description="Type of relationship with each segment")
    channels: List[str] = Field(default_factory=list, description="How the product reaches customers")
    customer_segments: List[str] = Field(default_factory=list, description="Target customer groups")
    cost_structure: List[str] = Field(default_factory=list, description="Major cost drivers")
    revenue_streams: List[str] = Field(default_factory=list, description="Revenue mechanisms")


class MarketSizeEstimate(BaseModel):
    tam: str = Field(..., description="Total Addressable Market (TAM)")
    sam: str = Field(..., description="Serviceable Addressable Market (SAM)")
    som: str = Field(..., description="Serviceable Obtainable Market (SOM)")
    rationale: str = Field(..., description="Methodology and reasoning behind the market size estimates")


# ---------------------------------------------------------------------------
# Top-Level Response Schema
# ---------------------------------------------------------------------------

class BusinessStrategyResponse(BaseModel):
    """Complete business strategy output produced by the agent."""

    # Core outputs
    target_customers: List[CustomerSegment] = Field(
        ..., description="Identified customer segments with persona details"
    )
    value_proposition: str = Field(
        ..., description="Concise, compelling value proposition statement"
    )
    pricing_model: str = Field(
        ..., description="Recommended pricing model with justification (e.g., Freemium, Usage-Based, Tiered SaaS)"
    )
    business_model: str = Field(
        ..., description="Core business model type (e.g., B2B SaaS, Marketplace, D2C, Platform)"
    )
    revenue_streams: List[RevenueStream] = Field(
        default_factory=list, description="Diversified revenue streams with contribution estimates"
    )
    go_to_market: str = Field(
        ..., description="Phased go-to-market strategy narrative"
    )
    marketing_channels: List[str] = Field(
        default_factory=list, description="Recommended marketing and distribution channels"
    )
    market_size: MarketSizeEstimate = Field(
        ..., description="TAM / SAM / SOM market size estimates"
    )
    competitors: List[Competitor] = Field(
        default_factory=list, description="Key competitors with strengths, weaknesses, and differentiation"
    )
    swot: SWOTAnalysis = Field(
        ..., description="SWOT analysis for this business idea"
    )
    business_canvas: BusinessModelCanvas = Field(
        ..., description="Business Model Canvas (Osterwalder framework)"
    )

    # Meta
    reasoning: List[str] = Field(
        default_factory=list, description="Step-by-step reasoning chain used to generate the strategy"
    )
    confidence: float = Field(
        default=0.7, ge=0.0, le=1.0,
        description="Confidence score: decreases with vague or underspecified input. Defaults to 0.7 if LLM omits it."
    )
