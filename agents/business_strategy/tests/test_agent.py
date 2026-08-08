"""
Unit Tests — Business Strategy Agent (Mocked)
==============================================
Tests all layers of the Business Strategy Agent using mocked LLM responses.
No live API calls — fast, deterministic, CI-safe.

Run with:
    pytest agents/business_strategy/tests/test_agent.py -v
"""

import pytest
import asyncio
import json
import logging
from unittest.mock import AsyncMock, MagicMock, patch

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Shared mock payload factory
# ---------------------------------------------------------------------------

def _make_mock_strategy_payload(
    business_model: str = "B2B SaaS",
    confidence: float = 0.87,
) -> dict:
    """Returns a minimal valid strategy payload for mocking the LLM."""
    return {
        "target_customers": [
            {
                "segment_name": "SMB Restaurant Owners",
                "description": "Small restaurant owners struggling with manual inventory.",
                "size_estimate": "~1.5M restaurants in the US",
                "willingness_to_pay": "Medium",
            },
            {
                "segment_name": "Multi-chain Restaurant Groups",
                "description": "Groups managing 5-50 locations needing centralised oversight.",
                "size_estimate": "~50K multi-chain operators globally",
                "willingness_to_pay": "High",
            },
        ],
        "value_proposition": (
            "We help SMB restaurant owners who lose 10-15% revenue to food waste "
            "by providing AI-powered inventory optimisation, unlike spreadsheets and generic POS "
            "systems we reduce waste by 40% within the first month."
        ),
        "pricing_model": (
            "Tiered SaaS: Starter ($49/mo for 1 location), Pro ($149/mo for up to 5), "
            "Enterprise (custom for 5+ locations). Justified by predictable cost for operators."
        ),
        "business_model": business_model,
        "revenue_streams": [
            {
                "stream_name": "SaaS Subscription",
                "description": "Monthly/annual plans billed per location.",
                "estimated_contribution": "75% of revenue",
            },
            {
                "stream_name": "Supplier Marketplace Commission",
                "description": "Commission on orders placed through integrated supplier network.",
                "estimated_contribution": "20% of revenue",
            },
            {
                "stream_name": "Professional Onboarding Services",
                "description": "One-time setup and staff training packages.",
                "estimated_contribution": "5% of revenue",
            },
        ],
        "go_to_market": (
            "Phase 1 (0-6mo): Target independent restaurant owners in 2 US metros via food-industry "
            "influencers and direct outreach. Offer free 30-day pilot. Achieve 50 paying customers. "
            "Phase 2 (6-18mo): Partner with POS vendors (Toast, Square) for co-marketing. "
            "Expand to 10 metros, 500 paying customers. "
            "Phase 3 (18mo+): Launch supplier marketplace, target multi-chain groups via enterprise sales."
        ),
        "marketing_channels": [
            "Content Marketing / SEO (restaurant management blog)",
            "LinkedIn Outbound targeting restaurant group owners",
            "Food industry conference sponsorships (NRA Show, FSTEC)",
            "POS vendor partnership referrals (Toast, Square)",
            "YouTube tutorials on food cost management",
        ],
        "market_size": {
            "tam": "$12B — Global restaurant management software market",
            "sam": "$3B — US SMB restaurants willing to adopt cloud SaaS",
            "som": "$150M — Achievable within 5 years targeting metro markets",
            "rationale": (
                "Bottom-up: 1.5M US restaurants × 40% SaaS adoption rate × $250 ARPU/year = $150M SOM."
            ),
        },
        "competitors": [
            {
                "name": "MarketMan",
                "strengths": "Established brand, deep POS integrations.",
                "weaknesses": "Complex UX, slow support, no AI features.",
                "differentiation": "AI-first waste prediction vs. manual rule configuration.",
            },
            {
                "name": "BlueCart",
                "strengths": "Strong supplier network, mobile ordering.",
                "weaknesses": "Inventory management is secondary, no AI insights.",
                "differentiation": "Inventory AI is core, supplier marketplace is an add-on.",
            },
        ],
        "swot": {
            "strengths": [
                "AI-driven waste prediction as core differentiator",
                "Real-time dashboards reducing cognitive load for operators",
                "Fast 30-day onboarding with measurable ROI",
            ],
            "weaknesses": [
                "No brand awareness vs. incumbents",
                "POS integrations require engineering investment",
                "High churn risk if ROI not demonstrated early",
            ],
            "opportunities": [
                "Post-pandemic restaurant digitisation wave",
                "Rising food costs increasing sensitivity to waste",
                "Lack of AI-native tools in this vertical",
            ],
            "threats": [
                "Toast and Square launching native inventory AI features",
                "Economic recession reducing restaurant SaaS budgets",
                "High sales cycle in conservative restaurant industry",
            ],
        },
        "business_canvas": {
            "key_partners": [
                "POS vendors (Toast, Square, Lightspeed)",
                "Food suppliers and distributors",
                "Cloud infrastructure (AWS / GCP)",
            ],
            "key_activities": [
                "AI model development and continuous training",
                "POS integration engineering",
                "Customer success and onboarding",
                "Supplier marketplace curation",
            ],
            "key_resources": [
                "Proprietary waste prediction ML model",
                "Engineering team (8-12 engineers)",
                "POS integration library",
                "Customer success playbooks",
            ],
            "value_propositions": [
                "Reduce food waste by 40% using AI-driven inventory forecasting",
                "Centralised multi-location inventory control for restaurant groups",
            ],
            "customer_relationships": [
                "Self-service onboarding with in-app tutorials (SMB)",
                "Dedicated Customer Success Manager (Enterprise)",
                "Community forum and knowledge base",
            ],
            "channels": [
                "Direct sales website",
                "POS marketplace listings",
                "Food industry events",
                "Content marketing and SEO",
            ],
            "customer_segments": [
                "SMB independent restaurant owners (1-4 locations)",
                "Multi-chain restaurant groups (5-50 locations)",
            ],
            "cost_structure": [
                "Cloud infrastructure and ML compute",
                "Engineering salaries (60% of OPEX)",
                "Sales and marketing spend",
                "Customer success team",
            ],
            "revenue_streams": [
                "Monthly SaaS subscription per location",
                "Supplier marketplace transaction commission",
                "One-time onboarding service fee",
            ],
        },
        "reasoning": [
            "Step 1: Identified SMBs and multi-chain operators as primary customer segments based on operational pain...",
            "Step 2: Value proposition anchored on 40% waste reduction as measurable outcome...",
            "Step 3: Tiered SaaS pricing chosen as it aligns with restaurant scale and reduces churn risk...",
            "Step 4: B2B SaaS model as restaurants pay monthly for software access...",
            "Step 5: Three revenue streams diversify income: subscription, marketplace, services...",
            "Step 6: GTM starts with metro-focused direct sales then expands via POS partnerships...",
            "Step 7: Content marketing and conference presence best reach restaurant decision-makers...",
            "Step 8: Market size derived bottom-up from US restaurant count and SaaS adoption data...",
            "Step 9: MarketMan and BlueCart identified as closest competitors lacking AI-native approach...",
            "Step 10: SWOT shows strong AI differentiation but brand awareness gap is key weakness...",
            "Step 11: BMC canvas built to highlight POS integration as critical key activity...",
        ],
        "confidence": confidence,
    }


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def agent():
    """Create a BusinessStrategyAgent with a mocked service."""
    from agents.business_strategy.agent import BusinessStrategyAgent
    return BusinessStrategyAgent()


@pytest.fixture
def valid_request():
    """Return a valid BusinessStrategyRequest fixture."""
    from agents.business_strategy.schemas.strategy_schema import BusinessStrategyRequest
    return BusinessStrategyRequest(
        problem_statement=(
            "Build an AI-powered platform that helps small restaurants manage "
            "inventory and reduce food waste using predictive analytics."
        )
    )


@pytest.fixture
def mock_llm_response():
    """Return a JSON string simulating the LLM response."""
    return json.dumps(_make_mock_strategy_payload())


# ---------------------------------------------------------------------------
# Schema Tests
# ---------------------------------------------------------------------------

class TestBusinessStrategySchemas:
    """Unit tests for Pydantic schema validation."""

    def test_request_schema_valid(self):
        from agents.business_strategy.schemas.strategy_schema import BusinessStrategyRequest
        req = BusinessStrategyRequest(
            problem_statement="Build a SaaS platform for remote teams."
        )
        assert req.problem_statement == "Build a SaaS platform for remote teams."
        assert req.context is None

    def test_request_schema_with_context(self):
        from agents.business_strategy.schemas.strategy_schema import BusinessStrategyRequest
        req = BusinessStrategyRequest(
            problem_statement="Build a fintech lending app for gig workers.",
            context={"region": "India", "stage": "Pre-seed"}
        )
        assert req.context["region"] == "India"

    def test_request_schema_too_short_raises(self):
        from agents.business_strategy.schemas.strategy_schema import BusinessStrategyRequest
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            BusinessStrategyRequest(problem_statement="hi")

    def test_response_schema_full_payload(self):
        from agents.business_strategy.schemas.strategy_schema import BusinessStrategyResponse
        payload = _make_mock_strategy_payload()
        response = BusinessStrategyResponse(**payload)
        assert response.confidence == 0.87
        assert len(response.target_customers) == 2
        assert len(response.revenue_streams) == 3
        assert response.swot.strengths
        assert response.swot.weaknesses
        assert response.swot.opportunities
        assert response.swot.threats
        assert response.business_canvas.key_partners

    def test_response_confidence_bounds(self):
        from agents.business_strategy.schemas.strategy_schema import BusinessStrategyResponse
        from pydantic import ValidationError
        payload = _make_mock_strategy_payload(confidence=1.5)
        with pytest.raises(ValidationError):
            BusinessStrategyResponse(**payload)

    def test_response_confidence_zero_allowed(self):
        from agents.business_strategy.schemas.strategy_schema import BusinessStrategyResponse
        payload = _make_mock_strategy_payload(confidence=0.0)
        response = BusinessStrategyResponse(**payload)
        assert response.confidence == 0.0

    def test_market_size_fields_present(self):
        from agents.business_strategy.schemas.strategy_schema import BusinessStrategyResponse
        payload = _make_mock_strategy_payload()
        response = BusinessStrategyResponse(**payload)
        assert response.market_size.tam
        assert response.market_size.sam
        assert response.market_size.som
        assert response.market_size.rationale

    def test_business_canvas_has_all_nine_blocks(self):
        from agents.business_strategy.schemas.strategy_schema import BusinessStrategyResponse
        payload = _make_mock_strategy_payload()
        response = BusinessStrategyResponse(**payload)
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


# ---------------------------------------------------------------------------
# Service Tests (Mocked LLM)
# ---------------------------------------------------------------------------

class TestBusinessStrategyService:
    """Unit tests for BusinessStrategyService with mocked Groq client."""

    def _make_service(self):
        from agents.business_strategy.services.strategy_service import BusinessStrategyService
        return BusinessStrategyService(api_key="test-api-key", model_name="llama-3.3-70b-versatile")

    def test_validate_problem_statement_valid(self):
        service = self._make_service()
        service.validate_problem_statement("Build a SaaS tool for restaurant inventory management.")

    def test_validate_problem_statement_too_short_alpha(self):
        from fastapi import HTTPException
        service = self._make_service()
        with pytest.raises(HTTPException) as exc_info:
            service.validate_problem_statement("123!!")
        assert exc_info.value.status_code == 400

    def test_validate_problem_statement_repetitive_symbols(self):
        from fastapi import HTTPException
        service = self._make_service()
        with pytest.raises(HTTPException) as exc_info:
            service.validate_problem_statement("aaaaaaaaaaaaa")
        assert exc_info.value.status_code == 400

    def test_parse_json_response_clean(self):
        service = self._make_service()
        payload = _make_mock_strategy_payload()
        raw = json.dumps(payload)
        result = service._parse_json_response(raw)
        assert result["business_model"] == "B2B SaaS"

    def test_parse_json_response_with_markdown_fences(self):
        service = self._make_service()
        payload = _make_mock_strategy_payload()
        raw = "```json\n" + json.dumps(payload) + "\n```"
        result = service._parse_json_response(raw)
        assert "target_customers" in result

    def test_parse_json_response_with_plain_fences(self):
        service = self._make_service()
        payload = _make_mock_strategy_payload()
        raw = "```\n" + json.dumps(payload) + "\n```"
        result = service._parse_json_response(raw)
        assert "swot" in result

    @pytest.mark.asyncio
    async def test_analyze_missing_api_key_raises_503(self):
        from agents.business_strategy.services.strategy_service import BusinessStrategyService
        from agents.business_strategy.schemas.strategy_schema import BusinessStrategyRequest
        from fastapi import HTTPException

        service = BusinessStrategyService(api_key=None, model_name="llama-3.3-70b-versatile")
        service.api_key = None  # Force None

        request = BusinessStrategyRequest(
            problem_statement="Build an e-commerce platform for handmade crafts."
        )
        with pytest.raises(HTTPException) as exc_info:
            await service.analyze(request)
        assert exc_info.value.status_code == 503

    @pytest.mark.asyncio
    async def test_analyze_mocked_success(self, mock_llm_response):
        from agents.business_strategy.services.strategy_service import BusinessStrategyService
        from agents.business_strategy.schemas.strategy_schema import BusinessStrategyRequest

        service = BusinessStrategyService(api_key="test-key", model_name="llama-3.3-70b-versatile")

        with patch.object(service, "_call_llm", new=AsyncMock(return_value=mock_llm_response)):
            request = BusinessStrategyRequest(
                problem_statement=(
                    "Build an AI-powered platform for restaurant inventory management."
                )
            )
            response = await service.analyze(request)

        assert response is not None
        assert response.business_model == "B2B SaaS"
        assert response.confidence == 0.87
        assert len(response.target_customers) == 2
        assert len(response.revenue_streams) == 3


# ---------------------------------------------------------------------------
# Agent Tests (Mocked)
# ---------------------------------------------------------------------------

class TestBusinessStrategyAgent:
    """Unit tests for the BusinessStrategyAgent orchestration layer."""

    @pytest.mark.asyncio
    async def test_run_returns_response(self, mock_llm_response):
        from agents.business_strategy.agent import BusinessStrategyAgent

        agent = BusinessStrategyAgent()

        with patch.object(
            agent.service, "_call_llm", new=AsyncMock(return_value=mock_llm_response)
        ):
            response = await agent.run(
                "Build an AI-powered restaurant inventory management platform."
            )

        assert response is not None
        assert response.value_proposition
        assert response.go_to_market
        assert response.swot is not None
        assert response.business_canvas is not None
        assert len(response.competitors) >= 1
        assert len(response.marketing_channels) >= 1

    @pytest.mark.asyncio
    async def test_run_with_context(self, mock_llm_response):
        from agents.business_strategy.agent import BusinessStrategyAgent

        agent = BusinessStrategyAgent()
        context = {"region": "Europe", "stage": "Seed", "budget": "$1M"}

        with patch.object(
            agent.service, "_call_llm", new=AsyncMock(return_value=mock_llm_response)
        ):
            response = await agent.run(
                "Build an AI restaurant inventory management platform.",
                context=context,
            )

        assert response.confidence > 0.0

    @pytest.mark.asyncio
    async def test_execute_full_pipeline_returns_metadata(self, mock_llm_response):
        from agents.business_strategy.agent import BusinessStrategyAgent
        from agents.business_strategy.schemas.strategy_schema import BusinessStrategyRequest
        from agents.business_strategy.models.domain import BusinessStrategyResult

        agent = BusinessStrategyAgent()
        request = BusinessStrategyRequest(
            problem_statement="Build an AI restaurant inventory management platform."
        )

        with patch.object(
            agent.service, "_call_llm", new=AsyncMock(return_value=mock_llm_response)
        ):
            result = await agent.execute_full_pipeline(request)

        assert isinstance(result, BusinessStrategyResult)
        assert result.request_id is not None
        assert result.metadata.agent_name == "BusinessStrategyAgent"
        assert result.metadata.version == "1.0.0"
        assert result.metadata.model_used == agent.service.model_name
        assert result.metadata.execution_time_ms > 0
        assert "target_customers" in result.strategy_output
        assert "swot" in result.strategy_output
        assert "business_canvas" in result.strategy_output

    @pytest.mark.asyncio
    async def test_agent_propagates_http_exception(self):
        from agents.business_strategy.agent import BusinessStrategyAgent
        from fastapi import HTTPException

        agent = BusinessStrategyAgent()

        with patch.object(
            agent.service,
            "analyze",
            new=AsyncMock(
                side_effect=HTTPException(status_code=503, detail="LLM unavailable")
            ),
        ):
            with pytest.raises(HTTPException) as exc_info:
                await agent.run("Build a SaaS tool for HR departments.")
            assert exc_info.value.status_code == 503

    @pytest.mark.asyncio
    async def test_agent_has_correct_name_and_version(self):
        from agents.business_strategy.agent import BusinessStrategyAgent
        agent = BusinessStrategyAgent()
        assert agent.agent_name == "BusinessStrategyAgent"
        assert agent.version == "1.0.0"

    def test_agent_model_name_from_config(self):
        from agents.business_strategy.agent import BusinessStrategyAgent
        from agents.business_strategy.config import settings
        agent = BusinessStrategyAgent()
        assert agent.service.model_name == settings.model_name
