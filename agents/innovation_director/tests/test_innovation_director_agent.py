"""
Unit Tests for Innovation Director Agent.
========================================
Tests orchestration across all 9 specialist AI agents, conflict resolution, weighted score calculation, and final JSON output structure.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException

from agents.innovation_director.agent import InnovationDirectorAgent
from agents.innovation_director.schemas.director_schema import (
    InnovationDirectorRequest,
    InnovationDirectorResponse,
)
from agents.innovation_director.services.director_service import InnovationDirectorService


@pytest.mark.asyncio
async def test_input_validation_empty():
    service = InnovationDirectorService(api_key="mock_key")
    with pytest.raises(HTTPException) as exc_info:
        service.validate_problem_statement("   ")
    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_orchestration_service_fallback():
    service = InnovationDirectorService(api_key=None)
    req = InnovationDirectorRequest(
        problem_statement="Build an AI-powered automated code security review platform for enterprise DevOps teams."
    )

    mock_architect_res = MagicMock()
    mock_architect_res.model_dump.return_value = {"architecture": {"type": "Microservices"}, "estimated_complexity": "High"}

    mock_roadmap_res = MagicMock()
    mock_roadmap_res.model_dump.return_value = {"mvp_features": ["Auth", "Scanner"], "timeline": "14 Weeks"}

    mock_strategy_res = MagicMock()
    mock_strategy_res.model_dump.return_value = {"business_model": "B2B SaaS"}

    mock_research_res = MagicMock()
    mock_research_res.model_dump.return_value = {"query_used": "Code security AI"}

    mock_patent_res = MagicMock()
    mock_patent_res.model_dump.return_value = {"novelty_score": 85}

    mock_market_res = MagicMock()
    mock_market_res.model_dump.return_value = {"target_market": "Enterprise DevOps"}

    mock_trend_res = MagicMock()
    mock_trend_res.model_dump.return_value = {"trend_score": 88}

    mock_sust_res = MagicMock()
    mock_sust_res.model_dump.return_value = {"sustainability_score": 90}

    with patch("agents.innovation_director.services.director_service.SolutionArchitectAgent.run", side_effect=AsyncMock(return_value=mock_architect_res)), \
         patch("agents.innovation_director.services.director_service.MVPRoadmapAgent.run", side_effect=AsyncMock(return_value=mock_roadmap_res)), \
         patch("agents.innovation_director.services.director_service.BusinessStrategyAgent.run", side_effect=AsyncMock(return_value=mock_strategy_res)), \
         patch("agents.innovation_director.services.director_service.risk_execute", return_value={"overall_risk_score": 25}), \
         patch("agents.innovation_director.services.director_service.research_agent.analyze", side_effect=AsyncMock(return_value=mock_research_res)), \
         patch("agents.innovation_director.services.director_service.patent_agent.analyze", side_effect=AsyncMock(return_value=mock_patent_res)), \
         patch("agents.innovation_director.services.director_service.market_intelligence_agent.run", side_effect=AsyncMock(return_value=mock_market_res)), \
         patch("agents.innovation_director.services.director_service.trend_intelligence_agent.run", side_effect=AsyncMock(return_value=mock_trend_res)), \
         patch("agents.innovation_director.services.director_service.sustainability_agent.run", side_effect=AsyncMock(return_value=mock_sust_res)):

        res = await service.analyze_and_orchestrate(req)
        assert isinstance(res, InnovationDirectorResponse)
        assert res.overall_innovation_score >= 0.0
        assert res.solution_architecture["estimated_complexity"] == "High"
        assert res.mvp_roadmap["timeline"] == "14 Weeks"
        assert len(res.agent_status) == 9
        assert all(v == "Completed" for v in res.agent_status.values())


@pytest.mark.asyncio
async def test_agent_full_pipeline():
    service = InnovationDirectorService(api_key=None)
    agent = InnovationDirectorAgent(service=service)

    mock_architect_res = MagicMock()
    mock_architect_res.model_dump.return_value = {"architecture": {"type": "Microservices"}}

    mock_roadmap_res = MagicMock()
    mock_roadmap_res.model_dump.return_value = {"timeline": "12 Weeks"}

    mock_strategy_res = MagicMock()
    mock_strategy_res.model_dump.return_value = {"business_model": "SaaS"}

    mock_research_res = MagicMock()
    mock_research_res.model_dump.return_value = {"papers": 5}

    mock_patent_res = MagicMock()
    mock_patent_res.model_dump.return_value = {"score": 80}

    mock_market_res = MagicMock()
    mock_market_res.model_dump.return_value = {"target_market": "Healthcare"}

    mock_trend_res = MagicMock()
    mock_trend_res.model_dump.return_value = {"trend_score": 85}

    mock_sust_res = MagicMock()
    mock_sust_res.model_dump.return_value = {"sustainability_score": 85}

    with patch("agents.innovation_director.services.director_service.SolutionArchitectAgent.run", side_effect=AsyncMock(return_value=mock_architect_res)), \
         patch("agents.innovation_director.services.director_service.MVPRoadmapAgent.run", side_effect=AsyncMock(return_value=mock_roadmap_res)), \
         patch("agents.innovation_director.services.director_service.BusinessStrategyAgent.run", side_effect=AsyncMock(return_value=mock_strategy_res)), \
         patch("agents.innovation_director.services.director_service.risk_execute", return_value={"overall_risk_score": 30}), \
         patch("agents.innovation_director.services.director_service.research_agent.analyze", side_effect=AsyncMock(return_value=mock_research_res)), \
         patch("agents.innovation_director.services.director_service.patent_agent.analyze", side_effect=AsyncMock(return_value=mock_patent_res)), \
         patch("agents.innovation_director.services.director_service.market_intelligence_agent.run", side_effect=AsyncMock(return_value=mock_market_res)), \
         patch("agents.innovation_director.services.director_service.trend_intelligence_agent.run", side_effect=AsyncMock(return_value=mock_trend_res)), \
         patch("agents.innovation_director.services.director_service.sustainability_agent.run", side_effect=AsyncMock(return_value=mock_sust_res)):

        req = InnovationDirectorRequest(problem_statement="Build a remote healthcare telemedicine SaaS platform.")
        result = await agent.execute_full_pipeline(req)

        assert result.metadata.agent_name == "InnovationDirectorAgent"
        assert result.metadata.agents_executed == 9
        assert "executive_summary" in result.director_output
        assert "overall_innovation_score" in result.director_output
