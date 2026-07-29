from typing import List, Optional, Union, Dict, Any
from pydantic import BaseModel, Field


class RiskAssessmentRequest(BaseModel):
    """Input request model for Risk Assessment Agent."""
    problem_statement: str = Field(..., description="The startup problem statement or solution description.")


class RiskItem(BaseModel):
    """Detailed risk description item."""
    category: str = Field(..., description="Risk category: Technical, Financial, Legal, or Security")
    title: str = Field(..., description="Short title of the risk")
    description: str = Field(..., description="Detailed description of the risk")
    severity: str = Field("Medium", description="Severity level: High, Medium, Low")


class MitigationItem(BaseModel):
    """Mitigation strategy item."""
    risk_title: str = Field(..., description="The title or topic of the risk being mitigated")
    strategy: str = Field(..., description="Practical actionable solution for the risk")


class RiskAssessmentResponse(BaseModel):
    """Successful output response schema matching exact requirements."""
    agent_name: str = Field("Risk Assessment Agent", description="Agent name identifier")
    status: str = Field("success", description="Status of execution: success")
    overall_risk_score: int = Field(..., ge=0, le=100, description="Overall risk score from 0-100")
    risk_level: str = Field(..., description="Risk level category: Low, Medium, High, Critical")
    technical_risks: List[Union[str, Dict[str, Any]]] = Field(default_factory=list, description="Technical risks identified")
    financial_risks: List[Union[str, Dict[str, Any]]] = Field(default_factory=list, description="Financial risks identified")
    legal_risks: List[Union[str, Dict[str, Any]]] = Field(default_factory=list, description="Legal risks identified")
    security_risks: List[Union[str, Dict[str, Any]]] = Field(default_factory=list, description="Security risks identified")
    mitigation: List[Union[str, Dict[str, Any]]] = Field(default_factory=list, description="Mitigation strategies")
    summary: str = Field(..., description="Executive summary of overall risk assessment")


class ErrorResponse(BaseModel):
    """Error output response schema matching exact requirements."""
    status: str = Field("failed", description="Status of execution: failed")
    error: str = Field(..., description="Reason for failure")
