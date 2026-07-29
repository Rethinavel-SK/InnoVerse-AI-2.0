"""
MVP & Roadmap Service
=====================
Core reasoning engine for the MVP & Roadmap Agent.
Calls Groq LLM using an 9-point CPO reasoning prompt and parses
structured JSON output into Pydantic response models.
"""

import json
import logging
import os
import re
from typing import Dict, Any, Optional

from fastapi import HTTPException, status

from agents.roadmap_planner.config import settings
from agents.roadmap_planner.schemas.mvp_roadmap_schema import (
    MvpRoadmapRequest,
    MvpRoadmapResponse,
)
from agents.roadmap_planner.prompts.system_prompt import (
    MVP_ROADMAP_SYSTEM_PROMPT,
    build_user_prompt,
)

logger = logging.getLogger(__name__)


class MVPRoadmapService:
    """
    MVP & Roadmap Reasoning Engine.

    Executes 9 core analysis steps:
      1. Generate MVP core features
      2. Prioritize future features
      3. Create product roadmap phases
      4. Divide development into sequential milestones
      5. Formulate sprint-by-sprint planning
      6. Estimate overall timeline
      7. Recommend team composition & size
      8. Estimate development budget
      9. Identify development risks & mitigations
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
    ):
        self.api_key = api_key or settings.groq_api_key or os.getenv("GROQ_API_KEY")
        self.model_name = model_name or settings.model_name
        logger.debug("MVPRoadmapService initialised (model=%s)", self.model_name)

    def validate_problem_statement(self, problem_statement: str) -> None:
        """
        Validates that the problem statement contains meaningful text.

        Raises:
            HTTPException 400: If the input is invalid.
        """
        if not problem_statement or not problem_statement.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Problem statement cannot be empty."
            )

        ps = problem_statement.strip()
        alpha_chars = re.findall(r"[a-zA-Z]", ps)
        if len(alpha_chars) < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Invalid problem statement: Input must contain a meaningful textual "
                    "description of the problem or product vision."
                ),
            )

        unique_chars = set(ps.replace(" ", ""))
        if len(unique_chars) <= 2 and len(ps) > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid problem statement: Repetitive symbols detected."
            )

    async def analyze(self, request: MvpRoadmapRequest) -> MvpRoadmapResponse:
        """
        Main entry-point: validates input, calls LLM async, and parses response.

        Args:
            request: Validated MvpRoadmapRequest.

        Returns:
            MvpRoadmapResponse matching required schema.
        """
        self.validate_problem_statement(request.problem_statement)

        logger.info(
            "Starting MVP & Roadmap generation for: '%s'",
            request.problem_statement[:120],
        )

        if not self.api_key:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="LLM API key is missing. Please configure GROQ_API_KEY in .env file."
            )

        try:
            raw_response = await self._call_llm(request)
            parsed_data = self._parse_json_response(raw_response)
            response = MvpRoadmapResponse(**parsed_data)

            logger.info(
                "MVP & Roadmap successfully generated. Confidence=%.2f | Features Count=%d",
                response.confidence,
                len(response.mvp_features),
            )
            return response

        except HTTPException:
            raise
        except Exception as exc:
            logger.error("LLM call or JSON parsing failed: %s", exc, exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"LLM provider unavailable or invalid response: {str(exc)}"
            )

    async def _call_llm(self, request: MvpRoadmapRequest) -> str:
        """
        Makes an async call to Groq LLM API.
        """
        from groq import AsyncGroq

        client = AsyncGroq(api_key=self.api_key)
        user_prompt = build_user_prompt(request.problem_statement, request.context)

        logger.info("Calling Groq LLM model '%s' ...", self.model_name)

        chat_response = await client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": MVP_ROADMAP_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
            response_format={"type": "json_object"},
            timeout=settings.request_timeout,
        )

        raw_content = chat_response.choices[0].message.content
        logger.debug("Raw LLM response (first 300 chars): %s", raw_content[:300])
        return raw_content

    def _parse_json_response(self, raw_text: str) -> Dict[str, Any]:
        """
        Cleans markdown formatting and parses JSON payload into a dictionary.
        """
        cleaned = raw_text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        parsed = json.loads(cleaned.strip())
        logger.debug("Parsed JSON keys: %s", list(parsed.keys()))
        return parsed
