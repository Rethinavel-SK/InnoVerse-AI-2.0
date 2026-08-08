import logging
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Import agent routers
from backend.routes.solution_architect_route import router as solution_architect_router
from backend.routes.mvp_roadmap_route import router as mvp_roadmap_router
from backend.routes.business_strategy_route import router as business_strategy_router
from backend.routes.innovation_director_route import router as innovation_director_router

# Import intelligence agent routers
from agents.risk_assessment.router import router as risk_router
from agents.research_intelligence.router import router as research_router
from agents.patent_intelligence.router import router as patent_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="AI Innovation Discovery Platform - Master Multi-Agent API",
    version="1.0.0",
    description="Enterprise Multi-Agent Platform API serving Innovation Director Agent, Solution Architect Agent, Business Strategy Agent, Research Agent, Patent Analysis Agent, Market Analysis Agent, Trend Analysis Agent, Risk Assessment Agent, Sustainability Agent, and MVP & Roadmap Planner Agent."
)

# Enable CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from backend.routes.enterprise_routes import router as enterprise_router

# Include agent routers
app.include_router(innovation_director_router)
app.include_router(solution_architect_router)
app.include_router(mvp_roadmap_router)
app.include_router(business_strategy_router)
app.include_router(risk_router)
app.include_router(research_router)
app.include_router(patent_router)
app.include_router(enterprise_router)


# Mount static assets if dist or public directory exists
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
DIST_DIR = os.path.join(FRONTEND_DIR, "dist")
PUBLIC_DIR = os.path.join(FRONTEND_DIR, "public")

if os.path.exists(DIST_DIR):
    assets_dir = os.path.join(DIST_DIR, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
elif os.path.exists(PUBLIC_DIR):
    app.mount("/public", StaticFiles(directory=PUBLIC_DIR), name="public")


@app.get("/", tags=["Dashboard"])
async def serve_dashboard():
    dist_index = os.path.join(DIST_DIR, "index.html")
    if os.path.exists(dist_index):
        return FileResponse(dist_index)
    public_index = os.path.join(PUBLIC_DIR, "index.html")
    if os.path.exists(public_index):
        return FileResponse(public_index)
    return {
        "message": "AI Innovation Discovery Platform API is running.",
        "docs_url": "http://localhost:8000/docs",
        "active_agents": 10
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "ok",
        "platform": "AI Innovation Discovery Platform",
        "active_agents": 10,
        "agents": [
            "Innovation Director Agent (Orchestrator)",
            "Solution Architect Agent",
            "Business Strategy Agent",
            "Research Agent",
            "Patent Analysis Agent",
            "Market Analysis Agent",
            "Trend Analysis Agent",
            "Risk Assessment Agent",
            "Sustainability Agent",
            "MVP & Roadmap Planner Agent"
        ]
    }


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
