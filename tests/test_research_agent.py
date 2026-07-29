import pytest
import pytest_asyncio
from agents.research_intelligence.schemas import ResearchAgentRequest, ResearchAgentResponse, RawPaper
from agents.research_intelligence.tools import deduplicate_papers, search_arxiv, search_semantic_scholar, search_crossref
from agents.research_intelligence.agent import research_agent


def test_deduplication():
    papers = [
        RawPaper(title="AI for Food Waste", authors=["Alice"], year="2023", abstract="Ab 1", doi="10.1234/test", source="arXiv"),
        RawPaper(title="AI for Food Waste", authors=["Alice"], year="2023", abstract="Ab 1", doi="10.1234/test", source="Semantic Scholar"),
        RawPaper(title="Unique Paper Title", authors=["Bob"], year="2024", abstract="Ab 2", doi="10.5678/test2", source="CrossRef"),
    ]
    deduped = deduplicate_papers(papers)
    assert len(deduped) == 2
    assert deduped[0].title == "AI for Food Waste"
    assert deduped[1].title == "Unique Paper Title"


@pytest.mark.asyncio
async def test_tool_searches():
    query = "food waste artificial intelligence"
    arxiv_res = await search_arxiv(query, max_results=2)
    assert isinstance(arxiv_res, list)

    ss_res = await search_semantic_scholar(query, max_results=2)
    assert isinstance(ss_res, list)

    crossref_res = await search_crossref(query, max_results=2)
    assert isinstance(crossref_res, list)


@pytest.mark.asyncio
async def test_agent_end_to_end():
    req = ResearchAgentRequest(problem_statement="Reduce food waste in restaurants using AI.")
    res = await research_agent.analyze(req)
    
    assert isinstance(res, ResearchAgentResponse)
    assert hasattr(res, "research_summary")
    assert hasattr(res, "papers")
    assert hasattr(res, "research_gaps")
    assert hasattr(res, "recommended_datasets")
    assert hasattr(res, "confidence_score")
    assert 0.0 <= res.confidence_score <= 1.0
