"""
Comprehensive System Verification Test for All 9 AI Agents + Innovation Director
==============================================================================
Validates that every single specialist agent and the master orchestrator execute
cleanly and return structured responses.
"""

import pytest
import asyncio
from typing import Dict, Any

from agents.solution_architect.agent import SolutionArchitectAgent
from agents.business_strategy.agent import BusinessStrategyAgent
from agents.research_intelligence.agent import research_agent
from agents.research_intelligence.schemas import ResearchAgentRequest
from agents.patent_intelligence.agent import patent_agent
from agents.patent_intelligence.schemas import PatentAgentRequest
from agents.market_intelligence.agent import market_intelligence_agent
from agents.trend_intelligence.agent import trend_intelligence_agent
from agents.risk_assessment.agent import execute as risk_execute
from agents.sustainability.agent import sustainability_agent
from agents.roadmap_planner import MVPRoadmapAgent
from agents.innovation_director.agent import InnovationDirectorAgent

TEST_PROBLEM = "Build an AI-powered automated code security review platform for enterprise DevOps teams."


@pytest.mark.asyncio
async def test_agent_1_solution_architect():
    agent = SolutionArchitectAgent()
    res = await agent.run(TEST_PROBLEM)
    assert res is not None
    assert hasattr(res, "architecture") or hasattr(res, "tech_stack") or isinstance(res, dict)


@pytest.mark.asyncio
async def test_agent_2_business_strategy():
    agent = BusinessStrategyAgent()
    res = await agent.run(TEST_PROBLEM)
    assert res is not None
    assert hasattr(res, "business_model") or hasattr(res, "value_proposition") or isinstance(res, dict)


@pytest.mark.asyncio
async def test_agent_3_research():
    req = ResearchAgentRequest(problem_statement=TEST_PROBLEM)
    res = await research_agent.analyze(req)
    assert res is not None
    assert hasattr(res, "research_summary") or hasattr(res, "papers") or isinstance(res, dict)


@pytest.mark.asyncio
async def test_agent_4_patent_analysis():
    req = PatentAgentRequest(problem_statement=TEST_PROBLEM)
    res = await patent_agent.analyze(req)
    assert res is not None
    assert hasattr(res, "novelty_score") or hasattr(res, "patent_summary") or isinstance(res, dict)


@pytest.mark.asyncio
async def test_agent_5_market_analysis():
    res = await market_intelligence_agent.run(TEST_PROBLEM)
    assert res is not None
    assert res.target_market is not None
    assert res.status == "Completed"


@pytest.mark.asyncio
async def test_agent_6_trend_analysis():
    res = await trend_intelligence_agent.run(TEST_PROBLEM)
    assert res is not None
    assert res.adoption_lifecycle_phase is not None
    assert res.status == "Completed"


@pytest.mark.asyncio
async def test_agent_7_risk_assessment():
    res = risk_execute(TEST_PROBLEM)
    assert res is not None
    assert "status" in res or "overall_risk_score" in res


@pytest.mark.asyncio
async def test_agent_8_sustainability():
    res = await sustainability_agent.run(TEST_PROBLEM)
    assert res is not None
    assert res.sustainability_score >= 0
    assert res.status == "Completed"


@pytest.mark.asyncio
async def test_agent_9_mvp_roadmap():
    agent = MVPRoadmapAgent()
    res = await agent.run(TEST_PROBLEM)
    assert res is not None
    assert hasattr(res, "timeline") or hasattr(res, "phases") or isinstance(res, dict)


@pytest.mark.asyncio
async def test_agent_10_innovation_director_orchestration():
    director = InnovationDirectorAgent()
    res = await director.run(TEST_PROBLEM)
    assert res is not None
    assert res.executive_summary is not None
    assert res.problem_understanding is not None
    assert len(res.agent_status) == 9
    assert res.overall_innovation_score >= 0.0
    assert res.confidence >= 0.0
    assert res.final_recommendation is not None
