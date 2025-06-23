# Piper Morgan 1.0 - Pattern Catalog

## Overview

This catalog documents the key architectural and design patterns used in Piper Morgan. Each pattern includes its purpose, implementation details, usage guidelines, and anti-patterns to avoid.

## 1. Repository Pattern

### Purpose
Encapsulate data access logic and provide a clean interface between domain models and database implementation.

### Implementation
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

class ProjectRepository(BaseRepository):
    """Domain-specific repository"""
    
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, ProductDB)
    
    async def list_active_projects(self) -> List[Project]:
        result = await self.db.execute(
            select(ProductDB).where(ProductDB.is_archived == False)
        )
        db_projects = result.scalars().all()
        return [self._to_domain(p) for p in db_projects]
    
    def _to_domain(self, db_model: ProductDB) -> Project:
        """Convert database model to domain model"""
        # Conversion logic here
```

### Usage Guidelines
- One repository per aggregate root
- Repository methods return domain models, not database models
- Keep business logic out of repositories
- Use repositories for all data access

### Anti-patterns to Avoid
- ❌ Direct database access from services
- ❌ Business logic in repositories
- ❌ Exposing database models outside repository
- ❌ Generic repositories without domain methods

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

## 3. Query Service Pattern (CQRS-lite)

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
| Use Query Service When | Use Workflow When |
|------------------------|-------------------|
| Reading data | Changing state |
| Single repository access | Multiple system coordination |
| Synchronous response expected | Background processing needed |
| No side effects | Side effects required |

### Anti-patterns to Avoid
- ❌ Forcing queries through workflow pattern
- ❌ State changes in query services
- ❌ Complex business logic in queries
- ❌ Cross-repository transactions in queries

## 4. Domain-First Database Pattern

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

## 5. Event-Driven Communication Pattern

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

## 6. Plugin Architecture Pattern

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

## 7. Context Resolution Pattern

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

## 8. Adapter Pattern for LLM Providers

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

## 9. Session Management Pattern

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

## 10. Error Handling Pattern (API Contract)

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
    "details": { /* optional context */ }
  }
}
```

### Status Code Guidelines
| Code | Usage | Example |
|------|-------|---------|
| 200 | Success | Request completed successfully |
| 400 | Bad Request | Invalid JSON format or missing required fields |
| 404 | Not Found | Project, workflow, or resource doesn't exist |
| 422 | Validation Error | Valid format but business rules violated |
| 429 | Rate Limited | Too many requests from client |
| 500 | Server Error | Unexpected internal error |
| 502 | Service Unavailable | External service (GitHub, Claude) unavailable |

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

## Summary

These patterns form the architectural foundation of Piper Morgan:

1. **Repository Pattern** - Clean data access
2. **Factory Pattern (Stateless)** - Safe object creation
3. **Query Service Pattern** - Optimized reads
4. **Domain-First Database** - Business-driven schema
5. **Event-Driven Communication** - Loose coupling
6. **Plugin Architecture** - Extensible integrations
7. **Context Resolution** - Smart defaults
8. **Adapter Pattern** - Provider abstraction
9. **Session Management** - Resource safety
10. **Error Handling Pattern** - User-friendly API responses

Each pattern addresses specific architectural concerns while maintaining overall system coherence and enabling future evolution.

---
*Last Updated: June 21, 2025*

## Revision Log
- **June 21, 2025**: Added Error Handling Pattern (#10) and consolidated error-pattern-guide.md content