"""Research Intelligence Agent Module.

Provides automated academic paper discovery, deduplication, summarization,
and structured research report generation.
"""

from .agent import ResearchIntelligenceAgent, research_agent
from .schemas import ResearchAgentRequest, ResearchAgentResponse, PaperDetail
from .router import router

__all__ = [
    "ResearchIntelligenceAgent",
    "research_agent",
    "ResearchAgentRequest",
    "ResearchAgentResponse",
    "PaperDetail",
    "router",
]
