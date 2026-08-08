"""
Innovation Director Agent
===========================
Production-ready master AI orchestrator that coordinates 9 specialist agents:
1. Solution Architect Agent
2. Business Strategy Agent
3. Research Agent
4. Patent Analysis Agent
5. Market Analysis Agent
6. Trend Analysis Agent
7. Risk Assessment Agent
8. Sustainability Agent
9. MVP & Roadmap Planner Agent

Usage:
    agent = InnovationDirectorAgent()
    response = await agent.run("Build an AI platform for legal document analysis.")
"""

import logging
import time
import uuid
from typing import Dict, Any, Optional

from agents.innovation_director.schemas.director_schema import (
    InnovationDirectorRequest,
    InnovationDirectorResponse,
)
from agents.innovation_director.services.director_service import InnovationDirectorService
from agents.innovation_director.models.domain import ExecutionMetadata, InnovationDirectorResult

logger = logging.getLogger(__name__)


class InnovationDirectorAgent:
    """
    Production-Ready Innovation Director Agent.
    Master orchestrator coordinating 9 specialist AI agents.
    """

    def __init__(self, service: Optional[InnovationDirectorService] = None):
        self.agent_name = "InnovationDirectorAgent"
        self.version = "1.0.0"
        self.service = service or InnovationDirectorService()
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
    ) -> InnovationDirectorResponse:
        """
        Main entry-point for the Innovation Director Agent.
        """
        request = InnovationDirectorRequest(
            problem_statement=problem_statement,
            context=context,
        )
        return await self.process_request(request)

    async def process_request(
        self, request: InnovationDirectorRequest
    ) -> InnovationDirectorResponse:
        """
        Processes request across all 9 specialist agents.
        """
        start_time = time.perf_counter()
        logger.info(
            "[%s] Orchestrating discovery across specialist agents for: '%s'",
            self.agent_name,
            request.problem_statement[:100],
        )

        try:
            response = await self.service.analyze_and_orchestrate(request)
            elapsed_ms = (time.perf_counter() - start_time) * 1000

            logger.info(
                "[%s] Master discovery complete in %.2fms | Score: %.1f | Confidence: %.2f",
                self.agent_name,
                elapsed_ms,
                response.overall_innovation_score,
                response.confidence,
            )
            return response

        except Exception as exc:
            logger.error(
                "[%s] Exception during orchestration: %s",
                self.agent_name,
                exc,
                exc_info=True,
            )
            raise

    async def execute_full_pipeline(
        self, request: InnovationDirectorRequest
    ) -> InnovationDirectorResult:
        """
        Executes full orchestration pipeline with metadata.
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

        completed_agents = sum(1 for v in response.agent_status.values() if v == "Completed")

        metadata = ExecutionMetadata(
            agent_name=self.agent_name,
            version=self.version,
            execution_time_ms=round(elapsed_ms, 2),
            model_used=self.service.model_name,
            agents_executed=completed_agents,
        )

        result = InnovationDirectorResult(
            request_id=request_id,
            metadata=metadata,
            director_output=response.model_dump(),
        )

        return result
