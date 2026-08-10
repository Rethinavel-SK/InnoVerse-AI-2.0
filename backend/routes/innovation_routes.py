"""
InnoVerse AI 2.0 — Innovation API v2 Routes
=============================================
New REST endpoints for the 2.0 features:
- Innovation projects CRUD
- Full analysis pipeline
- Idea evolution
- Re-evaluation
- Task management
- Score breakdown
- Debate trace
- Communication history
- Approval workflow
"""

import logging
import time
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from backend.database.db import db_manager
from backend.database.models import (
    InnovationProject, InnovationVersion, Task, Approval,
    CommunicationEvent, InnovationMemory, DecisionLog,
    ProjectStatus, TaskStatus, TaskPriority, ApprovalLevel,
    ApprovalStatus, ChannelType,
)
from agents.innovation_director.services.director_service import InnovationDirectorService
from agents.innovation_director.schemas.director_schema import InnovationDirectorRequest
from agents.innovation_director.services.score_engine import score_engine
from agents.innovation_director.services.idea_evolution import idea_evolution_engine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v2", tags=["InnoVerse AI 2.0"])

director_service = InnovationDirectorService()


# ---------------------------------------------------------------------------
# Request / Response Models
# ---------------------------------------------------------------------------

class CreateProjectRequest(BaseModel):
    problem_statement: str = Field(..., min_length=10)
    title: str = ""
    context: Optional[Dict[str, Any]] = None


class ImproveIdeaRequest(BaseModel):
    max_iterations: int = Field(default=1, ge=1, le=3)


class UpdateTaskRequest(BaseModel):
    status: Optional[str] = None
    progress: Optional[int] = None
    progress_detail: Optional[str] = None
    owner: Optional[str] = None


class CreateTaskRequest(BaseModel):
    title: str
    description: str = ""
    priority: str = "medium"
    category: str = "general"
    deadline: Optional[str] = None


class ApprovalActionRequest(BaseModel):
    approved_by: str = "user"


class ReEvaluateRequest(BaseModel):
    new_information: str = Field(..., min_length=5)


# ---------------------------------------------------------------------------
# Innovation Project Endpoints
# ---------------------------------------------------------------------------

@router.post("/innovations", status_code=status.HTTP_201_CREATED)
async def create_innovation_project(req: CreateProjectRequest):
    """Create a new innovation project."""
    project = InnovationProject(
        problem_statement=req.problem_statement,
        title=req.title or req.problem_statement[:80],
    )
    project = await db_manager.create_project(project)

    # Create version 1
    version = InnovationVersion(
        project_id=project.id,
        version_number=1,
        problem_statement=req.problem_statement,
    )
    await db_manager.create_version(version)

    return {"project": project.model_dump(), "version": version.model_dump()}


@router.get("/innovations")
async def list_innovation_projects(limit: int = 50):
    """List all innovation projects."""
    projects = await db_manager.list_projects(limit=limit)
    return {"projects": [p.model_dump() for p in projects], "total": len(projects)}


@router.get("/innovations/{project_id}")
async def get_innovation_project(project_id: str):
    """Get full project details."""
    project = await db_manager.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")

    versions = await db_manager.get_versions(project_id)
    scores = await db_manager.get_scores(project_id)
    tasks = await db_manager.get_tasks(project_id)
    decisions = await db_manager.get_decisions(project_id)
    conflicts = await db_manager.get_conflicts(project_id)

    return {
        "project": project.model_dump(),
        "versions": [v.model_dump() for v in versions],
        "scores": [s.model_dump() for s in scores],
        "tasks": [t.model_dump() for t in tasks],
        "decisions": [d.model_dump() for d in decisions],
        "conflicts": [c.model_dump() for c in conflicts],
    }


# ---------------------------------------------------------------------------
# Analysis Endpoints
# ---------------------------------------------------------------------------

@router.post("/innovations/{project_id}/analyze")
async def analyze_innovation(project_id: str):
    """Run full 11-agent analysis on a project."""
    project = await db_manager.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")

    # Update status
    await db_manager.update_project(project_id, status="analyzing")

    # Run director pipeline
    request = InnovationDirectorRequest(problem_statement=project.problem_statement)

    try:
        result = await director_service.analyze_and_orchestrate(request)
        result_dict = result.model_dump()

        # Update project with results
        await db_manager.update_project(
            project_id,
            status="analyzed",
            overall_score=result.overall_innovation_score,
            confidence=result.confidence,
            recommendation=result.recommendation,
        )

        # Save score to database
        score_breakdown = result_dict.get("score_breakdown", {})
        if score_breakdown:
            from backend.database.models import InnovationScore
            versions = await db_manager.get_versions(project_id)
            version_id = versions[0].id if versions else "v1"
            score = InnovationScore(
                project_id=project_id,
                version_id=version_id,
                market_potential=score_breakdown.get("market_potential", 0),
                technical_feasibility=score_breakdown.get("technical_feasibility", 0),
                business_viability=score_breakdown.get("business_viability", 0),
                innovation_differentiation=score_breakdown.get("innovation_differentiation", 0),
                patent_ip_position=score_breakdown.get("patent_ip_position", 0),
                risk_score=score_breakdown.get("risk_score", 0),
                sustainability=score_breakdown.get("sustainability", 0),
                mvp_feasibility=score_breakdown.get("mvp_feasibility", 0),
                customer_value=score_breakdown.get("customer_value", 0),
                scalability=score_breakdown.get("scalability", 0),
                overall_score=result.overall_innovation_score,
                explanation=score_breakdown.get("explanation", ""),
            )
            await db_manager.save_score(score)

        # Save tasks from execution planner
        exec_plan = result_dict.get("execution_plan", {})
        if isinstance(exec_plan, dict):
            plan_data = exec_plan.get("execution_plan", exec_plan)
            tasks = plan_data.get("tasks", [])
            for task_data in tasks[:15]:  # Limit to 15 tasks
                if isinstance(task_data, dict):
                    task = Task(
                        project_id=project_id,
                        title=task_data.get("title", "Untitled"),
                        description=task_data.get("description", ""),
                        priority=task_data.get("priority", "MEDIUM").lower(),
                        category=task_data.get("category", "general"),
                    )
                    await db_manager.create_task(task)

        # Log decision
        await db_manager.log_decision(DecisionLog(
            project_id=project_id,
            decision=f"Innovation analysis completed. Score: {result.overall_innovation_score}/100. Recommendation: {result.recommendation}",
            reasoning=f"Based on 11-agent analysis with {result.confidence:.0%} confidence.",
            decision_type="proceed" if result.overall_innovation_score >= 60 else "pause",
            confidence=result.confidence,
        ))

        return result_dict

    except Exception as e:
        logger.error("Analysis failed for project %s: %s", project_id, e, exc_info=True)
        await db_manager.update_project(project_id, status="draft")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


# ---------------------------------------------------------------------------
# Idea Evolution Endpoints
# ---------------------------------------------------------------------------

@router.post("/innovations/{project_id}/improve")
async def improve_innovation(project_id: str, req: ImproveIdeaRequest):
    """Trigger idea evolution — improve the idea based on agent weaknesses."""
    project = await db_manager.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")

    versions = await db_manager.get_versions(project_id)
    current_version = len(versions)

    if current_version > 3:
        raise HTTPException(status_code=400, detail="Maximum 3 evolution iterations reached.")

    # Get last analysis results to extract weaknesses
    analyses = await db_manager.get_agent_analyses(project_id)
    agent_results = {}
    for a in analyses:
        agent_results[a.agent_name] = a.findings

    weaknesses = idea_evolution_engine.extract_weaknesses_from_agents(agent_results)

    if not weaknesses:
        weaknesses = [
            "Market differentiation unclear",
            "Unit economics need validation",
            "Technical complexity risk",
        ]

    previous_improvements = [
        v.improvement_reasoning or "" for v in versions
        if v.improvement_reasoning
    ]

    new_version = await idea_evolution_engine.improve_idea(
        project_id=project_id,
        original_statement=project.problem_statement,
        weaknesses=weaknesses,
        current_version=current_version,
        previous_improvements=previous_improvements,
    )

    if not new_version:
        raise HTTPException(status_code=400, detail="Cannot improve further (max iterations reached).")

    # Update project
    await db_manager.update_project(project_id, current_version=new_version.version_number, status="improving")

    return {
        "version": new_version.model_dump(),
        "weaknesses_addressed": weaknesses,
        "evolution_history": await idea_evolution_engine.get_evolution_history(project_id),
    }


@router.get("/innovations/{project_id}/evolution")
async def get_evolution_history(project_id: str):
    """Get the full idea evolution history."""
    history = await idea_evolution_engine.get_evolution_history(project_id)
    return {"project_id": project_id, "evolution_history": history}


# ---------------------------------------------------------------------------
# Score Endpoints
# ---------------------------------------------------------------------------

@router.get("/innovations/{project_id}/score")
async def get_score_breakdown(project_id: str):
    """Get detailed 10-dimension score breakdown."""
    scores = await db_manager.get_scores(project_id)
    if not scores:
        raise HTTPException(status_code=404, detail="No scores found for this project.")
    return {"project_id": project_id, "scores": [s.model_dump() for s in scores]}


# ---------------------------------------------------------------------------
# Task Endpoints
# ---------------------------------------------------------------------------

@router.get("/innovations/{project_id}/tasks")
async def get_project_tasks(project_id: str):
    """Get all tasks for a project."""
    tasks = await db_manager.get_tasks(project_id)
    completed = sum(1 for t in tasks if t.status == TaskStatus.COMPLETED)
    return {
        "project_id": project_id,
        "tasks": [t.model_dump() for t in tasks],
        "total": len(tasks),
        "completed": completed,
        "progress": round(completed / max(len(tasks), 1) * 100, 1),
    }


@router.post("/innovations/{project_id}/tasks", status_code=status.HTTP_201_CREATED)
async def create_project_task(project_id: str, req: CreateTaskRequest):
    """Create a new task for a project."""
    project = await db_manager.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")

    task = Task(
        project_id=project_id,
        title=req.title,
        description=req.description,
        priority=req.priority,
        category=req.category,
        deadline=req.deadline,
    )
    task = await db_manager.create_task(task)
    return {"task": task.model_dump()}


@router.patch("/tasks/{task_id}")
async def update_task(task_id: str, req: UpdateTaskRequest):
    """Update task status/progress."""
    kwargs = {}
    if req.status is not None:
        kwargs["status"] = req.status
    if req.progress is not None:
        kwargs["progress"] = req.progress
    if req.progress_detail is not None:
        kwargs["progress_detail"] = req.progress_detail
    if req.owner is not None:
        kwargs["owner"] = req.owner

    task = await db_manager.update_task(task_id, **kwargs)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    return {"task": task.model_dump()}


# ---------------------------------------------------------------------------
# Communication Endpoints
# ---------------------------------------------------------------------------

@router.get("/innovations/{project_id}/communications")
async def get_communications(project_id: str, limit: int = 50):
    """Get communication history for a project."""
    events = await db_manager.get_communications(project_id, limit=limit)
    return {"project_id": project_id, "communications": [e.model_dump() for e in events]}


# ---------------------------------------------------------------------------
# Approval Endpoints
# ---------------------------------------------------------------------------

@router.post("/approvals/{approval_id}/approve")
async def approve_action(approval_id: str, req: ApprovalActionRequest):
    """Approve a pending action."""
    approval = await db_manager.resolve_approval(
        approval_id, "approved", approved_by=req.approved_by, approved_via="dashboard"
    )
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found.")
    return {"approval": approval.model_dump()}


@router.post("/approvals/{approval_id}/reject")
async def reject_action(approval_id: str, req: ApprovalActionRequest):
    """Reject a pending action."""
    approval = await db_manager.resolve_approval(
        approval_id, "rejected", approved_by=req.approved_by, approved_via="dashboard"
    )
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found.")
    return {"approval": approval.model_dump()}


# ---------------------------------------------------------------------------
# Memory Endpoints
# ---------------------------------------------------------------------------

@router.get("/innovations/{project_id}/memory")
async def get_project_memory(project_id: str):
    """Get innovation memory for a project."""
    memories = await db_manager.get_project_memory(project_id)
    return {"project_id": project_id, "memories": [m.model_dump() for m in memories]}


# ---------------------------------------------------------------------------
# Debate Endpoints
# ---------------------------------------------------------------------------

@router.get("/innovations/{project_id}/debate")
async def get_debate_trace(project_id: str):
    """Get agent debate trace for a project."""
    conflicts = await db_manager.get_conflicts(project_id)
    return {
        "project_id": project_id,
        "debates": [c.model_dump() for c in conflicts],
    }


# ---------------------------------------------------------------------------
# System Status
# ---------------------------------------------------------------------------

@router.get("/status")
async def get_system_status():
    """Get InnoVerse AI 2.0 system status."""
    from backend.caspian.client import caspian_client

    projects = await db_manager.list_projects(limit=1)

    return {
        "version": "2.0.0",
        "status": "operational",
        "total_agents": 11,
        "agent_names": [
            "Solution Architect", "Business Strategy", "Research Intelligence",
            "Patent Intelligence", "Market Intelligence", "Trend Intelligence",
            "Risk Assessment", "Sustainability", "MVP Roadmap",
            "Failure Hunter", "Execution Planner",
        ],
        "caspian": {
            "configured": caspian_client.is_configured,
            "connected_channels": caspian_client.connected_channels,
            "email_address": caspian_client.email_address,
            "listener_running": caspian_client.is_running,
        },
        "database": {
            "status": "connected",
            "total_projects": len(projects),
        },
        "features": [
            "11-Agent Orchestration",
            "10-Dimension Scoring",
            "Multi-Agent Debate",
            "Evidence Classification",
            "Idea Evolution Engine",
            "Execution Planning",
            "Caspian Communication (Telegram/Email/Discord)",
            "Follow-up & Approval System",
            "Innovation Memory",
        ],
    }
