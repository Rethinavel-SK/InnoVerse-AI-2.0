"""
InnoVerse AI 2.0 — Async SQLite Database Manager
==================================================
Provides async CRUD operations for all InnoVerse entities.
Uses aiosqlite for non-blocking database access alongside FastAPI.
"""

import json
import logging
import os
import aiosqlite
from typing import Dict, Any, List, Optional

from backend.database.models import (
    SCHEMA_SQL,
    InnovationProject, InnovationVersion, AgentAnalysis,
    AgentConflict, InnovationScore, Task, CommunicationEvent,
    Approval, FollowUp, DecisionLog, InnovationMemory,
    ProjectStatus, TaskStatus, ApprovalStatus,
)

logger = logging.getLogger(__name__)

DB_PATH = os.environ.get("INNOVERSE_DB_PATH", os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "innoverse.db"
))


class DatabaseManager:
    """Async SQLite database manager for InnoVerse AI 2.0."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._db: Optional[aiosqlite.Connection] = None

    async def initialize(self):
        """Initialize database and create tables."""
        self._db = await aiosqlite.connect(self.db_path)
        self._db.row_factory = aiosqlite.Row
        await self._db.executescript(SCHEMA_SQL)
        await self._db.commit()
        logger.info("Database initialized at %s", self.db_path)

    async def close(self):
        if self._db:
            await self._db.close()

    @property
    def db(self) -> aiosqlite.Connection:
        if not self._db:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        return self._db

    # -----------------------------------------------------------------------
    # Innovation Projects
    # -----------------------------------------------------------------------

    async def create_project(self, project: InnovationProject) -> InnovationProject:
        await self.db.execute(
            """INSERT INTO innovation_projects
               (id, title, problem_statement, status, current_version,
                overall_score, confidence, recommendation, created_at, updated_at, metadata)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (project.id, project.title, project.problem_statement,
             project.status.value, project.current_version,
             project.overall_score, project.confidence, project.recommendation,
             project.created_at, project.updated_at, json.dumps(project.metadata))
        )
        await self.db.commit()
        return project

    async def get_project(self, project_id: str) -> Optional[InnovationProject]:
        cursor = await self.db.execute(
            "SELECT * FROM innovation_projects WHERE id = ?", (project_id,)
        )
        row = await cursor.fetchone()
        if not row:
            return None
        return self._row_to_project(row)

    async def list_projects(self, limit: int = 50) -> List[InnovationProject]:
        cursor = await self.db.execute(
            "SELECT * FROM innovation_projects ORDER BY updated_at DESC LIMIT ?", (limit,)
        )
        rows = await cursor.fetchall()
        return [self._row_to_project(r) for r in rows]

    async def update_project(self, project_id: str, **kwargs) -> Optional[InnovationProject]:
        import time
        kwargs["updated_at"] = time.time()
        sets = ", ".join(f"{k} = ?" for k in kwargs)
        vals = list(kwargs.values()) + [project_id]
        await self.db.execute(
            f"UPDATE innovation_projects SET {sets} WHERE id = ?", vals
        )
        await self.db.commit()
        return await self.get_project(project_id)

    def _row_to_project(self, row) -> InnovationProject:
        return InnovationProject(
            id=row["id"], title=row["title"],
            problem_statement=row["problem_statement"],
            status=ProjectStatus(row["status"]),
            current_version=row["current_version"],
            overall_score=row["overall_score"],
            confidence=row["confidence"],
            recommendation=row["recommendation"],
            created_at=row["created_at"], updated_at=row["updated_at"],
            metadata=json.loads(row["metadata"] or "{}"),
        )

    # -----------------------------------------------------------------------
    # Innovation Versions
    # -----------------------------------------------------------------------

    async def create_version(self, version: InnovationVersion) -> InnovationVersion:
        await self.db.execute(
            """INSERT INTO innovation_versions
               (id, project_id, version_number, problem_statement,
                improved_statement, improvement_reasoning,
                overall_score, score_breakdown, confidence, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (version.id, version.project_id, version.version_number,
             version.problem_statement, version.improved_statement,
             version.improvement_reasoning, version.overall_score,
             json.dumps(version.score_breakdown), version.confidence,
             version.created_at)
        )
        await self.db.commit()
        return version

    async def get_versions(self, project_id: str) -> List[InnovationVersion]:
        cursor = await self.db.execute(
            "SELECT * FROM innovation_versions WHERE project_id = ? ORDER BY version_number",
            (project_id,)
        )
        rows = await cursor.fetchall()
        return [InnovationVersion(
            id=r["id"], project_id=r["project_id"],
            version_number=r["version_number"],
            problem_statement=r["problem_statement"],
            improved_statement=r["improved_statement"],
            improvement_reasoning=r["improvement_reasoning"],
            overall_score=r["overall_score"],
            score_breakdown=json.loads(r["score_breakdown"] or "{}"),
            confidence=r["confidence"], created_at=r["created_at"],
        ) for r in rows]

    # -----------------------------------------------------------------------
    # Agent Analyses
    # -----------------------------------------------------------------------

    async def save_agent_analysis(self, analysis: AgentAnalysis) -> AgentAnalysis:
        await self.db.execute(
            """INSERT INTO agent_analyses
               (id, project_id, version_id, agent_name, status,
                score, confidence, classification, findings,
                evidence, risks, recommendations, execution_time_ms, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (analysis.id, analysis.project_id, analysis.version_id,
             analysis.agent_name, analysis.status, analysis.score,
             analysis.confidence, analysis.classification.value,
             json.dumps(analysis.findings), json.dumps(analysis.evidence),
             json.dumps(analysis.risks), json.dumps(analysis.recommendations),
             analysis.execution_time_ms, analysis.created_at)
        )
        await self.db.commit()
        return analysis

    async def get_agent_analyses(self, project_id: str, version_id: Optional[str] = None) -> List[AgentAnalysis]:
        if version_id:
            cursor = await self.db.execute(
                "SELECT * FROM agent_analyses WHERE project_id = ? AND version_id = ?",
                (project_id, version_id)
            )
        else:
            cursor = await self.db.execute(
                "SELECT * FROM agent_analyses WHERE project_id = ? ORDER BY created_at DESC",
                (project_id,)
            )
        rows = await cursor.fetchall()
        return [AgentAnalysis(
            id=r["id"], project_id=r["project_id"], version_id=r["version_id"],
            agent_name=r["agent_name"], status=r["status"],
            score=r["score"], confidence=r["confidence"],
            classification=r["classification"],
            findings=json.loads(r["findings"] or "{}"),
            evidence=json.loads(r["evidence"] or "[]"),
            risks=json.loads(r["risks"] or "[]"),
            recommendations=json.loads(r["recommendations"] or "[]"),
            execution_time_ms=r["execution_time_ms"],
            created_at=r["created_at"],
        ) for r in rows]

    # -----------------------------------------------------------------------
    # Agent Conflicts
    # -----------------------------------------------------------------------

    async def save_conflict(self, conflict: AgentConflict) -> AgentConflict:
        await self.db.execute(
            """INSERT INTO agent_conflicts
               (id, project_id, version_id, agents_involved,
                conflict_description, agent_positions, evidence,
                confidence, resolution, reasoning, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (conflict.id, conflict.project_id, conflict.version_id,
             json.dumps(conflict.agents_involved), conflict.conflict_description,
             json.dumps(conflict.agent_positions), json.dumps(conflict.evidence),
             conflict.confidence, conflict.resolution, conflict.reasoning,
             conflict.created_at)
        )
        await self.db.commit()
        return conflict

    async def get_conflicts(self, project_id: str) -> List[AgentConflict]:
        cursor = await self.db.execute(
            "SELECT * FROM agent_conflicts WHERE project_id = ? ORDER BY created_at DESC",
            (project_id,)
        )
        rows = await cursor.fetchall()
        return [AgentConflict(
            id=r["id"], project_id=r["project_id"], version_id=r["version_id"],
            agents_involved=json.loads(r["agents_involved"] or "[]"),
            conflict_description=r["conflict_description"],
            agent_positions=json.loads(r["agent_positions"] or "{}"),
            evidence=json.loads(r["evidence"] or "[]"),
            confidence=r["confidence"], resolution=r["resolution"],
            reasoning=r["reasoning"], created_at=r["created_at"],
        ) for r in rows]

    # -----------------------------------------------------------------------
    # Innovation Scores
    # -----------------------------------------------------------------------

    async def save_score(self, score: InnovationScore) -> InnovationScore:
        await self.db.execute(
            """INSERT INTO innovation_scores
               (id, project_id, version_id, market_potential, technical_feasibility,
                business_viability, innovation_differentiation, patent_ip_position,
                risk_score, sustainability, mvp_feasibility, customer_value,
                scalability, overall_score, weights, explanation, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (score.id, score.project_id, score.version_id,
             score.market_potential, score.technical_feasibility,
             score.business_viability, score.innovation_differentiation,
             score.patent_ip_position, score.risk_score,
             score.sustainability, score.mvp_feasibility,
             score.customer_value, score.scalability,
             score.overall_score, json.dumps(score.weights),
             score.explanation, score.created_at)
        )
        await self.db.commit()
        return score

    async def get_scores(self, project_id: str) -> List[InnovationScore]:
        cursor = await self.db.execute(
            "SELECT * FROM innovation_scores WHERE project_id = ? ORDER BY created_at DESC",
            (project_id,)
        )
        rows = await cursor.fetchall()
        return [InnovationScore(
            id=r["id"], project_id=r["project_id"], version_id=r["version_id"],
            market_potential=r["market_potential"],
            technical_feasibility=r["technical_feasibility"],
            business_viability=r["business_viability"],
            innovation_differentiation=r["innovation_differentiation"],
            patent_ip_position=r["patent_ip_position"],
            risk_score=r["risk_score"], sustainability=r["sustainability"],
            mvp_feasibility=r["mvp_feasibility"], customer_value=r["customer_value"],
            scalability=r["scalability"], overall_score=r["overall_score"],
            weights=json.loads(r["weights"] or "{}"),
            explanation=r["explanation"], created_at=r["created_at"],
        ) for r in rows]

    # -----------------------------------------------------------------------
    # Tasks
    # -----------------------------------------------------------------------

    async def create_task(self, task: Task) -> Task:
        await self.db.execute(
            """INSERT INTO tasks
               (id, project_id, title, description, priority, status,
                owner, deadline, dependencies, progress, progress_detail,
                category, created_at, updated_at, completed_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (task.id, task.project_id, task.title, task.description,
             task.priority.value, task.status.value, task.owner, task.deadline,
             json.dumps(task.dependencies), task.progress, task.progress_detail,
             task.category, task.created_at, task.updated_at, task.completed_at)
        )
        await self.db.commit()
        return task

    async def get_tasks(self, project_id: str) -> List[Task]:
        cursor = await self.db.execute(
            "SELECT * FROM tasks WHERE project_id = ? ORDER BY created_at", (project_id,)
        )
        rows = await cursor.fetchall()
        return [self._row_to_task(r) for r in rows]

    async def get_task(self, task_id: str) -> Optional[Task]:
        cursor = await self.db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = await cursor.fetchone()
        return self._row_to_task(row) if row else None

    async def update_task(self, task_id: str, **kwargs) -> Optional[Task]:
        import time
        kwargs["updated_at"] = time.time()
        if kwargs.get("status") == "completed":
            kwargs["completed_at"] = time.time()
        sets = ", ".join(f"{k} = ?" for k in kwargs)
        vals = list(kwargs.values()) + [task_id]
        await self.db.execute(f"UPDATE tasks SET {sets} WHERE id = ?", vals)
        await self.db.commit()
        return await self.get_task(task_id)

    def _row_to_task(self, row) -> Task:
        return Task(
            id=row["id"], project_id=row["project_id"],
            title=row["title"], description=row["description"],
            priority=row["priority"], status=row["status"],
            owner=row["owner"], deadline=row["deadline"],
            dependencies=json.loads(row["dependencies"] or "[]"),
            progress=row["progress"], progress_detail=row["progress_detail"],
            category=row["category"],
            created_at=row["created_at"], updated_at=row["updated_at"],
            completed_at=row["completed_at"],
        )

    # -----------------------------------------------------------------------
    # Communication Events
    # -----------------------------------------------------------------------

    async def log_communication(self, event: CommunicationEvent) -> CommunicationEvent:
        await self.db.execute(
            """INSERT INTO communication_events
               (id, project_id, channel, direction, sender, recipient,
                content, message_type, conversation_id, connection_id, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (event.id, event.project_id, event.channel.value, event.direction,
             event.sender, event.recipient, event.content, event.message_type,
             event.conversation_id, event.connection_id, event.created_at)
        )
        await self.db.commit()
        return event

    async def get_communications(self, project_id: str, limit: int = 50) -> List[CommunicationEvent]:
        cursor = await self.db.execute(
            "SELECT * FROM communication_events WHERE project_id = ? ORDER BY created_at DESC LIMIT ?",
            (project_id, limit)
        )
        rows = await cursor.fetchall()
        return [CommunicationEvent(
            id=r["id"], project_id=r["project_id"],
            channel=r["channel"], direction=r["direction"],
            sender=r["sender"], recipient=r["recipient"],
            content=r["content"], message_type=r["message_type"],
            conversation_id=r["conversation_id"],
            connection_id=r["connection_id"], created_at=r["created_at"],
        ) for r in rows]

    # -----------------------------------------------------------------------
    # Approvals
    # -----------------------------------------------------------------------

    async def create_approval(self, approval: Approval) -> Approval:
        await self.db.execute(
            """INSERT INTO approvals
               (id, project_id, action_description, action_type, level,
                status, requested_via, approved_via, approved_by,
                created_at, resolved_at, expires_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (approval.id, approval.project_id, approval.action_description,
             approval.action_type, approval.level.value, approval.status.value,
             approval.requested_via.value, None, None,
             approval.created_at, None, approval.expires_at)
        )
        await self.db.commit()
        return approval

    async def get_pending_approvals(self, project_id: Optional[str] = None) -> List[Approval]:
        if project_id:
            cursor = await self.db.execute(
                "SELECT * FROM approvals WHERE project_id = ? AND status = 'pending' ORDER BY created_at",
                (project_id,)
            )
        else:
            cursor = await self.db.execute(
                "SELECT * FROM approvals WHERE status = 'pending' ORDER BY created_at"
            )
        rows = await cursor.fetchall()
        return [Approval(
            id=r["id"], project_id=r["project_id"],
            action_description=r["action_description"],
            action_type=r["action_type"], level=r["level"],
            status=r["status"], requested_via=r["requested_via"],
            approved_via=r["approved_via"], approved_by=r["approved_by"],
            created_at=r["created_at"], resolved_at=r["resolved_at"],
            expires_at=r["expires_at"],
        ) for r in rows]

    async def resolve_approval(self, approval_id: str, status: str,
                                approved_by: Optional[str] = None,
                                approved_via: Optional[str] = None) -> Optional[Approval]:
        import time
        await self.db.execute(
            """UPDATE approvals SET status = ?, approved_by = ?,
               approved_via = ?, resolved_at = ? WHERE id = ?""",
            (status, approved_by, approved_via, time.time(), approval_id)
        )
        await self.db.commit()
        cursor = await self.db.execute("SELECT * FROM approvals WHERE id = ?", (approval_id,))
        row = await cursor.fetchone()
        if not row:
            return None
        return Approval(
            id=row["id"], project_id=row["project_id"],
            action_description=row["action_description"],
            action_type=row["action_type"], level=row["level"],
            status=row["status"], requested_via=row["requested_via"],
            approved_via=row["approved_via"], approved_by=row["approved_by"],
            created_at=row["created_at"], resolved_at=row["resolved_at"],
            expires_at=row["expires_at"],
        )

    # -----------------------------------------------------------------------
    # Follow-ups
    # -----------------------------------------------------------------------

    async def create_followup(self, followup: FollowUp) -> FollowUp:
        await self.db.execute(
            """INSERT INTO follow_ups
               (id, project_id, task_id, channel, conversation_id,
                reminder_count, max_reminders, reminder_interval_hours,
                last_reminder_at, next_reminder_at, escalation_level,
                opted_out, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (followup.id, followup.project_id, followup.task_id,
             followup.channel.value, followup.conversation_id,
             followup.reminder_count, followup.max_reminders,
             followup.reminder_interval_hours, followup.last_reminder_at,
             followup.next_reminder_at, followup.escalation_level,
             int(followup.opted_out), followup.created_at)
        )
        await self.db.commit()
        return followup

    async def get_due_followups(self, current_time: float) -> List[FollowUp]:
        cursor = await self.db.execute(
            """SELECT * FROM follow_ups
               WHERE opted_out = 0
               AND reminder_count < max_reminders
               AND (next_reminder_at IS NULL OR next_reminder_at <= ?)
               ORDER BY next_reminder_at""",
            (current_time,)
        )
        rows = await cursor.fetchall()
        return [FollowUp(
            id=r["id"], project_id=r["project_id"], task_id=r["task_id"],
            channel=r["channel"], conversation_id=r["conversation_id"],
            reminder_count=r["reminder_count"], max_reminders=r["max_reminders"],
            reminder_interval_hours=r["reminder_interval_hours"],
            last_reminder_at=r["last_reminder_at"],
            next_reminder_at=r["next_reminder_at"],
            escalation_level=r["escalation_level"],
            opted_out=bool(r["opted_out"]), created_at=r["created_at"],
        ) for r in rows]

    async def update_followup(self, followup_id: str, **kwargs):
        sets = ", ".join(f"{k} = ?" for k in kwargs)
        vals = list(kwargs.values()) + [followup_id]
        await self.db.execute(f"UPDATE follow_ups SET {sets} WHERE id = ?", vals)
        await self.db.commit()

    # -----------------------------------------------------------------------
    # Decision Logs
    # -----------------------------------------------------------------------

    async def log_decision(self, decision: DecisionLog) -> DecisionLog:
        await self.db.execute(
            """INSERT INTO decision_logs
               (id, project_id, decision, reasoning, decision_type,
                confidence, made_by, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (decision.id, decision.project_id, decision.decision,
             decision.reasoning, decision.decision_type,
             decision.confidence, decision.made_by, decision.created_at)
        )
        await self.db.commit()
        return decision

    async def get_decisions(self, project_id: str) -> List[DecisionLog]:
        cursor = await self.db.execute(
            "SELECT * FROM decision_logs WHERE project_id = ? ORDER BY created_at DESC",
            (project_id,)
        )
        rows = await cursor.fetchall()
        return [DecisionLog(
            id=r["id"], project_id=r["project_id"],
            decision=r["decision"], reasoning=r["reasoning"],
            decision_type=r["decision_type"], confidence=r["confidence"],
            made_by=r["made_by"], created_at=r["created_at"],
        ) for r in rows]

    # -----------------------------------------------------------------------
    # Innovation Memory
    # -----------------------------------------------------------------------

    async def save_memory(self, memory: InnovationMemory) -> InnovationMemory:
        await self.db.execute(
            """INSERT INTO innovation_memory
               (id, project_id, memory_type, content, tags,
                related_project_ids, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (memory.id, memory.project_id, memory.memory_type,
             memory.content, json.dumps(memory.tags),
             json.dumps(memory.related_project_ids), memory.created_at)
        )
        await self.db.commit()
        return memory

    async def search_memory(self, query: str, limit: int = 10) -> List[InnovationMemory]:
        cursor = await self.db.execute(
            "SELECT * FROM innovation_memory WHERE content LIKE ? ORDER BY created_at DESC LIMIT ?",
            (f"%{query}%", limit)
        )
        rows = await cursor.fetchall()
        return [InnovationMemory(
            id=r["id"], project_id=r["project_id"],
            memory_type=r["memory_type"], content=r["content"],
            tags=json.loads(r["tags"] or "[]"),
            related_project_ids=json.loads(r["related_project_ids"] or "[]"),
            created_at=r["created_at"],
        ) for r in rows]

    async def get_project_memory(self, project_id: str) -> List[InnovationMemory]:
        cursor = await self.db.execute(
            "SELECT * FROM innovation_memory WHERE project_id = ? ORDER BY created_at DESC",
            (project_id,)
        )
        rows = await cursor.fetchall()
        return [InnovationMemory(
            id=r["id"], project_id=r["project_id"],
            memory_type=r["memory_type"], content=r["content"],
            tags=json.loads(r["tags"] or "[]"),
            related_project_ids=json.loads(r["related_project_ids"] or "[]"),
            created_at=r["created_at"],
        ) for r in rows]


# Singleton
db_manager = DatabaseManager()
