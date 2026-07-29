"""
MVP & Roadmap Agent
===================
Production-ready AI agent that generates an MVP feature set, prioritizes features,
creates a product roadmap, divides development into milestones, suggests sprint plans,
estimates timeline, recommends team size, estimates budget, and identifies development risks.

Usage:
    agent = MVPRoadmapAgent()
    response = await agent.run("Build an AI platform for legal document analysis.")
"""

import logging
import time
import uuid
from typing import Dict, Any, Optional

from agents.roadmap_planner.schemas.mvp_roadmap_schema import (
    MvpRoadmapRequest,
    MvpRoadmapResponse,
)
from agents.roadmap_planner.services.roadmap_service import MVPRoadmapService
from agents.roadmap_planner.models.domain import ExecutionMetadata, MVPRoadmapResult

logger = logging.getLogger(__name__)


class MVPRoadmapAgent:
    """
    Production-Ready MVP & Roadmap Agent.

    Responsibilities:
    - Generate an MVP
    - Prioritize features
    - Create a product roadmap
    - Divide development into milestones
    - Suggest sprint planning
    - Estimate timeline
    - Recommend team size
    - Estimate budget
    - Identify risks during development
    """

    def __init__(self, service: Optional[MVPRoadmapService] = None):
        self.agent_name = "MVPRoadmapAgent"
        self.version = "1.0.0"
        self.service = service or MVPRoadmapService()
        logger.info(
            "Initialized %s (v%s) using model: %s",
            self.agent_name,
            self.version,
            self.service.model_name,
        )

    async def run(
        self,
        problem_statement: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> MvpRoadmapResponse:
        """
        Main entry-point for the MVP & Roadmap Agent.

        Args:
            problem_statement: Description of the business problem or product vision.
            context: Optional dict with hints (e.g. target industry, budget, tech constraints).

        Returns:
            MvpRoadmapResponse: Fully structured roadmap & MVP output.
        """
        request = MvpRoadmapRequest(
            problem_statement=problem_statement,
            context=context,
        )
        return await self.process_request(request)

    async def process_request(
        self, request: MvpRoadmapRequest
    ) -> MvpRoadmapResponse:
        """
        Processes an MvpRoadmapRequest and returns a structured MvpRoadmapResponse.
        """
        start_time = time.perf_counter()
        logger.info(
            "[%s] Processing request for: '%s'",
            self.agent_name,
            request.problem_statement[:100],
        )

        try:
            response = await self.service.analyze(request)
            elapsed_ms = (time.perf_counter() - start_time) * 1000

            logger.info(
                "[%s] MVP & Roadmap generated in %.2fms | Confidence: %.2f",
                self.agent_name,
                elapsed_ms,
                response.confidence,
            )
            return response

        except Exception as exc:
            logger.error(
                "[%s] Exception during MVP & Roadmap generation: %s",
                self.agent_name,
                exc,
                exc_info=True,
            )
            raise

    async def execute_full_pipeline(
        self, request: MvpRoadmapRequest
    ) -> MVPRoadmapResult:
        """
        Executes the full agent pipeline and wraps result with execution metadata.
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

        result = MVPRoadmapResult(
            request_id=request_id,
            metadata=metadata,
            roadmap_output=response.model_dump(),
        )

        logger.info(
            "[%s] Full pipeline complete (request_id=%s, elapsed=%.2fms)",
            self.agent_name,
            request_id,
            elapsed_ms,
        )
        return result
