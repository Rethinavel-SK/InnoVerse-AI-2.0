import logging
from fastapi import APIRouter, HTTPException, status
from agents.business_strategy.agent import BusinessStrategyAgent
from agents.business_strategy.schemas.strategy_schema import (
    BusinessStrategyRequest,
    BusinessStrategyResponse,
)
from agents.business_strategy.models.domain import BusinessStrategyResult

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/agents/business-strategy",
    tags=["Business Strategy Agent"]
)

agent_instance = BusinessStrategyAgent()


@router.post(
    "/analyze",
    response_model=BusinessStrategyResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate 11-Step Business Strategy",
    description="Analyzes a business problem statement and generates customer segments, value proposition, pricing model, revenue streams, GTM strategy, market size (TAM/SAM/SOM), competitor analysis, SWOT, and Business Model Canvas."
)
async def analyze_business_strategy(request: BusinessStrategyRequest) -> BusinessStrategyResponse:
    try:
        return await agent_instance.process_request(request)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in business strategy route: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate business strategy: {str(e)}"
        )


@router.post(
    "/analyze/full",
    response_model=BusinessStrategyResult,
    status_code=status.HTTP_200_OK,
    summary="Generate Full Business Strategy with Execution Metadata"
)
async def analyze_business_strategy_full(request: BusinessStrategyRequest) -> BusinessStrategyResult:
    try:
        return await agent_instance.execute_full_pipeline(request)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in business strategy full route: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate full business strategy result: {str(e)}"
        )
