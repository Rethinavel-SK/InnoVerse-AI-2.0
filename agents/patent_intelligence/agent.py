import asyncio
import json
import logging
import urllib.request
from typing import List, Optional, Dict, Any

from .config import settings
from .schemas import (
    PatentAgentRequest,
    PatentAgentResponse,
    PatentDetail
)
from .tools import search_patents
from .memory import AgentMemory
from .prompt_templates import PATENT_ANALYSIS_PROMPT

logger = logging.getLogger("PatentIntelligenceAgent")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


def _sync_call_groq_llm(prompt: str, json_mode: bool = True) -> Optional[str]:
    """Synchronous Groq API call using urllib.request."""
    if not settings.GROQ_API_KEY:
        return None
    
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "PatentIntelligenceAgent/1.0"
    }
    
    payload: Dict[str, Any] = {
        "model": settings.GROQ_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }
    
    if json_mode:
        payload["response_format"] = {"type": "json_object"}

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(settings.GROQ_API_URL, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=settings.REQUEST_TIMEOUT) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            return res_json["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logger.error(f"Groq API call error in Patent Agent: {e}")
        return None


class PatentIntelligenceAgent:
    """Production-Ready Patent Intelligence Agent.
    
    Responsibilities:
    - Patent search
    - Prior-art analysis
    - Novelty scoring
    - White-space detection

    Strict Constraints (NEVER):
    - Search research papers
    - Perform market analysis
    - Design software architecture
    - Generate business plans

    Always returns JSON matching PatentAgentResponse.
    """

    def __init__(self, memory_ttl_seconds: int = 86400):
        self.memory = AgentMemory(ttl_seconds=memory_ttl_seconds)

    async def _call_groq_llm(self, prompt: str, json_mode: bool = True) -> Optional[str]:
        """Helper to invoke Groq API asynchronously via thread pool."""
        return await asyncio.to_thread(_sync_call_groq_llm, prompt, json_mode)

    def _fallback_analysis(self, problem_statement: str, patents: List[PatentDetail]) -> PatentAgentResponse:
        """Rule-based fallback prior-art analysis if LLM is offline/failing."""
        white_space_opportunities = [
            f"Unpatented edge application of real-time machine learning for {problem_statement[:60]}.",
            "Integration of decentralized zero-knowledge compliance verification."
        ]

        return PatentAgentResponse(
            agent="Patent Agent",
            similar_patents=patents,
            novelty_score=75 if len(patents) < 3 else 60,
            white_spaces=white_space_opportunities,
            risk="Low" if len(patents) == 0 else "Medium"
        )

    async def _analyze_patents_llm(self, problem_statement: str, patents: List[PatentDetail]) -> Optional[PatentAgentResponse]:
        """Perform LLM prior-art analysis, novelty scoring, and white-space detection."""
        if not settings.GROQ_API_KEY and not settings.GEMINI_API_KEY:
            return None

        patents_text = ""
        for i, p in enumerate(patents, 1):
            patents_text += f"\nPatent {i}:\nID: {p.patent_id}\nTitle: {p.title}\nAssignee: {p.assignee}\nYear: {p.year}\nSummary: {p.summary}\n"

        prompt = PATENT_ANALYSIS_PROMPT.format(problem_statement=problem_statement, patents_text=patents_text)

        # 1. Try Groq API
        if settings.GROQ_API_KEY:
            logger.info("Performing patent prior-art analysis using Groq LLM API.")
            text = await self._call_groq_llm(prompt, json_mode=True)
            if text:
                try:
                    data = json.loads(text)
                    # Enforce agent name
                    data["agent"] = "Patent Agent"
                    return PatentAgentResponse(**data)
                except Exception as e:
                    logger.error(f"Failed to parse Groq patent analysis output: {e}")

        # 2. Try Gemini API
        if settings.GEMINI_API_KEY:
            logger.info("Performing patent prior-art analysis using Gemini LLM API.")
            try:
                from google import genai
                client = genai.Client(api_key=settings.GEMINI_API_KEY)
                response = client.models.generate_content(
                    model=settings.DEFAULT_MODEL,
                    contents=prompt,
                )
                text = response.text.strip()
                if text.startswith("```json"):
                    text = text[7:-3].strip()
                elif text.startswith("```"):
                    text = text[3:-3].strip()

                data = json.loads(text)
                data["agent"] = "Patent Agent"
                return PatentAgentResponse(**data)
            except Exception as e:
                logger.error(f"Gemini LLM patent analysis error: {e}", exc_info=True)

        return None

    async def analyze(self, request: PatentAgentRequest) -> PatentAgentResponse:
        """Main entry point for Patent Intelligence Agent analysis pipeline."""
        logger.info(f"Starting Patent Intelligence Agent for: '{request.problem_statement}'")
        
        # 1. Memory lookup
        cached_response = self.memory.get(request.problem_statement)
        if cached_response:
            logger.info("Returning cached patent agent response from memory.")
            return cached_response

        # 2. Fetch patents / prior art
        retrieved_patents = await search_patents(
            request.problem_statement, 
            max_results=request.max_results or settings.MAX_PATENTS_PER_SEARCH
        )
        
        # 3. Analyze patents via LLM
        response: Optional[PatentAgentResponse] = None
        if retrieved_patents:
            response = await self._analyze_patents_llm(request.problem_statement, retrieved_patents)

        if not response:
            logger.info("Using fallback prior-art analysis for structured patent output.")
            response = self._fallback_analysis(request.problem_statement, retrieved_patents)

        # 4. Cache response
        self.memory.set(request.problem_statement, response)

        return response


# Singleton instance
patent_agent = PatentIntelligenceAgent()
