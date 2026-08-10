"""
Execution Planner Agent
========================
Converts innovation analysis into actionable execution tasks,
milestones, validation experiments, and deadlines.

Uses Groq LLM with Gemini fallback.
"""

import asyncio
import json
import logging
import os
from typing import Dict, Any, Optional

from .schemas import (
    ExecutionPlannerRequest, ExecutionPlannerResponse,
    ExecutionPlan, Milestone, ExecutionTask, ValidationExperiment,
)
from .prompts import EXECUTION_PLANNER_SYSTEM_PROMPT, EXECUTION_PLANNER_PROMPT

logger = logging.getLogger("ExecutionPlannerAgent")


def _sync_call_groq(system_prompt: str, user_prompt: str) -> Optional[str]:
    """Synchronous Groq API call."""
    import urllib.request

    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        return None

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "ExecutionPlannerAgent/2.0"
    }
    payload = {
        "model": os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 3000,
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
        logger.error(f"Groq API error in Execution Planner: {e}")
        return None


class ExecutionPlannerAgent:
    """
    Production-Ready Execution Planner Agent.
    Generates actionable execution plans from innovation analysis.
    """

    def __init__(self):
        self.agent_name = "ExecutionPlannerAgent"
        self.version = "2.0.0"

    async def run(
        self, problem_statement: str, context: Optional[Dict[str, Any]] = None,
        analysis_summary: Optional[str] = None
    ) -> ExecutionPlannerResponse:
        request = ExecutionPlannerRequest(
            problem_statement=problem_statement,
            context=context,
            analysis_summary=analysis_summary,
        )
        return await self.analyze(request)

    async def analyze(self, request: ExecutionPlannerRequest) -> ExecutionPlannerResponse:
        logger.info("Execution Planner processing: '%s'", request.problem_statement[:60])

        context_section = ""
        if request.context:
            context_section = "ADDITIONAL CONTEXT:\n"
            for k, v in request.context.items():
                context_section += f"- {k}: {v}\n"

        analysis_context = ""
        if request.analysis_summary:
            analysis_context = f"ANALYSIS SUMMARY:\n{request.analysis_summary}\n"

        user_prompt = EXECUTION_PLANNER_PROMPT.format(
            problem_statement=request.problem_statement,
            context_section=context_section,
            analysis_context=analysis_context,
        )

        # Try Groq LLM
        raw = await asyncio.to_thread(
            _sync_call_groq, EXECUTION_PLANNER_SYSTEM_PROMPT, user_prompt
        )
        if raw:
            try:
                data = json.loads(raw)
                return ExecutionPlannerResponse(**data)
            except Exception as e:
                logger.warning(f"Failed to parse Groq execution plan: {e}")

        # Try Gemini fallback
        gemini_key = os.getenv("GEMINI_API_KEY", "")
        if gemini_key:
            try:
                from google import genai
                client = genai.Client(api_key=gemini_key)
                full_prompt = EXECUTION_PLANNER_SYSTEM_PROMPT + "\n\n" + user_prompt
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
                return ExecutionPlannerResponse(**data)
            except Exception as e:
                logger.error(f"Gemini execution plan error: {e}")

        # Heuristic fallback
        return self._fallback_plan(request.problem_statement)

    def _fallback_plan(self, problem_statement: str) -> ExecutionPlannerResponse:
        """Rule-based fallback when LLM is unavailable."""
        short = problem_statement[:60]
        return ExecutionPlannerResponse(
            execution_plan=ExecutionPlan(
                recommended_approach=f"Phased MVP approach for '{short}' — validate market demand first, then build core product, then scale.",
                total_estimated_weeks=16,
                milestones=[
                    Milestone(
                        milestone="Market Validation Complete",
                        description="Validate demand through customer interviews and competitor analysis.",
                        target_week=4,
                        deliverables=["10 customer interviews completed", "Competitor analysis report", "Validated value proposition"]
                    ),
                    Milestone(
                        milestone="MVP Prototype Ready",
                        description="Build and test minimum viable product with core features.",
                        target_week=10,
                        deliverables=["Working prototype", "Core feature set implemented", "Internal testing completed"]
                    ),
                    Milestone(
                        milestone="Pilot Launch",
                        description="Launch with initial users and gather feedback.",
                        target_week=14,
                        deliverables=["5 pilot users onboarded", "Feedback collection system", "Iteration plan"]
                    ),
                ],
                tasks=[
                    ExecutionTask(title="Interview 10 potential customers", description="Conduct structured interviews to validate demand and understand pain points.", category="customer", priority="HIGH", estimated_days=10, suggested_owner="Product Lead", deadline_offset_days=14, success_criteria="10 interviews completed with documented insights"),
                    ExecutionTask(title="Competitive landscape analysis", description="Map direct and indirect competitors, identify gaps.", category="research", priority="HIGH", estimated_days=5, suggested_owner="Research Lead", deadline_offset_days=10, success_criteria="Competitor matrix with differentiation analysis"),
                    ExecutionTask(title="Define MVP feature scope", description="Identify minimum feature set for first release.", category="business", priority="HIGH", estimated_days=3, suggested_owner="Product Lead", deadline_offset_days=7, dependencies=["Interview 10 potential customers"], success_criteria="Prioritized feature list approved"),
                    ExecutionTask(title="Design system architecture", description="Create technical architecture for MVP.", category="technical", priority="HIGH", estimated_days=5, suggested_owner="Tech Lead", deadline_offset_days=21, dependencies=["Define MVP feature scope"], success_criteria="Architecture document approved"),
                    ExecutionTask(title="Build core backend API", description="Implement core API endpoints and business logic.", category="technical", priority="HIGH", estimated_days=15, suggested_owner="Backend Engineer", deadline_offset_days=42, dependencies=["Design system architecture"], success_criteria="API endpoints passing tests"),
                    ExecutionTask(title="Build frontend interface", description="Implement user-facing interface.", category="technical", priority="MEDIUM", estimated_days=12, suggested_owner="Frontend Engineer", deadline_offset_days=49, dependencies=["Build core backend API"], success_criteria="UI functional with core features"),
                    ExecutionTask(title="Create pitch deck", description="Prepare investor/stakeholder pitch materials.", category="business", priority="MEDIUM", estimated_days=3, suggested_owner="Business Lead", deadline_offset_days=14, success_criteria="12-slide pitch deck reviewed"),
                    ExecutionTask(title="Set up CI/CD pipeline", description="Automate testing and deployment.", category="technical", priority="MEDIUM", estimated_days=3, suggested_owner="DevOps Engineer", deadline_offset_days=28, success_criteria="Automated deployment pipeline working"),
                    ExecutionTask(title="Collect training data/content", description="Gather data needed for the product.", category="research", priority="MEDIUM", estimated_days=10, suggested_owner="Data Engineer", deadline_offset_days=35, success_criteria="Dataset collected and validated"),
                    ExecutionTask(title="Recruit pilot users", description="Identify and onboard initial pilot users.", category="customer", priority="MEDIUM", estimated_days=7, suggested_owner="Product Lead", deadline_offset_days=56, dependencies=["Build frontend interface"], success_criteria="5 pilot users confirmed"),
                ],
                validation_experiments=[
                    ValidationExperiment(experiment="Customer demand survey", hypothesis="At least 70% of interviewed prospects express willingness to use this solution.", success_metric="Survey completion rate and interest score", estimated_duration_days=10),
                    ValidationExperiment(experiment="Prototype usability test", hypothesis="Users can complete core tasks without assistance.", success_metric="Task completion rate > 80%", estimated_duration_days=5),
                    ValidationExperiment(experiment="Pricing sensitivity test", hypothesis="Target customers accept the proposed price point.", success_metric="3+ customers willing to pre-pay or commit", estimated_duration_days=7),
                ],
                immediate_next_steps=[
                    "Schedule first 3 customer discovery interviews this week",
                    "Begin competitive landscape mapping",
                    "Draft one-page product vision document",
                    "Identify technical risks and prototype critical path",
                    "Set up project management board for task tracking",
                ],
            ),
            confidence=0.70,
            classification="INFERENCE",
            summary=f"Execution plan for '{short}...' recommends a 16-week phased approach starting with market validation (4 weeks), followed by MVP build (6 weeks), and pilot launch (4 weeks). 10 tasks across customer, research, technical, and business categories."
        )


# Singleton
execution_planner_agent = ExecutionPlannerAgent()
