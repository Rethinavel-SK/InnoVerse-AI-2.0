from fastapi import APIRouter, HTTPException, status
from .schemas import ResearchAgentRequest, ResearchAgentResponse
from .agent import research_agent

router = APIRouter(
    prefix="/agents/research-intelligence",
    tags=["Research Intelligence Agent"]
)


@router.post(
    "/analyze",
    response_model=ResearchAgentResponse,
    status_code=status.HTTP_200_OK,
    summary="Run Research Intelligence Agent Analysis",
    description="Analyzes a problem statement, queries Semantic Scholar/arXiv/CrossRef, summarizes papers, extracts methodologies, and outputs structured JSON analysis."
)
async def analyze_research(request: ResearchAgentRequest) -> ResearchAgentResponse:
    try:
        response = await research_agent.analyze(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Research Agent Execution Error: {str(e)}"
        )
