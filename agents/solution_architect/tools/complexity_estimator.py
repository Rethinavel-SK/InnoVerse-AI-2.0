import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


async def estimate_complexity(problem_statement: str) -> Dict[str, Any]:
    """
    Async tool to estimate technical complexity, development time, team size, cost, and maintainability.
    """
    logger.info("Evaluating architectural complexity heuristics for problem statement...")
    length = len(problem_statement.split())
    problem_lower = problem_statement.lower()
    
    keywords_high = [
        "robot", "warehouse", "kafka", "distributed", "blockchain", "multi-tenant",
        "high throughput", "million", "real-time", "edge", "hipaa", "pci", "iot", "vision", "autonomous"
    ]
    keywords_medium = ["dashboard", "api", "database", "analytics", "authentication", "workflow", "e-commerce", "recommendation"]
    
    high_count = sum(1 for kw in keywords_high if kw in problem_lower)
    medium_count = sum(1 for kw in keywords_medium if kw in problem_lower)
    
    if high_count >= 3 or length > 100:
        complexity = "Very High"
        dev_time = "6 - 12 Months"
        team_size = "6 - 10 Engineers (Architect, Backend, Frontend, DevOps, ML/IoT Engineers)"
        cost = "$2,500 - $8,000 / month"
        scalability = "9.5/10 (Extreme Scale)"
        maintainability = "8.0/10 (Modular Services)"
        confidence = 0.94
    elif high_count >= 1 or medium_count >= 3 or length > 50:
        complexity = "High"
        dev_time = "3 - 6 Months"
        team_size = "4 - 6 Engineers (Backend, Frontend, DevOps, ML Specialist)"
        cost = "$800 - $2,500 / month"
        scalability = "8.8/10 (High Scale)"
        maintainability = "8.5/10 (Clean Architecture)"
        confidence = 0.92
    elif medium_count >= 1:
        complexity = "Medium"
        dev_time = "2 - 3 Months"
        team_size = "2 - 4 Engineers"
        cost = "$250 - $800 / month"
        scalability = "8.0/10 (Medium Scale)"
        maintainability = "9.0/10 (High Maintainability)"
        confidence = 0.90
    else:
        complexity = "Low"
        dev_time = "3 - 6 Weeks"
        team_size = "1 - 2 Engineers"
        cost = "$50 - $250 / month"
        scalability = "7.5/10 (Standard Scale)"
        maintainability = "9.5/10 (Low Overhead)"
        confidence = 0.88

    return {
        "technical_complexity": complexity,
        "estimated_development_time": dev_time,
        "recommended_team_size": team_size,
        "estimated_monthly_cost": cost,
        "scalability_score": scalability,
        "maintainability_score": maintainability,
        "base_confidence": confidence
    }
