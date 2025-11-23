"""
Piper Morgan 1.0 - Domain Models
The heart of the system - these models drive everything else.
Pure business logic with no persistence concerns.
"""

from __future__ import annotations

# 2025-06-14: Fixed Task type field and status enum to match database model and shared_types
# 2025-06-15: Added Project and ProjectIntegration models for PM-009
# 2025-06-17: Cleaned separation - removed SQLAlchemy code, fixed duplicate imports
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID, uuid4

# Import Item primitive for Todo to extend
from services.domain.primitives import Item

# Import shared types for consistency
from services.shared_types import (
    EdgeType,
    IntegrationType,
    IntentCategory,
    ListType,
    NodeType,
    OrderingStrategy,
    TaskStatus,
    TaskType,
    TodoPriority,
    TodoStatus,
    WorkflowStatus,
    WorkflowType,
)


# SEC-RBAC Phase 2: Role-Based Permissions
class ShareRole(str, Enum):
    """Role for shared resource access (SEC-RBAC Phase 2)"""

    VIEWER = "viewer"  # Read-only access
    EDITOR = "editor"  # Can modify content
    ADMIN = "admin"  # Can share with others and change roles


@dataclass
class SharePermission:
    """Permission entry for a shared resource (SEC-RBAC Phase 2)"""

    user_id: str
    role: ShareRole

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for JSONB serialization"""
        return {"user_id": self.user_id, "role": self.role.value}

    @staticmethod
    def from_dict(data: Dict[str, str]) -> SharePermission:
        """Create from dictionary (JSONB deserialization)"""
        return SharePermission(user_id=data["user_id"], role=ShareRole(data["role"]))


# Core Entities
@dataclass
class Product:
    """A product being managed"""

    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    vision: str = ""
    strategy: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # Relationships
    features: List["Feature"] = field(default_factory=list)
    stakeholders: List["Stakeholder"] = field(default_factory=list)
    metrics: List["Metric"] = field(default_factory=list)
    work_items: List["WorkItem"] = field(default_factory=list)


@dataclass
class Feature:
    """A feature or capability"""

    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    hypothesis: str = ""
    acceptance_criteria: List[str] = field(default_factory=list)
    status: str = "draft"
    product_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # Relationships
    dependencies: List["Feature"] = field(default_factory=list)
    risks: List["Risk"] = field(default_factory=list)
    work_items: List["WorkItem"] = field(default_factory=list)


@dataclass
class Stakeholder:
    """Someone with interest in the product"""

    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    email: Optional[str] = None
    role: str = ""
    interests: List[str] = field(default_factory=list)
    influence_level: int = 1  # 1-5 scale
    satisfaction: Optional[float] = None
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class WorkItem:
    """Universal work item - can be from any system"""

    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    description: str = ""
    type: str = "task"  # bug, feature, task, improvement
    status: str = "open"
    priority: str = "medium"  # low, medium, high, critical
    labels: List[str] = field(default_factory=list)
    assignee: Optional[str] = None
    project_id: Optional[str] = None
    source_system: str = ""
    external_id: str = ""
    external_url: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    updated_at: Optional[datetime] = None
    feature_id: Optional[str] = None
    external_refs: Optional[Dict[str, Any]] = None
    product_id: Optional[str] = None
    item_metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = field(default_factory=datetime.now)

    # Relationships
    feature: Optional["Feature"] = None
    product: Optional["Product"] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "type": self.type,
            "status": self.status,
            "priority": self.priority,
            "labels": self.labels,
            "assignee": self.assignee,
            "project_id": self.project_id,
            "source_system": self.source_system,
            "external_id": self.external_id,
            "external_url": self.external_url,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


# PM-009: Project Management Domain Models
@dataclass
class ProjectIntegration:
    """Integration configuration for a project"""

    type: IntegrationType  # Required field - no default
    id: str = field(default_factory=lambda: str(uuid4()))
    project_id: str = ""
    name: str = ""  # User-friendly name like "Main Repository", "Bug Tracker"
    config: Dict[str, Any] = field(default_factory=dict)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)

    # Relationships
    project: Optional["Project"] = None

    def validate_config(self) -> bool:
        """Validate configuration based on integration type"""
        if self.type == IntegrationType.GITHUB:
            return "repository" in self.config
        elif self.type == IntegrationType.JIRA:
            return all(k in self.config for k in ["url", "project_key"])
        elif self.type == IntegrationType.LINEAR:
            return all(k in self.config for k in ["api_key", "team_id"])
        elif self.type == IntegrationType.SLACK:
            return all(k in self.config for k in ["webhook_url", "channel"])
        return True


@dataclass
class Project:
    """A PM project with multiple tool integrations"""

    id: str = field(default_factory=lambda: str(uuid4()))
    owner_id: str = ""
    name: str = ""
    description: str = ""
    integrations: List[ProjectIntegration] = field(default_factory=list)
    shared_with: List[SharePermission] = field(default_factory=list)
    is_default: bool = False
    is_archived: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def get_integration(self, integration_type: IntegrationType) -> Optional[ProjectIntegration]:
        """Get first active integration of specified type"""
        for integration in self.integrations:
            if integration.type == integration_type and integration.is_active:
                return integration
        return None

    def get_github_repository(self) -> Optional[str]:
        """Get GitHub repository for this project"""
        github_integration = self.get_integration(IntegrationType.GITHUB)
        return github_integration.config.get("repository") if github_integration else None

    def validate_integrations(self) -> List[str]:
        """Validate all integrations, return list of errors"""
        errors = []
        for integration in self.integrations:
            if not integration.validate_config():
                errors.append(f"{integration.type.value}: Invalid configuration")
        return errors

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "name": self.name,
            "description": self.description,
            "integrations": [
                {
                    "id": integ.id,
                    "type": integ.type.value,
                    "name": integ.name,
                    "config": integ.config,
                    "is_active": integ.is_active,
                    "created_at": integ.created_at.isoformat(),
                }
                for integ in self.integrations
            ],
            "shared_with": [perm.to_dict() for perm in self.shared_with],
            "is_default": self.is_default,
            "is_archived": self.is_archived,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class ProjectContext:
    """Simplified project context for content generation"""

    name: str = ""
    description: str = ""
    technologies: List[str] = field(default_factory=list)


@dataclass
class Intent:
    """User intent parsed from natural language"""

    category: IntentCategory
    action: str
    id: str = field(default_factory=lambda: str(uuid4()))
    context: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    original_message: str = ""
    workflow_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

    # Relationships
    workflow: Optional["Workflow"] = None


@dataclass
class Task:
    """Individual task within a workflow"""

    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    type: TaskType = TaskType.ANALYZE_REQUEST
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    output_data: Optional[Dict[str, Any]] = None
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    workflow_id: Optional[str] = None
    input_data: Optional[Dict[str, Any]] = None
    created_at: datetime = field(default_factory=datetime.now)

    # Relationships
    workflow: Optional["Workflow"] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value if self.type else None,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class WorkflowResult:
    """Result of workflow execution"""

    success: bool = False
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Workflow:
    """Workflow definition and state"""

    type: WorkflowType
    id: str = field(default_factory=lambda: str(uuid4()))
    status: WorkflowStatus = WorkflowStatus.PENDING
    tasks: List[Task] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    result: Optional[WorkflowResult] = None
    error: Optional[str] = None
    intent_id: Optional[str] = None
    output_data: Optional[Dict[str, Any]] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    input_data: Optional[Dict[str, Any]] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # Relationships
    intent: Optional["Intent"] = None

    def get_next_task(self) -> Optional[Task]:
        """Get the next pending task in the workflow"""
        for task in self.tasks:
            if task.status == TaskStatus.PENDING:
                return task
        return None

    def mark_task_completed(self, task_id: str, result: Dict[str, Any]):
        """Mark a task as completed with result"""
        for task in self.tasks:
            if task.id == task_id:
                task.status = TaskStatus.COMPLETED
                task.result = result
                break

    def mark_task_failed(self, task_id: str, error: str):
        """Mark a task as failed with error"""
        for task in self.tasks:
            if task.id == task_id:
                task.status = TaskStatus.FAILED
                task.error = error
                break

    def is_complete(self) -> bool:
        """Check if all tasks are completed"""
        return all(task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED] for task in self.tasks)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "status": self.status.value,
            "tasks": [task.to_dict() for task in self.tasks],
            "context": self.context,
            "result": self.result.__dict__ if self.result else None,
            "error": self.error,
            "intent_id": self.intent_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Workflow":
        """Create Workflow from dictionary"""
        workflow = cls(
            id=data.get("id", str(uuid4())),
            type=WorkflowType(data["type"]),
            status=WorkflowStatus(data.get("status", "pending")),
            context=data.get("context", {}),
            error=data.get("error"),
            intent_id=data.get("intent_id"),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat())),
        )

        # Convert tasks
        for task_data in data.get("tasks", []):
            task = Task(
                id=task_data.get("id", str(uuid4())),
                name=task_data.get("name", ""),
                type=TaskType(task_data["type"]) if task_data.get("type") else None,
                status=TaskStatus(task_data.get("status", "pending")),
                result=task_data.get("result"),
                error=task_data.get("error"),
                created_at=datetime.fromisoformat(
                    task_data.get("created_at", datetime.now().isoformat())
                ),
            )
            workflow.tasks.append(task)

        # Convert result
        if data.get("result"):
            workflow.result = WorkflowResult(**data["result"])

        return workflow


# Events
@dataclass
class Event:
    """Base event class"""

    id: str = field(default_factory=lambda: str(uuid4()))
    type: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class FeatureCreated(Event):
    """Feature was created"""

    type: str = "feature.created"
    feature_id: str = ""
    created_by: str = ""
    source: str = ""


@dataclass
class InsightGenerated(Event):
    """AI generated an insight"""

    type: str = "insight.generated"
    insight: str = ""
    confidence: float = 0.0
    sources: List[str] = field(default_factory=list)


@dataclass
class UploadedFile:
    """Domain model for uploaded files"""

    id: str = field(default_factory=lambda: str(uuid4()))
    owner_id: str = ""
    filename: str = ""
    file_type: str = ""  # MIME type
    file_size: int = 0
    storage_path: str = ""  # Where file is stored
    upload_time: datetime = field(default_factory=datetime.now)
    last_referenced: Optional[datetime] = None
    reference_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    file_metadata: Dict[str, Any] = field(default_factory=dict)


class AnalysisType(Enum):
    DATA = "data"
    DOCUMENT = "document"
    TEXT = "text"
    UNKNOWN = "unknown"


@dataclass
class ValidationResult:
    """Result of file security validation"""

    is_valid: bool
    message: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FileTypeInfo:
    """File type detection results"""

    mime_type: str
    extension: str
    analyzer_type: str  # Will convert to AnalysisType enum later
    confidence: float = 0.0


@dataclass
class Document:
    """Core document entity for document memory system"""

    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    content: str = ""
    document_type: str = "general"  # general, decision, meeting_notes, analysis

    # Document classification
    tags: List[str] = field(default_factory=list)
    topics: List[str] = field(default_factory=list)
    decisions: List[str] = field(default_factory=list)

    # File information
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None

    # Processing metadata
    summary: str = ""
    key_findings: List[str] = field(default_factory=list)
    analysis_metadata: Dict[str, Any] = field(default_factory=dict)

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to serializable dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "document_type": self.document_type,
            "tags": self.tags,
            "topics": self.topics,
            "decisions": self.decisions,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "mime_type": self.mime_type,
            "summary": self.summary,
            "key_findings": self.key_findings,
            "analysis_metadata": self.analysis_metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Document":
        """Create from dictionary with type conversion"""
        # Convert ISO strings back to datetime objects
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        data["last_accessed"] = datetime.fromisoformat(data["last_accessed"])
        return cls(**data)


@dataclass
class DocumentSample:
    """Smart content sampling result"""

    content: str
    is_complete: bool
    sampling_method: str
    total_length: Optional[int] = None


@dataclass
class ContentSample:
    """Sample of file content for analysis"""

    text: str
    is_truncated: bool
    original_length: int
    sample_ranges: Optional[List[Tuple[int, int]]] = None


@dataclass
class AnalysisResult:
    """Results from file analysis"""

    file_id: str
    analysis_type: AnalysisType
    summary: str
    key_findings: List[str]
    metadata: Dict[str, Any]
    recommendations: List[str]
    generated_at: datetime
    filename: str = ""
    analysis_metadata: Dict[str, Any] = field(default_factory=dict)


# Document Summary Domain Models for JSON Mode
@dataclass
class SummarySection:
    """A section within a document summary"""

    heading: str
    points: List[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        """Generate clean markdown for this section"""
        if not self.points:
            return f"### {self.heading}\n\nNo items found.\n"

        markdown = f"### {self.heading}\n\n"
        for point in self.points:
            markdown += f"- {point}\n"
        markdown += "\n"
        return markdown


@dataclass
class DocumentSummary:
    """Structured document summary with clean markdown generation"""

    title: str
    document_type: str
    key_findings: List[str] = field(default_factory=list)
    sections: List[SummarySection] = field(default_factory=list)

    def to_markdown(self) -> str:
        """Generate clean, consistent markdown for the entire summary"""
        markdown = f"# {self.title}\n\n"
        markdown += f"**Document Type:** {self.document_type}\n\n"

        # Key findings section
        if self.key_findings:
            markdown += "## Key Findings\n\n"
            for finding in self.key_findings:
                markdown += f"- {finding}\n"
            markdown += "\n"

        # Additional sections
        for section in self.sections:
            markdown += section.to_markdown()

        return markdown

    def add_section(self, heading: str, points: List[str]) -> None:
        """Add a new section to the summary"""
        self.sections.append(SummarySection(heading=heading, points=points))

    def get_section(self, heading: str) -> Optional[SummarySection]:
        """Get a section by heading"""
        for section in self.sections:
            if section.heading == heading:
                return section
        return None


@dataclass
class ActionHumanization:
    """Cached human-readable version of technical action strings"""

    id: str = field(default_factory=lambda: str(uuid4()))
    action: str = ""  # e.g., "investigate_crash"
    category: Optional[str] = None  # e.g., "ANALYSIS"
    human_readable: str = ""  # e.g., "investigate a crash"
    created_at: datetime = field(default_factory=datetime.now)
    usage_count: int = 0
    last_used: Optional[datetime] = None


# Spatial Domain Models
# These models implement the spatial metaphor system using integer positions
# to maintain clean separation from external system identifiers


@dataclass
class SpatialEvent:
    """Spatial event within the spatial metaphor system"""

    id: str = field(default_factory=lambda: str(uuid4()))
    event_type: str = ""  # join, leave, message_posted, thread_started, etc.

    # Integer spatial positioning (pure domain)
    territory_position: int = 0
    room_position: int = 0
    path_position: Optional[int] = None
    object_position: Optional[int] = None

    # Event details
    actor_id: Optional[str] = None
    affected_objects: List[str] = field(default_factory=list)
    spatial_changes: Dict[str, Any] = field(default_factory=dict)

    # Context
    event_time: Optional[datetime] = None
    significance_level: str = "routine"  # routine, notable, significant, critical

    def get_spatial_coordinates(self) -> Dict[str, int]:
        """Get spatial coordinates as integer positions"""
        coords = {
            "territory_position": self.territory_position,
            "room_position": self.room_position,
        }
        if self.path_position is not None:
            coords["path_position"] = self.path_position
        if self.object_position is not None:
            coords["object_position"] = self.object_position
        return coords


@dataclass
class SpatialObject:
    """Object placed within spatial environment"""

    id: str = field(default_factory=lambda: str(uuid4()))
    object_type: str = "text_message"  # text_message, file_document, code_block, etc.

    # Integer spatial positioning (pure domain)
    territory_position: int = 0
    room_position: int = 0
    path_position: Optional[int] = None
    object_position: Optional[int] = None

    # Object properties
    content: str = ""
    creator_id: str = ""
    size_category: str = "standard"  # minimal, standard, substantial, extensive

    # Spatial relationships
    attention_attractors: List[str] = field(default_factory=list)
    emotional_markers: List[str] = field(default_factory=list)
    connected_objects: List[str] = field(default_factory=list)

    # Context
    placement_time: Optional[datetime] = None
    last_interaction: Optional[datetime] = None
    interaction_count: int = 0

    def get_spatial_context(self) -> Dict[str, Any]:
        """Get spatial context for object interaction"""
        return {
            "object_type": self.object_type,
            "size_category": self.size_category,
            "attention_level": len(self.attention_attractors),
            "emotional_resonance": len(self.emotional_markers),
            "connections": len(self.connected_objects),
            "interaction_history": self.interaction_count,
            "spatial_coordinates": self.get_spatial_coordinates(),
        }

    def get_spatial_coordinates(self) -> Dict[str, int]:
        """Get spatial coordinates as integer positions"""
        coords = {
            "territory_position": self.territory_position,
            "room_position": self.room_position,
        }
        if self.path_position is not None:
            coords["path_position"] = self.path_position
        if self.object_position is not None:
            coords["object_position"] = self.object_position
        return coords


@dataclass
class SpatialContext:
    """Spatial context information for positioning"""

    # Integer spatial positioning (pure domain)
    territory_position: int = 0
    room_position: int = 0
    path_position: Optional[int] = None
    object_position: Optional[int] = None

    # Spatial characteristics
    attention_level: str = "medium"  # low, medium, high, urgent
    emotional_valence: str = "neutral"  # positive, negative, neutral
    navigation_intent: str = "monitor"  # respond, investigate, monitor, explore

    # External system mapping (via adapter)
    external_system: str = ""
    external_id: str = ""
    external_context: Dict[str, Any] = field(default_factory=dict)

    def get_spatial_coordinates(self) -> Dict[str, int]:
        """Get spatial coordinates as integer positions"""
        coords = {
            "territory_position": self.territory_position,
            "room_position": self.room_position,
        }
        if self.path_position is not None:
            coords["path_position"] = self.path_position
        if self.object_position is not None:
            coords["object_position"] = self.object_position
        return coords


# PM-087 Ethics Domain Models
@dataclass
class EthicalDecision:
    """Domain model for ethics decisions"""

    decision_id: str = field(default_factory=lambda: str(uuid4()))
    boundary_type: str = ""
    violation_detected: bool = False
    explanation: str = ""
    audit_data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    session_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "decision_id": self.decision_id,
            "boundary_type": self.boundary_type,
            "violation_detected": self.violation_detected,
            "explanation": self.explanation,
            "audit_data": self.audit_data,
            "timestamp": self.timestamp.isoformat(),
            "session_id": self.session_id,
        }


@dataclass
class BoundaryViolation:
    """Domain model for boundary violations"""

    violation_id: str = field(default_factory=lambda: str(uuid4()))
    violation_type: str = ""
    context: str = ""
    session_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    severity: str = "medium"  # low, medium, high, critical
    audit_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KnowledgeNode:
    """Domain model for knowledge graph nodes"""

    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    node_type: NodeType = NodeType.CONCEPT
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    session_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "node_type": self.node_type.value if self.node_type else None,
            "description": self.description,
            "metadata": self.metadata,
            "properties": self.properties,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "session_id": self.session_id,
        }


@dataclass
class KnowledgeEdge:
    """Domain model for knowledge graph edges (Issue #278: CORE-KNOW-ENHANCE)"""

    id: str = field(default_factory=lambda: str(uuid4()))
    source_node_id: str = ""
    target_node_id: str = ""
    edge_type: EdgeType = EdgeType.REFERENCES
    weight: float = 1.0
    # Issue #278: Confidence weighting for relationship-based reasoning
    confidence: float = 1.0  # 0.0 to 1.0, strength of relationship
    usage_count: int = 0  # Reinforced with use
    metadata: Dict[str, Any] = field(default_factory=dict)
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_accessed: Optional[datetime] = None  # For confidence decay
    session_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "source_node_id": self.source_node_id,
            "target_node_id": self.target_node_id,
            "edge_type": self.edge_type.value if self.edge_type else None,
            "weight": self.weight,
            "confidence": self.confidence,
            "usage_count": self.usage_count,
            "metadata": self.metadata,
            "properties": self.properties,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat() if self.last_accessed else None,
            "session_id": self.session_id,
        }


# PM-081: Universal List Architecture
# Chief Architect's universal composition over specialization principle


@dataclass
class List:
    """Universal List model for ANY item type (todo, feature, bug, attendee)"""

    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    item_type: str = "todo"  # todo, feature, bug, attendee, etc.
    list_type: str = "personal"  # personal, shared, project
    ordering_strategy: str = "manual"  # manual, due_date, priority, created
    color: Optional[str] = None  # Hex color for UI theming
    emoji: Optional[str] = None  # Emoji for visual identification
    is_archived: bool = False
    is_default: bool = False  # Default list for new items of this type

    # Metadata for PM-040 Knowledge Graph integration
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)

    # Ownership and sharing (SEC-RBAC Phase 1.3 & 1.4 & 2)
    owner_id: Optional[str] = None
    shared_with: List[SharePermission] = field(default_factory=list)  # Array of {user_id, role}

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # Performance optimization - cached counts (SEC-RBAC Phase 1)
    item_count: int = 0  # Total items in list (cached for performance)
    completed_count: int = 0  # Completed items in list (cached for performance)

    def get_user_role(self, user_id: str) -> Optional[ShareRole]:
        """Get user's role for this list (returns owner for owner, or role from shared_with)"""
        if self.owner_id == user_id:
            return None  # Owner has all permissions (represented as None/owner)

        for perm in self.shared_with:
            if perm.user_id == user_id:
                return perm.role

        return None

    def user_can_read(self, user_id: str) -> bool:
        """Check if user can read this list (any role can read)"""
        return self.owner_id == user_id or self.get_user_role(user_id) is not None

    def user_can_write(self, user_id: str) -> bool:
        """Check if user can modify this list (editor or admin can write)"""
        if self.owner_id == user_id:
            return True
        role = self.get_user_role(user_id)
        return role in (ShareRole.EDITOR, ShareRole.ADMIN)

    def user_can_share(self, user_id: str) -> bool:
        """Check if user can share this list (only admin or owner)"""
        if self.owner_id == user_id:
            return True
        role = self.get_user_role(user_id)
        return role == ShareRole.ADMIN

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "item_type": self.item_type,
            "list_type": self.list_type,
            "ordering_strategy": self.ordering_strategy,
            "color": self.color,
            "emoji": self.emoji,
            "is_archived": self.is_archived,
            "is_default": self.is_default,
            "metadata": self.metadata,
            "tags": self.tags,
            "owner_id": self.owner_id,
            "shared_with": [perm.to_dict() for perm in self.shared_with],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "item_count": self.item_count,
            "completed_count": self.completed_count,
        }


@dataclass
class ListItem:
    """Universal ListItem relationship - polymorphic with item_type discriminator"""

    id: str = field(default_factory=lambda: str(uuid4()))
    list_id: str = ""
    item_id: str = ""
    item_type: str = "todo"  # todo, feature, bug, attendee, etc.
    position: int = 0  # Order within the list

    # Membership metadata
    added_at: datetime = field(default_factory=datetime.now)
    added_by: str = ""  # User who added item to this list

    # List-specific overrides (optional)
    list_priority: Optional[str] = None  # Override item's default priority
    list_due_date: Optional[datetime] = None  # Override item's default due date
    list_notes: str = ""  # List-specific notes

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "list_id": self.list_id,
            "item_id": self.item_id,
            "item_type": self.item_type,
            "position": self.position,
            "added_at": self.added_at.isoformat() if self.added_at else None,
            "added_by": self.added_by,
            "list_priority": self.list_priority,
            "list_due_date": self.list_due_date.isoformat() if self.list_due_date else None,
            "list_notes": self.list_notes,
        }


# PM-081: Refactored Todo to extend Item primitive (Phase 2)
@dataclass
class Todo(Item):
    """A todo is an Item that can be completed and has priority.

    Extends Item with todo-specific properties.
    Inherits from Item: id, text, position, list_id, created_at, updated_at

    Design Decision: Todo IS-A Item. This enables todos to use all
    generic Item operations (reordering, text updates) while adding
    todo-specific behavior (completion, priority).

    Examples:
        >>> todo = Todo(text="Review PR", priority="high")
        >>> assert isinstance(todo, Item)  # Todo IS-A Item
        >>> assert todo.text == "Review PR"
        >>> todo.complete()  # Todo-specific method
        >>> assert todo.completed is True
    """

    # Inherited from Item (do NOT redefine):
    # - id: str
    # - text: str (was 'title')
    # - position: int
    # - list_id: Optional[str]
    # - created_at: datetime
    # - updated_at: datetime

    # Todo-specific fields (matching TodoDB):
    # Core fields
    description: str = ""
    priority: str = "medium"  # low, medium, high, urgent
    status: str = "pending"  # pending, in_progress, completed, cancelled
    completed: bool = False

    # Hierarchical structure
    parent_id: Optional[str] = None

    # Scheduling
    due_date: Optional[datetime] = None
    reminder_date: Optional[datetime] = None
    scheduled_date: Optional[datetime] = None

    # Context and categorization
    tags: List[str] = field(default_factory=list)
    project_id: Optional[str] = None
    context: Optional[str] = None  # @home, @work, etc.

    # Progress tracking
    estimated_minutes: Optional[int] = None
    actual_minutes: Optional[int] = None
    completion_notes: str = ""

    # PM-040 Knowledge Graph integration
    metadata: Dict[str, Any] = field(default_factory=dict)
    knowledge_node_id: Optional[str] = None
    related_todos: List[str] = field(default_factory=list)

    # PM-034 Intent Classification integration
    creation_intent: Optional[str] = None
    intent_confidence: Optional[float] = None

    # External integrations
    external_refs: Dict[str, Any] = field(default_factory=dict)

    # Timestamps
    completed_at: Optional[datetime] = None

    # Ownership and sharing (SEC-RBAC Phase 1.3 & 1.4 & 2)
    owner_id: Optional[str] = None
    shared_with: List[SharePermission] = field(default_factory=list)  # Array of {user_id, role}
    assigned_to: Optional[str] = None

    def get_user_role(self, user_id: str) -> Optional[ShareRole]:
        """Get user's role for this todo (returns owner for owner, or role from shared_with)"""
        if self.owner_id == user_id:
            return None  # Owner has all permissions (represented as None/owner)

        for perm in self.shared_with:
            if perm.user_id == user_id:
                return perm.role

        return None

    def user_can_read(self, user_id: str) -> bool:
        """Check if user can read this todo (any role can read)"""
        return self.owner_id == user_id or self.get_user_role(user_id) is not None

    def user_can_write(self, user_id: str) -> bool:
        """Check if user can modify this todo (editor or admin can write)"""
        if self.owner_id == user_id:
            return True
        role = self.get_user_role(user_id)
        return role in (ShareRole.EDITOR, ShareRole.ADMIN)

    def user_can_share(self, user_id: str) -> bool:
        """Check if user can share this todo (only admin or owner)"""
        if self.owner_id == user_id:
            return True
        role = self.get_user_role(user_id)
        return role == ShareRole.ADMIN

    @property
    def title(self) -> str:
        """Backward compatibility: title maps to text.

        DEPRECATED: Use .text instead.
        This property exists for backward compatibility during migration.
        """
        return self.text

    @title.setter
    def title(self, value: str):
        """Backward compatibility: setting title sets text."""
        self.text = value

    def complete(self):
        """Mark todo as complete."""
        self.completed = True
        self.completed_at = datetime.now()
        self.status = "completed"
        self.updated_at = datetime.now()

    def reopen(self):
        """Reopen completed todo."""
        self.completed = False
        self.completed_at = None
        self.status = "pending"
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            # Inherited from Item
            "id": self.id,
            "text": self.text,
            "title": self.title,  # Backward compatibility
            "position": self.position,
            "list_id": self.list_id,
            # Core Todo fields
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "completed": self.completed,
            # Hierarchical structure
            "parent_id": self.parent_id,
            # Scheduling
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "reminder_date": self.reminder_date.isoformat() if self.reminder_date else None,
            "scheduled_date": self.scheduled_date.isoformat() if self.scheduled_date else None,
            # Context and categorization
            "tags": self.tags,
            "project_id": self.project_id,
            "context": self.context,
            # Progress tracking
            "estimated_minutes": self.estimated_minutes,
            "actual_minutes": self.actual_minutes,
            "completion_notes": self.completion_notes,
            # Knowledge Graph integration
            "metadata": self.metadata,
            "knowledge_node_id": self.knowledge_node_id,
            "related_todos": self.related_todos,
            # Intent Classification integration
            "creation_intent": self.creation_intent,
            "intent_confidence": self.intent_confidence,
            # External integrations
            "external_refs": self.external_refs,
            # Timestamps
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            # Ownership and sharing
            "owner_id": self.owner_id,
            "shared_with": [perm.to_dict() for perm in self.shared_with],
            "assigned_to": self.assigned_to,
        }


# PM-081: Backward compatibility - TodoList as alias for List(item_type='todo')
@dataclass
class TodoList:
    """Backward compatibility alias for List(item_type='todo')"""

    def __init__(self, **kwargs):
        # Convert TodoList to universal List with item_type='todo'
        list_data = {**kwargs, "item_type": "todo"}
        self._list = List(**list_data)

    def __getattr__(self, name):
        """Delegate to underlying List object"""
        return getattr(self._list, name)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return self._list.to_dict()


# PM-081: Backward compatibility - ListMembership as alias for ListItem(item_type='todo')
@dataclass
class ListMembership:
    """Backward compatibility alias for ListItem(item_type='todo')"""

    def __init__(self, **kwargs):
        # Convert ListMembership to universal ListItem with item_type='todo'
        item_data = {**kwargs, "item_type": "todo"}
        self._list_item = ListItem(**item_data)

    def __getattr__(self, name):
        """Delegate to underlying ListItem object"""
        return getattr(self._list_item, name)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return self._list_item.to_dict()


# PM-034 Phase 1: Conversation Foundation Domain Models
@dataclass
class Conversation:
    """Domain model for conversational interactions"""

    id: str = field(default_factory=lambda: str(uuid4()))
    user_id: UUID = ""
    session_id: str = ""
    title: str = ""  # Optional conversation title/summary
    context: Dict[str, Any] = field(default_factory=dict)  # Conversation context
    is_active: bool = True

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_activity_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "title": self.title,
            "context": self.context,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_activity_at": (
                self.last_activity_at.isoformat() if self.last_activity_at else None
            ),
        }


@dataclass
class ConversationTurn:
    """Domain model for individual turns in a conversation"""

    id: str = field(default_factory=lambda: str(uuid4()))
    conversation_id: str = ""
    turn_number: int = 0  # Sequential turn number within conversation

    # Turn content
    user_message: str = ""
    assistant_response: str = ""
    intent: Optional[str] = None  # Classified intent for this turn

    # Context and entities
    entities: List[str] = field(default_factory=list)  # Extracted entities
    references: Dict[str, str] = field(default_factory=dict)  # Anaphoric references
    context_used: Dict[str, Any] = field(default_factory=dict)  # Context used in response

    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    processing_time: Optional[float] = None  # Response processing time in ms

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "turn_number": self.turn_number,
            "user_message": self.user_message,
            "assistant_response": self.assistant_response,
            "intent": self.intent,
            "entities": self.entities,
            "references": self.references,
            "context_used": self.context_used,
            "metadata": self.metadata,
            "processing_time": self.processing_time,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
