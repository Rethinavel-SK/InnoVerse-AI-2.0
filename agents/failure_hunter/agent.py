"""
Failure Hunter Agent
=====================
Actively searches for reasons why an innovation could fail.
Challenges assumptions, identifies critical failure points, and suggests mitigations.

Uses Groq LLM with Gemini fallback, following the same pattern as Research/Patent agents.
"""

import asyncio
import json
import logging
import os
from typing import Dict, Any, Optional, List

from .schemas import FailureHunterRequest, FailureHunterResponse, FailureRisk
from .prompts import FAILURE_HUNTER_SYSTEM_PROMPT, FAILURE_HUNTER_PROMPT

logger = logging.getLogger("FailureHunterAgent")


def _sync_call_groq(system_prompt: str, user_prompt: str) -> Optional[str]:
    """Synchronous Groq API call."""
    import urllib.request

    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        return None

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "FailureHunterAgent/2.0"
    }
    payload = {
        "model": os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.4,
        "max_tokens": 2500,
        "response_format": {"type": "json_object"},
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=data, headers=headers, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return body["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logger.error(f"Groq API error in Failure Hunter: {e}")
        return None


class FailureHunterAgent:
    """
    Production-Ready Failure Hunter Agent.
    Challenges innovation ideas by finding their most critical failure risks.
    """

    def __init__(self):
        self.agent_name = "FailureHunterAgent"
        self.version = "2.0.0"

    async def run(
        self, problem_statement: str, context: Optional[Dict[str, Any]] = None
    ) -> FailureHunterResponse:
        request = FailureHunterRequest(
            problem_statement=problem_statement, context=context
        )
        return await self.analyze(request)

    async def analyze(self, request: FailureHunterRequest) -> FailureHunterResponse:
        logger.info("Failure Hunter analyzing: '%s'", request.problem_statement[:60])

        context_section = ""
        if request.context:
            context_section = "ADDITIONAL CONTEXT:\n"
            for k, v in request.context.items():
                context_section += f"- {k}: {v}\n"

        user_prompt = FAILURE_HUNTER_PROMPT.format(
            problem_statement=request.problem_statement,
            context_section=context_section,
        )

        # Try Groq LLM
        raw = await asyncio.to_thread(
            _sync_call_groq, FAILURE_HUNTER_SYSTEM_PROMPT, user_prompt
        )
        if raw:
            try:
                data = json.loads(raw)
                return FailureHunterResponse(**data)
            except Exception as e:
                logger.warning(f"Failed to parse Groq failure analysis: {e}")

        # Try Gemini fallback
        gemini_key = os.getenv("GEMINI_API_KEY", "")
        if gemini_key:
            try:
                from google import genai
                client = genai.Client(api_key=gemini_key)
                full_prompt = FAILURE_HUNTER_SYSTEM_PROMPT + "\n\n" + user_prompt
                response = client.models.generate_content(
                    model=os.getenv("DEFAULT_MODEL", "gemini-2.0-flash"),
                    contents=full_prompt,
                )
                text = response.text.strip()
                if text.startswith("```json"):
                    text = text[7:-3].strip()
                elif text.startswith("```"):
                    text = text[3:-3].strip()
                data = json.loads(text)
                return FailureHunterResponse(**data)
            except Exception as e:
                logger.error(f"Gemini failure analysis error: {e}")

        # Heuristic fallback
        return self._fallback_analysis(request.problem_statement)

    def _fallback_analysis(self, problem_statement: str) -> FailureHunterResponse:
        """Rule-based fallback when LLM is unavailable."""
        return FailureHunterResponse(
            top_failure_risks=[
                FailureRisk(
                    rank=1, risk="Unclear market differentiation from existing solutions",
                    category="competition", probability="HIGH", impact="HIGH",
                    evidence="Most innovation ideas face significant competition from established players.",
                    mitigation="Conduct detailed competitive analysis and identify unique value proposition."
                ),
                FailureRisk(
                    rank=2, risk="Customer acquisition cost may exceed lifetime value",
                    category="cost", probability="MEDIUM", impact="HIGH",
                    evidence="Early-stage products often struggle with unit economics.",
                    mitigation="Validate pricing model with at least 10 potential customers before building."
                ),
                FailureRisk(
                    rank=3, risk="Technical complexity may delay MVP delivery",
                    category="technical", probability="MEDIUM", impact="MEDIUM",
                    evidence="Complex technical solutions often take 2-3x longer than estimated.",
                    mitigation="Define a minimal viable scope and build iteratively."
                ),
                FailureRisk(
                    rank=4, risk="Regulatory or compliance requirements may create barriers",
                    category="regulatory", probability="LOW", impact="HIGH",
                    evidence="Industry-specific regulations can block or delay market entry.",
                    mitigation="Consult with legal experts early in the process."
                ),
                FailureRisk(
                    rank=5, risk="Key technical dependencies may change or become unavailable",
                    category="dependency", probability="LOW", impact="MEDIUM",
                    evidence="Third-party APIs and services can change terms, pricing, or availability.",
                    mitigation="Design with abstraction layers to minimize single-vendor lock-in."
                ),
            ],
            overall_failure_probability="MEDIUM",
            critical_assumption=f"The core assumption is that users will actively seek and pay for a solution to: '{problem_statement[:80]}'.",
            contrarian_view="Even with strong execution, the market may not be ready for this level of innovation — timing risk is real.",
            confidence=0.65,
            classification="INFERENCE",
            summary=f"Failure analysis for '{problem_statement[:50]}...' identified medium overall failure probability. Key risks include competition, unit economics, and technical complexity. All risks have actionable mitigations."
        )


# Singleton
failure_hunter_agent = FailureHunterAgent()
