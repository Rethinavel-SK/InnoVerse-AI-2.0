"""
InnoVerse AI 2.0 — Idea Evolution Engine
==========================================
Iteratively improves innovation ideas based on agent feedback.
Takes weaknesses identified by agents, generates improved versions,
and re-evaluates. Maximum 3 iterations.
"""

import asyncio
import json
import logging
import os
import time
from typing import Dict, Any, Optional, List

from backend.database.models import InnovationVersion
from backend.database.db import db_manager

logger = logging.getLogger("IdeaEvolution")

MAX_ITERATIONS = 3

EVOLUTION_SYSTEM_PROMPT = """You are an Innovation Improvement Specialist within the InnoVerse AI Platform.

Your job: Take an innovation idea along with identified weaknesses and criticisms,
and produce an IMPROVED version of the idea that addresses the key concerns.

RULES:
- Keep the core innovation intent intact
- Address the top 3 weaknesses identified
- Be specific about what changed and why
- The improved idea should be strictly BETTER, not just different
- Do NOT add unnecessary complexity

Return ONLY valid JSON:
{
    "improved_statement": "The improved innovation idea (2-4 sentences)",
    "changes_made": [
        "Change 1: What was changed and why",
        "Change 2: ...",
        "Change 3: ..."
    ],
    "weaknesses_addressed": ["weakness 1", "weakness 2", "weakness 3"],
    "reasoning": "Brief explanation of the improvement strategy"
}
"""

EVOLUTION_USER_PROMPT = """ORIGINAL IDEA:
{original_statement}

IDENTIFIED WEAKNESSES:
{weaknesses}

PREVIOUS IMPROVEMENTS (if any):
{previous_improvements}

Generate an improved version of this idea that addresses the key weaknesses.
Return as valid JSON."""


def _sync_call_groq(system_prompt: str, user_prompt: str) -> Optional[str]:
    import urllib.request

    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        return None

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.5,
        "max_tokens": 1500,
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
        logger.error(f"Groq API error in idea evolution: {e}")
        return None


class IdeaEvolutionEngine:
    """
    Iteratively improves innovation ideas based on agent critique.
    """

    def __init__(self):
        self.max_iterations = MAX_ITERATIONS

    async def improve_idea(
        self,
        project_id: str,
        original_statement: str,
        weaknesses: List[str],
        current_version: int = 1,
        previous_improvements: Optional[List[str]] = None,
    ) -> Optional[InnovationVersion]:
        """
        Generate an improved version of the idea.
        Returns a new InnovationVersion with the improved statement.
        """
        if current_version >= self.max_iterations + 1:
            logger.info("Maximum iterations (%d) reached for project %s", self.max_iterations, project_id)
            return None

        weaknesses_text = "\n".join(f"- {w}" for w in weaknesses[:5])
        prev_text = "\n".join(previous_improvements or ["None — this is the first iteration."])

        user_prompt = EVOLUTION_USER_PROMPT.format(
            original_statement=original_statement,
            weaknesses=weaknesses_text,
            previous_improvements=prev_text,
        )

        # Try LLM
        raw = await asyncio.to_thread(_sync_call_groq, EVOLUTION_SYSTEM_PROMPT, user_prompt)

        improved_statement = None
        improvement_reasoning = None

        if raw:
            try:
                data = json.loads(raw)
                improved_statement = data.get("improved_statement", "")
                changes = data.get("changes_made", [])
                reasoning = data.get("reasoning", "")
                improvement_reasoning = f"Changes: {'; '.join(changes)}. Reasoning: {reasoning}"
            except Exception as e:
                logger.warning("Failed to parse evolution LLM response: %s", e)

        # Fallback: simple augmentation
        if not improved_statement:
            improved_statement = (
                f"{original_statement} — Enhanced with: "
                f"addressed {weaknesses[0] if weaknesses else 'core concerns'}; "
                f"improved differentiation strategy; "
                f"strengthened unit economics model."
            )
            improvement_reasoning = f"Heuristic improvement addressing top weaknesses: {', '.join(weaknesses[:3])}"

        # Create new version
        new_version = InnovationVersion(
            project_id=project_id,
            version_number=current_version + 1,
            problem_statement=original_statement,
            improved_statement=improved_statement,
            improvement_reasoning=improvement_reasoning,
        )

        try:
            await db_manager.create_version(new_version)
            logger.info(
                "Created version %d for project %s",
                new_version.version_number, project_id
            )
        except Exception as e:
            logger.error("Failed to save new version: %s", e)

        return new_version

    async def get_evolution_history(self, project_id: str) -> List[Dict[str, Any]]:
        """Get the full evolution history of an innovation idea."""
        versions = await db_manager.get_versions(project_id)
        scores = await db_manager.get_scores(project_id)

        # Build version-to-score map
        score_map = {}
        for s in scores:
            score_map[s.version_id] = s.overall_score

        history = []
        for v in versions:
            history.append({
                "version": v.version_number,
                "version_id": v.id,
                "problem_statement": v.problem_statement,
                "improved_statement": v.improved_statement,
                "improvement_reasoning": v.improvement_reasoning,
                "score": score_map.get(v.id),
                "created_at": v.created_at,
            })

        return history

    def extract_weaknesses_from_agents(self, agent_results: Dict[str, Any]) -> List[str]:
        """
        Extract key weaknesses from agent analysis results.
        Used to feed into the improvement loop.
        """
        weaknesses = []

        # From Failure Hunter
        failure_data = agent_results.get("failure_hunter", {})
        risks = failure_data.get("top_failure_risks", [])
        for risk in risks[:3]:
            if isinstance(risk, dict):
                weaknesses.append(risk.get("risk", "Unknown risk"))
            elif isinstance(risk, str):
                weaknesses.append(risk)

        contrarian = failure_data.get("contrarian_view", "")
        if contrarian:
            weaknesses.append(f"Contrarian concern: {contrarian}")

        # From Risk Assessment
        risk_data = agent_results.get("risk_assessment", {})
        risk_items = risk_data.get("risks", risk_data.get("risk_factors", []))
        if isinstance(risk_items, list):
            for ri in risk_items[:2]:
                if isinstance(ri, dict):
                    weaknesses.append(ri.get("risk", ri.get("description", "")))
                elif isinstance(ri, str):
                    weaknesses.append(ri)

        # From Business Strategy (weaknesses)
        biz_data = agent_results.get("business_strategy", {})
        biz_weaknesses = biz_data.get("swot", {}).get("weaknesses", [])
        if isinstance(biz_weaknesses, list):
            for w in biz_weaknesses[:2]:
                weaknesses.append(f"Business weakness: {w}")

        # Deduplicate and limit
        seen = set()
        unique = []
        for w in weaknesses:
            if w and w not in seen:
                seen.add(w)
                unique.append(w)

        return unique[:8]


# Singleton
idea_evolution_engine = IdeaEvolutionEngine()
