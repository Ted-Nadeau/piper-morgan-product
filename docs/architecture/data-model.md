# Piper Morgan 1.0 - Data Model Document

## Overview

This document describes the complete data model for Piper Morgan, including domain models, database schema, and the mapping between them. The system follows a domain-first approach where business logic drives technical implementation.

## Domain Models

### Core Entities

#### Product

Represents a product or project being managed.

```python
@dataclass
class Product:
    """A product being managed"""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    vision: str = ""
    strategy: str = ""
    is_default: bool = False
    is_archived: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    # Relationships
    features: List['Feature'] = field(default_factory=list)
    stakeholders: List['Stakeholder'] = field(default_factory=list)
    metrics: List['Metric'] = field(default_factory=list)
    integrations: List['ProjectIntegration'] = field(default_factory=list)
```

#### Project (extends Product)

Alias for Product with additional project-specific methods.

```python
@dataclass
class Project(Product):
    """Project is a Product with additional context"""

    def get_integration(self, integration_type: IntegrationType) -> Optional[ProjectIntegration]:
        """Get integration configuration by type"""
        for integration in self.integrations:
            if integration.type == integration_type:
                return integration
        return None

    def get_github_repository(self) -> Optional[str]:
        """Convenience method to get GitHub repository"""
        github = self.get_integration(IntegrationType.GITHUB)
        return github.config.get("repository") if github else None
```

#### ProjectIntegration

Configuration for external system integrations.

```python
@dataclass
class ProjectIntegration:
    """External system integration configuration"""
    id: str = field(default_factory=lambda: str(uuid4()))
    type: IntegrationType
    name: str = ""
    config: Dict[str, Any] = field(default_factory=dict)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)

    def validate_config(self) -> bool:
        """Validate integration config. Example: GitHub requires 'repository' key."""
        if self.type == IntegrationType.GITHUB:
            return "repository" in self.config and isinstance(self.config["repository"], str)
        # Add validation for other types as needed
        return True
```

#### Feature

A feature or capability within a product.

```python
@dataclass
class Feature:
    """A feature or capability"""
    id: str = field(default_factory=lambda: str(uuid4()))
    product_id: Optional[str] = None
    name: str = ""
    description: str = ""
    hypothesis: str = ""
    acceptance_criteria: List[str] = field(default_factory=list)
    status: str = "draft"
    priority: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    # Relationships
    dependencies: List['Feature'] = field(default_factory=list)
    risks: List['Risk'] = field(default_factory=list)
    work_items: List['WorkItem'] = field(default_factory=list)
```

#### Stakeholder

Someone with interest in the product.

```python
@dataclass
class Stakeholder:
    """Someone with interest in the product"""
    id: str = field(default_factory=lambda: str(uuid4()))
    product_id: Optional[str] = None
    name: str = ""
    role: str = ""
    email: Optional[str] = None
    interests: List[str] = field(default_factory=list)
    influence_level: int = 1  # 1-5 scale
    satisfaction: Optional[float] = None
    created_at: datetime = field(default_factory=datetime.now)
```

#### WorkItem

Universal work item that can map to any external system.

```python
@dataclass
class WorkItem:
    """Universal work item - can be from any system"""
    id: str = field(default_factory=lambda: str(uuid4()))
    feature_id: Optional[str] = None
    title: str = ""
    description: str = ""
    status: str = "open"
    source_system: str = ""  # github, jira, etc.
    external_id: str = ""    # ID in external system
    external_refs: Dict[str, str] = field(default_factory=dict)  # Multiple system refs
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
```

### Intent System

#### Intent

User intent parsed from natural language.

```python
@dataclass
class Intent:
    """User intent parsed from natural language"""
    id: str = field(default_factory=lambda: str(uuid4()))
    category: IntentCategory
    action: str
    context: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    knowledge_context: List[str] = field(default_factory=list)
    original_message: str = ""
    created_at: datetime = field(default_factory=datetime.now)
```

### Workflow System

#### Workflow

Orchestrates multi-step processes.

```python
@dataclass
class Workflow:
    """Workflow orchestration"""
    id: str = field(default_factory=lambda: str(uuid4()))
    type: WorkflowType
    status: WorkflowStatus = WorkflowStatus.PENDING
    intent_id: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    tasks: List['Task'] = field(default_factory=list)
    result: Optional['WorkflowResult'] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def get_next_task(self) -> Optional['Task']:
        """Get next pending task"""
        for task in self.tasks:
            if task.status == TaskStatus.PENDING:
                return task
        return None
```

#### Task

Individual unit of work within a workflow.

```python
@dataclass
class Task:
    """Task within a workflow"""
    id: str = field(default_factory=lambda: str(uuid4()))
    workflow_id: Optional[str] = None
    type: TaskType
    status: TaskStatus = TaskStatus.PENDING
    input_data: Dict[str, Any] = field(default_factory=dict)
    output_data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
```

### Event System

#### Event

Base event for system activity tracking.

```python
@dataclass
class Event:
    """Base event class"""
    id: str = field(default_factory=lambda: str(uuid4()))
    type: str = ""
    aggregate_id: Optional[str] = None
    aggregate_type: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
```

## Database Schema

### SQLAlchemy Models

#### Base Model

```python
class Base(DeclarativeBase):
    """Base class for all database models"""
    pass

class TimestampMixin:
    """Mixin for created/updated timestamps"""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
```

#### Product Table

```python
class ProductDB(Base, TimestampMixin):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    vision = Column(Text)
    strategy = Column(Text)
    is_default = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)

    # Relationships
    features = relationship("FeatureDB", back_populates="product", cascade="all, delete-orphan")
    stakeholders = relationship("StakeholderDB", back_populates="product", cascade="all, delete-orphan")
    integrations = relationship("ProjectIntegrationDB", back_populates="project", cascade="all, delete-orphan")
```

#### ProjectIntegration Table

```python
class ProjectIntegrationDB(Base, TimestampMixin):
    __tablename__ = "project_integrations"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    project_id = Column(String, ForeignKey("products.id", ondelete="CASCADE"))
    type = Column(Enum(IntegrationType), nullable=False)
    name = Column(String(255), nullable=False)
    config = Column(JSON, default=dict)
    is_active = Column(Boolean, default=True)

    # Relationships
    project = relationship("ProductDB", back_populates="integrations")
```

#### Feature Table

```python
class FeatureDB(Base, TimestampMixin):
    __tablename__ = "features"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    product_id = Column(String, ForeignKey("products.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    hypothesis = Column(Text)
    acceptance_criteria = Column(JSON, default=list)
    status = Column(String(50), default="draft")
    priority = Column(Integer, default=0)

    # Relationships
    product = relationship("ProductDB", back_populates="features")
    work_items = relationship("WorkItemDB", back_populates="feature", cascade="all, delete-orphan")
```

#### WorkItem Table

```python
class WorkItemDB(Base, TimestampMixin):
    __tablename__ = "work_items"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    feature_id = Column(String, ForeignKey("features.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="open")
    source_system = Column(String(50))  # github, jira, etc.
    external_id = Column(String(255))    # ID in source system
    external_refs = Column(JSON, default=dict)  # {"github": "123", "jira": "PROJ-456"}
    metadata = Column(JSON, default=dict)

    # Relationships
    feature = relationship("FeatureDB", back_populates="work_items")

    # Indexes
    __table_args__ = (
        Index('idx_work_items_external', 'source_system', 'external_id'),
    )
```

#### Intent Table

```python
class IntentDB(Base):
    __tablename__ = "intents"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    category = Column(Enum(IntentCategory), nullable=False)
    action = Column(String(255), nullable=False)
    context = Column(JSON, default=dict)
    confidence = Column(Float, default=0.0)
    knowledge_context = Column(JSON, default=list)
    original_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    workflows = relationship("WorkflowDB", back_populates="intent")
```

#### Workflow Table

```python
class WorkflowDB(Base):
    __tablename__ = "workflows"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    type = Column(Enum(WorkflowType), nullable=False)
    status = Column(Enum(WorkflowStatus), default=WorkflowStatus.PENDING)
    intent_id = Column(String, ForeignKey("intents.id", ondelete="CASCADE"), nullable=True)
    context = Column(JSON, default=dict)
    result = Column(JSON)
    error = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime)

    # Relationships
    intent = relationship("IntentDB", back_populates="workflows")
    tasks = relationship("TaskDB", back_populates="workflow", cascade="all, delete-orphan")
```

#### Task Table

```python
class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    workflow_id = Column(String, ForeignKey("workflows.id", ondelete="CASCADE"))
    type = Column(Enum(TaskType), nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    input_data = Column(JSON, default=dict)
    output_data = Column(JSON, default=dict)
    error = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

    # Relationships
    workflow = relationship("WorkflowDB", back_populates="tasks")
```

#### Event Table

```python
class EventDB(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    type = Column(String(100), nullable=False)
    aggregate_id = Column(String)
    aggregate_type = Column(String(50))
    data = Column(JSON, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Indexes
    __table_args__ = (
        Index('idx_events_aggregate', 'aggregate_type', 'aggregate_id'),
        Index('idx_events_timestamp', 'timestamp'),
    )
```

## Enumerations

### IntentCategory

```python
class IntentCategory(Enum):
    EXECUTION = "execution"    # Create, update, status changes
    ANALYSIS = "analysis"      # Trends, risks, opportunities
    SYNTHESIS = "synthesis"    # Generate docs, summarize
    STRATEGY = "strategy"      # Prioritize, plan, recommend
    LEARNING = "learning"      # What worked, patterns
    QUERY = "query"           # Read-only data retrieval
```

### WorkflowType

```python
class WorkflowType(Enum):
    CREATE_FEATURE = "create_feature"
    ANALYZE_METRICS = "analyze_metrics"
    CREATE_TICKET = "create_ticket"
    CREATE_TASK = "create_task"
    REVIEW_ITEM = "review_item"
    GENERATE_REPORT = "generate_report"
    PLAN_STRATEGY = "plan_strategy"
    LEARN_PATTERN = "learn_pattern"
```

### IntegrationType

```python
class IntegrationType(Enum):
    GITHUB = "github"
    JIRA = "jira"
    SLACK = "slack"
    LINEAR = "linear"
    ASANA = "asana"
```

### WorkflowStatus

```python
class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
```

### TaskType

```python
class TaskType(Enum):
    # Analysis tasks
    ANALYZE_REQUEST = "analyze_request"
    EXTRACT_REQUIREMENTS = "extract_requirements"
    IDENTIFY_DEPENDENCIES = "identify_dependencies"

    # Execution tasks
    CREATE_WORK_ITEM = "create_work_item"
    UPDATE_WORK_ITEM = "update_work_item"
    NOTIFY_STAKEHOLDERS = "notify_stakeholders"

    # Integration tasks
    GITHUB_CREATE_ISSUE = "github_create_issue"
    ANALYZE_GITHUB_ISSUE = "analyze_github_issue"
    JIRA_CREATE_TICKET = "jira_create_ticket"
    SLACK_SEND_MESSAGE = "slack_send_message"
```

### TaskStatus

```python
class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
```

## Repository Pattern

### Base Repository

```python
class BaseRepository:
    """Base repository with common CRUD operations"""

    def __init__(self, db_session: AsyncSession, model_class: Type[Base]):
        self.db = db_session
        self.model_class = model_class

    async def create(self, **kwargs) -> Any:
        instance = self.model_class(**kwargs)
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def get_by_id(self, id: str) -> Optional[Any]:
        return await self.db.get(self.model_class, id)

    async def update(self, id: str, **kwargs) -> Optional[Any]:
        instance = await self.get_by_id(id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            await self.db.commit()
            await self.db.refresh(instance)
        return instance

    async def delete(self, id: str) -> bool:
        instance = await self.get_by_id(id)
        if instance:
            await self.db.delete(instance)
            await self.db.commit()
            return True
        return False
```

### Domain-Specific Repositories

#### ProjectRepository

```python
class ProjectRepository(BaseRepository):
    """Repository for Project/Product operations"""

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, ProductDB)

    async def list_active_projects(self) -> List[Project]:
        result = await self.db.execute(
            select(ProductDB).where(ProductDB.is_archived == False)
        )
        db_projects = result.scalars().all()
        return [self._to_domain(p) for p in db_projects]

    async def get_default_project(self) -> Optional[Project]:
        result = await self.db.execute(
            select(ProductDB).where(ProductDB.is_default == True)
        )
        db_project = result.scalar_one_or_none()
        return self._to_domain(db_project) if db_project else None

    async def find_by_name(self, name: str) -> List[Project]:
        result = await self.db.execute(
            select(ProductDB).where(
                ProductDB.name.ilike(f"%{name}%"),
                ProductDB.is_archived == False
            )
        )
        db_projects = result.scalars().all()
        return [self._to_domain(p) for p in db_projects]

    def _to_domain(self, db_model: ProductDB) -> Project:
        """Convert database model to domain model"""
        return Project(
            id=db_model.id,
            name=db_model.name,
            description=db_model.description,
            vision=db_model.vision,
            strategy=db_model.strategy,
            is_default=db_model.is_default,
            is_archived=db_model.is_archived,
            created_at=db_model.created_at,
            updated_at=db_model.updated_at,
            integrations=[
                ProjectIntegration(
                    id=i.id,
                    type=i.type,
                    name=i.name,
                    config=i.config,
                    is_active=i.is_active
                ) for i in db_model.integrations
            ]
        )
```

## Data Access Patterns

### Query Pattern

For read-only operations, use Query Services that directly access repositories:

```python
# Query Service → Repository → Database
projects = await project_query_service.list_active_projects()
```

### Command Pattern

For state changes, use Workflows that orchestrate multiple operations:

```python
# Workflow → Tasks → Repositories → Database
workflow = await workflow_factory.create_from_intent(intent)
result = await orchestration_engine.execute_workflow(workflow.id)
```

### Transaction Boundaries

- Each repository method is a transaction
- Workflows may span multiple transactions
- Use database transactions for consistency
- Event sourcing for audit trail

## Migration Strategy

### Schema Evolution

1. Use Alembic for database migrations
2. Domain models drive schema changes
3. Backward compatibility for API changes
4. Zero-downtime deployment support

### Example Migration

```python
# alembic/versions/001_add_project_integrations.py
def upgrade():
    op.create_table(
        'project_integrations',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('project_id', sa.String(), nullable=False),
        sa.Column('type', sa.Enum(IntegrationType), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('config', sa.JSON(), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['project_id'], ['products.id'], ondelete='CASCADE')
    )
```

## Performance Considerations

### Indexes

- Primary keys on all tables
- Foreign key indexes for joins
- Composite indexes for common queries
- Full-text search for descriptions

### Query Optimization

- Use eager loading for related data
- Pagination for large result sets
- Database-level filtering
- Connection pooling

### Caching Strategy

- Redis for frequently accessed data
- In-memory caching for session data
- Invalidation on updates
- TTL-based expiration

## Workflow Context Patterns

Workflows carry a context dictionary that is enriched automatically during creation. For GitHub workflows, the repository is injected if available.

**Example: GitHub Issue Creation Workflow Context**

```json
{
  "project_id": "proj-123",
  "project_name": "Mobile App",
  "repository": "acme/mobile-app",
  "title": "Login fails on iOS",
  "body": "Steps to reproduce...",
  "labels": ["bug", "ios"]
}
```

- The `repository` field is injected automatically if available from project context.
- Downstream handlers (e.g., GitHub issue creation) consume this context.

## TaskResult Model

@dataclass
class TaskResult:
"""Result of a completed task"""
task_id: str
status: TaskStatus
output: Dict[str, Any] = field(default_factory=dict)
error: Optional[str] = None
completed_at: Optional[datetime] = None

## Integration Configuration Examples

### GitHub Integration Example

```json
{
  "type": "github",
  "name": "Acme GitHub",
  "config": {
    "repository": "acme/mobile-app",
    "default_labels": ["bug", "ios"]
  },
  "is_active": true
}
```

### Jira Integration Example

```json
{
  "type": "jira",
  "name": "Acme Jira",
  "config": {
    "project_key": "ACME",
    "url": "https://acme.atlassian.net"
  },
  "is_active": true
}
```

### Workflow Creation with Context

For workflows that require repository context (e.g., GitHub issue creation), the context is enriched automatically:

```python
workflow = await workflow_factory.create_from_intent(intent, session_id, project_context)
# The resulting workflow.context will include 'repository' if available from project
```

## Revision Log

- **June 28, 2025**: Added workflow context patterns, TaskResult model, ProjectIntegration config validation, integration config examples, and workflow creation with context example for GitHub integration

---

_Last Updated: June 28, 2025_
