"""
Piper Morgan 1.0 - Domain Models
The heart of the system - these models drive everything else.
Pure business logic with no persistence concerns.
"""
# 2025-06-14: Fixed Task type field and status enum to match database model and shared_types
# 2025-06-15: Added Project and ProjectIntegration models for PM-009
# 2025-06-17: Cleaned separation - removed SQLAlchemy code, fixed duplicate imports
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
from uuid import uuid4
from enum import Enum

# Import shared types for consistency
from services.shared_types import (
    TaskType, TaskStatus, IntentCategory, WorkflowType, WorkflowStatus, IntegrationType
)

# Core Entities
@dataclass
class Product:
    """A product being managed"""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    vision: str = ""
    strategy: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    
    # Relationships
    features: List['Feature'] = field(default_factory=list)
    stakeholders: List['Stakeholder'] = field(default_factory=list)
    metrics: List['Metric'] = field(default_factory=list)

@dataclass
class Feature:
    """A feature or capability"""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    hypothesis: str = ""
    acceptance_criteria: List[str] = field(default_factory=list)
    status: str = "draft"
    created_at: datetime = field(default_factory=datetime.now)
    
    # Relationships
    dependencies: List['Feature'] = field(default_factory=list)
    risks: List['Risk'] = field(default_factory=list)

@dataclass
class Stakeholder:
    """Someone with interest in the product"""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    role: str = ""
    interests: List[str] = field(default_factory=list)
    influence_level: int = 1  # 1-5 scale
    satisfaction: Optional[float] = None

@dataclass
class WorkItem:
    """Universal work item - can be from any system"""
    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    description: str = ""
    status: str = "open"
    source_system: str = ""
    external_id: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

# PM-009: Project Management Domain Models
@dataclass
class ProjectIntegration:
    """Integration configuration for a project"""
    type: IntegrationType  # Required field - no default
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""  # User-friendly name like "Main Repository", "Bug Tracker"
    config: Dict[str, Any] = field(default_factory=dict)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    
    def validate_config(self) -> bool:
        """Validate configuration based on integration type"""
        if self.type == IntegrationType.GITHUB:
            return 'repository' in self.config
        elif self.type == IntegrationType.JIRA:
            return all(k in self.config for k in ['url', 'project_key'])
        elif self.type == IntegrationType.LINEAR:
            return all(k in self.config for k in ['api_key', 'team_id'])
        elif self.type == IntegrationType.SLACK:
            return all(k in self.config for k in ['webhook_url', 'channel'])
        return True

@dataclass
class Project:
    """A PM project with multiple tool integrations"""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    integrations: List[ProjectIntegration] = field(default_factory=list)
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
        return github_integration.config.get('repository') if github_integration else None
    
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
            "name": self.name,
            "description": self.description,
            "integrations": [
                {
                    "id": integ.id,
                    "type": integ.type.value,
                    "name": integ.name,
                    "config": integ.config,
                    "is_active": integ.is_active,
                    "created_at": integ.created_at.isoformat()
                }
                for integ in self.integrations
            ],
            "is_default": self.is_default,
            "is_archived": self.is_archived,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

@dataclass  
class Intent:
    """User intent parsed from natural language"""
    category: IntentCategory
    action: str
    id: str = field(default_factory=lambda: str(uuid4()))
    context: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Task:
    """Individual task within a workflow"""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    type: Optional[TaskType] = None
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value if self.type else None,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at.isoformat()
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
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
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
        return all(task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED] 
                   for task in self.tasks)
    
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
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Workflow':
        """Create Workflow from dictionary"""
        workflow = cls(
            id=data.get("id", str(uuid4())),
            type=WorkflowType(data["type"]),
            status=WorkflowStatus(data.get("status", "pending")),
            context=data.get("context", {}),
            error=data.get("error"),
            intent_id=data.get("intent_id"),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat()))
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
                created_at=datetime.fromisoformat(task_data.get("created_at", datetime.now().isoformat()))
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
    session_id: str = ""
    filename: str = ""
    file_type: str = ""  # MIME type
    file_size: int = 0
    storage_path: str = ""  # Where file is stored
    upload_time: datetime = field(default_factory=datetime.now)
    last_referenced: Optional[datetime] = None
    reference_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

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