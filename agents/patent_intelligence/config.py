import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Settings:
    """Configuration settings for Patent Intelligence Agent."""
    
    # LLM settings
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    GROQ_API_URL: str = "https://api.groq.com/openai/v1/chat/completions"

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DEFAULT_MODEL: str = os.getenv("RESEARCH_AGENT_MODEL", "gemini-2.5-flash")

    # Patent API Endpoints
    USPTO_API_URL: str = "https://developer.uspto.gov/ibd-api/v1/patent/application"
    CROSSREF_API_URL: str = "https://api.crossref.org/works"

    REQUEST_TIMEOUT: float = 15.0  # seconds per external API request
    MAX_PATENTS_PER_SEARCH: int = 5
    CACHE_EXPIRATION_HOURS: int = 24


settings = Settings()
