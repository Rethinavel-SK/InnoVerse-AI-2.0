<<<<<<< HEAD
import logging
from fastapi import FastAPI
from backend.routes.solution_architect_route import router as solution_architect_router
from backend.routes.mvp_roadmap_route import router as mvp_roadmap_router
from backend.routes.business_strategy_route import router as business_strategy_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="Innovation Discovery Platform - Multi-Agent AI API",
    version="1.0.0",
    description="Enterprise Multi-Agent Platform API serving Solution Architect Agent, MVP & Roadmap Agent, Business Strategy Agent, and intelligence modules."
)

app.include_router(solution_architect_router)
app.include_router(mvp_roadmap_router)
app.include_router(business_strategy_router)




@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "platform": "Innovation Discovery Platform"}
=======
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Import agent routers
from agents.risk_assessment.router import router as risk_router
from agents.research_intelligence.router import router as research_router
from agents.patent_intelligence.router import router as patent_router

app = FastAPI(
    title="AI Innovation Discovery Platform - Agents API",
    description="REST API server to test independent AI agents using Thunder Client / Postman.",
    version="1.0.0"
)

# Enable CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include agent routers
app.include_router(risk_router)
app.include_router(research_router)
app.include_router(patent_router)

@app.get("/")
def root():
    return {
        "message": "AI Innovation Discovery Platform API is running.",
        "docs_url": "http://localhost:8000/docs",
        "endpoints": [
            "POST /agents/risk-assessment/analyze",
            "POST /agents/research-intelligence/analyze",
            "POST /agents/patent-intelligence/analyze"
        ]
    }

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
>>>>>>> origin/feature/mubaarak
