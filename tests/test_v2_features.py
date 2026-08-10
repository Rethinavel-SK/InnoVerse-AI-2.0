import pytest
import asyncio
from agents.failure_hunter.agent import failure_hunter_agent
from agents.execution_planner.agent import execution_planner_agent
from agents.innovation_director.services.score_engine import score_engine
from agents.innovation_director.services.idea_evolution import idea_evolution_engine

@pytest.mark.asyncio
async def test_failure_hunter():
    res = await failure_hunter_agent.run("Build an automated code audit bot")
    assert res.agent == "Failure Hunter Agent"
    assert len(res.top_failure_risks) >= 1
    assert res.critical_assumption != ""

@pytest.mark.asyncio
async def test_execution_planner():
    res = await execution_planner_agent.run("Build an automated code audit bot")
    assert res.agent == "Execution Planner Agent"
    assert len(res.execution_plan.tasks) >= 1
    assert len(res.execution_plan.milestones) >= 1

def test_score_engine():
    mock_results = {
        "solution_architect": {"feasibility_score": 85},
        "business_strategy": {"confidence": 0.8},
        "risk_assessment": {"overall_risk_score": 30},
        "failure_hunter": {"overall_failure_probability": "LOW"}
    }
    score = score_engine.calculate_score(mock_results, "p1", "v1")
    assert score.overall_score > 0
    assert "market_potential" in score.weights

@pytest.mark.asyncio
async def test_idea_evolution_weaknesses_extraction():
    mock_results = {
        "failure_hunter": {
            "top_failure_risks": [{"risk": "High churn risk"}],
            "contrarian_view": "Market is already saturated"
        }
    }
    weaknesses = idea_evolution_engine.extract_weaknesses_from_agents(mock_results)
    assert len(weaknesses) >= 1
    assert "High churn risk" in weaknesses
