# Architecture Overview

## System Architecture Status - June 19, 2025

```

┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACE LAYER                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  ✅ FastAPI Web Server     │  ✅ Web UI (DDD, TDD, resizable chat window) │  📋 Admin Interface    │
│  (Built & Running)         │  (Built & Working)    │  (Not Yet Designed)   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                          APPLICATION LAYER                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  ✅ Intent Classifier       │  ✅ Workflow Factory    │  📋 Learning Engine   │
│  (Built & Working)          │  (Built & Working)      │  (Not Yet Designed)   │
│                             │                         │                       │
│  🔄 Query Service           │  ✅ Orchestration       │  📋 Analytics Engine  │
│  (Being Added)              │  Engine                 │  (Not Yet Designed)   │
│                             │  (Working E2E)          │                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                            SERVICE LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  ✅ Domain Models           │  ✅ Workflow Service    │  📋 Feedback Service  │
│  (Built)                    │  (Built & Working)      │  (Not Yet Designed)   │
│                             │                         │                       │
│  ✅ Event System            │  ✅ GitHub Integration  │  📋 Analytics Agent   │
│  (Built)                    │  (Fully Integrated)     │  (Not Yet Designed)   │
│                             │  (Issue Creation Working)│                      │
│  ✅ Knowledge Base          │  ✅ Document Processor  │  📋 Report Generator  │
│  (Built & Working)          │  (Built & Working)      │  (Not Yet Designed)   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           DATA LAYER                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│  ✅ PostgreSQL              │  ✅ ChromaDB            │  ✅ Redis              │
│  (Domain-First Schema)      │  (Deployed & Working)   │  (Deployed & Working)  │
│                             │                         │                       │
│  ✅ Domain Persistence      │  ✅ Vector Storage      │  ✅ Event Queue        │
│  (Working)                  │  (Working)              │  (Working)             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        INFRASTRUCTURE LAYER                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  ✅ Docker Compose          │  ✅ Traefik Gateway     │  ✅ Temporal           │
│  (Deployed & Running)       │  (Deployed & Running)   │  (Deployed & Running)  │
│                             │                         │                       │
│  ✅ Service Discovery       │  ✅ Load Balancing      │  ✅ Workflow Engine    │
│  (Working)                  │  (Working)              │  (Working)             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                       EXTERNAL INTEGRATIONS                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  ✅ Claude API              │  ✅ GitHub API          │  📋 Slack/Teams       │
│  (Connected & Working)      │  (Fully Integrated)    │  (Not Yet Designed)   │
│                             │  (Issue Creation Working)│                     │
│  ✅ OpenAI API              │  📋 Jira API            │  📋 Analytics APIs    │
│  (Connected & Working)      │  (Not Yet Designed)     │  (Planned Q3 2025)    │
│                             │                         │  - Datadog            │
│                             │                         │  - New Relic          │
│                             │                         │  - Google Analytics   │
└─────────────────────────────────────────────────────────────────────────────┘

## Planned: MCP Integration Layer (Q3 2025)

### Overview
Model Context Protocol (MCP) integration will enable Piper Morgan to discover and consume external tools and knowledge sources through a standardized protocol.

### Integration Architecture
```

Current: API → Service → Agent → External System
Future: API → Service → MCP Adapter → MCP Server → External System

```

### Phased Approach
- **Phase 1**: MCP Consumer (4-6 weeks) - Enable consumption of external MCP services
- **Phase 2**: Hybrid Integration (2-3 weeks) - Bridge existing agents to MCP
- **Phase 3**: MCP Provider (Future) - Expose Piper capabilities as MCP services

### Target Use Cases
- Federated knowledge base search
- Multi-tool project context resolution
- Dynamic tool discovery and integration

> **[TODO: Update the architecture diagram above to show the planned MCP layer, marked as "Planned Q3 2025"]**

## Legend

- **✅ Built & Working**: Implemented and operational
- **🔄 In Progress**: Designed and partially implemented
- **📋 Not Started/Designed**: Planned for future phases

## Query vs Command Pattern

### Command Flow (State Changes)

```

User Intent → Intent Classifier → EXECUTION/SYNTHESIS → Workflow Factory → Orchestration Engine → External Systems
↓
State Changes

```

### Query Flow (Data Retrieval)

```

User Intent → Intent Classifier → QUERY → Query Service → Repository → Direct Data Access
↓
Read-Only Results

````

### Decision Criteria

- **Use Workflows for**: Multi-step processes, state changes, external system updates, complex orchestration
- **Use Queries for**: Data retrieval, listings, searches, read-only operations, simple aggregations

### Benefits

- **Performance**: Queries bypass workflow overhead
- **Clarity**: Clear separation of concerns
- **Scalability**: Can optimize read and write paths independently
- **Simplicity**: No workflow complexity for simple data fetches

## CQRS-lite Query Pattern Implementation

### Overview

The CQRS-lite pattern separates read operations (queries) from write operations (commands) in the Piper Morgan system. This provides clear architectural boundaries, better performance for simple data fetches, and prevents forcing query-like operations into complex workflow patterns.

### Implementation

### Intent Classification

Queries are identified through intent classification:

```python

python
# Intent classifier recognizes QUERY category for read-only operations
if intent.category == IntentCategory.QUERY:
# Route to QueryRouter
    result = await query_router.route_query(intent)
else:
# Route to WorkflowFactory for commands
    workflow = await workflow_factory.create_from_intent(intent)

````

### Query Router

The `QueryRouter` dispatches QUERY intents to appropriate query services:

```python

python
class QueryRouter:
    async def route_query(self, intent: Intent) -> Any:
        if intent.action == "list_projects":
            return await self.project_queries.list_active_projects()
        elif intent.action == "get_project":
            return await self.project_queries.get_project_by_id(project_id)
# ... other query actions

```

### Query Services

Query services provide read-only access to domain data:

```python

python
class ProjectQueryService:
    async def list_active_projects(self) -> List[Project]:
        return await self.repo.list_active_projects()

    async def get_project_by_id(self, project_id: str) -> Optional[Project]:
        return await self.repo.get_by_id(project_id)

```

### Supported Query Actions

- `list_projects` - List all active projects
- `get_project` - Get specific project by ID
- `get_default_project` - Get the default project
- `find_project` - Find project by name
- `count_projects` - Count active projects

## Web UI: DDD-Compliant Response Rendering (2025)

The web UI is now implemented as a DDD-compliant, test-driven interface. All bot message rendering and response handling is unified in a shared domain module (`bot-message-renderer.js`), ensuring:

- Consistent user experience across all response types
- Separation of domain logic from UI/infrastructure
- Full test coverage via TDD (unit and integration tests)
- Easy extensibility for new message types and workflows

**Key Features:**

- Unified renderer for all bot messages (success, error, thinking)
- Modular, reusable domain logic
- Real-time feedback and error handling
- Markdown rendering with `marked.js` (battle-tested library)

**Architecture Impact:**

- UI layer now fully reflects DDD principles
- All message formatting and business rules live in the domain module, not the presentation layer
- TDD process ensures maintainability and reliability

## Current Architecture Strengths

### 1. Solid Infrastructure Foundation

All core infrastructure services are deployed and operational:

- **PostgreSQL**: Primary data store with domain-first schema (SQLAlchemy model-driven)
- **Redis**: Event queue and caching
- **ChromaDB**: Vector storage for knowledge base (85+ documents indexed)
- **Temporal**: Workflow orchestration engine
- **Traefik**: API gateway and load balancing

### 2. Working Intelligence Layer

Core AI capabilities are operational:

- **Intent Classification**: Natural language understanding with context (95%+ accuracy on PM tasks)
- **Knowledge Integration**: Document search and context injection
- **LLM Integration**: Claude and OpenAI APIs connected and working
- **Multi-turn Conversations**: Clarifying questions system operational

### 3. Domain-Driven Design

Clean separation of concerns with PM concepts driving architecture:

- **Domain Models**: Product, Feature, Stakeholder, WorkItem, Intent, Project
- **Event System**: Asynchronous communication patterns
- **Plugin Architecture**: External systems as modular components
- **Repository Pattern**: Clean data access layer
- **Domain-First Database**: Schema generated from domain models

## Recent Architectural Decisions (June 2025)

### 1. Stateless WorkflowFactory

Adopted per-call pattern for context injection rather than stateful factories. Benefits:

- Explicit dependencies
- Better testability
- Concurrency safety
- Follows functional programming principles

### 2. CQRS-lite Pattern

Introduced Query Service pattern to separate reads from writes:

- Commands go through workflows
- Queries go directly to services
- Prevents forcing simple reads into complex workflow patterns

### 3. Project Context Resolution

Implemented sophisticated project resolution with:

- Explicit project IDs take precedence
- Session-based project memory
- LLM-powered inference from context
- Graceful ambiguity handling

### 4. Domain-First Database Schema

Moved from hardcoded SQL to SQLAlchemy model-driven schema:

- Database schema generated from domain models
- Eliminates manual schema drift
- Ensures consistency between domain and persistence layers

### 5. Internal Task Handler Pattern (June 2025)

Discovered and documented during GitHub integration:

- OrchestrationEngine uses internal method handlers instead of separate task handler classes
- Pattern: `self.task_handlers = {TaskType.X: self._method_x}`
- Benefits: Simpler architecture, fewer files, direct access to engine state
- Example: `TaskType.GITHUB_CREATE_ISSUE: self._create_github_issue`

### 6. Repository Context Enrichment Pattern (June 2025)

Implemented automatic repository lookup for GitHub workflows:

- Context enrichment happens in `create_workflow_from_intent`
- Non-blocking pattern: failures logged but don't break workflow creation
- Hierarchy: Project → Integration → Repository → Workflow Context
- Enables seamless "create a ticket" without specifying repository

### 7. Docker Best Practices (June 2025)

**Named Volumes (Recommended)**:

```yaml
volumes:
  piper_postgres_data:
    name: piper_postgres_data_v1 # Explicit versioned name
```

**Benefits**:

- Survives directory renames
- Managed by Docker
- Explicit versioning
- No path dependencies

**Avoid Bind Mounts for Databases**:

- Fragile with directory changes
- Path-dependent
- Can be lost during refactoring

**Lesson Learned**: PM-011 - Directory rename caused data loss with bind mounts

## Critical Gaps (Current Priority)

### 1. Basic Error Handling

**Status**: Not implemented
**Impact**: Users get technical errors instead of helpful messages
**Solution**: Implement comprehensive error handling with user-friendly messages

### 2. Web Chat Interface

**Status**: Not started
**Impact**: API-only interaction blocks user testing
**Solution**: Build simple Streamlit or FastAPI chat interface

### 3. Query/Command Separation

**Status**: Partially implemented (PM-009 query work in progress)
**Impact**: Some queries forced into workflow pattern
**Solution**: Complete Query Service implementation for LIST_PROJECTS and similar operations

## Architectural Decisions

### 1. Event-Driven Communication

All services communicate through events for:

- **Scalability**: Asynchronous processing
- **Learning**: Event history for pattern analysis
- **Reliability**: Retry and replay capabilities

### 2. Multi-LLM Strategy

Different models for different tasks:

- **Claude Opus**: Complex reasoning and analysis
- **Claude Sonnet**: Quick intent classification
- **OpenAI**: Embeddings and specialized tasks
- **Future**: Task-specific model selection

### 3. Plugin-Based Integrations

External systems as plugins for:

- **Modularity**: Independent development and testing
- **Flexibility**: Easy addition of new integrations
- **Maintenance**: Isolated failure and updates

## Evolution Path

### Phase 1 (Current - Q2 2025): Foundation + Basic Execution

**Status**: 100% Complete

- ✅ Infrastructure deployment and configuration
- ✅ Core domain models and persistence
- ✅ Intent classification with high accuracy
- ✅ Basic workflow execution (working end-to-end)
- ✅ GitHub integration functional (issue creation and analysis automated)
- ✅ SUMMARIZE task handler domain model consistency fixed
- ✅ Workflow context handling robustness improved
- ✅ Database persistence with domain-first schema
- 🔄 PM-009 multi-project support (context resolution done, queries in progress)
- 🔄 Query/Command pattern introduction
- 📋 Basic error handling and user feedback
- 📋 Web chat interface

### Phase 2 (Next - Q3 2025): Intelligence Enhancement

**Goals**: Complete CQRS, activate learning, enhance workflows

- Complete Query/Command separation
- Implement feedback-based learning
- Multi-repository workflow support
- Enhanced knowledge search with relationship awareness
- Basic analytics and reporting
- Production monitoring and hardening
- Analytics platform integration (Datadog, New Relic, GA)
- Meeting transcript processing and visualization
- Advanced knowledge graph with relationship mapping
- Visual content analysis foundation

### Phase 3 (Future - Q4 2025+): Advanced Capabilities

**Vision**: Autonomous assistance and strategic insights

- Predictive analytics from PM patterns
- Cross-system orchestration (Jira, Slack, Analytics)
- Autonomous workflow optimization
- Strategic recommendations
- Multi-team support and knowledge sharing

## Technical Debt & Risks

### Immediate Risks

1. **Import Dependencies**: Some circular dependency risks in orchestration layer
2. **Error Handling**: No user-friendly error messages

### Medium-Term Considerations

1. **Performance**: Vector search needs optimization for larger knowledge bases
2. **Security**: API key rotation and audit logging needed
3. **Monitoring**: Observability gaps for debugging production issues

### Long-Term Architecture Evolution

1. **Microservices**: May need service decomposition as complexity grows
2. **Multi-Tenancy**: Current design assumes single organization
3. **Federated Learning**: Cross-organization knowledge sharing capabilities

## Success Metrics

### Current Performance

- **Intent Classification**: 95%+ accuracy on common PM tasks
- **Workflow Completion**: Working end-to-end with placeholder handlers
- **Knowledge Relevance**: 70%+ (needs tuning)
- **Response Time**: 2-4 seconds average

### Target Metrics (Q3 2025)

- **Query Response Time**: <1 second
- **Workflow Success Rate**: 95%+ with real handlers
- **Knowledge Relevance**: 90%+
- **User Satisfaction**: 4.5/5 rating
- **Error Handling**: 90%+ errors with user-friendly messages
- **Meeting Processing**: 90%+ action item extraction accuracy
- **Analytics Integration**: Daily automated insights generation
- **Knowledge Discovery**: 50%+ improvement in cross-project insight finding
- **Autonomous Operations**: 30%+ routine tasks self-managed

---

_Last Updated: June 28, 2025_

## Revision Log

- **June 28, 2025**: GitHub integration complete, added Internal Task Handler and Repository Context Enrichment patterns, updated Service Layer and External Integrations, removed placeholder handler risk, updated Evolution Path
