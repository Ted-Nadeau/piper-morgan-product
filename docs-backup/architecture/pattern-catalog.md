# Piper Morgan 1.0 - Pattern Catalog

## Overview

This catalog documents the key architectural and design patterns used in Piper Morgan. Each pattern includes its purpose, implementation details, usage guidelines, and anti-patterns to avoid.

## 1. Repository Pattern

### Purpose

Encapsulate data access logic and provide a clean interface between domain models and database implementation, with automatic resource management and consistent transaction handling.

### Implementation

```python
class BaseRepository:
    """Base repository with common CRUD operations"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs) -> Any:
        # Use transaction context for automatic commit/rollback
        async with self.session.begin():
            instance = self.model(**kwargs)
            self.session.add(instance)
            # Automatic commit via context manager
        return instance

    async def get_by_id(self, id: str) -> Optional[Any]:
        result = await self.session.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

class ProjectRepository(BaseRepository):
    """Domain-specific repository"""

    model = ProjectDB

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def list_active_projects(self) -> List[Project]:
        result = await self.session.execute(
            select(ProjectDB).where(ProjectDB.is_archived == False)
        )
        db_projects = result.scalars().all()
        return [db_project.to_domain() for db_project in db_projects]

# Session Management Pattern
from contextlib import asynccontextmanager
from services.database.session_factory import AsyncSessionFactory

async def service_example():
    """Example service using context manager for automatic resource management"""
    async with AsyncSessionFactory.session_scope() as session:
        repo = ProjectRepository(session)
        return await repo.list_active_projects()
    # Automatic cleanup and transaction handling
```

### Usage Guidelines

**Repository Design:**

- One repository per aggregate root
- Repository methods return domain models, not database models
- Keep business logic out of repositories
- Use repositories for all data access
- **NEW**: Use `async with session.begin()` for all operations
- **NEW**: No manual `session.commit()` calls

**Session Management:**

- **NEW**: Use `AsyncSessionFactory.session_scope()` context manager
- **NEW**: No manual session creation or cleanup
- **NEW**: Automatic transaction handling via context manager
- **NEW**: Single session per operation scope

### Anti-patterns to Avoid

**Repository Anti-patterns:**

- ❌ Direct database access from services
- ❌ Business logic in repositories
- ❌ Exposing database models outside repository
- ❌ Generic repositories without domain methods

**Session Anti-patterns:**

- ❌ Manual session creation/cleanup
- ❌ Sharing sessions across operation boundaries
- ❌ Manual `session.commit()` calls
- ❌ Missing session cleanup in exception handlers

## 2. Factory Pattern (Stateless)

### Purpose

Create complex objects without exposing construction logic, maintaining stateless design for concurrency safety.

### Implementation

```python
class WorkflowFactory:
    """Stateless factory - all context passed per-call"""

    def __init__(self):
        self.workflow_registry = {}
        self._register_default_workflows()

    async def create_from_intent(
        self,
        intent: Intent,
        session_id: str,
        project_context: Optional[ProjectContext] = None
    ) -> Optional[Workflow]:
        """Create workflow with per-call context injection"""
        # No instance state used - all data from parameters

        if project_context:
            project, needs_confirm = await project_context.resolve_project(
                intent, session_id
            )
            intent.context.update({
                "project_id": project.id,
                "project_name": project.name
            })

        workflow_class = self._match_workflow(intent)
        return workflow_class(context=intent.context) if workflow_class else None
```

### Usage Guidelines

- Pass all context as method parameters
- No instance variables for request-specific data
- Support concurrent creation safely
- Make dependencies explicit

### Anti-patterns to Avoid

- ❌ Storing request context in factory instance
- ❌ Stateful factories that require reset between uses
- ❌ Hidden dependencies through instance state
- ❌ Thread-unsafe shared state

## 3. Robust Task Manager Pattern

### Purpose

Manage background tasks with context preservation and comprehensive tracking, preventing garbage collection and providing full observability into task execution lifecycle.

### Implementation

```python
class RobustTaskManager:
    """Manages background tasks with context preservation and comprehensive tracking"""

    def __init__(self):
        self.active_tasks: Set[asyncio.Task] = set()
        self.task_metrics: Dict[str, TaskMetrics] = {}
        self.context: Dict[str, Any] = {}
        self.correlation_id: Optional[str] = None

    def add_task(self, task_name: str, task_data: Dict[str, Any]) -> str:
        """Add a task to the manager for tracking"""
        task_id = str(uuid.uuid4())
        metrics = TaskMetrics(task_id=task_id, name=task_name, ...)
        self.task_metrics[task_id] = metrics
        return task_id

    def start_task(self, task_name: str) -> bool:
        """Mark a task as started"""
        for task_id, metrics in self.task_metrics.items():
            if metrics.name == task_name and metrics.started_at is None:
                metrics.mark_started()
                return True
        return False

    def complete_task(self, task_name: str, result: Dict[str, Any]) -> bool:
        """Mark a task as completed with result"""
        for task_id, metrics in self.task_metrics.items():
            if metrics.name == task_name and metrics.completed_at is None:
                metrics.mark_completed(success=True)
                self.task_results[task_id] = result
                return True
        return False
```

### Usage Guidelines

- Use for all background task management
- Preserve context across async boundaries
- Track task lifecycle with metrics
- Prevent garbage collection of active tasks
- Maintain correlation IDs for observability

### Anti-patterns to Avoid

- ❌ Manual task tracking without metrics
- ❌ Losing context across async boundaries
- ❌ No correlation tracking
- ❌ Tasks that can be garbage collected

## 4. Pipeline Metrics Pattern

### Purpose

Track comprehensive metrics for pipeline execution with correlation tracking and stage recording for observability.

### Implementation

```python
@dataclass
class SlackPipelineMetrics:
    """Comprehensive metrics tracking for pipeline execution"""
    correlation_id: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    processing_stages: List[Any] = field(default_factory=list)

    def start_pipeline(self):
        """Start pipeline timing"""
        self.start_time = datetime.utcnow()

    def end_pipeline(self):
        """End pipeline timing"""
        self.end_time = datetime.utcnow()

    def record_stage(self, stage_name: str, stage_data: Dict[str, Any]):
        """Record a processing stage with data"""
        stage_record = {
            "name": stage_name,
            "data": stage_data,
            "correlation_id": self.correlation_id,
            "timestamp": datetime.utcnow()
        }
        self.processing_stages.append(stage_record)
```

### Usage Guidelines

- Track all pipeline stages with correlation IDs
- Record timing for performance monitoring
- Maintain stage data for debugging
- Use for end-to-end observability

### Anti-patterns to Avoid

- ❌ No correlation tracking across stages
- ❌ Missing timing information
- ❌ No stage data preservation
- ❌ Inconsistent observability

## 5. Response Handler Pattern

### Purpose

Handle response generation with intent-based routing and monitoring bypass for different types of requests.

### Implementation

```python
class SlackResponseHandler:
    """Handle Slack responses with intent-based routing"""

    async def _process_through_orchestration(self, intent: Intent, slack_context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process intent through orchestration engine with monitoring bypass"""

        # Skip monitoring intents that should bypass orchestration
        if intent.action == "monitor_system" or intent.context.get("monitoring"):
            return {
                "type": "monitoring_response",
                "content": "Monitoring active - system status normal",
                "intent": intent,
            }

        # Process other intents through orchestration
        return await self.orchestration_engine.process_intent(intent, slack_context)
```

### Usage Guidelines

- Implement intent-based routing
- Provide monitoring bypass for system requests
- Maintain observability throughout processing
- Handle different response types appropriately

### Anti-patterns to Avoid

- ❌ No intent-based routing
- ❌ Processing all requests through orchestration
- ❌ Missing monitoring bypass
- ❌ No observability tracking

## 6. Spatial Adapter Pattern

### Purpose

Map external identifiers to spatial positions with bidirectional mapping and context preservation for response routing.

### Implementation

```python
class SlackSpatialAdapter(BaseSpatialAdapter):
    """Spatial adapter for Slack integration with channel ID preservation"""

    async def create_spatial_event_from_slack(self, slack_timestamp: str, event_type: str, context: Dict[str, Any]) -> SpatialEvent:
        """Create SpatialEvent from Slack timestamp with proper ID mapping"""

        # Handle both integer positions and string IDs
        territory_position = context.get("territory_position", 0)
        if isinstance(territory_position, str):
            territory_position = hash(territory_position) % 1000

        room_position = context.get("room_position", 0)
        if isinstance(room_position, str):
            room_position = hash(room_position) % 1000
        elif "room_id" in context and not room_position:
            room_position = hash(context["room_id"]) % 1000

        # Create spatial event with integer positioning
        return SpatialEvent(
            event_type=event_type,
            territory_position=territory_position,
            room_position=room_position,
            # ... other fields
        )

    async def get_response_context(self, slack_timestamp: str) -> Optional[Dict[str, Any]]:
        """Get context for response routing to Slack"""
        async with self._lock:
            if slack_timestamp not in self._context_storage:
                return None

            context = self._context_storage[slack_timestamp]
            return {
                "channel_id": context.get("room_id") or context.get("original_channel_id"),
                "thread_ts": context.get("path_id") or context.get("thread_ts"),
                "workspace_id": context.get("territory_id"),
                "user_id": context.get("user_id"),
                "content": context.get("content", ""),
            }
```

### Usage Guidelines

- Map external IDs to spatial positions consistently
- Preserve context for response routing
- Maintain bidirectional mapping
- Handle both string and integer positions

### Anti-patterns to Avoid

- ❌ No bidirectional mapping
- ❌ Losing context during mapping
- ❌ Inconsistent ID handling
- ❌ No response context preservation

## 7. Query Service Pattern (CQRS-lite)

### Purpose

Separate read operations from write operations, providing optimized paths for simple data retrieval.

### Implementation

```python
class QueryRouter:
    """Routes query intents to appropriate services"""

    def __init__(self, project_repository: ProjectRepository):
        self.project_queries = ProjectQueryService(project_repository)

    async def route_query(self, intent: Intent) -> QueryResult:
        if intent.action == "list_projects":
            projects = await self.project_queries.list_active_projects()
            return QueryResult(
                success=True,
                data={"projects": [p.to_dict() for p in projects]}
            )
        # Route other queries...

class ProjectQueryService:
    """Handles project-related queries"""

    def __init__(self, repository: ProjectRepository):
        self.repo = repository

    async def list_active_projects(self) -> List[Project]:
        # Direct repository access, no workflow overhead
        return await self.repo.list_active_projects()
```

### Usage Guidelines

- Use for read-only operations
- Bypass workflow orchestration
- Return data directly from repositories
- Keep queries simple and focused

### Decision Criteria

| Use Query Service When        | Use Workflow When            |
| ----------------------------- | ---------------------------- |
| Reading data                  | Changing state               |
| Single repository access      | Multiple system coordination |
| Synchronous response expected | Background processing needed |
| No side effects               | Side effects required        |

### Anti-patterns to Avoid

- ❌ Forcing queries through workflow pattern
- ❌ State changes in query services
- ❌ Complex business logic in queries
- ❌ Cross-repository transactions in queries

## 8. Domain-First Database Pattern

### Purpose

Ensure database schema is driven by domain models, not the other way around.

### Implementation

```python
# Domain model drives design
@dataclass
class Project:
    """Domain model - pure business logic"""
    id: str
    name: str
    description: str
    integrations: List[ProjectIntegration]

    def get_github_repository(self) -> Optional[str]:
        """Business method"""
        github = self.get_integration(IntegrationType.GITHUB)
        return github.config.get("repository") if github else None

# Database model follows domain
class ProductDB(Base):
    """Database model - persistence concerns"""
    __tablename__ = "products"

    id = Column(String, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)

    # Relationships match domain model
    integrations = relationship("ProjectIntegrationDB", back_populates="project")

# Schema generated from models
async def init_database():
    # Let SQLAlchemy create schema from models
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

### Usage Guidelines

- Define domain models first
- Database models mirror domain structure
- Use SQLAlchemy to generate schema
- Keep persistence logic in repositories

### Anti-patterns to Avoid

- ❌ Hardcoded SQL schema files
- ❌ Database-driven domain design
- ❌ Exposing database details in domain
- ❌ Manual schema synchronization

## 9. Event-Driven Communication Pattern

### Purpose

Enable loose coupling between services through asynchronous event publishing and handling.

### Implementation

```python
class EventBus:
    """Central event distribution"""

    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable):
        self._handlers.setdefault(event_type, []).append(handler)

    async def publish(self, event: Event):
        handlers = self._handlers.get(event.type, [])
        for handler in handlers:
            # Fire and forget pattern
            asyncio.create_task(self._safe_handler_call(handler, event))

    async def _safe_handler_call(self, handler: Callable, event: Event):
        try:
            await handler(event)
        except Exception as e:
            logger.error(f"Event handler failed: {e}")

# Usage
event_bus = EventBus()

# Subscribe to events
event_bus.subscribe("workflow.completed", handle_workflow_completion)
event_bus.subscribe("intent.classified", handle_intent_classified)

# Publish events
await event_bus.publish(Event(
    type="workflow.completed",
    data={"workflow_id": workflow.id, "status": "success"}
))
```

### Usage Guidelines

- Use for cross-service communication
- Keep events immutable
- Design for eventual consistency
- Make handlers idempotent

### Anti-patterns to Avoid

- ❌ Synchronous event handling
- ❌ Complex event chains
- ❌ Business logic in event handlers
- ❌ Assuming event ordering

## 10. Plugin Architecture Pattern

### Purpose

Enable extensible integrations with external systems without modifying core logic.

### Implementation

```python
class IntegrationPlugin(ABC):
    """Base plugin interface"""

    @abstractmethod
    async def create_issue(self, title: str, description: str, **kwargs) -> Dict:
        pass

    @abstractmethod
    async def get_issue(self, issue_id: str) -> Dict:
        pass

class GitHubPlugin(IntegrationPlugin):
    """GitHub-specific implementation"""

    def __init__(self, token: str):
        self.client = Github(token)

    async def create_issue(self, title: str, description: str, **kwargs) -> Dict:
        repo = self.client.get_repo(kwargs['repository'])
        issue = repo.create_issue(
            title=title,
            body=description,
            labels=kwargs.get('labels', [])
        )
        return {"id": issue.number, "url": issue.html_url}

class IntegrationManager:
    """Manages plugins"""

    def __init__(self):
        self._plugins: Dict[IntegrationType, IntegrationPlugin] = {}

    def register(self, integration_type: IntegrationType, plugin: IntegrationPlugin):
        self._plugins[integration_type] = plugin

    def get_plugin(self, integration_type: IntegrationType) -> IntegrationPlugin:
        return self._plugins.get(integration_type)
```

### Usage Guidelines

- Define clear plugin interfaces
- Keep plugins isolated from core
- Use dependency injection
- Support multiple plugin instances

### Anti-patterns to Avoid

- ❌ Hardcoding integration logic
- ❌ Plugin-specific code in core
- ❌ Tight coupling to external APIs
- ❌ Assuming plugin availability

## 11. Context Resolution Pattern

### Purpose

Resolve implicit context (like current project) from multiple sources with clear precedence rules.

### Implementation

```python
class ProjectContext:
    """Resolves project from various sources"""

    def __init__(self, repository: ProjectRepository, llm: LLMClient):
        self.repo = repository
        self.llm = llm
        self._session_memory: Dict[str, str] = {}

    async def resolve_project(
        self,
        intent: Intent,
        session_id: str,
        confirmed: bool = False
    ) -> Tuple[Project, bool]:
        """
        Resolution hierarchy:
        1. Explicit project_id (always wins)
        2. Session history (if confirmed)
        3. LLM inference from message
        4. Default project fallback
        """

        # 1. Explicit always wins
        if project_id := intent.context.get("project_id"):
            project = await self.repo.get_by_id(project_id)
            if not project:
                raise ProjectNotFoundError(project_id)
            return project, False

        # 2. Session history
        if session_id in self._session_memory and confirmed:
            project = await self.repo.get_by_id(self._session_memory[session_id])
            return project, False

        # 3. Inference
        inferred = await self._infer_from_message(intent)
        if inferred:
            self._session_memory[session_id] = inferred.id
            needs_confirm = session_id in self._session_memory and \
                           self._session_memory[session_id] != inferred.id
            return inferred, needs_confirm

        # 4. Default fallback
        default = await self.repo.get_default_project()
        if default:
            return default, False

        raise AmbiguousProjectError("Cannot determine project")
```

### Usage Guidelines

- Define clear precedence rules
- Make resolution transparent
- Cache decisions appropriately
- Handle ambiguity gracefully

### Anti-patterns to Avoid

- ❌ Hidden resolution logic
- ❌ Unpredictable precedence
- ❌ Silent fallbacks
- ❌ Assuming context exists

## 12. Adapter Pattern for LLM Providers

### Purpose

Abstract LLM provider differences behind a common interface to enable provider switching.

### Implementation

```python
class LLMAdapter(ABC):
    """Common interface for all LLM providers"""

    @abstractmethod
    async def complete(self, prompt: str, **kwargs) -> str:
        pass

    @abstractmethod
    async def classify(self, text: str, categories: List[str]) -> Tuple[str, float]:
        pass

class ClaudeAdapter(LLMAdapter):
    """Claude-specific implementation"""

    def __init__(self, api_key: str, model: str = "claude-3-opus"):
        self.client = Anthropic(api_key=api_key)
        self.model = model

    async def complete(self, prompt: str, **kwargs) -> str:
        response = await self.client.messages.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=kwargs.get("max_tokens", 1000)
        )
        return response.content[0].text

class LLMFactory:
    """Creates appropriate adapter"""

    @staticmethod
    def create(provider: str, **kwargs) -> LLMAdapter:
        if provider == "claude":
            return ClaudeAdapter(kwargs["api_key"])
        elif provider == "openai":
            return OpenAIAdapter(kwargs["api_key"])
        else:
            raise ValueError(f"Unknown provider: {provider}")
```

### Usage Guidelines

- Define provider-agnostic interfaces
- Keep provider specifics isolated
- Support configuration-based switching
- Handle provider differences transparently

### Anti-patterns to Avoid

- ❌ Provider-specific code in business logic
- ❌ Assuming provider capabilities
- ❌ Hardcoding provider choice
- ❌ Leaking provider abstractions

## 13. Session Management Pattern

### Purpose

Manage database sessions and connections consistently across async operations.

### Implementation

```python
class RepositoryFactory:
    """Manages repository lifecycle and sessions"""

    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url)
        self.async_session = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    @asynccontextmanager
    async def get_repository(self, repo_class: Type[BaseRepository]):
        """Provide repository with managed session"""
        async with self.async_session() as session:
            try:
                yield repo_class(session)
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def close(self):
        """Clean shutdown"""
        await self.engine.dispose()

# Usage
factory = RepositoryFactory(DATABASE_URL)

async with factory.get_repository(ProjectRepository) as repo:
    projects = await repo.list_active_projects()
    # Session automatically managed
```

### Usage Guidelines

- Use context managers for session lifecycle
- Ensure proper cleanup in all paths
- Handle transactions at repository level
- Document session ownership clearly

### Anti-patterns to Avoid

- ❌ Manual session management
- ❌ Leaked database connections
- ❌ Sessions crossing service boundaries
- ❌ Assuming session state

## 14. Error Handling Pattern (API Contract)

### Purpose

Provide consistent, actionable error responses that follow RESTful principles and give users clear guidance on resolution.

### Implementation

```python
class APIErrorHandler:
    """Centralized error handling for consistent responses"""

    ERROR_MESSAGES = {
        ProjectNotFoundError: "I couldn't find that project. Try 'list projects' to see available options.",
        AmbiguousProjectError: "Multiple projects match your request. Please be more specific.",
        GitHubAPIError: "GitHub is temporarily unavailable. Please try again in a few moments.",
        InsufficientContextError: "I need more information to complete this task. {details}"
    }

    @staticmethod
    def handle_error(error: Exception) -> JSONResponse:
        """Convert exceptions to user-friendly API responses"""
        if isinstance(error, ProjectNotFoundError):
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "error": {
                        "code": "PROJECT_NOT_FOUND",
                        "message": "The specified project does not exist",
                        "user_message": APIErrorHandler.ERROR_MESSAGES[ProjectNotFoundError],
                        "details": {"project_id": error.project_id}
                    }
                }
            )
        elif isinstance(error, ValidationError):
            return JSONResponse(
                status_code=422,
                content={
                    "status": "error",
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": str(error),
                        "field": getattr(error, 'field', None)
                    }
                }
            )
        else:
            # Generic error with safe message
            return JSONResponse(
                status_code=500,
                content={
                    "status": "error",
                    "error": {
                        "code": "INTERNAL_ERROR",
                        "message": "An unexpected error occurred",
                        "user_message": "Something went wrong. Please try again or contact support."
                    }
                }
            )

# API endpoint with error handling
@app.post("/api/v1/intent")
async def process_intent(request: IntentRequest):
    try:
        result = await intent_service.process(request)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        return APIErrorHandler.handle_error(e)
```

### Error Response Contract

```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Technical error message",
    "user_message": "User-friendly guidance",
    "field": "field_name (if applicable)",
    "details": {
      /* optional context */
    }
  }
}
```

### Status Code Guidelines

| Code | Usage               | Example                                        |
| ---- | ------------------- | ---------------------------------------------- |
| 200  | Success             | Request completed successfully                 |
| 400  | Bad Request         | Invalid JSON format or missing required fields |
| 404  | Not Found           | Project, workflow, or resource doesn't exist   |
| 422  | Validation Error    | Valid format but business rules violated       |
| 429  | Rate Limited        | Too many requests from client                  |
| 500  | Server Error        | Unexpected internal error                      |
| 502  | Service Unavailable | External service (GitHub, Claude) unavailable  |

### User Message Guidelines

- **Actionable**: Tell users what they can do to resolve the issue
- **Contextual**: Reference the specific situation (project names, etc.)
- **Helpful**: Suggest alternatives or next steps
- **Consistent**: Use the same tone and terminology across errors

### Usage Guidelines

- Always include both technical and user-friendly messages
- Log technical details separately for debugging
- Never expose internal implementation details
- Provide recovery suggestions when possible

### Anti-patterns to Avoid

- ❌ Generic "Something went wrong" without guidance
- ❌ Exposing stack traces or internal errors to users
- ❌ Inconsistent error formats across endpoints
- ❌ Wrong HTTP status codes for error types
- ❌ Technical jargon in user-facing messages

## 15. Internal Task Handler Pattern

### Purpose

Handle orchestration tasks using internal engine methods rather than separate handler classes, ensuring direct access to engine state, reducing indirection, and simplifying the codebase.

### Full Implementation

```python
class OrchestrationEngine:
    def __init__(self, github_agent: GitHubAgent, ...):
        self.github_agent = github_agent
        self.task_handlers = {
            TaskType.FILE_ANALYSIS: self._analyze_file,
            TaskType.GITHUB_CREATE_ISSUE: self._create_github_issue,
            # ... other handlers ...
        }

    async def handle_task(self, task: Task, context: dict):
        handler = self.task_handlers.get(task.type)
        if not handler:
            raise NotImplementedError(f"No handler for {task.type}")
        return await handler(task, context)

    async def _analyze_file(self, task: Task, context: dict):
        # ... file analysis logic ...
        pass

    async def _create_github_issue(self, task: Task, context: dict):
        """
        Handler for GITHUB_CREATE_ISSUE tasks. Uses GitHubAgent to create an issue.
        Expects context to include 'repository', 'title', and 'body'.
        """
        repo = context.get("repository")
        title = context.get("title")
        body = context.get("body")
        if not repo or not title or not body:
            return {"error": "Missing required context for GitHub issue creation"}
        result = await self.github_agent.create_issue(
            repository=repo,
            title=title,
            body=body,
            labels=context.get("labels", [])
        )
        return {"github_issue": result}
```

### Usage Guidelines

- Register all task handlers as methods on the engine instance.
- Use a single `task_handlers` mapping for all supported task types.
- Keep handler logic close to orchestration state for easier debugging.
- Avoid proliferation of handler classes or external handler modules.
- Use clear, descriptive method names for handlers.

### Benefits

- Simpler architecture and fewer files to maintain.
- Direct access to orchestration state and dependencies.
- Easier to trace, debug, and extend task handling logic.
- Reduces indirection and cognitive overhead for new contributors.

### Anti-patterns to Avoid

- ❌ Creating a separate handler class for each task type.
- ❌ Scattering handler logic across multiple modules.
- ❌ Indirect state access via external handler classes.
- ❌ Registering handlers dynamically in multiple places.

## 16. Repository Context Enrichment Pattern

### Purpose

Automatically enrich workflow context with repository information for GitHub and similar integrations, enabling seamless ticket creation and analysis without requiring explicit repository input from the user.

### Full Implementation

```python
def create_workflow_from_intent(intent: Intent, project_context: Project):
    """
    Enriches the workflow context with repository info for CREATE_TICKET workflows.
    This pattern ensures that downstream handlers (e.g., GitHub issue creation) have
    the necessary repository context, even if the user did not specify it.
    """
    context = dict(intent.context)
    if intent.type == WorkflowType.CREATE_TICKET:
        try:
            repo = project_context.get_github_repository()
            if repo:
                context["repository"] = repo
            else:
                logger.warning(f"No GitHub repository found for project {project_context.id}")
        except Exception as e:
            logger.error(f"Failed to enrich context with repository: {e}")
    # ... continue with workflow creation using enriched context ...
    return Workflow(context=context)
```

### Usage Guidelines

- Always attempt repository enrichment for workflows that require it (e.g., CREATE_TICKET).
- Log enrichment failures as warnings or errors, but do not block workflow creation.
- Centralize enrichment logic in the workflow factory or orchestration engine.
- Support multiple integration types by extending the enrichment logic as needed.
- Document the context flow for maintainers and integrators.

### Context Flow

1. **Intent arrives** (e.g., user says "create a ticket for bug X").
2. **Project context is resolved** (via explicit ID, session, or inference).
3. **Enrichment logic runs**:
   - If the workflow type is CREATE_TICKET, attempt to fetch the repository from the project context.
   - If found, inject `repository` into the workflow context.
   - If not found, log a warning but proceed.
4. **Workflow is created** with the enriched context.
5. **Downstream handlers** (e.g., GitHub issue creation) consume the repository info from context.

### Anti-patterns to Avoid

- ❌ Forcing users to specify repository every time.
- ❌ Hardcoding repository info in workflow logic.
- ❌ Failing workflows on enrichment errors.
- ❌ Scattering enrichment logic across multiple modules.

## 17. Background Task Error Handling Pattern

### Purpose

Wrap background task execution in a robust error handling pattern to ensure task failures are logged and managed appropriately, preventing application crashes and enabling graceful degradation.

### Implementation

```python
class RobustTaskManager:
    """Manages background tasks with context preservation and comprehensive tracking"""

    def __init__(self):
        self.active_tasks: Set[asyncio.Task] = set()
        self.task_metrics: Dict[str, TaskMetrics] = {}
        self.context: Dict[str, Any] = {}
        self.correlation_id: Optional[str] = None

    def add_task(self, task_name: str, task_data: Dict[str, Any]) -> str:
        """Add a task to the manager for tracking"""
        task_id = str(uuid.uuid4())
        metrics = TaskMetrics(task_id=task_id, name=task_name, ...)
        self.task_metrics[task_id] = metrics
        return task_id

    def start_task(self, task_name: str) -> bool:
        """Mark a task as started"""
        for task_id, metrics in self.task_metrics.items():
            if metrics.name == task_name and metrics.started_at is None:
                metrics.mark_started()
                return True
        return False

    def complete_task(self, task_name: str, result: Dict[str, Any]) -> bool:
        """Mark a task as completed with result"""
        for task_id, metrics in self.task_metrics.items():
            if metrics.name == task_name and metrics.completed_at is None:
                metrics.mark_completed(success=True)
                self.task_results[task_id] = result
                return True
        return False
```

### Usage Guidelines

- Use for all background task management
- Preserve context across async boundaries
- Track task lifecycle with metrics
- Prevent garbage collection of active tasks
- Maintain correlation IDs for observability

### Anti-patterns to Avoid

- ❌ Manual task tracking without metrics
- ❌ Losing context across async boundaries
- ❌ No correlation tracking
- ❌ Tasks that can be garbage collected

## 18. Configuration Access Pattern

### Purpose

Provide consistent, layer-appropriate configuration access that maintains clean architecture boundaries while supporting practical infrastructure needs.

### Implementation

**Application/Domain Layer Configuration:**

```python
# ✅ APPROVED: ConfigService injection for application logic
class WorkflowService:
    def __init__(self, config_service: ConfigService):
        self.config = config_service

    async def process_workflow(self, workflow_type: WorkflowType):
        # Application configuration through service
        if self.config.feature_enabled("advanced_workflows"):
            return await self._process_advanced_workflow(workflow_type)
        return await self._process_basic_workflow(workflow_type)

    def get_timeout_config(self) -> int:
        return self.config.get_timeout("workflow_execution", default=300)
```

**Infrastructure Layer Configuration:**

```python
# ✅ APPROVED: Repository with ConfigService + FeatureFlags utility
from services.infrastructure.config.feature_flags import FeatureFlags

class FileRepository(BaseRepository):
    def __init__(self, session: AsyncSession, config_service: ConfigService):
        super().__init__(session)
        self.config = config_service

    async def search_files_with_content(self, session_id: str, query: str):
        # Infrastructure feature detection
        if FeatureFlags.is_mcp_content_search_enabled():
            return await self._enhanced_mcp_search(session_id, query)
        return await self._standard_search(session_id, query)

    def _get_cache_config(self) -> int:
        # Application config through service
        return self.config.get_int("file_cache_ttl", 300)
```

**Test Configuration:**

```python
# ✅ APPROVED: Mock ConfigService, not environment variables
@pytest.fixture
def mock_config_with_feature_enabled():
    mock_config = Mock(spec=ConfigService)
    mock_config.feature_enabled.return_value = True
    mock_config.get_int.return_value = 300
    return mock_config

def test_feature_behavior(mock_config_with_feature_enabled):
    service = WorkflowService(mock_config_with_feature_enabled)
    # Test focuses on behavior, not environment state
    result = await service.process_workflow(WorkflowType.ANALYSIS)
    assert result.uses_advanced_features == True
```

### Usage Guidelines

**Layer-Specific Rules:**

- **Application/Domain**: Use ConfigService exclusively
- **Infrastructure**: ConfigService preferred, FeatureFlags utility for infrastructure toggles
- **Testing**: Mock ConfigService, avoid environment variable patching

**Configuration Categories:**

- **ConfigService**: Application behavior, user-facing features, business logic parameters
- **FeatureFlags**: Infrastructure toggles, runtime detection, emergency overrides
- **Environment Direct**: Container orchestration, security credentials (through utilities)

### Anti-patterns to Avoid

```python
# ❌ AVOID: Direct environment access in domain layer
class WorkflowService:
    async def process_workflow(self):
        if os.getenv("ENABLE_ADVANCED_WORKFLOWS") == "true":  # Violates layer boundary
            pass

# ❌ AVOID: Mixed configuration patterns
class MCPResourceManager:
    def __init__(self):
        if CONFIG_SERVICE_AVAILABLE:
            config = get_config()  # Sometimes use service
        else:
            self.use_pool = os.getenv("USE_MCP_POOL")  # Sometimes use env

# ❌ AVOID: Environment patching in tests
@pytest.fixture
def test_config():
    os.environ["ENABLE_FEATURE"] = "true"  # Brittle, environment-dependent
    yield
    del os.environ["ENABLE_FEATURE"]
```

### References

- **ADR-010**: Configuration Access Patterns
- **Implementation**: `services/infrastructure/config/feature_flags.py`
- **Migration**: GitHub Issues #39 (MCPResourceManager), #40 (FileRepository)

## 19. LLM Placeholder Instruction Pattern

### Purpose

Prevent Large Language Model (LLM) hallucination by instructing models to use explicit placeholders when information is missing or uncertain, rather than fabricating technical details.

### Implementation

```python
# In prompt instructions for LLM content generation
prompt_instructions = """
6. PLACEHOLDER INSTRUCTIONS (CRITICAL):
   **NEVER fabricate specific technical details not provided in the user request.**

   When information is missing or uncertain, use explicit placeholders:
   - **[SPECIFIC EXAMPLE NEEDED: describe what kind]** - For technical details, error messages, version numbers
   - **[FACT CHECK: claim]** - For unverified details, environments, browser versions, test results
   - **[QUESTION: ask clarifying question]** - When guessing would be required

   Examples:
   - Instead of: "Error message: 'An unexpected error occurred. Please try again later.'"
   - Use: "Error message: [SPECIFIC EXAMPLE NEEDED: exact error message displayed]"

   - Instead of: "Tested on Chrome 89, Firefox 86, Safari 14"
   - Use: "Tested on [FACT CHECK: browser versions and environments where issue occurs]"
"""
```

### Usage Guidelines

- Apply to all LLM-generated content where accuracy is critical
- Use three placeholder types: SPECIFIC EXAMPLE NEEDED, FACT CHECK, QUESTION
- Include clear examples of what NOT to fabricate
- Make placeholders clearly visible and actionable for reviewers
- Maintain professional content structure while preventing misinformation

### Anti-Patterns

- ❌ Allowing LLM to guess technical details
- ❌ Fabricating browser versions, error messages, or environment details
- ❌ Making unverified claims about testing or environments
- ❌ Generating vague placeholders without specific guidance

### Benefits

- Increased accuracy and trustworthiness
- Clear communication about missing information
- Professional standards in generated content
- Prevents misleading stakeholders with fabricated details

## 20. Spatial Metaphor Integration Pattern (PM-074)

### Purpose

Process external system events (like Slack) as spatial changes to an AI agent's environment, enabling natural navigation and interaction patterns through physical space metaphors. Creates embodied AI experiences with persistent spatial memory.

### Core Spatial Architecture

```python
@dataclass
class Territory:
    """Slack workspace as navigable territory/building"""
    id: str
    name: str
    territory_type: TerritoryType  # CORPORATE, STARTUP, COMMUNITY
    domain: Optional[str] = None
    spatial_properties: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Room:
    """Slack channel as specialized room with purpose"""
    id: str
    name: str
    territory_id: str
    purpose: RoomPurpose  # COLLABORATION, DEVELOPMENT, SUPPORT, PLANNING, SOCIAL
    inhabitants: Set[str] = field(default_factory=set)
    attention_history: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class AttentionEvent:
    """Attention-generating event with decay models"""
    event_id: str
    source: AttentionSource  # MENTION, MESSAGE, EMERGENCY, WORKFLOW
    spatial_coordinates: SpatialCoordinates
    base_intensity: float  # 0.0 to 1.0
    urgency_level: float
    created_at: datetime = field(default_factory=datetime.now)

    def get_current_intensity(self, decay_model: AttentionDecay = AttentionDecay.EXPONENTIAL) -> float:
        """Calculate attention intensity with temporal decay"""
        age = (datetime.now() - self.created_at).total_seconds()
        if decay_model == AttentionDecay.EXPONENTIAL:
            half_life = 1800.0  # 30 minutes
            return self.base_intensity * math.exp(-age * math.log(2) / half_life)
        # ... other decay models
```

### Advanced Components

#### Spatial Memory with Pattern Learning
```python
class SpatialMemoryStore:
    """Persistent spatial memory across sessions"""

    def learn_spatial_pattern(self, category: str, pattern_name: str,
                            pattern_data: Dict[str, Any], confidence: float,
                            applicable_locations: List[str]):
        """Learn navigation and interaction patterns"""
        pattern = SpatialPattern(
            pattern_id=f"spatial_{uuid4().hex[:8]}",
            category=category,
            pattern_name=pattern_name,
            pattern_data=pattern_data,
            confidence=confidence,
            applicable_locations=applicable_locations
        )
        self._patterns[pattern.pattern_id] = pattern
```

#### Multi-Workspace Navigation
```python
class WorkspaceNavigator:
    """Navigate across multiple territories with intelligence"""

    def suggest_next_territory(self, context: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Suggest territory based on attention priorities"""
        priorities = self.attention_model.get_attention_priorities()
        if priorities:
            top_event, score = priorities[0]
            return top_event.spatial_coordinates.territory_id
        return None

    def switch_territory(self, territory_id: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """Execute territory switch with state management"""
        if territory_id not in self._territories:
            return False

        old_territory = self._current_territory
        self._current_territory = territory_id

        # Record navigation history
        self._navigation_history.append({
            "from_territory": old_territory,
            "to_territory": territory_id,
            "timestamp": datetime.now().isoformat(),
            "context": context
        })
        return True
```

### Integration Pipeline

#### Slack → Spatial → Workflow Flow
```python
class SlackSpatialMapper:
    """Convert Slack events to spatial objects"""

    async def map_message_to_spatial_event(self, slack_event: Dict[str, Any],
                                         room: Room,
                                         attention_attractor: Optional[AttentionAttractor] = None) -> SpatialEvent:
        """Map Slack message to spatial event"""
        coordinates = SpatialCoordinates(
            territory_id=slack_event["team"],
            room_id=slack_event["channel"],
            object_id=slack_event["ts"]
        )

        # Determine event type from content analysis
        event_type = self._classify_event_type(slack_event["text"])

        return SpatialEvent(
            event_type=event_type,
            coordinates=coordinates,
            content=slack_event["text"],
            timestamp=datetime.fromtimestamp(float(slack_event["ts"])),
            attention_attractor=attention_attractor
        )

# Workflow Integration
class SpatialWorkflowIntegration:
    """Connect spatial events to Piper workflows"""

    async def create_workflow_from_spatial_event(self, spatial_event: SpatialEvent,
                                               attention_event: AttentionEvent) -> Dict[str, Any]:
        """Create Piper workflow with spatial context enrichment"""
        workflow_context = {
            "spatial_trigger": {
                "event_type": spatial_event.event_type,
                "coordinates": spatial_event.coordinates.to_slack_reference(),
                "urgency": attention_event.urgency_level,
                "requires_immediate_response": attention_event.urgency_level > 0.7
            },
            "attention_metadata": {
                "source": attention_event.source.value,
                "intensity": attention_event.base_intensity,
                "keywords": attention_event.keywords
            }
        }
        return workflow_context
```

### Quality Implementation Standards

#### TDD Integration Testing
```python
# Tests written FIRST, expected to FAIL initially
async def test_slack_help_request_creates_piper_task_workflow(
    spatial_mapper, workspace_navigator, attention_model,
    mock_workflow_factory, mock_orchestration_engine
):
    """Complete OAuth → Spatial → Workflow → Attention integration test"""
    # Test validates complete end-to-end spatial intelligence pipeline
    # 52 comprehensive integration tests covering all scenarios
```

### Usage Guidelines

- **Spatial Consistency**: Maintain coherent spatial metaphors across all interactions
- **Attention Management**: Use multi-factor scoring (proximity, urgency, relationships)
- **Memory Persistence**: Enable cross-session spatial learning and pattern recognition
- **Multi-Territory Support**: Handle complex multi-workspace scenarios with intelligent prioritization
- **Performance Requirements**: <100ms spatial processing for real-time responsiveness

### Anti-Patterns

- ❌ Treating events as abstract data without spatial context
- ❌ Ignoring temporal attention decay and emotional dimensions
- ❌ Not maintaining persistent spatial memory across sessions
- ❌ Complex spatial metaphors that don't match user mental models
- ❌ Single-workspace assumptions in multi-territory environments

### Benefits

- **Embodied AI Experience**: Natural spatial navigation and environmental awareness
- **Intelligent Attention**: Context-aware prioritization with decay algorithms
- **Pattern Learning**: Automatic behavior adaptation from interaction history
- **Scalable Architecture**: Supports multiple workspaces with persistent memory
- **Workflow Integration**: Seamless connection between spatial events and Piper workflows

## 21. TDD Integration Testing Pattern

### Purpose

Apply Test-Driven Development (TDD) methodology to integration testing, ensuring component interactions are validated through failing tests first, then implementation.

### Implementation

```python
class TestOAuthSpatialIntegration:
    """Test OAuth flow integration with spatial system initialization"""

    async def test_oauth_success_initializes_spatial_territory(self, oauth_handler, spatial_agent):
        """Test that successful OAuth initializes spatial territory"""
        # Arrange
        oauth_response = {
            "access_token": "xoxb-test-token",
            "team": {"id": "T123456", "name": "Test Workspace"}
        }

        # Act
        spatial_territory = oauth_handler.initialize_spatial_territory(oauth_response)

        # Assert
        assert spatial_territory.territory_id == "T123456"
        assert spatial_territory.type == TerritoryType.WORKSPACE

# TDD Process:
# 1. Write failing test first
# 2. Run test to see it fail (verification of test validity)
# 3. Verify components work together (integration validation)
# 4. Make test pass (implementation validation)
```

### Usage Guidelines

- Write failing tests FIRST for each component interaction
- Run tests to see them fail (verification of test validity)
- Verify components work together (integration validation)
- Make tests pass (implementation validation)
- Use comprehensive mocking for external dependencies
- Test both success and error scenarios

### Anti-Patterns

- ❌ Writing tests after implementation
- ❌ Not verifying test failures before implementation
- ❌ Insufficient mocking of external dependencies
- ❌ Testing only happy path scenarios

### Benefits

- Ensures integration points are properly designed
- Validates component contracts and interfaces
- Prevents integration issues through early testing
- Maintains high test coverage for complex interactions

Each pattern addresses specific architectural concerns while maintaining overall system coherence and enabling future evolution.

---

_Last Updated: July 27, 2025_

## Revision Log

- **July 27, 2025**: Added Spatial Metaphor Integration Pattern (#20) and TDD Integration Testing Pattern (#21) for Slack integration with comprehensive spatial metaphor processing and 52 integration tests
- **July 27, 2025**: Added LLM Placeholder Instruction Pattern (#19) to prevent hallucination in AI-generated content
- **July 21, 2025**: Added Configuration Access Pattern (#18) implementing ADR-010 layer-appropriate configuration management
- **July 16, 2025**: Added Background Task Error Handling Pattern (#17) for safe background task execution
- **July 09, 2025**: Added vertical resize feature to chat window for improved usability
- **June 29, 2025**: Added Repository Domain Model Conversion Pattern (#13) and Async Relationship Eager Loading Pattern (#14) for PM-011 GitHub integration
- **June 28, 2025**: Added Internal Task Handler Pattern (#11) and Repository Context Enrichment Pattern (#12) for GitHub integration
