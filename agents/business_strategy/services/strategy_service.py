"""
Business Strategy Service
=========================
Core reasoning engine for the Business Strategy Agent.
Calls the Groq LLM using an 11-step business strategy reasoning prompt
and parses the structured JSON response into Pydantic models.
"""

import json
import logging
import os
import re
from typing import Dict, Any, Optional

from fastapi import HTTPException, status

from agents.business_strategy.config import settings
from agents.business_strategy.schemas.strategy_schema import (
    BusinessStrategyRequest,
    BusinessStrategyResponse,
)
from agents.business_strategy.prompts.system_prompt import (
    BUSINESS_STRATEGY_SYSTEM_PROMPT,
    build_user_prompt,
)

logger = logging.getLogger(__name__)


class BusinessStrategyService:
    """
    Business Strategy Reasoning Engine.

    Executes an 11-step strategy analysis pipeline:
      1. Customer Segments
      2. Value Proposition
      3. Pricing Model
      4. Business Model
      5. Revenue Streams
      6. Go-to-Market Strategy
      7. Marketing Channels
      8. Market Size Estimation
      9. Competitor Identification
     10. SWOT Analysis
     11. Business Model Canvas
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
    ):
        self.api_key = api_key or settings.groq_api_key or os.getenv("GROQ_API_KEY")
        self.model_name = model_name or settings.model_name
        logger.debug(
            "BusinessStrategyService initialised (model=%s)", self.model_name
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def validate_problem_statement(self, problem_statement: str) -> None:
        """
        Validates that the problem statement is meaningful human-readable text
        and not gibberish, symbols, or single-character repetition.

        Raises:
            HTTPException 400: If the input is invalid.
        """
        ps = problem_statement.strip()

        alpha_chars = re.findall(r"[a-zA-Z]", ps)
        if len(alpha_chars) < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Invalid problem statement: Input must contain a meaningful textual "
                    "description of the business idea or problem. "
                    "Numbers or symbols alone are not accepted."
                ),
            )

        unique_chars = set(ps.replace(" ", ""))
        if len(unique_chars) <= 2 and len(ps) > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Invalid problem statement: Repetitive symbols or characters detected. "
                    "Please enter a valid business problem description."
                ),
            )

    async def analyze(
        self, request: BusinessStrategyRequest
    ) -> BusinessStrategyResponse:
        """
        Main entry-point: validates input, calls the LLM, and returns a
        fully-typed BusinessStrategyResponse.

        Args:
            request: Validated BusinessStrategyRequest.

        Returns:
            BusinessStrategyResponse with all 11 strategy components.

        Raises:
            HTTPException 400: Invalid problem statement.
            HTTPException 503: LLM API unavailable or key missing.
        """
        self.validate_problem_statement(request.problem_statement)

        logger.info(
            "Starting 11-step business strategy analysis for: '%s'",
            request.problem_statement[:120],
        )

        if not self.api_key:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=(
                    "LLM API key is missing. "
                    "Please configure GROQ_API_KEY in the .env file."
                ),
            )

        try:
            raw_response = await self._call_llm(request)
            parsed_data = self._parse_json_response(raw_response)
            response = BusinessStrategyResponse(**parsed_data)
            logger.info(
                "Strategy analysis complete. Confidence=%.2f  Business Model=%s",
                response.confidence,
                response.business_model[:80],
            )
            return response

        except HTTPException:
            raise  # Re-raise FastAPI exceptions as-is

        except Exception as exc:
            logger.error("LLM call or parsing failed: %s", exc, exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=(
                    "LLM provider is currently unavailable or returned an unexpected response. "
                    "Please try again later."
                ),
            )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    async def _call_llm(self, request: BusinessStrategyRequest) -> str:
        """
        Makes an async call to the Groq LLM and returns the raw string response.

        Uses response_format={"type": "json_object"} to enforce JSON output.
        """
        from groq import AsyncGroq

        client = AsyncGroq(api_key=self.api_key)
        user_prompt = build_user_prompt(request.problem_statement, request.context)

        logger.info("Calling Groq model '%s' ...", self.model_name)

        chat_response = await client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": BUSINESS_STRATEGY_SYSTEM_PROMPT},
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
        Strips optional markdown fences and parses the JSON payload.

        Args:
            raw_text: Raw string returned by the LLM.

        Returns:
            Parsed Python dict.

        Raises:
            json.JSONDecodeError: If the response is not valid JSON.
        """
        cleaned = raw_text.strip()

        # Strip markdown code fences if present
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        parsed = json.loads(cleaned.strip())
        logger.debug("Successfully parsed JSON response with keys: %s", list(parsed.keys()))
        return parsed
