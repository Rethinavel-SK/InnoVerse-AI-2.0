"""
InnoVerse AI 2.0 — Database Models
====================================
Pydantic models and SQLite schema definitions for persistent storage.
"""

import uuid
import time
from typing import Dict, Any, List, Optional
from enum import Enum
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ProjectStatus(str, Enum):
    DRAFT = "draft"
    ANALYZING = "analyzing"
    ANALYZED = "analyzed"
    IMPROVING = "improving"
    EXECUTING = "executing"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ApprovalLevel(str, Enum):
    LOW = "low"          # AI acts automatically
    MEDIUM = "medium"    # AI prepares, asks for approval
    HIGH = "high"        # Human approval required
    CRITICAL = "critical"  # Never without explicit confirmation


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class EvidenceClassification(str, Enum):
    FACT = "FACT"
    INFERENCE = "INFERENCE"
    PREDICTION = "PREDICTION"
    ASSUMPTION = "ASSUMPTION"


class ChannelType(str, Enum):
    TELEGRAM = "telegram"
    EMAIL = "email"
    DISCORD = "discord"
    DASHBOARD = "dashboard"


# ---------------------------------------------------------------------------
# Core Models
# ---------------------------------------------------------------------------

class InnovationProject(BaseModel):
    """Core innovation project entity."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:12])
    title: str = ""
    problem_statement: str
    status: ProjectStatus = ProjectStatus.DRAFT
    current_version: int = 1
    overall_score: Optional[float] = None
    confidence: Optional[float] = None
    recommendation: Optional[str] = None
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class InnovationVersion(BaseModel):
    """A version of an innovation idea (for idea evolution tracking)."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:12])
    project_id: str
    version_number: int = 1
    problem_statement: str
    improved_statement: Optional[str] = None
    improvement_reasoning: Optional[str] = None
    overall_score: Optional[float] = None
    score_breakdown: Dict[str, Any] = Field(default_factory=dict)
    confidence: Optional[float] = None
    created_at: float = Field(default_factory=time.time)


class AgentAnalysis(BaseModel):
    """Stored output from a specialist agent for a specific version."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:12])
    project_id: str
    version_id: str
    agent_name: str
    status: str = "completed"
    score: Optional[float] = None
    confidence: Optional[float] = None
    classification: EvidenceClassification = EvidenceClassification.INFERENCE
    findings: Dict[str, Any] = Field(default_factory=dict)
    evidence: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    execution_time_ms: Optional[float] = None
    created_at: float = Field(default_factory=time.time)


class AgentConflict(BaseModel):
    """Detected conflict between two or more agents."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:12])
    project_id: str
    version_id: str
    agents_involved: List[str]
    conflict_description: str
    agent_positions: Dict[str, str] = Field(default_factory=dict)
    evidence: List[str] = Field(default_factory=list)
    confidence: Optional[float] = None
    resolution: Optional[str] = None
    reasoning: Optional[str] = None
    created_at: float = Field(default_factory=time.time)


class InnovationScore(BaseModel):
    """Transparent 10-dimension innovation score."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:12])
    project_id: str
    version_id: str
    market_potential: float = 0.0
    technical_feasibility: float = 0.0
    business_viability: float = 0.0
    innovation_differentiation: float = 0.0
    patent_ip_position: float = 0.0
    risk_score: float = 0.0           # inverted: lower risk = higher score
    sustainability: float = 0.0
    mvp_feasibility: float = 0.0
    customer_value: float = 0.0
    scalability: float = 0.0
    overall_score: float = 0.0
    weights: Dict[str, float] = Field(default_factory=lambda: {
        "market_potential": 0.15,
        "technical_feasibility": 0.15,
        "business_viability": 0.12,
        "innovation_differentiation": 0.12,
        "patent_ip_position": 0.08,
        "risk_score": 0.08,
        "sustainability": 0.06,
        "mvp_feasibility": 0.10,
        "customer_value": 0.08,
        "scalability": 0.06,
    })
    explanation: str = ""
    created_at: float = Field(default_factory=time.time)


class Task(BaseModel):
    """Execution task generated from innovation analysis."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:12])
    project_id: str
    title: str
    description: str = ""
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    owner: Optional[str] = None
    deadline: Optional[str] = None
    dependencies: List[str] = Field(default_factory=list)
    progress: int = 0                  # 0-100
    progress_detail: Optional[str] = None
    category: str = "general"          # validation, research, technical, business
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)
    completed_at: Optional[float] = None


class CommunicationEvent(BaseModel):
    """Record of a message sent/received via Caspian channels."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:12])
    project_id: Optional[str] = None
    channel: ChannelType
    direction: str = "outbound"        # inbound / outbound
    sender: Optional[str] = None
    recipient: Optional[str] = None
    content: str
    message_type: str = "notification" # notification, report, reminder, approval, update
    conversation_id: Optional[str] = None
    connection_id: Optional[str] = None
    created_at: float = Field(default_factory=time.time)


class Approval(BaseModel):
    """Approval request for human-in-the-loop safety."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:12])
    project_id: str
    action_description: str
    action_type: str                   # send_report, send_update, external_communication
    level: ApprovalLevel = ApprovalLevel.MEDIUM
    status: ApprovalStatus = ApprovalStatus.PENDING
    requested_via: ChannelType = ChannelType.TELEGRAM
    approved_via: Optional[ChannelType] = None
    approved_by: Optional[str] = None
    created_at: float = Field(default_factory=time.time)
    resolved_at: Optional[float] = None
    expires_at: Optional[float] = None


class FollowUp(BaseModel):
    """Follow-up reminder tracking."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:12])
    project_id: str
    task_id: str
    channel: ChannelType = ChannelType.TELEGRAM
    conversation_id: Optional[str] = None
    reminder_count: int = 0
    max_reminders: int = 3
    reminder_interval_hours: int = 24
    last_reminder_at: Optional[float] = None
    next_reminder_at: Optional[float] = None
    escalation_level: int = 0
    opted_out: bool = False
    created_at: float = Field(default_factory=time.time)


class DecisionLog(BaseModel):
    """Decision history for an innovation project."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:12])
    project_id: str
    decision: str
    reasoning: str
    decision_type: str = "general"     # proceed, pivot, pause, cancel, escalate
    confidence: Optional[float] = None
    made_by: str = "innovation_director"
    created_at: float = Field(default_factory=time.time)


class InnovationMemory(BaseModel):
    """Persistent memory entry for cross-project learning."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:12])
    project_id: Optional[str] = None
    memory_type: str = "lesson"        # lesson, pattern, feedback, research, decision
    content: str
    tags: List[str] = Field(default_factory=list)
    related_project_ids: List[str] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)


# ---------------------------------------------------------------------------
# SQL Schema
# ---------------------------------------------------------------------------

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS innovation_projects (
    id TEXT PRIMARY KEY,
    title TEXT DEFAULT '',
    problem_statement TEXT NOT NULL,
    status TEXT DEFAULT 'draft',
    current_version INTEGER DEFAULT 1,
    overall_score REAL,
    confidence REAL,
    recommendation TEXT,
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL,
    metadata TEXT DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS innovation_versions (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    version_number INTEGER DEFAULT 1,
    problem_statement TEXT NOT NULL,
    improved_statement TEXT,
    improvement_reasoning TEXT,
    overall_score REAL,
    score_breakdown TEXT DEFAULT '{}',
    confidence REAL,
    created_at REAL NOT NULL,
    FOREIGN KEY (project_id) REFERENCES innovation_projects(id)
);

CREATE TABLE IF NOT EXISTS agent_analyses (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    version_id TEXT NOT NULL,
    agent_name TEXT NOT NULL,
    status TEXT DEFAULT 'completed',
    score REAL,
    confidence REAL,
    classification TEXT DEFAULT 'INFERENCE',
    findings TEXT DEFAULT '{}',
    evidence TEXT DEFAULT '[]',
    risks TEXT DEFAULT '[]',
    recommendations TEXT DEFAULT '[]',
    execution_time_ms REAL,
    created_at REAL NOT NULL,
    FOREIGN KEY (project_id) REFERENCES innovation_projects(id),
    FOREIGN KEY (version_id) REFERENCES innovation_versions(id)
);

CREATE TABLE IF NOT EXISTS agent_conflicts (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    version_id TEXT NOT NULL,
    agents_involved TEXT DEFAULT '[]',
    conflict_description TEXT,
    agent_positions TEXT DEFAULT '{}',
    evidence TEXT DEFAULT '[]',
    confidence REAL,
    resolution TEXT,
    reasoning TEXT,
    created_at REAL NOT NULL,
    FOREIGN KEY (project_id) REFERENCES innovation_projects(id)
);

CREATE TABLE IF NOT EXISTS innovation_scores (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    version_id TEXT NOT NULL,
    market_potential REAL DEFAULT 0,
    technical_feasibility REAL DEFAULT 0,
    business_viability REAL DEFAULT 0,
    innovation_differentiation REAL DEFAULT 0,
    patent_ip_position REAL DEFAULT 0,
    risk_score REAL DEFAULT 0,
    sustainability REAL DEFAULT 0,
    mvp_feasibility REAL DEFAULT 0,
    customer_value REAL DEFAULT 0,
    scalability REAL DEFAULT 0,
    overall_score REAL DEFAULT 0,
    weights TEXT DEFAULT '{}',
    explanation TEXT DEFAULT '',
    created_at REAL NOT NULL,
    FOREIGN KEY (project_id) REFERENCES innovation_projects(id)
);

CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    priority TEXT DEFAULT 'medium',
    status TEXT DEFAULT 'pending',
    owner TEXT,
    deadline TEXT,
    dependencies TEXT DEFAULT '[]',
    progress INTEGER DEFAULT 0,
    progress_detail TEXT,
    category TEXT DEFAULT 'general',
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL,
    completed_at REAL,
    FOREIGN KEY (project_id) REFERENCES innovation_projects(id)
);

CREATE TABLE IF NOT EXISTS communication_events (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    channel TEXT NOT NULL,
    direction TEXT DEFAULT 'outbound',
    sender TEXT,
    recipient TEXT,
    content TEXT NOT NULL,
    message_type TEXT DEFAULT 'notification',
    conversation_id TEXT,
    connection_id TEXT,
    created_at REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS approvals (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    action_description TEXT NOT NULL,
    action_type TEXT NOT NULL,
    level TEXT DEFAULT 'medium',
    status TEXT DEFAULT 'pending',
    requested_via TEXT DEFAULT 'telegram',
    approved_via TEXT,
    approved_by TEXT,
    created_at REAL NOT NULL,
    resolved_at REAL,
    expires_at REAL,
    FOREIGN KEY (project_id) REFERENCES innovation_projects(id)
);

CREATE TABLE IF NOT EXISTS follow_ups (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    channel TEXT DEFAULT 'telegram',
    conversation_id TEXT,
    reminder_count INTEGER DEFAULT 0,
    max_reminders INTEGER DEFAULT 3,
    reminder_interval_hours INTEGER DEFAULT 24,
    last_reminder_at REAL,
    next_reminder_at REAL,
    escalation_level INTEGER DEFAULT 0,
    opted_out INTEGER DEFAULT 0,
    created_at REAL NOT NULL,
    FOREIGN KEY (project_id) REFERENCES innovation_projects(id),
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);

CREATE TABLE IF NOT EXISTS decision_logs (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    decision TEXT NOT NULL,
    reasoning TEXT NOT NULL,
    decision_type TEXT DEFAULT 'general',
    confidence REAL,
    made_by TEXT DEFAULT 'innovation_director',
    created_at REAL NOT NULL,
    FOREIGN KEY (project_id) REFERENCES innovation_projects(id)
);

CREATE TABLE IF NOT EXISTS innovation_memory (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    memory_type TEXT DEFAULT 'lesson',
    content TEXT NOT NULL,
    tags TEXT DEFAULT '[]',
    related_project_ids TEXT DEFAULT '[]',
    created_at REAL NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_versions_project ON innovation_versions(project_id);
CREATE INDEX IF NOT EXISTS idx_analyses_project ON agent_analyses(project_id);
CREATE INDEX IF NOT EXISTS idx_analyses_version ON agent_analyses(version_id);
CREATE INDEX IF NOT EXISTS idx_tasks_project ON tasks(project_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_comms_project ON communication_events(project_id);
CREATE INDEX IF NOT EXISTS idx_approvals_status ON approvals(status);
CREATE INDEX IF NOT EXISTS idx_followups_next ON follow_ups(next_reminder_at);
CREATE INDEX IF NOT EXISTS idx_memory_type ON innovation_memory(memory_type);
"""
