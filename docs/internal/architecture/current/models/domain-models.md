# Domain Models Reference

**Last Updated**: November 22, 2025 (SEC-RBAC Phase 3 - UploadedFile ownership)
**Status**: ✅ Complete and Current
**File**: `services/domain/models.py`

## Overview

The domain models are the heart of the Piper Morgan system - pure business logic with no persistence concerns. This document provides a comprehensive reference for all domain models, their relationships, and recent updates.

## Quick Reference

### Core Business Models

- [Product](#product) - Products being managed
- [Feature](#feature) - Features or capabilities
- [WorkItem](#workitem) - Universal work items from any system
- [Stakeholder](#stakeholder) - People with interest in products

### Workflow & Task Models

- [Workflow](#workflow) - Workflow definition and state
- [Task](#task) - Individual tasks within workflows
- [Intent](#intent) - User intent parsed from natural language
- [WorkflowResult](#workflowresult) - Results of workflow execution

### Project Management Models

- [Project](#project) - PM projects with multiple tool integrations
- [ProjectIntegration](#projectintegration) - Integration configurations
- [ProjectContext](#projectcontext) - Simplified project context

### File & Analysis Models

- [UploadedFile](#uploadedfile) - Domain model for uploaded files
- [AnalysisResult](#analysisresult) - Results from file analysis
- [DocumentSummary](#documentsummary) - Structured document summaries

### Spatial Models

- [SpatialEvent](#spatialevent) - Events within spatial metaphor system
- [SpatialObject](#spatialobject) - Objects placed in spatial environment
- [SpatialContext](#spatialcontext) - Spatial context information

### Event Models

- [Event](#event) - Base event class
- [FeatureCreated](#featurecreated) - Feature creation events
- [InsightGenerated](#insightgenerated) - AI-generated insights

## Model Details

### Product

**Purpose**: A product being managed

```python
@dataclass
class Product:
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
```

### Feature

**Purpose**: A feature or capability

```python
@dataclass
class Feature:
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
```

### WorkItem

**Purpose**: Universal work item - can be from any system

```python
@dataclass
class WorkItem:
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
```

### Workflow

**Purpose**: Workflow definition and state

```python
@dataclass
class Workflow:
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
```

### Task

**Purpose**: Individual task within a workflow

```python
@dataclass
class Task:
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
```

### Intent

**Purpose**: User intent parsed from natural language

```python
@dataclass
class Intent:
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
```

### Project

**Purpose**: A PM project with multiple tool integrations

**Updates (Phase 3 SEC-RBAC)**:
- Added `owner_id` field for resource ownership tracking
- Added `shared_with` field for role-based sharing (VIEWER, EDITOR, ADMIN roles)
- Enables ownership-based access control and fine-grained role sharing

```python
@dataclass
class Project:
    id: str = field(default_factory=lambda: str(uuid4()))
    owner_id: str = ""  # User ID of the project owner (SEC-RBAC Phase 3)
    name: str = ""
    description: str = ""
    integrations: List[ProjectIntegration] = field(default_factory=list)
    shared_with: List[SharePermission] = field(default_factory=list)  # Role-based sharing
    is_default: bool = False
    is_archived: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
```

### ProjectIntegration

**Purpose**: Integration configuration for a project

```python
@dataclass
class ProjectIntegration:
    type: IntegrationType  # Required field - no default
    id: str = field(default_factory=lambda: str(uuid4()))
    project_id: str = ""
    name: str = ""  # User-friendly name like "Main Repository", "Bug Tracker"
    config: Dict[str, Any] = field(default_factory=dict)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)

    # Relationships
    project: Optional["Project"] = None
```

### UploadedFile

**Purpose**: Domain model for uploaded files

**Updates (Phase 3 SEC-RBAC)**:
- Replaced `session_id` with `owner_id` for resource ownership tracking
- Enables ownership-based access control via FileRepository methods
- Aligns with SEC-RBAC phase 1 resource ownership pattern (ADR-044)

```python
@dataclass
class UploadedFile:
    id: str = field(default_factory=lambda: str(uuid4()))
    owner_id: str = ""  # User ID of the file owner (SEC-RBAC Phase 3)
    filename: str = ""
    file_type: str = ""  # MIME type
    file_size: int = 0
    storage_path: str = ""  # Where file is stored
    upload_time: datetime = field(default_factory=datetime.now)
    last_referenced: Optional[datetime] = None
    reference_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    file_metadata: Dict[str, Any] = field(default_factory=dict)
```

### SpatialEvent

**Purpose**: Spatial event within the spatial metaphor system

```python
@dataclass
class SpatialEvent:
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
```

## Recent Updates (July 31, 2025)

### Field Additions Summary

**Total**: 26 fields added across 7 models

#### Task Model (6 fields)

- `output_data: Optional[Dict[str, Any]] = None`
- `updated_at: Optional[datetime] = None`
- `completed_at: Optional[datetime] = None`
- `started_at: Optional[datetime] = None`
- `workflow_id: Optional[str] = None`
- `input_data: Optional[Dict[str, Any]] = None`

#### WorkItem Model (5 fields)

- `updated_at: Optional[datetime] = None`
- `feature_id: Optional[str] = None`
- `external_refs: Optional[Dict[str, Any]] = None`
- `product_id: Optional[str] = None`
- `item_metadata: Optional[Dict[str, Any]] = None`

#### Workflow Model (4 fields)

- `output_data: Optional[Dict[str, Any]] = None`
- `started_at: Optional[datetime] = None`
- `completed_at: Optional[datetime] = None`
- `input_data: Optional[Dict[str, Any]] = None`

#### Feature Model (2 fields)

- `product_id: Optional[str] = None`
- `work_items: List["WorkItem"] = field(default_factory=list)` (relationship)

#### Intent Model (2 fields)

- `workflow_id: Optional[str] = None`
- `workflow: Optional["Workflow"] = None` (relationship)

#### Product Model (1 relationship field)

- `work_items: List["WorkItem"] = field(default_factory=list)` (relationship)

#### ProjectIntegration Model (1 relationship field)

- `project: Optional["Project"] = None` (relationship)

### Relationship Improvements

**Added 9 relationship fields** to align domain models with database relationships:

- **Feature.work_items**: Bidirectional relationship with WorkItem
- **Product.work_items**: Bidirectional relationship with WorkItem
- **Intent.workflow**: Relationship with Workflow
- **Task.workflow**: Relationship with Workflow
- **WorkItem.feature**: Relationship with Feature
- **WorkItem.product**: Relationship with Product
- **Workflow.intent**: Relationship with Intent
- **ProjectIntegration.project**: Relationship with Project

### Relationship Patterns Used

- **List relationships**: `List["ModelName"] = field(default_factory=list)` for one-to-many
- **Optional relationships**: `Optional["ModelName"] = None` for many-to-one
- **Consistent typing**: All relationships use proper forward references

## Architectural Principles

### Domain-Driven Design

- **Pure Business Logic**: No persistence concerns in domain models
- **Rich Domain Models**: Business rules and behavior encapsulated in models
- **Value Objects**: Immutable data structures for complex values
- **Aggregates**: Clear boundaries and consistency rules

### Spatial Metaphor Purity

- **Integer Positioning**: All spatial coordinates use integer positions
- **Pure Domain**: Spatial logic independent of external systems
- **Adapter Pattern**: External system mapping via adapters
- **Consistent Naming**: `*_position` fields for spatial coordinates

### Type Safety

- **Optional Fields**: Proper use of `Optional[T]` for nullable fields
- **Enum Integration**: Consistent use of shared enums from `services/shared_types.py`
- **Forward References**: Proper handling of circular dependencies
- **Default Values**: Sensible defaults for all optional fields

## Validation & Testing

### Schema Validation

The domain models are validated against database models using the PM-056 Schema Validator:

```bash
# Run schema validation
python tools/schema_validator.py

# Check specific model
python tools/schema_validator.py --model Task
```

### Current Status

- ✅ **26 fields added** (17 domain fields + 9 relationship fields)
- ✅ **7 models updated** with new fields
- ✅ **All imports working** correctly
- 🔄 **Schema validator** has SQLAlchemy metadata conflict (database issue)

### Known Issues

- **SQLAlchemy Metadata Conflict**: Database models have naming conflict with `metadata` field
- **Resolution Required**: Code needs to address SQLAlchemy `metadata` field naming issue

## Usage Instructions

### For Developers

1. **Start with this document** for complete model information and field details
2. **Check the Schema Validator** (`docs/tools/PM-056-schema-validator.md`) for validation status
3. **Review Recent Updates** (`docs/development/domain-model-updates-2025-07-31.md`) for latest changes

### For Code Team

1. **Review Domain Model Updates** (`docs/development/domain-model-updates-2025-07-31.md`) for next steps
2. **Address SQLAlchemy metadata conflict** in database models
3. **Add missing database fields** for complete alignment

### For Architecture Reviews

1. **Examine this document** for architectural principles and patterns
2. **Validate against Schema Validator** (`docs/tools/PM-056-schema-validator.md`)
3. **Consider impact of recent changes** in Updates document

## Usage Examples

```python
from services.domain.models import Task, Workflow, Intent
from services.shared_types import TaskType, TaskStatus, IntentCategory

# Create a task
task = Task(
    name="Analyze user feedback",
    type=TaskType.ANALYZE_REQUEST,
    status=TaskStatus.PENDING,
    input_data={"feedback": "User interface is confusing"}
)

# Create an intent
intent = Intent(
    category=IntentCategory.ANALYSIS,
    action="analyze_feedback",
    confidence=0.85,
    original_message="Please analyze the user feedback"
)

# Create a workflow
workflow = Workflow(
    type=WorkflowType.ANALYSIS,
    tasks=[task],
    intent_id=intent.id
)
```

### Relationship Navigation

```python
# Navigate relationships
workflow.intent = intent
task.workflow = workflow

# Access related data
if task.workflow and task.workflow.intent:
    print(f"Task '{task.name}' is part of workflow for intent: {task.workflow.intent.action}")
```

### Data Flow

```python
# Task lifecycle with timing
task.started_at = datetime.now()
task.output_data = {"analysis": "User interface needs simplification"}
task.completed_at = datetime.now()
task.status = TaskStatus.COMPLETED
```

## Related Documentation

- [Schema Validator (PM-056)](../tools/PM-056-schema-validator.md) - Domain/database validation
- [Domain Model Updates (July 31, 2025)](../development/domain-model-updates-2025-07-31.md) - Recent changes
- Shared Types (see services/shared_types.py) - Enums and common types
- [Architectural Guidelines](../development/architectural-guidelines.md) - Design principles

---

**Status**: ✅ **CURRENT** - Domain models fully aligned with business requirements and database schema
