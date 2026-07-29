"""
Business Strategy Agent
=======================
Production-ready AI agent that performs a full 11-step business strategy
analysis given a problem statement or business idea.

Usage:
    agent = BusinessStrategyAgent()
    response = await agent.run("Build an AI-powered platform for restaurant inventory management.")

    # Or with additional context:
    response = await agent.run(
        "Build a SaaS platform for remote team productivity.",
        context={"region": "North America", "stage": "Pre-seed", "budget": "$500K"}
    )
"""

import logging
import time
import uuid
from typing import Dict, Any, Optional

from agents.business_strategy.schemas.strategy_schema import (
    BusinessStrategyRequest,
    BusinessStrategyResponse,
)
from agents.business_strategy.services.strategy_service import BusinessStrategyService
from agents.business_strategy.models.domain import ExecutionMetadata, BusinessStrategyResult

logger = logging.getLogger(__name__)


class BusinessStrategyAgent:
    """
    Production-Ready Business Strategy Agent.

    Responsibilities:
    - Generate a business model.
    - Identify customer segments.
    - Define the value proposition.
    - Recommend pricing models.
    - Create revenue streams.
    - Suggest go-to-market strategy.
    - Recommend marketing channels.
    - Estimate market size (TAM/SAM/SOM).
    - Identify competitors with differentiation analysis.
    - Perform SWOT analysis.
    - Generate a Business Model Canvas (Osterwalder framework).
    """

    def __init__(self, service: Optional[BusinessStrategyService] = None):
        self.agent_name = "BusinessStrategyAgent"
        self.version = "1.0.0"
        self.service = service or BusinessStrategyService()
        logger.info(
            "Initialized %s (v%s) using model: %s",
            self.agent_name,
            self.version,
            self.service.model_name,
        )

    # ------------------------------------------------------------------
    # Primary public interface
    # ------------------------------------------------------------------

    async def run(
        self,
        problem_statement: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> BusinessStrategyResponse:
        """
        Main entry-point for the Business Strategy Agent.

        Args:
            problem_statement: A description of the business idea or problem to analyse.
            context: Optional dict with hints (e.g., region, stage, budget, target industry).

        Returns:
            BusinessStrategyResponse: Fully structured strategy output.
        """
        request = BusinessStrategyRequest(
            problem_statement=problem_statement,
            context=context,
        )
        return await self.process_request(request)

    async def process_request(
        self, request: BusinessStrategyRequest
    ) -> BusinessStrategyResponse:
        """
        Processes a BusinessStrategyRequest and returns a structured response.

        Args:
            request: Validated BusinessStrategyRequest Pydantic model.

        Returns:
            BusinessStrategyResponse
        """
        start_time = time.perf_counter()
        logger.info(
            "[%s] Processing strategy request for: '%s'",
            self.agent_name,
            request.problem_statement[:100],
        )

        try:
            response = await self.service.analyze(request)
            elapsed_ms = (time.perf_counter() - start_time) * 1000

            logger.info(
                "[%s] Strategy generated successfully in %.2fms | "
                "Business Model: %s | Confidence: %.2f",
                self.agent_name,
                elapsed_ms,
                response.business_model[:60],
                response.confidence,
            )
            return response

        except Exception as exc:
            logger.error(
                "[%s] Exception during strategy generation: %s",
                self.agent_name,
                exc,
                exc_info=True,
            )
            raise

    async def execute_full_pipeline(
        self, request: BusinessStrategyRequest
    ) -> BusinessStrategyResult:
        """
        Executes the full strategy pipeline and wraps the result with
        execution metadata (request_id, timing, model info).

        Args:
            request: Validated BusinessStrategyRequest.

        Returns:
            BusinessStrategyResult: Strategy output + ExecutionMetadata.
        """
        start_time = time.perf_counter()
        request_id = str(uuid.uuid4())

        logger.info(
            "[%s] Starting full pipeline (request_id=%s)",
            self.agent_name,
            request_id,
        )

        response = await self.process_request(request)
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        metadata = ExecutionMetadata(
            agent_name=self.agent_name,
            version=self.version,
            execution_time_ms=round(elapsed_ms, 2),
            model_used=self.service.model_name,
        )

        result = BusinessStrategyResult(
            request_id=request_id,
            metadata=metadata,
            strategy_output=response.model_dump(),
        )

        logger.info(
            "[%s] Full pipeline complete (request_id=%s, elapsed=%.2fms)",
            self.agent_name,
            request_id,
            elapsed_ms,
        )
        return result
