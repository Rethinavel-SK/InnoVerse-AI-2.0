from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
from .schemas import RiskAssessmentRequest, RiskAssessmentResponse, ErrorResponse
from .agent import execute

router = APIRouter(
    prefix="/agents/risk-assessment",
    tags=["Risk Assessment Agent"]
)


@router.post(
    "/analyze",
    summary="Run Risk Assessment Analysis",
    description="Analyzes startup problem statement across technical, financial, legal, and security risks with mitigations."
)
async def analyze_risk(request: RiskAssessmentRequest) -> Dict[str, Any]:
    try:
        response = execute(request.problem_statement)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Risk Assessment Execution Error: {str(e)}"
        )
