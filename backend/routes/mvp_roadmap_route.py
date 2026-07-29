import logging
from fastapi import APIRouter, HTTPException, status
from agents.roadmap_planner.agent import MVPRoadmapAgent
from agents.roadmap_planner.schemas.mvp_roadmap_schema import (
    MvpRoadmapRequest,
    MvpRoadmapResponse,
)
from agents.roadmap_planner.models.domain import MVPRoadmapResult

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/agents/mvp-roadmap",
    tags=["MVP & Roadmap Agent"]
)

agent_instance = MVPRoadmapAgent()


@router.post(
    "/generate",
    response_model=MvpRoadmapResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate MVP & Product Roadmap",
    description="Receives a problem statement and generates an MVP feature set, feature prioritization, product roadmap, milestones, sprint planning, timeline, team size, budget estimation, and risk analysis."
)
async def generate_mvp_roadmap(request: MvpRoadmapRequest) -> MvpRoadmapResponse:
    try:
        return await agent_instance.process_request(request)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in MVP & Roadmap route: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate MVP & Roadmap: {str(e)}"
        )


@router.post(
    "/generate/full",
    response_model=MVPRoadmapResult,
    status_code=status.HTTP_200_OK,
    summary="Generate Full MVP & Product Roadmap with Execution Metadata"
)
async def generate_mvp_roadmap_full(request: MvpRoadmapRequest) -> MVPRoadmapResult:
    try:
        return await agent_instance.execute_full_pipeline(request)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in MVP & Roadmap full route: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate full MVP & Roadmap result: {str(e)}"
        )
