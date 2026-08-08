import logging
from fastapi import APIRouter, HTTPException, status
from agents.innovation_director.agent import InnovationDirectorAgent
from agents.innovation_director.schemas.director_schema import (
    InnovationDirectorRequest,
    InnovationDirectorResponse,
)
from agents.innovation_director.models.domain import InnovationDirectorResult

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/agents/innovation-director",
    tags=["Innovation Director Agent"]
)

agent_instance = InnovationDirectorAgent()


@router.post(
    "/analyze",
    response_model=InnovationDirectorResponse,
    status_code=status.HTTP_200_OK,
    summary="Run Master Innovation Discovery Analysis",
    description="Orchestrates execution across all 9 specialist AI agents and returns master executive synthesis and detailed reports."
)
async def analyze_innovation_concept(request: InnovationDirectorRequest) -> InnovationDirectorResponse:
    try:
        return await agent_instance.process_request(request)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in Innovation Director route: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to complete master innovation discovery: {str(e)}"
        )


@router.post(
    "/analyze/full",
    response_model=InnovationDirectorResult,
    status_code=status.HTTP_200_OK,
    summary="Run Master Innovation Discovery with Execution Metadata"
)
async def analyze_innovation_concept_full(request: InnovationDirectorRequest) -> InnovationDirectorResult:
    try:
        return await agent_instance.execute_full_pipeline(request)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in Innovation Director full route: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate full innovation result: {str(e)}"
        )
