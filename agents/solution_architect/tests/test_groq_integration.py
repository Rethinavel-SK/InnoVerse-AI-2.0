"""
Real LLM Integration Tests — Solution Architect Agent (Groq)
============================================================
These tests make LIVE calls to the Groq API (llama-3.3-70b-versatile).
No mocking. Requires GROQ_API_KEY in .env or environment.

Run with:
    pytest agents/solution_architect/tests/test_groq_integration.py -v -s
"""

import os
import time
import pytest
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def agent():
    """Create a single SolutionArchitectAgent instance for all tests."""
    from agents.solution_architect.agent import SolutionArchitectAgent
    return SolutionArchitectAgent()


@pytest.fixture(scope="module")
def groq_api_key():
    """Ensure the Groq API key is present; skip the module if not."""
    key = os.getenv("GROQ_API_KEY")
    if not key:
        # Try loading from .env via dotenv (fallback)
        try:
            from dotenv import load_dotenv
            load_dotenv()
            key = os.getenv("GROQ_API_KEY")
        except ImportError:
            pass
    if not key:
        pytest.skip("GROQ_API_KEY not set — skipping live Groq tests.")
    return key


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

async def _run(agent, problem: str, context=None):
    """Convenience wrapper to call agent.run with a timer and log output."""
    logger.info(f"\n{'='*60}")
    logger.info(f"PROBLEM: {problem}")
    if context:
        logger.info(f"CONTEXT: {context}")
    logger.info(f"{'='*60}")

    start = time.perf_counter()
    response = await agent.run(problem, context)
    elapsed = (time.perf_counter() - start) * 1000

    logger.info(f"\n[✓] Architecture: {response.architecture.type}")
    logger.info(f"[✓] Domain       : {response.problem_analysis.domain}")
    logger.info(f"[✓] Complexity   : {response.estimated_complexity}")
    logger.info(f"[✓] Dev Time     : {response.development_time}")
    logger.info(f"[✓] Team Size    : {response.team_size}")
    logger.info(f"[✓] Prototype $  : {response.prototype_cost}")
    logger.info(f"[✓] Production $ : {response.production_cost}")
    logger.info(f"[✓] Confidence   : {response.confidence}")
    logger.info(f"[✓] Elapsed      : {elapsed:.0f}ms")
    logger.info(f"\n[RATIONALE] {response.architecture.rationale}")
    logger.info(f"\n[REASONING CHAIN]")
    for i, step in enumerate(response.reasoning, 1):
        logger.info(f"  {i}. {step}")
    logger.info(f"\n[TECH STACK]")
    for key, val in response.technology_recommendations.items():
        if val:
            logger.info(f"  {key}: {val}")

    return response


# ---------------------------------------------------------------------------
# TEST 1: Simple personal todo app → should be lightweight architecture
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_simple_todo_app_live(agent, groq_api_key):
    """
    Simple personal todo app → expect Layered/Modular Monolith, Low complexity,
    no unnecessary AI/ML/Kafka/Qdrant.
    """
    problem = "Build a simple todo list app for personal task tracking."
    response = await _run(agent, problem)

    # Schema integrity
    assert response.problem_analysis is not None
    assert response.architecture is not None
    assert response.identified_requirements is not None

    # Architecture sanity: no heavyweight pattern needed
    assert response.architecture.type in [
        "Layered Architecture",
        "Modular Monolith",
        "Clean Architecture",
    ], f"Expected lightweight architecture, got: {response.architecture.type}"

    # Complexity
    assert response.estimated_complexity in ["Low", "Medium"], \
        f"Expected Low/Medium complexity, got: {response.estimated_complexity}"

    # No AI needed for a todo list
    assert not response.identified_requirements.ai_required, \
        "AI should NOT be required for a simple todo app"

    # No vector DB for a todo list
    tech = response.technology_recommendations
    assert tech.get("vector_database") is None or tech.get("vector_database") == "null", \
        "Vector DB should NOT be recommended for a simple todo app"

    # Confidence: should be low-to-medium (vague, underspecified)
    assert 0.0 < response.confidence <= 1.0

    logger.info("\n✅ TEST 1 PASSED: Simple Todo App")


# ---------------------------------------------------------------------------
# TEST 2: AI-powered warehouse management → expect complex architecture + AI
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_warehouse_ai_system_live(agent, groq_api_key):
    """
    AI-powered autonomous warehouse management with robots, demand prediction, IoT.
    Expect: Microservices/Event Driven/Edge, AI required, IoT required, High complexity.
    """
    problem = (
        "Build an AI-powered autonomous warehouse management system that "
        "optimizes inventory, predicts demand, and assigns robots to tasks in real time."
    )
    response = await _run(agent, problem)

    # AI must be identified
    assert response.identified_requirements.ai_required, \
        "AI should be required for an AI-powered warehouse system"

    # IoT should be identified (robots/sensors)
    assert response.identified_requirements.iot or response.identified_requirements.real_time, \
        "IoT or real-time should be flagged for a robot-based warehouse system"

    # Architecture should be complex
    assert response.architecture.type in [
        "Microservices",
        "Event Driven Architecture",
        "Edge Architecture",
        "Hybrid Architecture",
    ], f"Expected complex architecture, got: {response.architecture.type}"

    # Complexity should be High or Very High
    assert response.estimated_complexity in ["High", "Very High"], \
        f"Expected High/Very High complexity, got: {response.estimated_complexity}"

    # AI models should be recommended
    tech = response.technology_recommendations
    assert tech.get("ai_models") is not None, \
        "AI models should be recommended for an AI warehouse system"

    logger.info("\n✅ TEST 2 PASSED: AI Warehouse Management System")


# ---------------------------------------------------------------------------
# TEST 3: Healthcare telemedicine platform → HIPAA, real-time video, security
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_healthcare_telemedicine_live(agent, groq_api_key):
    """
    Healthcare telemedicine platform → expect security requirements, HIPAA,
    real-time video/communication requirements.
    """
    problem = (
        "Build a telemedicine platform for connecting patients with doctors "
        "via real-time video consultations, prescription management, and EHR integration. "
        "Must be HIPAA compliant."
    )
    response = await _run(agent, problem)

    # Domain should be Healthcare
    assert "Health" in response.problem_analysis.domain or "Medical" in response.problem_analysis.domain, \
        f"Domain should be Healthcare-related, got: {response.problem_analysis.domain}"

    # Security must be specified (HIPAA)
    assert response.problem_analysis.security_requirements != "Not Specified", \
        "Security requirements must be specified for HIPAA-compliant healthcare platform"

    # Real-time should be identified (video calls)
    assert response.identified_requirements.real_time, \
        "Real-time should be required for video consultations"

    # Should not be a simple monolith
    assert response.architecture.type not in ["Modular Monolith", "Layered Architecture"], \
        f"Healthcare platform should not use a simple monolith: {response.architecture.type}"

    # Authentication must be recommended
    tech = response.technology_recommendations
    assert tech.get("authentication") is not None, \
        "Authentication must be recommended for a healthcare platform"

    logger.info("\n✅ TEST 3 PASSED: Healthcare Telemedicine Platform")


# ---------------------------------------------------------------------------
# TEST 4: FinTech fraud detection → AI, analytics, high availability
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_fintech_fraud_detection_live(agent, groq_api_key):
    """
    FinTech real-time fraud detection using AI.
    Expect: AI required, analytics, event streaming, high availability.
    """
    problem = (
        "Build a real-time fraud detection system for a digital banking platform "
        "that analyzes transactions using ML models, supports 100,000 TPS, "
        "and must maintain 99.99% uptime with PCI DSS compliance."
    )
    response = await _run(agent, problem)

    # AI required
    assert response.identified_requirements.ai_required or response.identified_requirements.analytics, \
        "AI/Analytics should be required for fraud detection"

    # High availability should be flagged
    assert response.identified_requirements.high_availability, \
        "High availability should be required for 99.99% uptime"

    # Complexity should be High or Very High
    assert response.estimated_complexity in ["High", "Very High"], \
        f"Fraud detection at scale should be High/Very High complexity"

    # Security should be specified (PCI DSS)
    assert response.problem_analysis.security_requirements != "Not Specified", \
        "Security requirements must be specified for PCI DSS compliance"

    logger.info("\n✅ TEST 4 PASSED: FinTech Fraud Detection System")


# ---------------------------------------------------------------------------
# TEST 5: Smart agriculture IoT platform
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_smart_agriculture_iot_live(agent, groq_api_key):
    """
    Smart agriculture IoT platform with sensor data, weather APIs, and AI crop prediction.
    Expect: IoT flagged, AI required, external APIs (weather), analytics.
    """
    problem = (
        "Build a smart agriculture platform that collects soil sensor data from IoT devices, "
        "integrates weather APIs, and uses AI to predict optimal irrigation schedules and crop yields."
    )
    response = await _run(agent, problem)

    # IoT should be required
    assert response.identified_requirements.iot, \
        "IoT should be required for a sensor-based agriculture platform"

    # AI should be required
    assert response.identified_requirements.ai_required, \
        "AI should be required for crop yield prediction"

    # Domain should be Agriculture related
    assert "Agri" in response.problem_analysis.domain or "Farm" in response.problem_analysis.domain, \
        f"Domain should be Agriculture-related, got: {response.problem_analysis.domain}"

    # External APIs should include weather
    third_party = response.problem_analysis.third_party_integrations
    assert len(third_party) > 0, \
        "Weather API should be identified as third-party integration"

    logger.info("\n✅ TEST 5 PASSED: Smart Agriculture IoT Platform")


# ---------------------------------------------------------------------------
# TEST 6: Context-enriched request (explicit constraints provided)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_context_enriched_request_live(agent, groq_api_key):
    """
    Problem statement + explicit context (budget, scale, cloud preference).
    Verify that context influences the architecture output.
    """
    problem = "Build an e-commerce platform with product search and checkout."
    context = {
        "budget": "$5,000/month",
        "expected_users": "500,000 monthly active users",
        "cloud_preference": "AWS",
        "team_size": "10 engineers",
    }
    response = await _run(agent, problem, context)

    # Basic schema assertions
    assert response.problem_analysis is not None
    assert response.architecture.type is not None
    assert response.architecture.rationale is not None

    # Domain should be e-commerce or retail
    assert any(kw in response.problem_analysis.domain for kw in ["Commerce", "Retail", "E-commerce"]), \
        f"Domain should be E-commerce related, got: {response.problem_analysis.domain}"

    # Confidence should be higher with explicit context
    assert response.confidence >= 0.6, \
        f"Confidence should be reasonable with explicit context, got: {response.confidence}"

    logger.info("\n✅ TEST 6 PASSED: Context-Enriched E-Commerce Request")


# ---------------------------------------------------------------------------
# TEST 7: Full pipeline execution (returns SolutionDesignResult with metadata)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_full_pipeline_execution_live(agent, groq_api_key):
    """
    Tests execute_full_pipeline() which wraps the response with execution metadata.
    """
    from agents.solution_architect.schemas.architect_schema import SolutionArchitectRequest
    from agents.solution_architect.models.domain import SolutionDesignResult

    request = SolutionArchitectRequest(
        problem_statement="Build a ride-sharing platform like Uber for motorcycles in Southeast Asia."
    )

    start = time.perf_counter()
    result = await agent.execute_full_pipeline(request)
    elapsed = (time.perf_counter() - start) * 1000

    logger.info(f"\n[PIPELINE RESULT]")
    logger.info(f"  Request ID   : {result.request_id}")
    logger.info(f"  Agent        : {result.metadata.agent_name}")
    logger.info(f"  Version      : {result.metadata.version}")
    logger.info(f"  Model Used   : {result.metadata.model_used}")
    logger.info(f"  Exec Time    : {result.metadata.execution_time_ms}ms")
    logger.info(f"  Total Elapsed: {elapsed:.0f}ms")

    # SolutionDesignResult assertions
    assert isinstance(result, SolutionDesignResult)
    assert result.request_id is not None
    assert result.metadata.agent_name == "SolutionArchitectAgent"
    assert result.metadata.model_used == agent.service.model_name
    assert result.metadata.execution_time_ms > 0
    assert "architecture" in result.architecture_output
    assert "problem_analysis" in result.architecture_output

    # GPS tracking should be flagged for ride-sharing
    identified = result.architecture_output.get("identified_requirements", {})
    assert identified.get("gps_tracking") is True, \
        "GPS tracking should be required for a ride-sharing platform"

    logger.info("\n✅ TEST 7 PASSED: Full Pipeline Execution (Ride-Sharing)")
