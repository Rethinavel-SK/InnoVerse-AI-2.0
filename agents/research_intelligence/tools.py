import logging
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from typing import List
from .config import settings
from .schemas import RawPaper

logger = logging.getLogger("ResearchIntelligenceAgent.Tools")


def _http_get(url: str, params: dict = None, headers: dict = None) -> tuple[int, str]:
    """Helper function performing synchronous HTTP GET request with urllib."""
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=settings.REQUEST_TIMEOUT) as response:
            return response.status, response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        logger.error(f"HTTP GET Error for {url}: {e}")
        return 500, ""


async def search_arxiv(query: str, max_results: int = 5) -> List[RawPaper]:
    """Fetch academic papers asynchronously from arXiv API."""
    papers: List[RawPaper] = []
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    
    try:
        status_code, body = _http_get(settings.ARXIV_API_URL, params=params)
        if status_code == 200 and body:
            root = ET.fromstring(body)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            
            for entry in root.findall("atom:entry", ns):
                title_elem = entry.find("atom:title", ns)
                summary_elem = entry.find("atom:summary", ns)
                published_elem = entry.find("atom:published", ns)
                id_elem = entry.find("atom:id", ns)
                
                title = title_elem.text.strip().replace("\n", " ") if title_elem is not None and title_elem.text else "Untitled"
                abstract = summary_elem.text.strip().replace("\n", " ") if summary_elem is not None and summary_elem.text else ""
                year = published_elem.text[:4] if published_elem is not None and published_elem.text else "N/A"
                url = id_elem.text.strip() if id_elem is not None and id_elem.text else None
                
                authors = []
                for author_node in entry.findall("atom:author", ns):
                    name_node = author_node.find("atom:name", ns)
                    if name_node is not None and name_node.text:
                        authors.append(name_node.text.strip())
                        
                papers.append(RawPaper(
                    title=title,
                    authors=authors,
                    year=year,
                    abstract=abstract,
                    url=url,
                    source="arXiv"
                ))
        else:
            logger.warning(f"arXiv API returned status code {status_code}")
    except Exception as e:
        logger.error(f"Error fetching from arXiv: {e}", exc_info=True)
        
    return papers


async def search_semantic_scholar(query: str, max_results: int = 5) -> List[RawPaper]:
    """Fetch academic papers asynchronously from Semantic Scholar API."""
    papers: List[RawPaper] = []
    params = {
        "query": query,
        "limit": max_results,
        "fields": "title,authors,year,abstract,url,externalIds"
    }
    
    try:
        status_code, body = _http_get(settings.SEMANTIC_SCHOLAR_API_URL, params=params)
        if status_code == 200 and body:
            data = json.loads(body)
            for item in data.get("data", []):
                title = item.get("title") or "Untitled"
                abstract = item.get("abstract") or ""
                year = str(item.get("year")) if item.get("year") else "N/A"
                url = item.get("url")
                
                authors = [a.get("name") for a in item.get("authors", []) if a.get("name")]
                doi = item.get("externalIds", {}).get("DOI") if item.get("externalIds") else None
                
                papers.append(RawPaper(
                    title=title,
                    authors=authors,
                    year=year,
                    abstract=abstract,
                    url=url,
                    doi=doi,
                    source="Semantic Scholar"
                ))
        else:
            logger.warning(f"Semantic Scholar API returned status code {status_code}")
    except Exception as e:
        logger.error(f"Error fetching from Semantic Scholar: {e}", exc_info=True)
        
    return papers


async def search_crossref(query: str, max_results: int = 5) -> List[RawPaper]:
    """Fetch academic works asynchronously from CrossRef API."""
    papers: List[RawPaper] = []
    params = {
        "query": query,
        "rows": max_results,
        "sort": "relevance"
    }
    headers = {
        "User-Agent": "ResearchIntelligenceAgent/1.0 (mailto:researcher@innovation-platform.org)"
    }
    
    try:
        status_code, body = _http_get(settings.CROSSREF_API_URL, params=params, headers=headers)
        if status_code == 200 and body:
            data = json.loads(body)
            items = data.get("message", {}).get("items", [])
            for item in items:
                title_list = item.get("title", [])
                title = title_list[0] if title_list else "Untitled"
                
                abstract = item.get("abstract", "") or ""
                # Clean XML tags in CrossRef abstracts if present
                if "<" in abstract and ">" in abstract:
                    import re
                    abstract = re.sub(r"<[^>]+>", "", abstract)
                    
                published = item.get("published-print") or item.get("published-online") or {}
                date_parts = published.get("date-parts", [[]])[0]
                year = str(date_parts[0]) if date_parts else "N/A"
                
                url = item.get("URL")
                doi = item.get("DOI")
                
                authors = []
                for author in item.get("author", []):
                    given = author.get("given", "")
                    family = author.get("family", "")
                    name = f"{given} {family}".strip()
                    if name:
                        authors.append(name)
                        
                papers.append(RawPaper(
                    title=title,
                    authors=authors,
                    year=year,
                    abstract=abstract,
                    url=url,
                    doi=doi,
                    source="CrossRef"
                ))
        else:
            logger.warning(f"CrossRef API returned status code {status_code}")
    except Exception as e:
        logger.error(f"Error fetching from CrossRef: {e}", exc_info=True)
        
    return papers


def deduplicate_papers(papers: List[RawPaper]) -> List[RawPaper]:
    """Deduplicate papers based on DOI or clean title similarity."""
    seen_dois = set()
    seen_titles = set()
    unique_papers: List[RawPaper] = []
    
    for paper in papers:
        # Check DOI
        if paper.doi:
            clean_doi = paper.doi.strip().lower()
            if clean_doi in seen_dois:
                continue
            seen_dois.add(clean_doi)
            
        # Check normalized title
        clean_title = "".join(e for e in paper.title.lower() if e.isalnum())
        if not clean_title or clean_title in seen_titles:
            continue
            
        seen_titles.add(clean_title)
        unique_papers.append(paper)
        
    return unique_papers
