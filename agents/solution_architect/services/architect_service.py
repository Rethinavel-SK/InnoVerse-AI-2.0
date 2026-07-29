import json
import logging
import os
import re
from typing import Dict, Any, Optional

from fastapi import HTTPException, status
from agents.solution_architect.config import settings
from agents.solution_architect.schemas.architect_schema import (
    SolutionArchitectRequest,
    SolutionArchitectResponse,
    ProblemAnalysis,
    IdentifiedRequirements,
    ArchitectureSelection,
)
from agents.solution_architect.prompts.system_prompt import (
    SOLUTION_ARCHITECT_SYSTEM_PROMPT,
    build_user_prompt,
)

logger = logging.getLogger(__name__)


class SolutionArchitectService:
    """
    Principal Solution Architect Reasoning Engine.
    Executes a 7-step architectural reasoning process:
    Problem -> Requirements -> Architecture -> Technologies -> Cost.
    """

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or settings.groq_api_key or os.getenv("GROQ_API_KEY")
        self.model_name = model_name or settings.model_name

    def validate_problem_statement(self, problem_statement: str) -> None:
        """
        Validates that the problem statement contains meaningful human text and is not gibberish/symbols/numbers.
        """
        ps = problem_statement.strip()
        alpha_chars = re.findall(r'[a-zA-Z]', ps)
        if len(alpha_chars) < 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid problem statement: Input must contain a meaningful textual description of the problem to solve. Numbers or symbols alone are not allowed."
            )
            
        unique_chars = set(ps.replace(" ", ""))
        if len(unique_chars) <= 2 and len(ps) > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid problem statement: Repetitive symbols or characters detected. Please enter a valid problem statement."
            )

    async def analyze_and_design(
        self, request: SolutionArchitectRequest
    ) -> SolutionArchitectResponse:
        """
        Processes a problem statement using 7-step architectural reasoning.
        """
        self.validate_problem_statement(request.problem_statement)
        logger.info(f"Starting 7-step architectural analysis for: '{request.problem_statement}'")

        if not self.api_key:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="LLM API key is missing. Please configure GROQ_API_KEY in .env file."
            )

        try:
            raw_response = await self._call_llm(request)
            parsed_data = self._parse_json_response(raw_response)
            return SolutionArchitectResponse(**parsed_data)
        except Exception as e:
            logger.error(f"LLM API call failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="LLM Provider is currently unavailable. Please try again later."
            )

    async def _call_llm(self, request: SolutionArchitectRequest) -> str:
        """
        Async call to Groq LLM (llama-3.3-70b-versatile).
        """
        from groq import AsyncGroq

        client = AsyncGroq(api_key=self.api_key)
        user_prompt = build_user_prompt(request.problem_statement, request.context)

        logger.info(f"Calling Groq model {self.model_name}...")
        response = await client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": SOLUTION_ARCHITECT_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=settings.temperature,
            response_format={"type": "json_object"},
            timeout=settings.request_timeout,
        )
        return response.choices[0].message.content

    def _parse_json_response(self, raw_text: str) -> Dict[str, Any]:
        """
        Parses JSON from raw text response.
        """
        cleaned_text = raw_text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
        return json.loads(cleaned_text.strip())


