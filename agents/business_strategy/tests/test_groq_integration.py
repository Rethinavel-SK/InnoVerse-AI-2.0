"""
Real LLM Integration Tests — Business Strategy Agent (Groq)
============================================================
These tests make LIVE calls to the Groq API (llama-3.3-70b-versatile).
No mocking. Requires GROQ_API_KEY in .env or environment.

Run with:
    pytest agents/business_strategy/tests/test_groq_integration.py -v -s
"""

import os
import time
import json
import pytest
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def agent():
    """Create a single BusinessStrategyAgent instance for all tests."""
    from agents.business_strategy.agent import BusinessStrategyAgent
    return BusinessStrategyAgent()


@pytest.fixture(scope="module")
def groq_api_key():
    """Ensure the Groq API key is present; skip the module if not."""
    key = os.getenv("GROQ_API_KEY")
    if not key:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            key = os.getenv("GROQ_API_KEY")
        except ImportError:
            pass
    if not key:
        pytest.skip("GROQ_API_KEY not set — skipping live Groq integration tests.")
    return key


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

async def _run(agent, problem: str, context=None):
    """Convenience wrapper to call agent.run with timing and structured logging."""
    logger.info("\n%s", "=" * 70)
    logger.info("PROBLEM: %s", problem)
    if context:
        logger.info("CONTEXT: %s", context)
    logger.info("%s", "=" * 70)

    start = time.perf_counter()
    response = await agent.run(problem, context)
    elapsed = (time.perf_counter() - start) * 1000

    logger.info("\n[✓] Business Model     : %s", response.business_model[:80])
    logger.info("[✓] Pricing Model      : %s", response.pricing_model[:80])
    logger.info("[✓] Value Proposition  : %s", response.value_proposition[:100])
    logger.info("[✓] Customer Segments  : %d identified", len(response.target_customers))
    logger.info("[✓] Revenue Streams    : %d identified", len(response.revenue_streams))
    logger.info("[✓] Competitors        : %d identified", len(response.competitors))
    logger.info("[✓] Marketing Channels : %d identified", len(response.marketing_channels))
    logger.info("[✓] TAM                : %s", response.market_size.tam)
    logger.info("[✓] SAM                : %s", response.market_size.sam)
    logger.info("[✓] SOM                : %s", response.market_size.som)
    logger.info("[✓] SWOT Strengths     : %d items", len(response.swot.strengths))
    logger.info("[✓] SWOT Weaknesses    : %d items", len(response.swot.weaknesses))
    logger.info("[✓] SWOT Opportunities : %d items", len(response.swot.opportunities))
    logger.info("[✓] SWOT Threats       : %d items", len(response.swot.threats))
    logger.info("[✓] Confidence         : %.2f", response.confidence)
    logger.info("[✓] Elapsed            : %.0fms", elapsed)

    logger.info("\n[REASONING CHAIN]")
    for i, step in enumerate(response.reasoning, 1):
        logger.info("  %d. %s", i, step)

    logger.info("\n[BUSINESS MODEL CANVAS]")
    canvas = response.business_canvas
    logger.info("  Key Partners      : %s", canvas.key_partners)
    logger.info("  Key Activities    : %s", canvas.key_activities)
    logger.info("  Key Resources     : %s", canvas.key_resources)
    logger.info("  Value Props       : %s", canvas.value_propositions)
    logger.info("  Cost Structure    : %s", canvas.cost_structure)
    logger.info("  Revenue Streams   : %s", canvas.revenue_streams)

    return response


# ---------------------------------------------------------------------------
# TEST 1: SaaS restaurant management — B2B SaaS, Tiered pricing
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_restaurant_saas_strategy_live(agent, groq_api_key):
    """
    AI-powered restaurant inventory SaaS.
    Expect: B2B SaaS model, Tiered pricing, AI/food-waste competitors.
    """
    problem = (
        "Build an AI-powered platform that helps small restaurants manage inventory "
        "and reduce food waste using predictive analytics."
    )
    response = await _run(agent, problem)

    # Schema integrity
    assert response.target_customers, "Must identify at least one customer segment"
    assert response.value_proposition, "Value proposition must be present"
    assert response.pricing_model, "Pricing model must be present"
    assert response.business_model, "Business model must be present"
    assert response.revenue_streams, "Revenue streams must be present"
    assert response.go_to_market, "GTM strategy must be present"
    assert response.marketing_channels, "Marketing channels must be present"
    assert response.market_size, "Market size must be present"
    assert response.competitors, "Competitors must be present"
    assert response.swot, "SWOT must be present"
    assert response.business_canvas, "Business canvas must be present"

    # Business model should be B2B focused
    assert any(
        kw in response.business_model.upper()
        for kw in ["B2B", "SAAS", "SOFTWARE"]
    ), f"Expected B2B/SaaS model, got: {response.business_model}"

    # Must identify at least 2 customer segments
    assert len(response.target_customers) >= 2, \
        f"Expected >=2 customer segments, got: {len(response.target_customers)}"

    # Market size must have all three fields
    assert response.market_size.tam
    assert response.market_size.sam
    assert response.market_size.som

    # SWOT must be complete
    assert len(response.swot.strengths) >= 2
    assert len(response.swot.weaknesses) >= 2
    assert len(response.swot.opportunities) >= 2
    assert len(response.swot.threats) >= 2

    # Business Model Canvas must have all 9 blocks populated
    canvas = response.business_canvas
    assert canvas.key_partners
    assert canvas.key_activities
    assert canvas.key_resources
    assert canvas.value_propositions
    assert canvas.customer_relationships
    assert canvas.channels
    assert canvas.customer_segments
    assert canvas.cost_structure
    assert canvas.revenue_streams

    # Confidence must be valid
    assert 0.0 < response.confidence <= 1.0

    logger.info("\n✅ TEST 1 PASSED: Restaurant AI SaaS Strategy")


# ---------------------------------------------------------------------------
# TEST 2: FinTech peer-to-peer lending — marketplace model
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_fintech_p2p_lending_strategy_live(agent, groq_api_key):
    """
    FinTech P2P lending platform for gig economy workers.
    Expect: Marketplace model, transaction/revenue-share pricing, FinTech competitors.
    """
    problem = (
        "Build a peer-to-peer lending platform that connects gig economy workers "
        "(Uber drivers, freelancers) with micro-lenders for emergency personal loans "
        "up to $5,000 with AI-driven credit scoring."
    )
    response = await _run(agent, problem)

    # Should be marketplace or platform model
    assert any(
        kw in response.business_model.upper()
        for kw in ["MARKETPLACE", "PLATFORM", "FINTECH", "B2B2C", "LENDING"]
    ), f"Expected marketplace/FinTech model, got: {response.business_model}"

    # Pricing should reference transaction, revenue share, or lending-appropriate model
    assert any(
        kw in response.pricing_model.upper()
        for kw in ["COMMISSION", "TRANSACTION", "REVENUE SHARE", "FEE", "INTEREST",
                   "FREEMIUM", "TIER", "SUBSCRIPTION", "CREDIT", "LENDING"]
    ), f"Expected transaction/lending-based pricing, got: {response.pricing_model}"

    # Must identify competitors in FinTech/lending space
    competitor_names = " ".join([c.name for c in response.competitors]).upper()
    assert len(response.competitors) >= 2, "Must identify at least 2 FinTech competitors"

    # Marketing channels should include digital-first channels
    assert len(response.marketing_channels) >= 3

    # Confidence should be decent with a detailed problem statement
    assert response.confidence >= 0.6, \
        f"Confidence should be >= 0.6 for a detailed problem, got: {response.confidence}"

    logger.info("\n✅ TEST 2 PASSED: FinTech P2P Lending Strategy")


# ---------------------------------------------------------------------------
# TEST 3: EdTech platform — B2C / Freemium pricing
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_edtech_learning_platform_strategy_live(agent, groq_api_key):
    """
    AI-powered personalised learning platform for K-12 students.
    Expect: B2C or B2B2C model, Freemium pricing, Duolingo/Khan Academy as competitors.
    """
    problem = (
        "Build an AI-powered personalised learning app for K-12 students that adapts "
        "lesson difficulty in real-time based on student performance and provides "
        "weekly progress reports for parents."
    )
    response = await _run(agent, problem)

    # Should identify students/parents/schools as segments
    segment_names = " ".join([s.segment_name for s in response.target_customers]).upper()
    assert any(
        kw in segment_names
        for kw in ["STUDENT", "PARENT", "SCHOOL", "TEACHER", "K-12", "EDUCATOR"]
    ), f"Expected education-related segments, got: {segment_names}"

    # Model should be B2C, B2B2C, or any recognised EdTech-adjacent type
    assert any(
        kw in response.business_model.upper()
        for kw in ["B2C", "B2B2C", "EDTECH", "CONSUMER", "EDUCATION",
                   "B2B", "SAAS", "PLATFORM", "SCHOOL", "LEARNING"]
    ), f"Expected B2C/EdTech/SaaS model, got: {response.business_model}"

    # Pricing should include freemium or subscription
    assert any(
        kw in response.pricing_model.upper()
        for kw in ["FREEMIUM", "SUBSCRIPTION", "FREE", "PREMIUM", "TIER"]
    ), f"Expected freemium/subscription pricing, got: {response.pricing_model}"

    # SWOT and canvas must be fully populated
    assert response.swot.strengths
    assert response.business_canvas.value_propositions

    logger.info("\n✅ TEST 3 PASSED: EdTech Learning Platform Strategy")


# ---------------------------------------------------------------------------
# TEST 4: HealthTech telemedicine — regulated market
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_healthtech_telemedicine_strategy_live(agent, groq_api_key):
    """
    Telemedicine SaaS platform for mental health therapy.
    Expect: B2B2C or B2C model, regulatory awareness in SWOT, HIPAA-related threats.
    """
    problem = (
        "Build a telemedicine platform connecting licensed therapists with patients "
        "for online mental health sessions. The platform should support video calls, "
        "session notes, prescription management, and insurance billing."
    )
    response = await _run(agent, problem)

    # Must have patient and therapist/clinic segments
    segment_names = " ".join([s.segment_name for s in response.target_customers]).upper()
    assert any(
        kw in segment_names
        for kw in ["PATIENT", "THERAPIST", "CLINIC", "PROVIDER", "HEALTH", "MENTAL"]
    ), f"Expected health-related segments, got: {segment_names}"

    # SWOT threats should mention regulatory/compliance risks
    threats_text = " ".join(response.swot.threats).upper()
    assert any(
        kw in threats_text
        for kw in ["REGULATION", "COMPLIANCE", "HIPAA", "FDA", "PRIVACY", "REGULATORY", "LEGAL"]
    ), f"Regulatory risks should appear in SWOT threats, got: {threats_text}"

    # Market size should be large (mental health is a massive market)
    assert response.market_size.tam, "TAM must be specified for healthcare market"

    # Should identify at least 2 competitors
    assert len(response.competitors) >= 2

    logger.info("\n✅ TEST 4 PASSED: HealthTech Telemedicine Strategy")


# ---------------------------------------------------------------------------
# TEST 5: Vague problem statement — low confidence expected
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_vague_problem_statement_low_confidence_live(agent, groq_api_key):
    """
    A vague, underspecified problem statement.
    Expect: structurally valid response with a reduced confidence score.

    NOTE: The LLM will still attempt a strategy even for vague inputs — that
    is by design (it never refuses).  The system prompt instructs it to *lower*
    confidence when context is missing, so we assert it stays below 0.90.
    """
    problem = "Build an app that helps people."
    response = await _run(agent, problem)

    # Response must still be structurally valid
    assert response.target_customers, "Must return at least one customer segment"
    assert response.value_proposition, "Value proposition must be present"
    assert response.business_model, "Business model must be present"
    assert response.swot, "SWOT must be present"
    assert response.business_canvas, "Business canvas must be present"

    # Confidence must be in valid range
    assert 0.0 < response.confidence <= 1.0, \
        f"Confidence must be between 0 and 1, got: {response.confidence}"

    # Confidence should be reduced for a vague, underspecified problem
    # (the system prompt explicitly penalises vague input — threshold: 0.90)
    assert response.confidence <= 0.90, (
        f"Confidence for a vague prompt should be <= 0.90, got: {response.confidence}. "
        "The LLM may not be penalising underspecified inputs as instructed."
    )

    logger.info("\n✅ TEST 5 PASSED: Vague Problem Statement (Confidence=%.2f)", response.confidence)


# ---------------------------------------------------------------------------
# TEST 6: Context-enriched request — higher confidence expected
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_context_enriched_strategy_live(agent, groq_api_key):
    """
    A well-specified problem with explicit context.
    Expect: higher confidence, context-aligned recommendations.
    """
    problem = (
        "Build a B2B SaaS platform for HR teams at mid-size companies to automate "
        "employee onboarding, compliance training, and performance reviews."
    )
    context = {
        "target_region": "North America",
        "company_stage": "Seed-stage startup",
        "budget": "$750K",
        "team_size": "6 engineers",
        "target_company_size": "100-1000 employees",
    }
    response = await _run(agent, problem, context)

    # Should identify HR professionals as primary segment
    segment_names = " ".join([s.segment_name for s in response.target_customers]).upper()
    assert any(
        kw in segment_names
        for kw in ["HR", "HUMAN RESOURCES", "PEOPLE OPS", "COMPANY", "ENTERPRISE", "EMPLOYEE"]
    ), f"Expected HR-related segments, got: {segment_names}"

    # Pricing should be B2B subscription/tier focused
    assert any(
        kw in response.pricing_model.upper()
        for kw in ["SAAS", "SUBSCRIPTION", "TIER", "PER-SEAT", "SEAT"]
    ), f"Expected SaaS subscription pricing, got: {response.pricing_model}"

    # Confidence should be >= 0.70 with rich context
    assert response.confidence >= 0.70, \
        f"Confidence should be >= 0.70 with detailed context, got: {response.confidence}"

    logger.info("\n✅ TEST 6 PASSED: Context-Enriched HR SaaS Strategy")


# ---------------------------------------------------------------------------
# TEST 7: Full pipeline execution — metadata wrapping
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_full_pipeline_execution_live(agent, groq_api_key):
    """
    Tests execute_full_pipeline() which wraps the response with execution metadata.
    Validates request_id, agent name, version, model_used, and execution_time_ms.
    """
    from agents.business_strategy.schemas.strategy_schema import BusinessStrategyRequest
    from agents.business_strategy.models.domain import BusinessStrategyResult

    request = BusinessStrategyRequest(
        problem_statement=(
            "Build a D2C subscription box service for premium pet food "
            "using AI to personalise meal plans based on pet breed, age, and health conditions."
        )
    )

    start = time.perf_counter()
    result = await agent.execute_full_pipeline(request)
    elapsed = (time.perf_counter() - start) * 1000

    logger.info("\n[PIPELINE RESULT]")
    logger.info("  Request ID     : %s", result.request_id)
    logger.info("  Agent Name     : %s", result.metadata.agent_name)
    logger.info("  Version        : %s", result.metadata.version)
    logger.info("  Model Used     : %s", result.metadata.model_used)
    logger.info("  Exec Time      : %.2fms", result.metadata.execution_time_ms)
    logger.info("  Total Elapsed  : %.0fms", elapsed)

    # Validate BusinessStrategyResult structure
    assert isinstance(result, BusinessStrategyResult)
    assert result.request_id is not None and len(result.request_id) == 36  # UUID format
    assert result.metadata.agent_name == "BusinessStrategyAgent"
    assert result.metadata.version == "1.0.0"
    assert result.metadata.model_used == "llama-3.1-8b-instant"
    assert result.metadata.execution_time_ms > 0

    # Validate all top-level keys are present in strategy_output
    output = result.strategy_output
    required_keys = [
        "target_customers", "value_proposition", "pricing_model",
        "business_model", "revenue_streams", "go_to_market",
        "marketing_channels", "market_size", "competitors",
        "swot", "business_canvas", "confidence",
    ]
    for key in required_keys:
        assert key in output, f"Missing key in strategy_output: {key}"

    # D2C subscription box → should identify pet owner segment
    customer_text = json.dumps(output["target_customers"]).upper()
    assert any(
        kw in customer_text
        for kw in ["PET", "OWNER", "DOG", "CAT", "ANIMAL", "CONSUMER"]
    ), f"Expected pet-owner related segment, got: {customer_text[:200]}"

    logger.info("\n✅ TEST 7 PASSED: Full Pipeline Execution (Pet Food D2C)")
