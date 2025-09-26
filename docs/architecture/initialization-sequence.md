# Orchestration System Initialization Sequence

## Overview

This document describes the step-by-step initialization process for the orchestration system, including QueryRouter setup, database connections, and component integration.

## Initialization Flow Diagram

```
Application Startup
       ↓
OrchestrationEngine.__init__(llm_client=None)
       ↓
Component Setup (WorkflowFactory, IntentEnricher)
       ↓
QueryRouter Lazy Initialization (on-demand)
       ↓
Session-Aware Service Wrappers
       ↓
System Ready
```

## Detailed Initialization Steps

### Step 1: OrchestrationEngine Creation
**File**: `services/orchestration/engine.py`
**Entry Point**: `OrchestrationEngine.__init__(llm_client: Optional[LLMClient] = None)`

```python
class OrchestrationEngine:
    def __init__(self, llm_client: Optional[LLMClient] = None):
        # Use global llm_client if none provided
        if llm_client is None:
            from services.llm.clients import llm_client as global_llm_client
            llm_client = global_llm_client

        self.llm_client = llm_client
```

**Key Dependencies Loaded**:
- LLM Client (global or provided)
- WorkflowFactory for workflow creation
- IntentEnricher for intent processing
- Multi-Agent integration components

### Step 2: Core Component Initialization
**Location**: `OrchestrationEngine.__init__()` method

```python
# PM-039 Factory Pattern: Initialize WorkflowFactory and registry
from .workflow_factory import WorkflowFactory
self.factory = WorkflowFactory()
self.workflows = {}

# QueryRouter will be initialized on-demand using async session pattern
self.query_router = None

self.intent_enricher = IntentEnricher(llm_client)
self.logger = structlog.get_logger()

# Initialize Multi-Agent integration
self.workflow_integration = WorkflowIntegration()
self.session_integration = SessionIntegration()
self.performance_monitor = PerformanceMonitor()
```

**Components Initialized**:
1. **WorkflowFactory**: Handles workflow creation and management
2. **IntentEnricher**: Processes and enriches user intents
3. **Multi-Agent Integration**: Workflow, session, and performance monitoring
4. **QueryRouter**: Initialized lazily on first access

### Step 3: QueryRouter Lazy Initialization
**Location**: `OrchestrationEngine.get_query_router()` method
**Purpose**: Initialize QueryRouter with session-aware wrappers on-demand

```python
async def get_query_router(self) -> QueryRouter:
    """Get QueryRouter, initializing on-demand with session-aware wrappers"""
    if self.query_router is None:
        from services.queries.conversation_queries import ConversationQueryService
        from services.queries.session_aware_wrappers import (
            SessionAwareFileQueryService,
            SessionAwareProjectQueryService,
        )

        # Initialize QueryRouter with session-aware services
        self.query_router = QueryRouter(
            project_query_service=SessionAwareProjectQueryService(),
            conversation_query_service=ConversationQueryService(),
            file_query_service=SessionAwareFileQueryService(),
        )
        self.logger.info("QueryRouter initialized with session-aware wrappers")

    return self.query_router
```

**QueryRouter Dependencies**:
- **SessionAwareProjectQueryService**: Handles project-related queries
- **ConversationQueryService**: Manages conversation queries
- **SessionAwareFileQueryService**: File system query operations
- **AsyncSessionFactory**: Database session management (handled by wrappers)

### Step 4: Session-Aware Service Pattern
**Purpose**: Handle database sessions automatically within services

**Pattern Implementation**:
```python
# Session-aware services handle their own database connections
# No need to pass session parameters to QueryRouter
class SessionAwareProjectQueryService:
    async def query(self, ...):
        async with AsyncSessionFactory.session_scope() as session:
            # Use session for database operations
            return await self._execute_query(session, ...)
```

**Benefits**:
- Automatic session management
- No session parameter passing required
- Clean separation of concerns
- Proper connection cleanup

### Step 5: System Integration Points
**Purpose**: Connect all orchestration components

**Integration Architecture**:
```
OrchestrationEngine
├── LLMClient (global or injected)
├── WorkflowFactory (immediate initialization)
├── IntentEnricher (immediate initialization)
├── QueryRouter (lazy initialization)
│   ├── SessionAwareProjectQueryService
│   ├── ConversationQueryService
│   └── SessionAwareFileQueryService
└── Multi-Agent Integration
    ├── WorkflowIntegration
    ├── SessionIntegration
    └── PerformanceMonitor
```

## Common Initialization Patterns

### Lazy Loading Pattern
```python
# Components initialized on first access
async def get_query_router(self) -> QueryRouter:
    if self.query_router is None:
        self.query_router = self._create_query_router()
    return self.query_router
```

**Benefits**:
- Faster startup time
- Resources allocated only when needed
- Better memory efficiency

### Dependency Injection Pattern
```python
# Optional dependencies with fallback to global
def __init__(self, llm_client: Optional[LLMClient] = None):
    if llm_client is None:
        from services.llm.clients import llm_client as global_llm_client
        llm_client = global_llm_client
    self.llm_client = llm_client
```

### Session-Aware Wrapper Pattern
```python
# Services handle their own database sessions
class SessionAwareService:
    async def operation(self, params):
        async with AsyncSessionFactory.session_scope() as session:
            return await self._do_operation(session, params)
```

## Error Handling During Initialization

### LLM Client Initialization Failures
- **Symptom**: OrchestrationEngine creation fails with import error
- **Cause**: Global LLM client not available
- **Resolution**: Provide explicit LLM client or ensure global client is initialized

### QueryRouter Initialization Errors
- **Symptom**: `get_query_router()` fails with session errors
- **Cause**: Database connectivity issues in session-aware wrappers
- **Resolution**: Verify database connection and AsyncSessionFactory configuration

### Component Dependency Errors
- **Symptom**: AttributeError during component access
- **Cause**: Dependency import failures or circular imports
- **Resolution**: Check import paths and dependency availability

## Performance Considerations

### Initialization Time
- **Cold start**: ~50ms (without QueryRouter)
- **QueryRouter initialization**: ~100ms (first access)
- **Total warm-up**: ~150ms

### Memory Usage
- **Base orchestration**: ~5MB
- **With QueryRouter**: ~12MB
- **Full workflow context**: ~20MB

### Optimization Strategies
- Lazy loading reduces startup time
- Session-aware wrappers minimize connection overhead
- Component reuse within request scope

## Development Guidelines

### Adding New Components
1. Add component initialization to `__init__()` method
2. Consider lazy loading for heavy components
3. Use dependency injection for external dependencies
4. Add proper error handling and logging
5. Update this documentation

### Testing Initialization
```python
# Standard initialization test pattern
def test_orchestration_initialization():
    engine = OrchestrationEngine()
    
    # Verify components initialized
    assert engine.factory is not None
    assert engine.intent_enricher is not None
    assert engine.llm_client is not None
    
    # Test lazy loading
    assert engine.query_router is None  # Not yet initialized

@pytest.mark.asyncio
async def test_query_router_initialization():
    engine = OrchestrationEngine()
    
    # Trigger lazy initialization
    query_router = await engine.get_query_router()
    assert query_router is not None
    assert engine.query_router is not None  # Now cached
```

## Troubleshooting

### Slow Initialization
- Check database connection latency
- Verify component dependencies are available
- Consider lazy loading for heavy components

### Initialization Failures
- Review error logs for specific component failures
- Verify all required dependencies are installed
- Check configuration parameters

### Memory Issues
- Monitor component memory usage
- Consider component lifecycle management
- Use profiling tools to identify memory leaks

---

*This document is maintained alongside the orchestration system. Update when components or initialization flow changes.*
