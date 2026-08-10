"""
Innovation Director Service v2.0
=================================
Orchestrates execution across all 11 specialist AI agents (9 original + Failure Hunter + Execution Planner),
validates responses, resolves conflicts with debate reasoning, calculates 10-dimension innovation scores,
classifies evidence, and synthesizes outputs into a master executive innovation report.
"""

import asyncio
import json
import logging
import os
import re
from typing import Dict, Any, Optional, List, Union

from fastapi import HTTPException, status

from agents.innovation_director.config import settings
from agents.innovation_director.schemas.director_schema import (
    InnovationDirectorRequest,
    InnovationDirectorResponse,
    ConflictResolutionItem,
    FinalRecommendation,
    DebateEntry,
    EvidenceItem,
)
from agents.innovation_director.prompts.system_prompt import (
    INNOVATION_DIRECTOR_SYSTEM_PROMPT,
    build_synthesis_prompt,
)

# Import all 9 original specialist agents
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

# Import 2.0 agents
from agents.failure_hunter.agent import FailureHunterAgent
from agents.execution_planner.agent import ExecutionPlannerAgent

# Import 2.0 services
from agents.innovation_director.services.score_engine import score_engine

logger = logging.getLogger(__name__)


class InnovationDirectorService:
    """
    Master Orchestration, Reconciliation, and Synthesis Service.
    """

    ALL_AGENTS = [
        "solution_architect",
        "business_strategy",
        "research",
        "patent_analysis",
        "market_analysis",
        "trend_analysis",
        "risk_assessment",
        "sustainability",
        "mvp_roadmap",
        "failure_hunter",
        "execution_planner",
    ]

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
    ):
        self.api_key = api_key or settings.groq_api_key or os.getenv("GROQ_API_KEY")
        self.model_name = model_name or settings.model_name
        logger.debug("InnovationDirectorService initialized (model=%s)", self.model_name)

    def validate_problem_statement(self, problem_statement: str) -> None:
        """
        Validates problem statement.
        """
        if not problem_statement or not problem_statement.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Problem statement cannot be empty."
            )
        if len(problem_statement.strip()) < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Problem statement must be at least 10 characters long."
            )

    async def analyze_and_orchestrate(
        self, request: InnovationDirectorRequest
    ) -> InnovationDirectorResponse:
        """
        Runs required specialist agents with concurrency control (max 3 at a time to prevent Groq 429 rate limits),
        validates responses, resolves conflicts, calculates weighted score, and returns master synthesis report.
        """
        self.validate_problem_statement(request.problem_statement)

        logger.info(
            "Starting Master Innovation Director Orchestration for: '%s'",
            request.problem_statement[:100],
        )

        problem = request.problem_statement.strip()
        ctx = request.context or {}

        # Determine which agents should be invoked
        agents_to_run = request.selected_agents if request.selected_agents else self.ALL_AGENTS
        logger.info("Agents selected for execution: %s", agents_to_run)

        # Use a semaphore to cap concurrent LLM API calls at 3 to avoid Groq 429 rate limits
        semaphore = asyncio.Semaphore(3)

        async def safe_run(agent_id: str, coro_fn):
            if agent_id not in agents_to_run:
                return None
            async with semaphore:
                try:
                    res = await coro_fn()
                    if hasattr(res, "model_dump"):
                        return res.model_dump()
                    return res
                except Exception as exc:
                    logger.warning("Specialist Agent '%s' encountered an error: %s", agent_id, exc)
                    return None

        # Individual agent coroutines
        async def _architect():
            agent = SolutionArchitectAgent()
            return await agent.run(problem, ctx)

        async def _strategy():
            agent = BusinessStrategyAgent()
            return await agent.run(problem, ctx)

        async def _research():
            req = ResearchAgentRequest(problem_statement=problem)
            return await research_agent.analyze(req)

        async def _patent():
            req = PatentAgentRequest(problem_statement=problem)
            return await patent_agent.analyze(req)

        async def _market():
            return await market_intelligence_agent.run(problem, ctx)

        async def _trend():
            return await trend_intelligence_agent.run(problem, ctx)

        async def _risk():
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(None, risk_execute, problem)

        async def _sustainability():
            return await sustainability_agent.run(problem, ctx)

        async def _roadmap():
            agent = MVPRoadmapAgent()
            return await agent.run(problem, ctx)

        # 2.0: Failure Hunter
        async def _failure_hunter():
            agent = FailureHunterAgent()
            return await agent.run(problem, ctx)

        # 2.0: Execution Planner
        async def _execution_planner():
            agent = ExecutionPlannerAgent()
            return await agent.run(problem, ctx)

        # Run all agents concurrently with semaphore control
        results = await asyncio.gather(
            safe_run("solution_architect", _architect),
            safe_run("business_strategy", _strategy),
            safe_run("research", _research),
            safe_run("patent_analysis", _patent),
            safe_run("market_analysis", _market),
            safe_run("trend_analysis", _trend),
            safe_run("risk_assessment", _risk),
            safe_run("sustainability", _sustainability),
            safe_run("mvp_roadmap", _roadmap),
            safe_run("failure_hunter", _failure_hunter),
            safe_run("execution_planner", _execution_planner),
            return_exceptions=True
        )

        agent_keys = [
            "solution_architect",
            "business_strategy",
            "research",
            "patent_analysis",
            "market_analysis",
            "trend_analysis",
            "risk_assessment",
            "sustainability",
            "mvp_roadmap",
            "failure_hunter",
            "execution_planner",
        ]

        agents_data: Dict[str, Any] = {}
        agent_status: Dict[str, str] = {}
        completed_count = 0

        for key, res in zip(agent_keys, results):
            if key not in agents_to_run:
                agent_status[key] = "Unavailable"
                agents_data[key] = {}
            elif isinstance(res, Exception) or res is None:
                logger.warning("Agent '%s' failed or returned None: %s", key, res)
                agent_status[key] = "Unavailable"
                agents_data[key] = {}
            else:
                if isinstance(res, dict) and len(res) > 0:
                    agent_status[key] = "Completed"
                    agents_data[key] = res
                    completed_count += 1
                else:
                    agent_status[key] = "Unavailable"
                    agents_data[key] = {}

        # Calculate Confidence Score based on agent availability & completion
        total_agents = len(self.ALL_AGENTS)
        confidence = round(max(0.30, min(0.98, (completed_count / total_agents) * 0.95)), 2)

        # Intelligent Conflict Detection & Resolution
        conflicts = self._detect_and_resolve_conflicts(agents_data)

        # 2.0: Generate debate trace from conflicts
        debate_trace = self._generate_debate_trace(agents_data, conflicts)

        # 2.0: Classify evidence from agent results
        evidence_items = self._classify_evidence(agents_data)

        # 2.0: 10-Dimension Innovation Score via Score Engine
        score_result = score_engine.calculate_score(agents_data, "pipeline", "v1")
        weighted_score = score_result.overall_score
        score_breakdown_dict = {
            "market_potential": score_result.market_potential,
            "technical_feasibility": score_result.technical_feasibility,
            "business_viability": score_result.business_viability,
            "innovation_differentiation": score_result.innovation_differentiation,
            "patent_ip_position": score_result.patent_ip_position,
            "risk_score": score_result.risk_score,
            "sustainability": score_result.sustainability,
            "mvp_feasibility": score_result.mvp_feasibility,
            "customer_value": score_result.customer_value,
            "scalability": score_result.scalability,
            "overall_score": score_result.overall_score,
            "explanation": score_result.explanation,
        }

        # Master Executive Synthesis (LLM or Rule-Based Fallback)
        synthesis = await self._synthesize_master_report(
            problem, agents_data, agent_status, ctx
        )

        # Consolidate response dictionary
        exec_summary = synthesis.get(
            "executive_summary",
            f"Comprehensive master innovation report complete for problem statement: '{problem}'."
        )
        problem_und = synthesis.get(
            "problem_understanding",
            f"Evaluation of project concept: '{problem}'. Consolidated findings from {completed_count} of {total_agents} active specialist agents."
        )

        llm_conflicts = synthesis.get("conflict_resolution", [])
        combined_conflicts = conflicts if conflicts else llm_conflicts

        llm_final_rec = synthesis.get("final_recommendation", {})
        if not isinstance(llm_final_rec, dict):
            llm_final_rec = {}

        def _ensure_list(val: Any, default: List[str]) -> List[str]:
            if isinstance(val, list):
                return [str(x) for x in val if x is not None]
            if isinstance(val, str) and val.strip():
                return [val.strip()]
            return default

        final_rec = FinalRecommendation(
            build_recommendation=str(llm_final_rec.get("build_recommendation", "Yes (Conditional GO)")),
            expected_success_probability=str(llm_final_rec.get("expected_success_probability", "85%")),
            implementation_strategy=str(llm_final_rec.get("implementation_strategy", "Phased modular rollout starting with MVP validation.")),
            suggested_deployment_phases=_ensure_list(
                llm_final_rec.get("suggested_deployment_phases"),
                ["Phase 1: Core MVP Development", "Phase 2: Pilot Deployment & Feasibility", "Phase 3: Production Scale"]
            ),
            commercial_viability=str(llm_final_rec.get("commercial_viability", "High viability supported by market demand and clear monetization.")),
            investment_priority=str(llm_final_rec.get("investment_priority", "High Priority")),
            future_scope=_ensure_list(
                llm_final_rec.get("future_scope"),
                ["Multi-tenant scalability", "AI model auto-tuning", "Global deployment"]
            )
        )

        return InnovationDirectorResponse(
            executive_summary=exec_summary,
            problem_understanding=problem_und,
            agent_status=agent_status,
            # Original 9 agents
            technical_summary=agents_data.get("solution_architect", {}),
            business_summary=agents_data.get("business_strategy", {}),
            research_summary=agents_data.get("research", {}),
            patent_summary=agents_data.get("patent_analysis", {}),
            market_summary=agents_data.get("market_analysis", {}),
            trend_summary=agents_data.get("trend_analysis", {}),
            risk_summary=agents_data.get("risk_assessment", {}),
            sustainability_summary=agents_data.get("sustainability", {}),
            roadmap_summary=agents_data.get("mvp_roadmap", {}),
            # 2.0: New agents
            failure_analysis=agents_data.get("failure_hunter", {}),
            execution_plan=agents_data.get("execution_planner", {}),
            # 2.0: Debate, Evidence & Score
            debate_trace=debate_trace,
            evidence_items=evidence_items,
            score_breakdown=score_breakdown_dict,
            # Original fields
            conflict_resolution=combined_conflicts,
            overall_innovation_score=weighted_score,
            confidence=confidence,
            final_recommendation=final_rec,
        )

    def _detect_and_resolve_conflicts(self, agents_data: Dict[str, Any]) -> List[ConflictResolutionItem]:
        """
        Detects conflicts between agent outputs and applies critical reconciliation logic.
        """
        conflicts: List[ConflictResolutionItem] = []

        arch_data = str(agents_data.get("solution_architect", "")).lower()
        roadmap_data = str(agents_data.get("mvp_roadmap", "")).lower()
        strat_data = str(agents_data.get("business_strategy", "")).lower()
        market_data = str(agents_data.get("market_analysis", "")).lower()

        # Conflict 1: Microservices vs Simple MVP
        if "microservice" in arch_data and ("mvp" in roadmap_data or "fast" in roadmap_data or "simple" in roadmap_data):
            conflicts.append(
                ConflictResolutionItem(
                    agents_involved=["solution_architect", "mvp_roadmap"],
                    conflict_description="Solution Architect recommended Microservices architecture while MVP Planner recommended a Simple MVP timeframe.",
                    comparison="Microservices introduce significant initial infrastructure overhead, whereas a Simple MVP prioritizes rapid market entry and validation.",
                    resolution="Begin with a Modular Monolith for the MVP and migrate to Microservices as the system scales.",
                    reasoning="Reduces initial latency and deployment complexity for early validation while preserving future microservice migration paths."
                )
            )

        # Conflict 2: B2B SaaS vs Government Market
        if "saas" in strat_data and ("government" in market_data or "public sector" in market_data):
            conflicts.append(
                ConflictResolutionItem(
                    agents_involved=["business_strategy", "market_analysis"],
                    conflict_description="Business Strategy suggested B2B SaaS while Market Analysis indicated a Government-focused market.",
                    comparison="Commercial B2B SaaS focuses on self-serve onboarding, whereas Government markets require strict compliance (FedRAMP) and procurement cycles.",
                    resolution="Adopt a phased dual-track approach starting with commercial B2B pilots while preparing government compliance certifications.",
                    reasoning="Secures early cash flow and user feedback from enterprise clients while systematically opening high-barrier government channels."
                )
            )

        return conflicts

    def _calculate_weighted_innovation_score(self, agents_data: Dict[str, Any]) -> float:
        """
        Calculates overall score out of 100 using weighted multi-agent analysis:
        - Technical Feasibility: 25%
        - Business Potential: 20%
        - Innovation: 20%
        - Market Readiness: 15%
        - Scalability: 10%
        - Risk (Safety/Inverse): 5%
        - Sustainability: 5%
        """
        # Technical Feasibility (25%)
        tech_score = 85.0
        arch = agents_data.get("solution_architect", {})
        if isinstance(arch, dict) and "feasibility_score" in arch:
            try:
                tech_score = float(arch["feasibility_score"])
            except (ValueError, TypeError):
                tech_score = 85.0

        # Business Potential (20%)
        bus_score = 85.0
        strat = agents_data.get("business_strategy", {})
        if isinstance(strat, dict) and "confidence" in strat:
            try:
                val = float(strat["confidence"])
                bus_score = val * 100 if val <= 1.0 else val
            except (ValueError, TypeError):
                bus_score = 85.0

        # Innovation (20%)
        innov_score = 80.0
        pat = agents_data.get("patent_analysis", {})
        if isinstance(pat, dict):
            try:
                innov_score = float(pat.get("novelty_score", pat.get("score", 80.0)))
            except (ValueError, TypeError):
                innov_score = 80.0

        # Market Readiness (15%)
        mkt_score = 85.0
        trd = agents_data.get("trend_analysis", {})
        if isinstance(trd, dict) and "trend_score" in trd:
            try:
                mkt_score = float(trd["trend_score"])
            except (ValueError, TypeError):
                mkt_score = 85.0

        # Scalability (10%)
        scale_score = 85.0

        # Risk Safety Score (5%) - lower risk score means higher safety
        risk_safety = 80.0
        rsk = agents_data.get("risk_assessment", {})
        if isinstance(rsk, dict):
            raw_risk = rsk.get("overall_risk_score", rsk.get("risk_score", 30))
            if isinstance(raw_risk, (int, float)):
                risk_safety = max(10.0, 100.0 - float(raw_risk))

        # Sustainability Score (5%)
        sust_score = 85.0
        sus = agents_data.get("sustainability", {})
        if isinstance(sus, dict):
            try:
                sust_score = float(sus.get("sustainability_score", sus.get("esg_compliance_score", 85.0)))
            except (ValueError, TypeError):
                sust_score = 85.0

        weighted_total = (
            (tech_score * 0.25) +
            (bus_score * 0.20) +
            (innov_score * 0.20) +
            (mkt_score * 0.15) +
            (scale_score * 0.10) +
            (risk_safety * 0.05) +
            (sust_score * 0.05)
        )

        return round(max(0.0, min(100.0, weighted_total)), 1)

    async def _synthesize_master_report(
        self,
        problem: str,
        agents_data: Dict[str, Any],
        agent_status: Dict[str, str],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Invokes LLM synthesizer using system prompt or returns structured rule-based synthesis fallback.
        """
        if not self.api_key:
            logger.warning("No GROQ_API_KEY found, using rule-based synthesis fallback.")
            return self._fallback_synthesis(problem, agents_data)

        try:
            from groq import AsyncGroq

            client = AsyncGroq(api_key=self.api_key, max_retries=1)
            user_prompt = build_synthesis_prompt(problem, agents_data, agent_status, context)

            logger.info("Invoking Groq LLM for Innovation Director Master Synthesis...")

            chat_response = await client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": INNOVATION_DIRECTOR_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=settings.temperature,
                max_tokens=settings.max_tokens,
                response_format={"type": "json_object"},
                timeout=12.0,
            )

            raw_text = chat_response.choices[0].message.content
            return self._parse_json(raw_text)

        except Exception as exc:
            logger.error("Synthesis LLM call failed (%s), using structured fallback.", exc)
            return self._fallback_synthesis(problem, agents_data)

    def _parse_json(self, raw_text: str) -> Dict[str, Any]:
        cleaned = raw_text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        return json.loads(cleaned.strip())

    def _fallback_synthesis(self, problem: str, agents_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "executive_summary": (
                f"Master Executive Innovation Report for: '{problem}'. Synthesized findings across "
                "technical architecture, business strategy, research literature, patent novelty, market analysis, "
                "trend intelligence, risk assessment, sustainability, and MVP roadmap."
            ),
            "problem_understanding": (
                f"Comprehensive problem analysis for '{problem}'. The concept demonstrates clear technical viability "
                "and market demand, with structured implementation phases to mitigate risk."
            ),
            "final_recommendation": {
                "build_recommendation": "Yes (Conditional GO)",
                "expected_success_probability": "85%",
                "implementation_strategy": "Begin with Modular Monolith MVP and transition to scalable Microservices.",
                "suggested_deployment_phases": [
                    "Phase 1: Core MVP & Authentication",
                    "Phase 2: Enterprise Pilot & Compliance",
                    "Phase 3: Multi-region Scale"
                ],
                "commercial_viability": "High commercial potential supported by strong market tailwinds.",
                "investment_priority": "High Priority",
                "future_scope": [
                    "Automated model fine-tuning",
                    "Enterprise SSO & Security audit trail"
                ]
            }
        }

    # -------------------------------------------------------------------
    # 2.0: Debate Trace Generation
    # -------------------------------------------------------------------

    def _generate_debate_trace(self, agents_data: Dict[str, Any],
                                conflicts: List[ConflictResolutionItem]) -> List[Dict[str, Any]]:
        """
        Generate structured debate entries from detected conflicts and agent disagreements.
        The Innovation Director reasons about each conflict instead of simply averaging.
        """
        debate_entries = []

        # From detected conflicts
        for conflict in conflicts:
            entry = DebateEntry(
                topic=conflict.conflict_description,
                agents_involved=conflict.agents_involved,
                positions={agent: "See conflict description" for agent in conflict.agents_involved},
                evidence=[conflict.comparison],
                resolution=f"{conflict.resolution} — Reasoning: {conflict.reasoning}",
                confidence=0.8,
            )
            debate_entries.append(entry.model_dump())

        # Check for risk vs. optimism conflicts
        failure_data = agents_data.get("failure_hunter", {})
        biz_data = agents_data.get("business_strategy", {})

        failure_prob = failure_data.get("overall_failure_probability", "")
        biz_confidence = biz_data.get("confidence", 0)

        if isinstance(failure_prob, str) and failure_prob.upper() == "HIGH" and isinstance(biz_confidence, (int, float)) and biz_confidence > 0.7:
            debate_entries.append(DebateEntry(
                topic="Failure Hunter identifies HIGH failure risk while Business Strategy shows HIGH confidence",
                agents_involved=["failure_hunter", "business_strategy"],
                positions={
                    "failure_hunter": f"Overall failure probability: {failure_prob}. Key risks need immediate mitigation.",
                    "business_strategy": f"High business confidence ({biz_confidence}). Market opportunity is strong."
                },
                evidence=["Agent outputs show divergent risk assessment — Failure Hunter is adversarial by design."],
                resolution="Both perspectives are valid. Proceed with execution but implement Failure Hunter's top mitigations as prerequisites. The business opportunity justifies the risk IF mitigations are in place.",
                confidence=0.75,
            ).model_dump())

        return debate_entries

    # -------------------------------------------------------------------
    # 2.0: Evidence Classification
    # -------------------------------------------------------------------

    def _classify_evidence(self, agents_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Classify evidence from agent results as FACT, INFERENCE, PREDICTION, or ASSUMPTION.
        """
        evidence_items = []

        # Research findings are closer to FACTS (backed by papers/data)
        research = agents_data.get("research", {})
        if isinstance(research, dict):
            papers = research.get("papers_found", research.get("total_papers", 0))
            if papers:
                evidence_items.append(EvidenceItem(
                    statement=f"Research literature search found {papers} relevant papers.",
                    classification="FACT",
                    source="academic_databases",
                    agent="research_intelligence",
                    confidence=0.9,
                ).model_dump())

        # Patent analysis can be FACT-based
        patent = agents_data.get("patent_analysis", {})
        if isinstance(patent, dict):
            patent_count = patent.get("patents_found", patent.get("total_patents", 0))
            novelty = patent.get("novelty_score", patent.get("score", 0))
            if patent_count or novelty:
                evidence_items.append(EvidenceItem(
                    statement=f"Patent search found {patent_count} related patents. Novelty score: {novelty}.",
                    classification="FACT",
                    source="patent_databases",
                    agent="patent_intelligence",
                    confidence=0.85,
                ).model_dump())

        # Business projections are PREDICTIONS
        business = agents_data.get("business_strategy", {})
        if isinstance(business, dict):
            evidence_items.append(EvidenceItem(
                statement=f"Business strategy analysis completed with confidence {business.get('confidence', 'N/A')}.",
                classification="PREDICTION",
                source="llm_analysis",
                agent="business_strategy",
                confidence=0.7,
            ).model_dump())

        # Market analysis projections
        market = agents_data.get("market_analysis", {})
        if isinstance(market, dict) and market:
            evidence_items.append(EvidenceItem(
                statement="Market size and competitive landscape analysis based on available data.",
                classification="INFERENCE",
                source="market_data",
                agent="market_intelligence",
                confidence=0.65,
            ).model_dump())

        # Failure risks are INFERENCES
        failure = agents_data.get("failure_hunter", {})
        if isinstance(failure, dict):
            for risk in failure.get("top_failure_risks", [])[:3]:
                if isinstance(risk, dict):
                    evidence_items.append(EvidenceItem(
                        statement=f"Failure risk: {risk.get('risk', 'Unknown')}",
                        classification="INFERENCE",
                        source="adversarial_analysis",
                        agent="failure_hunter",
                        confidence=0.7,
                    ).model_dump())

        # Technical architecture is INFERENCE
        tech = agents_data.get("solution_architect", {})
        if isinstance(tech, dict) and tech:
            evidence_items.append(EvidenceItem(
                statement="Technical architecture recommendation based on requirements analysis.",
                classification="INFERENCE",
                source="llm_analysis",
                agent="solution_architect",
                confidence=0.75,
            ).model_dump())

        return evidence_items
