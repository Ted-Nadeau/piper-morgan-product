# Piper Morgan 1.0 - Migration Guide

## Overview

This guide provides strategies and patterns for migrating existing code to align with Piper Morgan's architecture, evolving the CQRS implementation, and managing future architectural changes. It serves as a reference for refactoring efforts and system evolution.

## 1. Current State Assessment

### Identifying Migration Candidates

Before migrating, assess your current code for:

```python
# Signs that code needs migration:

# 1. Workflows used for simple queries
class ListProjectsWorkflow(Workflow):  # ❌ Query forced into workflow
    async def execute(self):
        projects = await repo.list_all()
        return projects

# 2. Direct database access in services
class ProjectService:
    async def get_project(self, id):
        result = await db.execute("SELECT...")  # ❌ Direct DB access

# 3. Business logic in wrong layers
class ProjectRepository:
    async def create_project(self, name):
        if len(name) < 3:  # ❌ Business logic in repository
            raise ValueError("Name too short")

# 4. Tight coupling to external services
class WorkflowEngine:
    def __init__(self):
        self.github = GitHubClient()  # ❌ Direct instantiation
```

## 2. Migration Patterns

### 2.1 Workflow to Query Migration

**Before**: Query operation as workflow
```python
# ❌ Old pattern
class ListProjectsWorkflow(Workflow):
    type = WorkflowType.LIST_PROJECTS

    async def execute(self, context):
        repo = ProjectRepository(get_session())
        projects = await repo.list_active_projects()
        return {"projects": [p.to_dict() for p in projects]}

# In workflow factory
if intent.action == "list_projects":
    return ListProjectsWorkflow()
```

**After**: Direct query service
```python
# ✅ New pattern
class ProjectQueryService:
    def __init__(self, repository: ProjectRepository):
        self.repo = repository

    async def list_active_projects(self) -> List[Project]:
        return await self.repo.list_active_projects()

# In intent router
if intent.category == IntentCategory.QUERY:
    if intent.action == "list_projects":
        projects = await query_service.list_active_projects()
        return QueryResult(data={"projects": projects})
```

**Migration Steps**:
1. Create query service class
2. Move logic from workflow to service
3. Update intent routing
4. Remove workflow class
5. Update tests

### 2.2 Repository Pattern Adoption

**Before**: Direct database access
```python
# ❌ Old pattern
class ProjectService:
    def __init__(self, db_connection):
        self.db = db_connection

    async def get_project(self, project_id: str):
        result = await self.db.execute(
            "SELECT * FROM projects WHERE id = ?",
            [project_id]
        )
        return self._map_to_project(result)
```

**After**: Repository pattern
```python
# ✅ New pattern
class ProjectRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProjectDB)

    async def get_by_id(self, project_id: str) -> Optional[Project]:
        db_project = await self.session.get(ProjectDB, project_id)
        return self._to_domain(db_project) if db_project else None

class ProjectService:
    def __init__(self, repo_factory: RepositoryFactory):
        self.repo_factory = repo_factory

    async def get_project(self, project_id: str) -> Project:
        async with self.repo_factory.get_repository(ProjectRepository) as repo:
            project = await repo.get_by_id(project_id)
            if not project:
                raise ProjectNotFoundError(project_id)
            return project
```

**Migration Steps**:
1. Create repository class
2. Move SQL to repository methods
3. Implement domain model conversion
4. Update service to use repository
5. Add proper error handling

### 2.3 Domain Model Extraction

**Before**: Mixed business and persistence logic
```python
# ❌ Old pattern
class ProjectDB(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True)
    name = Column(String)

    def validate(self):  # Business logic in DB model
        if len(self.name) < 3:
            raise ValueError("Name too short")

    def add_integration(self, integration):  # Business method
        self.integrations.append(integration)
```

**After**: Separate domain and database models
```python
# ✅ New pattern
# Domain model (pure business logic)
@dataclass
class Project:
    id: str
    name: str
    integrations: List[ProjectIntegration]

    def validate(self):
        if len(self.name) < 3:
            raise ValidationError("Project name must be at least 3 characters")

    def add_integration(self, integration_type: IntegrationType, config: Dict):
        integration = ProjectIntegration(type=integration_type, config=config)
        self.integrations.append(integration)

# Database model (persistence only)
class ProjectDB(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True)
    name = Column(String(255), nullable=False)
    # Pure schema definition
```

**Migration Steps**:
1. Create domain model class
2. Move business methods to domain model
3. Keep database model minimal
4. Implement conversion methods in repository
5. Update all references

### 2.4 Event-Driven Decoupling

**Before**: Direct service coupling
```python
# ❌ Old pattern
class WorkflowEngine:
    def __init__(self):
        self.notification_service = NotificationService()
        self.analytics_service = AnalyticsService()

    async def complete_workflow(self, workflow):
        # Direct calls create tight coupling
        await self.notification_service.send_completion_email(workflow)
        await self.analytics_service.record_completion(workflow)
```

**After**: Event-driven communication
```python
# ✅ New pattern
class WorkflowEngine:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def complete_workflow(self, workflow):
        # Publish event - no direct dependencies
        await self.event_bus.publish(
            WorkflowCompletedEvent(
                workflow_id=workflow.id,
                completed_at=datetime.now()
            )
        )

# Subscribers handle their own concerns
class NotificationService:
    def __init__(self, event_bus: EventBus):
        event_bus.subscribe("workflow.completed", self.handle_completion)

    async def handle_completion(self, event: WorkflowCompletedEvent):
        await self.send_completion_email(event.workflow_id)
```

**Migration Steps**:
1. Identify coupled services
2. Define event types
3. Implement event bus
4. Refactor to publish events
5. Create event handlers
6. Remove direct dependencies

## 3. CQRS Evolution Path

### Phase 1: Basic Separation (Current State)
```python
# Simple query/command routing
if intent.category == IntentCategory.QUERY:
    result = await query_router.route_query(intent)
else:
    workflow = await workflow_factory.create_from_intent(intent)
```

### Phase 2: Dedicated Read Models
```python
# Optimized read models for queries
class ProjectReadModel:
    """Denormalized view optimized for queries"""
    id: str
    name: str
    github_repo: str  # Denormalized from integration
    last_activity: datetime
    open_issues_count: int  # Cached aggregate

class ProjectQueryService:
    async def get_project_summary(self, project_id: str) -> ProjectReadModel:
        # Query optimized read model instead of domain model
        return await self.read_repo.get_project_summary(project_id)
```

### Phase 3: Event Sourcing
```python
# Store events instead of state
@dataclass
class ProjectCreatedEvent(Event):
    project_id: str
    name: str
    created_by: str

@dataclass
class IntegrationAddedEvent(Event):
    project_id: str
    integration_type: IntegrationType
    config: Dict

# Rebuild state from events
class ProjectAggregate:
    def __init__(self, events: List[Event]):
        self.id = None
        self.name = None
        self.integrations = []

        for event in events:
            self.apply(event)

    def apply(self, event: Event):
        if isinstance(event, ProjectCreatedEvent):
            self.id = event.project_id
            self.name = event.name
        elif isinstance(event, IntegrationAddedEvent):
            self.integrations.append(...)
```

### Phase 4: Full CQRS with Eventual Consistency
```python
# Separate write and read databases
class CommandHandler:
    async def handle_create_project(self, command: CreateProjectCommand):
        # Write to event store
        events = [ProjectCreatedEvent(...)]
        await self.event_store.append(events)

        # Async projection to read model
        await self.event_bus.publish(events)

class ProjectionHandler:
    async def handle_project_created(self, event: ProjectCreatedEvent):
        # Update read model asynchronously
        await self.read_db.create_project_summary(...)
```

## 4. Breaking Changes Management

### API Versioning Strategy

```python
# Support multiple API versions
@app.post("/api/v1/intent")  # Current version
async def process_intent_v1(request: IntentRequestV1):
    # Current implementation

@app.post("/api/v2/intent")  # New version
async def process_intent_v2(request: IntentRequestV2):
    # Enhanced implementation with breaking changes

# Version adapter for smooth migration
class VersionAdapter:
    def adapt_v1_to_v2(self, v1_request: IntentRequestV1) -> IntentRequestV2:
        return IntentRequestV2(
            message=v1_request.message,
            context=v1_request.context,
            # New v2 fields with defaults
            session_id=v1_request.session_id or str(uuid4()),
            confidence_threshold=0.8
        )
---
*Last Updated: June 21, 2025*

## Revision Log
- **June 21, 2025**: Added systematic documentation dating and revision tracking
