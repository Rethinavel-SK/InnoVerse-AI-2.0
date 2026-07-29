import logging
import time
import uuid
from typing import Dict, Any, Optional

from agents.solution_architect.schemas.architect_schema import (
    SolutionArchitectRequest,
    SolutionArchitectResponse,
)
from agents.solution_architect.services.architect_service import SolutionArchitectService
from agents.solution_architect.models.domain import ExecutionMetadata, SolutionDesignResult

logger = logging.getLogger(__name__)


class SolutionArchitectAgent:
    """
    Production-Ready Solution Architect Agent for Innovation Discovery Platform.
    Receives a validated problem statement and designs the best technical solution.
    """

    def __init__(self, service: Optional[SolutionArchitectService] = None):
        self.agent_name = "SolutionArchitectAgent"
        self.version = "1.0.0"
        self.service = service or SolutionArchitectService()
        logger.info(f"Initialized {self.agent_name} (v{self.version})")

    async def run(self, problem_statement: str, context: Optional[Dict[str, Any]] = None) -> SolutionArchitectResponse:
        """
        Main execution method for the Solution Architect Agent.
        
        Args:
            problem_statement: The target problem description to architect.
            context: Optional context map (scale requirements, budgets, etc.)
            
        Returns:
            SolutionArchitectResponse: Pydantic model with structured technical architecture.
        """
        request = SolutionArchitectRequest(
            problem_statement=problem_statement,
            context=context
        )
        return await self.process_request(request)

    async def process_request(self, request: SolutionArchitectRequest) -> SolutionArchitectResponse:
        """
        Processes a SolutionArchitectRequest and returns structured response.
        """
        start_time = time.perf_counter()
        logger.info(f"[{self.agent_name}] Processing architecture request...")

        try:
            response = await self.service.analyze_and_design(request)
            execution_time = (time.perf_counter() - start_time) * 1000

            logger.info(
                f"[{self.agent_name}] Successfully generated solution architecture "
                f"in {execution_time:.2f}ms (Complexity: {response.estimated_complexity})"
            )
            return response
        except Exception as e:
            logger.error(f"[{self.agent_name}] Exception encountered during execution: {e}", exc_info=True)
            raise e

    async def execute_full_pipeline(self, request: SolutionArchitectRequest) -> SolutionDesignResult:
        """
        Executes full pipeline and returns response wrapped with execution metadata.
        """
        start_time = time.perf_counter()
        request_id = str(uuid.uuid4())
        response = await self.process_request(request)
        execution_time = (time.perf_counter() - start_time) * 1000

        metadata = ExecutionMetadata(
            agent_name=self.agent_name,
            version=self.version,
            execution_time_ms=round(execution_time, 2),
            model_used=self.service.model_name
        )

        return SolutionDesignResult(
            request_id=request_id,
            metadata=metadata,
            architecture_output=response.model_dump()
        )
