import logging
from fastapi import APIRouter, HTTPException, status
from agents.solution_architect.agent import SolutionArchitectAgent
from agents.solution_architect.schemas.architect_schema import (
    SolutionArchitectRequest,
    SolutionArchitectResponse,
)
from agents.solution_architect.models.domain import SolutionDesignResult

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/agents/solution-architect",
    tags=["Solution Architect Agent"]
)

agent_instance = SolutionArchitectAgent()


@router.post(
    "/analyze",
    response_model=SolutionArchitectResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Technical Solution Architecture",
    description="Receives a validated problem statement and returns comprehensive software architecture recommendations."
)
async def analyze_problem_statement(request: SolutionArchitectRequest) -> SolutionArchitectResponse:
    try:
        return await agent_instance.process_request(request)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in solution architect route: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate solution architecture: {str(e)}"
        )


@router.post(
    "/analyze/full",
    response_model=SolutionDesignResult,
    status_code=status.HTTP_200_OK,
    summary="Generate Full Solution Architecture with Execution Metadata"
)
async def analyze_problem_statement_full(request: SolutionArchitectRequest) -> SolutionDesignResult:
    try:
        return await agent_instance.execute_full_pipeline(request)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in solution architect full route: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate full solution architecture: {str(e)}"
        )
