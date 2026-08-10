"""
InnoVerse AI 2.0 — Innovation Score Engine
=============================================
Transparent 10-dimension scoring system that calculates,
explains, and compares innovation scores.
"""

import logging
from typing import Dict, Any, Optional, List
from backend.database.models import InnovationScore

logger = logging.getLogger("ScoreEngine")

# Default dimension weights (sum = 1.0)
DEFAULT_WEIGHTS = {
    "market_potential": 0.15,
    "technical_feasibility": 0.15,
    "business_viability": 0.12,
    "innovation_differentiation": 0.12,
    "patent_ip_position": 0.08,
    "risk_score": 0.08,
    "sustainability": 0.06,
    "mvp_feasibility": 0.10,
    "customer_value": 0.08,
    "scalability": 0.06,
}

# Agent-to-dimension mapping
AGENT_DIMENSION_MAP = {
    "market_intelligence": ["market_potential"],
    "business_strategy": ["business_viability", "customer_value"],
    "solution_architect": ["technical_feasibility", "scalability"],
    "research_intelligence": ["innovation_differentiation"],
    "patent_intelligence": ["patent_ip_position"],
    "risk_assessment": ["risk_score"],
    "sustainability": ["sustainability"],
    "roadmap_planner": ["mvp_feasibility"],
    "trend_intelligence": ["market_potential", "innovation_differentiation"],
    "failure_hunter": ["risk_score"],
    "execution_planner": ["mvp_feasibility"],
}


class InnovationScoreEngine:
    """
    Computes transparent 10-dimension innovation scores from agent outputs.
    """

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        self.weights = weights or DEFAULT_WEIGHTS.copy()

    def calculate_score(
        self,
        agent_results: Dict[str, Dict[str, Any]],
        project_id: str,
        version_id: str,
    ) -> InnovationScore:
        """
        Calculate 10-dimension innovation score from agent results.

        agent_results: Dict mapping agent_name -> agent output dict
        """
        dimensions = {dim: [] for dim in self.weights}

        for agent_name, result in agent_results.items():
            # Extract score from agent output
            agent_score = self._extract_agent_score(agent_name, result)
            if agent_score is None:
                continue

            # Map agent score to dimensions
            mapped_dims = AGENT_DIMENSION_MAP.get(agent_name, [])
            for dim in mapped_dims:
                if dim in dimensions:
                    dimensions[dim].append(agent_score)

        # Calculate dimension averages
        dim_scores = {}
        for dim, scores in dimensions.items():
            if scores:
                dim_scores[dim] = round(sum(scores) / len(scores), 1)
            else:
                dim_scores[dim] = 65.0  # Default neutral score

        # Calculate overall weighted score
        overall = 0.0
        for dim, weight in self.weights.items():
            overall += dim_scores.get(dim, 65.0) * weight

        overall = round(overall, 1)

        # Generate explanation
        explanation = self._generate_explanation(dim_scores, overall)

        return InnovationScore(
            project_id=project_id,
            version_id=version_id,
            market_potential=dim_scores.get("market_potential", 0),
            technical_feasibility=dim_scores.get("technical_feasibility", 0),
            business_viability=dim_scores.get("business_viability", 0),
            innovation_differentiation=dim_scores.get("innovation_differentiation", 0),
            patent_ip_position=dim_scores.get("patent_ip_position", 0),
            risk_score=dim_scores.get("risk_score", 0),
            sustainability=dim_scores.get("sustainability", 0),
            mvp_feasibility=dim_scores.get("mvp_feasibility", 0),
            customer_value=dim_scores.get("customer_value", 0),
            scalability=dim_scores.get("scalability", 0),
            overall_score=overall,
            weights=self.weights,
            explanation=explanation,
        )

    def _extract_agent_score(self, agent_name: str, result: Dict[str, Any]) -> Optional[float]:
        """Extract a normalized 0-100 score from an agent result."""
        # Try direct score field
        for key in ["score", "overall_score", "innovation_score", "feasibility_score"]:
            val = result.get(key)
            if val is not None:
                try:
                    score = float(val)
                    return max(0, min(100, score))
                except (ValueError, TypeError):
                    pass

        # Try to derive from confidence
        confidence = result.get("confidence")
        if confidence is not None:
            try:
                c = float(confidence)
                if 0 <= c <= 1:
                    return c * 100
                return max(0, min(100, c))
            except (ValueError, TypeError):
                pass

        # Special handling for failure_hunter (invert risk)
        if agent_name == "failure_hunter":
            prob = result.get("overall_failure_probability", "MEDIUM")
            if isinstance(prob, str):
                risk_map = {"LOW": 80, "MEDIUM": 55, "HIGH": 25}
                return risk_map.get(prob.upper(), 55)

        # Special handling for agents with structured sub-scores
        sub_scores = []
        for key, val in result.items():
            if isinstance(val, dict) and "score" in val:
                try:
                    sub_scores.append(float(val["score"]))
                except (ValueError, TypeError):
                    pass

        if sub_scores:
            avg = sum(sub_scores) / len(sub_scores)
            return max(0, min(100, avg))

        return None

    def _generate_explanation(self, dim_scores: Dict[str, float], overall: float) -> str:
        """Generate a human-readable explanation of the score."""
        strengths = []
        weaknesses = []

        for dim, score in sorted(dim_scores.items(), key=lambda x: x[1], reverse=True):
            label = dim.replace("_", " ").title()
            if score >= 75:
                strengths.append(f"{label} ({score}/100)")
            elif score < 50:
                weaknesses.append(f"{label} ({score}/100)")

        parts = []
        parts.append(f"Overall innovation score: {overall}/100.")

        if strengths:
            parts.append(f"Strengths: {', '.join(strengths[:3])}.")
        if weaknesses:
            parts.append(f"Areas for improvement: {', '.join(weaknesses[:3])}.")

        if overall >= 80:
            parts.append("Strong candidate for investment and development.")
        elif overall >= 60:
            parts.append("Promising concept with areas that need strengthening.")
        elif overall >= 40:
            parts.append("Significant challenges identified. Consider pivoting or addressing gaps.")
        else:
            parts.append("High risk. Major issues need resolution before proceeding.")

        return " ".join(parts)

    def compare_scores(self, score_a: InnovationScore, score_b: InnovationScore) -> Dict[str, Any]:
        """Compare two innovation scores and return a diff."""
        dims = list(self.weights.keys())
        comparison = {}

        for dim in dims:
            val_a = getattr(score_a, dim, 0)
            val_b = getattr(score_b, dim, 0)
            change = round(val_b - val_a, 1)
            comparison[dim] = {
                "before": val_a,
                "after": val_b,
                "change": change,
                "direction": "improved" if change > 0 else "declined" if change < 0 else "unchanged",
            }

        overall_change = round(score_b.overall_score - score_a.overall_score, 1)

        return {
            "overall_before": score_a.overall_score,
            "overall_after": score_b.overall_score,
            "overall_change": overall_change,
            "overall_direction": "improved" if overall_change > 0 else "declined" if overall_change < 0 else "unchanged",
            "dimensions": comparison,
        }


# Singleton
score_engine = InnovationScoreEngine()
