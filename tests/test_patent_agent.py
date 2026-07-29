import asyncio
from agents.patent_intelligence import (
    PatentIntelligenceAgent,
    patent_agent,
    PatentAgentRequest,
    PatentAgentResponse
)

async def run_patent_agent_test():
    print("Testing Patent Intelligence Agent...")
    req = PatentAgentRequest(
        problem_statement="AI edge-camera system for real-time food waste classification in commercial kitchens.",
        max_results=2
    )
    res = await patent_agent.analyze(req)
    
    assert isinstance(res, PatentAgentResponse), "Response must be PatentAgentResponse"
    assert res.agent == "Patent Agent", "Agent name must be 'Patent Agent'"
    assert isinstance(res.similar_patents, list), "similar_patents must be a list"
    assert 0 <= res.novelty_score <= 100, "novelty_score must be between 0 and 100"
    assert isinstance(res.white_spaces, list), "white_spaces must be a list"
    assert isinstance(res.risk, str), "risk must be a string"
    
    print("\n--- Live Output JSON ---")
    print(res.model_dump_json(indent=2))
    print("\n✅ Patent Agent Test Passed Successfully!")

if __name__ == "__main__":
    asyncio.run(run_patent_agent_test())
