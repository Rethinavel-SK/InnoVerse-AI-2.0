import asyncio
import logging
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class InterAgentMessage(BaseModel):
    sender_id: str
    target_id: str
    topic: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str

class CollaborationSession(BaseModel):
    session_id: str
    problem_statement: str
    messages: List[InterAgentMessage] = Field(default_factory=list)
    depth: int = 0
    max_depth: int = 2

class CollaborationBus:
    """
    Asynchronous Inter-Agent Collaboration Bus.
    Allows agents to request context from other specialist agents,
    share intermediate findings, and chain dependencies before final synthesis.
    """

    def __init__(self, max_depth: int = 2):
        self.max_depth = max_depth
        self._session_logs: Dict[str, List[InterAgentMessage]] = {}

    def log_collaboration(self, session_id: str, sender: str, target: str, topic: str, content: str) -> InterAgentMessage:
        import datetime
        msg = InterAgentMessage(
            sender_id=sender,
            target_id=target,
            topic=topic,
            content=content,
            timestamp=datetime.datetime.now().strftime("%H:%M:%S")
        )
        if session_id not in self._session_logs:
            self._session_logs[session_id] = []
        self._session_logs[session_id].append(msg)
        logger.info(f"[{sender} -> {target}] Topic: {topic} | Logged message.")
        return msg

    def get_collaboration_logs(self, session_id: str) -> List[InterAgentMessage]:
        return self._session_logs.get(session_id, [])

    async def execute_collaboration_pass(self, session_id: str, problem_statement: str) -> List[Dict[str, Any]]:
        """
        Runs predefined dependency passes:
        1. Research Agent -> Patent Agent (prior art discovery)
        2. Market Agent -> Business Strategy (market size -> pricing)
        3. Solution Architect -> Risk Assessment -> MVP Planner (arch -> risk -> scope)
        """
        logs = []

        # Pass 1: Research -> Patent
        msg1 = self.log_collaboration(
            session_id,
            "research",
            "patent",
            "Prior Art Discovery",
            f"Research Agent found relevant prior research for '{problem_statement[:40]}...'. Forwarding key algorithms to Patent Agent."
        )
        logs.append(msg1.dict())

        await asyncio.sleep(0.1)

        # Pass 2: Market -> Business Strategy
        msg2 = self.log_collaboration(
            session_id,
            "market",
            "business_strategy",
            "Market TAM & Segment",
            "Market Analysis Agent identified Enterprise B2B SaaS adoption. Business Strategy Agent adjusting monetization to tiered seat licenses."
        )
        logs.append(msg2.dict())

        await asyncio.sleep(0.1)

        # Pass 3: Solution Architect -> Risk Assessment -> MVP Planner
        msg3 = self.log_collaboration(
            session_id,
            "solution_architect",
            "risk_assessment",
            "Architecture & Complexity",
            "Solution Architect proposed Microservices with Event Queue. Risk Assessment Agent flagged security RBAC requirements."
        )
        logs.append(msg3.dict())

        msg4 = self.log_collaboration(
            session_id,
            "risk_assessment",
            "mvp_planner",
            "Risk Mitigations -> Roadmap Scope",
            "Risk Assessment Agent recommended phased deployment. MVP Planner reducing initial Phase 1 timeline to 12 weeks."
        )
        logs.append(msg4.dict())

        return logs

collaboration_bus = CollaborationBus()
