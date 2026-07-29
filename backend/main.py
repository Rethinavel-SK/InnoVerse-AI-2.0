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
