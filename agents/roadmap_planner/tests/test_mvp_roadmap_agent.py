"""
Unit and Integration Tests for MVP & Roadmap Agent.
====================================================
"""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException

from agents.roadmap_planner.agent import MVPRoadmapAgent
from agents.roadmap_planner.schemas.mvp_roadmap_schema import (
    MvpRoadmapRequest,
    MvpRoadmapResponse,
)
from agents.roadmap_planner.services.roadmap_service import MVPRoadmapService
from agents.roadmap_planner.tools.roadmap_calculator import RoadmapCalculator

MOCK_LLM_RESPONSE = """{
  "mvp_features": [
    {
      "feature": "User Authentication & Authorization",
      "description": "Secure JWT login and role-based access control.",
      "priority": "High",
      "complexity": "Low"
    },
    {
      "feature": "Automated Security Vulnerability Scanning",
      "description": "Scans repository code for secrets and dependencies CVEs.",
      "priority": "Critical",
      "complexity": "Medium"
    }
  ],
  "future_features": [
    {
      "feature": "AI Code Auto-Fixing",
      "description": "Generates automated pull requests fixing detected vulnerabilities.",
      "priority": "Medium",
      "target_release": "v1.5"
    }
  ],
  "roadmap": [
    {
      "phase": "Phase 1: Foundation & Core Scanner MVP",
      "duration": "Weeks 1-6",
      "objectives": ["Implement auth", "Deliver core AST scanner engine"]
    },
    {
      "phase": "Phase 2: CI/CD Integrations & Dashboard",
      "duration": "Weeks 7-12",
      "objectives": ["GitHub Action integration", "Executive dashboard"]
    }
  ],
  "milestones": [
    {
      "milestone": "M1: Architecture & Data Pipeline",
      "target_week": "Week 2",
      "deliverables": ["System design", "Scanner API baseline"]
    }
  ],
  "timeline": "14 Weeks (3.5 Months)",
  "sprint_plan": [
    {
      "sprint": "Sprint 1 (Weeks 1-2)",
      "goal": "Core Infra and Auth setup",
      "key_tasks": ["Setup FastAPI backend", "Implement JWT auth"]
    }
  ],
  "team_size": "4 Members (1 Lead Architect, 2 Full-Stack Engineers, 1 DevOps Engineer)",
  "estimated_budget": "$85,000 - $110,000",
  "risks": [
    {
      "risk": "High false positive rate in AST scanner",
      "impact": "High",
      "mitigation": "Fine-tune heuristic rule set and allow user rule customization."
    }
  ],
  "confidence": 0.95
}"""


@pytest.mark.asyncio
async def test_input_validation_empty_problem():
    service = MVPRoadmapService(api_key="mock_key")
    with pytest.raises(HTTPException) as exc_info:
        service.validate_problem_statement("   ")
    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_input_validation_short_gibberish():
    service = MVPRoadmapService(api_key="mock_key")
    with pytest.raises(HTTPException) as exc_info:
        service.validate_problem_statement("123!!!")
    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_input_validation_repetitive_symbols():
    service = MVPRoadmapService(api_key="mock_key")
    with pytest.raises(HTTPException) as exc_info:
        service.validate_problem_statement("aaaaaaaaaaaaa")
    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_service_analyze_with_mocked_llm():
    service = MVPRoadmapService(api_key="mock_key")
    request = MvpRoadmapRequest(
        problem_statement="Build an AI-powered code security review tool for enterprise developers."
    )

    with patch.object(service, "_call_llm", new_callable=AsyncMock) as mock_call:
        mock_call.return_value = MOCK_LLM_RESPONSE
        response = await service.analyze(request)

        assert isinstance(response, MvpRoadmapResponse)
        assert len(response.mvp_features) == 2
        assert len(response.future_features) == 1
        assert response.confidence == 0.95
        assert "14 Weeks" in response.timeline


@pytest.mark.asyncio
async def test_agent_run_and_full_pipeline():
    service = MVPRoadmapService(api_key="mock_key")
    agent = MVPRoadmapAgent(service=service)

    with patch.object(service, "_call_llm", new_callable=AsyncMock) as mock_call:
        mock_call.return_value = MOCK_LLM_RESPONSE

        # Test agent.run
        response = await agent.run("Build a SaaS platform for automated code reviews.")
        assert isinstance(response, MvpRoadmapResponse)
        assert len(response.roadmap) == 2

        # Test agent.execute_full_pipeline
        req = MvpRoadmapRequest(problem_statement="Build a SaaS platform for automated code reviews.")
        full_res = await agent.execute_full_pipeline(req)
        assert full_res.metadata.agent_name == "MVPRoadmapAgent"
        assert "mvp_features" in full_res.roadmap_output


def test_roadmap_calculator():
    metrics = RoadmapCalculator.estimate_project_metrics(mvp_feature_count=5, future_feature_count=3)
    assert metrics["total_estimated_hours"] > 0
    assert metrics["estimated_weeks"] >= 4
    assert "$" in metrics["budget_range"]
