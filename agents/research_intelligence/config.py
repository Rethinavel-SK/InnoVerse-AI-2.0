import os

# Load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class Settings:
    """Configuration settings for Research Intelligence Agent."""

    # LLM settings
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    GROQ_API_URL: str = "https://api.groq.com/openai/v1/chat/completions"
    
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DEFAULT_MODEL: str = os.getenv("RESEARCH_AGENT_MODEL", "gemini-2.0-flash")
    
    # External API endpoints & timeouts
    SEMANTIC_SCHOLAR_API_URL: str = "https://api.semanticscholar.org/graph/v1/paper/search"
    ARXIV_API_URL: str = "http://export.arxiv.org/api/query"
    CROSSREF_API_URL: str = "https://api.crossref.org/works"
    
    REQUEST_TIMEOUT: float = 15.0  # seconds per external API request
    MAX_PAPERS_PER_SOURCE: int = 5
    TOTAL_MAX_PAPERS: int = 8
    
    # Cache & Memory settings
    CACHE_EXPIRATION_HOURS: int = 24

settings = Settings()
