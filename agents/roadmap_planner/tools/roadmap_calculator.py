"""
Roadmap Calculator Utility.
===========================
Helper tool to estimate development hours, timeline metrics, team allocation,
and budget based on feature complexity and project scope.
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class RoadmapCalculator:
    """
    Utility for estimating timeline, effort, team distribution, and budget.
    """

    DEFAULT_HOURLY_RATE = 85.0  # Blended USD hourly rate

    @staticmethod
    def estimate_project_metrics(
        mvp_feature_count: int,
        future_feature_count: int,
        hourly_rate: float = DEFAULT_HOURLY_RATE,
    ) -> Dict[str, Any]:
        """
        Calculates baseline effort, weeks, team size, and budget range.
        """
        # Baseline: ~80 hours per MVP feature, ~40 hours per future feature
        mvp_hours = mvp_feature_count * 80
        future_hours = future_feature_count * 40
        total_hours = mvp_hours + future_hours

        # Assuming 3 engineers working ~35 effective hours/week
        weekly_team_capacity = 3 * 35
        estimated_weeks = max(4, round(total_hours / weekly_team_capacity))
        estimated_months = round(estimated_weeks / 4.33, 1)

        base_cost = total_hours * hourly_rate
        low_budget = round(base_cost * 0.9, -3)
        high_budget = round(base_cost * 1.25, -3)

        return {
            "total_estimated_hours": total_hours,
            "mvp_hours": mvp_hours,
            "estimated_weeks": estimated_weeks,
            "estimated_months": estimated_months,
            "recommended_team_size": "4 Members (1 Product Manager, 2 Fullstack Devs, 1 UI/UX Designer)",
            "budget_range": f"${low_budget:,.0f} - ${high_budget:,.0f}",
        }
