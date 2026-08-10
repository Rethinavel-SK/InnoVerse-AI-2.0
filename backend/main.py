import logging
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager

# Import agent routers
from backend.routes.solution_architect_route import router as solution_architect_router
from backend.routes.mvp_roadmap_route import router as mvp_roadmap_router
from backend.routes.business_strategy_route import router as business_strategy_router
from backend.routes.innovation_director_route import router as innovation_director_router
from backend.routes.innovation_routes import router as innovation_v2_router

# Import intelligence agent routers
from agents.risk_assessment.router import router as risk_router
from agents.research_intelligence.router import router as research_router
from agents.patent_intelligence.router import router as patent_router

from backend.database.db import db_manager
from backend.caspian.client import caspian_client
from backend.caspian.message_router import message_router
from agents.innovation_director.services.director_service import InnovationDirectorService

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

director_service = InnovationDirectorService()

async def _orchestrate_handler(project_id: str, problem_statement: str):
    from agents.innovation_director.schemas.director_schema import InnovationDirectorRequest
    req = InnovationDirectorRequest(problem_statement=problem_statement)
    res = await director_service.analyze_and_orchestrate(req)
    return res.model_dump()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Initializing InnoVerse AI 2.0 Database...")
    await db_manager.initialize()

    # Link message router handler
    message_router.set_innovation_handler(_orchestrate_handler)

    # Initialize Caspian SDK
    if caspian_client.initialize():
        caspian_client.set_message_handler(message_router.handle_message)
        caspian_client.start_listener()
        logger.info("Caspian SDK listener started successfully.")

    yield

    # Shutdown
    caspian_client.stop_listener()
    await db_manager.close()
    logger.info("InnoVerse AI 2.0 backend shutdown complete.")

app = FastAPI(
    title="InnoVerse AI 2.0 — Autonomous Multi-Agent AI Platform",
    version="2.0.0",
    description="Enterprise Autonomous Multi-Agent Platform serving Innovation Director Agent, Failure Hunter Agent, Execution Planner Agent, Solution Architect Agent, Business Strategy Agent, Research Agent, Patent Analysis Agent, Market Analysis Agent, Trend Analysis Agent, Risk Assessment Agent, Sustainability Agent, MVP & Roadmap Planner Agent, and Caspian SDK Multi-Channel Communications.",
    lifespan=lifespan
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

app.include_router(innovation_v2_router)
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
        "platform": "InnoVerse AI 2.0 Autonomous Platform",
        "version": "2.0.0",
        "active_agents": 11,
        "agents": [
            "Innovation Director Agent (Master Orchestrator)",
            "Failure Hunter Agent (Adversarial Critic)",
            "Execution Planner Agent (Roadmap & Tasks)",
            "Solution Architect Agent",
            "Business Strategy Agent",
            "Research Agent",
            "Patent Analysis Agent",
            "Market Analysis Agent",
            "Trend Analysis Agent",
            "Risk Assessment Agent",
            "Sustainability Agent",
            "MVP & Roadmap Planner Agent"
        ],
        "caspian": {
            "configured": caspian_client.is_configured,
            "channels": caspian_client.connected_channels,
            "running": caspian_client.is_running
        }
    }


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
