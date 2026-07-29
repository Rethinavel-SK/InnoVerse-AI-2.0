import pytest
from fastapi.testclient import TestClient

from agents.solution_architect.agent import SolutionArchitectAgent
from agents.solution_architect.schemas.architect_schema import (
    SolutionArchitectRequest,
    SolutionArchitectResponse,
)
from backend.main import app

client = TestClient(app)


from unittest.mock import patch

@pytest.mark.asyncio
async def test_simple_todo_app_pragmatic():
    agent = SolutionArchitectAgent()
    request = SolutionArchitectRequest(
        problem_statement="Build a simple todo list app for personal task tracking."
    )
    
    mock_json_response = '''
    {
      "problem_analysis": {
        "business_problem": "Task tracker",
        "domain": "Task Management",
        "primary_objective": "Track tasks",
        "end_users": "Not Specified",
        "functional_requirements": [],
        "non_functional_requirements": [],
        "expected_scale": "Not Specified",
        "availability_requirements": "Not Specified",
        "performance_requirements": "Not Specified",
        "security_requirements": "Not Specified",
        "ai_requirements": "Not Specified",
        "analytics_requirements": "Not Specified",
        "real_time_requirements": "Not Specified",
        "third_party_integrations": [],
        "deployment_constraints": "Not Specified"
      },
      "identified_requirements": {
        "real_time": false, "ai_required": false, "computer_vision": false,
        "nlp": false, "iot": false, "gps_tracking": false, "notifications": false,
        "authentication": false, "rbac": false, "queue_processing": false,
        "event_streaming": false, "caching": false, "analytics": false,
        "monitoring": false, "high_availability": false, "disaster_recovery": false
      },
      "architecture": {
        "type": "Monolith",
        "rationale": "Simple.",
        "why_alternatives_were_not_selected": "Overkill."
      },
      "technology_recommendations": {},
      "reasoning": [],
      "estimated_complexity": "Low",
      "development_time": "1 week",
      "team_size": "1",
      "prototype_cost": "$0",
      "production_cost": "$0",
      "confidence": 0.8
    }
    '''
    
    with patch.object(agent.service, '_call_llm', return_value=mock_json_response):
        response = await agent.process_request(request)

    assert isinstance(response, SolutionArchitectResponse)
    assert response.architecture.type == "Modular Monolith" or response.architecture.type == "Layered Architecture" or response.architecture.type == "Monolith"
    assert response.technology_recommendations.get("vector_database") is None
    assert response.technology_recommendations.get("cache") is None
    assert response.technology_recommendations.get("message_broker") is None
    assert response.technology_recommendations.get("ai_models") is None
    assert response.problem_analysis.end_users == "Not Specified"
    assert response.problem_analysis.expected_scale == "Not Specified"
    assert response.confidence < 0.90  # Reduced confidence due to missing scale/user details


@pytest.mark.asyncio
async def test_warehouse_app_pragmatic():
    agent = SolutionArchitectAgent()
    request = SolutionArchitectRequest(
        problem_statement="Build an AI-powered autonomous warehouse management system that optimizes inventory, predicts demand, and assigns robots to tasks."
    )
    
    mock_json_response = '''
    {
      "problem_analysis": {
        "business_problem": "Warehouse automation",
        "domain": "Warehouse & Logistics",
        "primary_objective": "Optimize inventory",
        "end_users": "Not Specified",
        "functional_requirements": [],
        "non_functional_requirements": [],
        "expected_scale": "Not Specified",
        "availability_requirements": "Not Specified",
        "performance_requirements": "Not Specified",
        "security_requirements": "Not Specified",
        "ai_requirements": "Required",
        "analytics_requirements": "Not Specified",
        "real_time_requirements": "Not Specified",
        "third_party_integrations": [],
        "deployment_constraints": "Not Specified"
      },
      "identified_requirements": {
        "real_time": true, "ai_required": true, "computer_vision": false,
        "nlp": false, "iot": true, "gps_tracking": false, "notifications": false,
        "authentication": false, "rbac": false, "queue_processing": false,
        "event_streaming": true, "caching": false, "analytics": false,
        "monitoring": false, "high_availability": false, "disaster_recovery": false
      },
      "architecture": {
        "type": "Edge Architecture",
        "rationale": "IoT Needs.",
        "why_alternatives_were_not_selected": "Latency."
      },
      "technology_recommendations": {
         "ai_models": {"technology": "GPT-4o-mini", "reason": "AI", "why_alternatives_not_selected": "N/A"}
      },
      "reasoning": [],
      "estimated_complexity": "High",
      "development_time": "3 months",
      "team_size": "5",
      "prototype_cost": "$500",
      "production_cost": "$2000",
      "confidence": 0.8
    }
    '''
    
    with patch.object(agent.service, '_call_llm', return_value=mock_json_response):
        response = await agent.process_request(request)

    assert isinstance(response, SolutionArchitectResponse)
    assert "Warehouse" in response.problem_analysis.domain or "Logistics" in response.problem_analysis.domain
    assert response.technology_recommendations.get("ai_models") is not None
    assert response.estimated_complexity in ["Medium", "High", "Very High"]


def test_fastapi_analyze_endpoint_pragmatic_schema():
    payload = {
        "problem_statement": "Build a personal habit tracker app."
    }
    
    mock_json_response = '''
    {
      "problem_analysis": {
        "business_problem": "Habit tracker",
        "domain": "Task Management",
        "primary_objective": "Track habits",
        "end_users": "Not Specified",
        "functional_requirements": [],
        "non_functional_requirements": [],
        "expected_scale": "Not Specified",
        "availability_requirements": "Not Specified",
        "performance_requirements": "Not Specified",
        "security_requirements": "Not Specified",
        "ai_requirements": "Not Specified",
        "analytics_requirements": "Not Specified",
        "real_time_requirements": "Not Specified",
        "third_party_integrations": [],
        "deployment_constraints": "Not Specified"
      },
      "identified_requirements": {
        "real_time": false, "ai_required": false, "computer_vision": false,
        "nlp": false, "iot": false, "gps_tracking": false, "notifications": false,
        "authentication": false, "rbac": false, "queue_processing": false,
        "event_streaming": false, "caching": false, "analytics": false,
        "monitoring": false, "high_availability": false, "disaster_recovery": false
      },
      "architecture": {
        "type": "Monolith",
        "rationale": "Simple.",
        "why_alternatives_were_not_selected": "Overkill."
      },
      "technology_recommendations": {},
      "reasoning": [],
      "estimated_complexity": "Low",
      "development_time": "1 week",
      "team_size": "1",
      "prototype_cost": "$0",
      "production_cost": "$0",
      "confidence": 0.8
    }
    '''
    with patch('agents.solution_architect.services.architect_service.SolutionArchitectService._call_llm', return_value=mock_json_response):
        response = client.post("/api/v1/agents/solution-architect/analyze", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    assert "problem_analysis" in data
    assert "domain" in data["problem_analysis"]
    assert "architecture" in data
    assert "type" in data["architecture"]
    assert "rationale" in data["architecture"]
    assert data["problem_analysis"]["end_users"] == "Not Specified"
    assert data["problem_analysis"]["expected_scale"] == "Not Specified"
    
    tech = data.get("technology_recommendations", {})
    assert tech.get("vector_database") is None
    assert tech.get("cache") is None
    assert tech.get("message_broker") is None
    assert tech.get("ai_models") is None


def test_invalid_gibberish_or_numeric_input():
    payload1 = {"problem_statement": "888888888888"}
    response1 = client.post("/api/v1/agents/solution-architect/analyze", json=payload1)
    assert response1.status_code == 400
    assert "Invalid problem statement" in response1.json()["detail"]


def test_fastapi_validation_error():
    payload = {"problem_statement": "short"}
    response = client.post("/api/v1/agents/solution-architect/analyze", json=payload)
    assert response.status_code == 422
