from fastapi import APIRouter, HTTPException
from .schemas import PatentAgentRequest, PatentAgentResponse
from .agent import patent_agent

router = APIRouter(
    prefix="/agents/patent-intelligence",
    tags=["Patent Intelligence Agent"]
)


@router.post(
    "/analyze",
    response_model=PatentAgentResponse,
    summary="Run Patent Intelligence Agent Prior-Art & Novelty Analysis",
    description="Analyzes inventions for prior art, computes novelty score (0-100), identifies white-space opportunities, and assesses patent risk."
)
async def analyze_patent(request: PatentAgentRequest) -> PatentAgentResponse:
    try:
        response = await patent_agent.analyze(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Patent Agent Execution Error: {str(e)}"
        )
