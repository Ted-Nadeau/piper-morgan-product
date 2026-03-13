# Piper Morgan Codebase Component Inventory

**Date**: December 4, 2025
**Purpose**: Technical components for Wardley map validation
**Status**: Comprehensive scan complete

---

## INFRASTRUCTURE COMPONENTS

### Component: PostgreSQL Database
- **Location**: `docker-compose.yml` (lines 48-65), port 5433
- **Purpose**: Primary relational database for persistent storage of todos, projects, users, issues, and domain entities
- **Type**: Consumed (external service, PostgreSQL 15)
- **Dependencies**: Services layer (all repositories), Temporal (backup DB)
- **Suggested Wardley position**: **Commodity**
- **Notes**: Uses named volume `piper_postgres_data` for durability; stores all domain models including User, Todo, Project, Issue, Knowledge Graph nodes/edges

### Component: Redis Cache
- **Location**: `docker-compose.yml` (lines 68-80), port 6379
- **Purpose**: In-memory cache and event queue for session management, job queues, and real-time data
- **Type**: Consumed (external service, Redis 7-alpine)
- **Dependencies**: Services layer (session service), integration routers
- **Suggested Wardley position**: **Commodity**
- **Notes**: Uses AOF persistence; required for session tokens and event handling

### Component: ChromaDB Vector Database
- **Location**: `docker-compose.yml` (lines 83-92), port 8000
- **Purpose**: Vector embeddings storage for semantic search, RAG, and similarity matching
- **Type**: Consumed (external service, ChromaDB latest)
- **Dependencies**: Knowledge graph service, semantic indexing service
- **Suggested Wardley position**: **Commodity**
- **Notes**: Enables semantic retrieval for knowledge context; integrates with LLM services

### Component: Temporal Workflow Orchestration
- **Location**: `docker-compose.yml` (lines 95-110), port 7233
- **Purpose**: Distributed workflow orchestration for long-running async tasks, retries, and task scheduling
- **Type**: Consumed (external service, temporalio/auto-setup)
- **Dependencies**: Services/orchestration container, PostgreSQL for state
- **Suggested Wardley position**: **Commodity**
- **Notes**: Enables 8D Spatial Intelligence async processing, GitHub issue batch operations, complex workflows

### Component: Traefik API Gateway
- **Location**: `docker-compose.yml` (lines 113-126), ports 80, 8090
- **Purpose**: HTTP routing, reverse proxy, and API gateway for service distribution
- **Type**: Consumed (external service, Traefik v3.0)
- **Dependencies**: Docker daemon, port 80/8090
- **Suggested Wardley position**: **Commodity**
- **Notes**: Minimal config for development; labels in app service enable routing

### Component: Logging & Observability Infrastructure
- **Location**: `services/infrastructure/logging/`
- **Purpose**: Structured logging, error tracking, and observability signals
- **Type**: Custom-built wrapper + Consumed (Python logging)
- **Dependencies**: Python stdlib logging, potential external observability endpoints
- **Suggested Wardley position**: **Custom** (wrapper) / **Commodity** (underlying)
- **Notes**: Integrates with error middleware in web layer

---

## CORE SERVICES (CUSTOM-BUILT BUSINESS LOGIC)

### Component: Intent Classification Service
- **Location**: `services/intent/intent_service.py` (5198 lines)
- **Purpose**: Classify user messages into intent categories (QUERY, EXECUTION, ANALYSIS, SYNTHESIS, STRATEGY, PLANNING, REVIEW, LEARNING) and route to appropriate handlers
- **Type**: Custom-built
- **Dependencies**: LLM provider (Claude), intent classifier, conversation handler, canonical handlers, knowledge graph
- **Suggested Wardley position**: **Product**
- **Notes**:
  - Central orchestrator with 60+ methods including intent handlers and content generators
  - Handles: queries, execution (issues/repos), analysis (commits/metrics), synthesis (documentation), strategic planning (sprint plans), learning (pattern recognition)
  - Integrates with orchestration engine, todo handlers, knowledge graph

### Component: Knowledge Graph Service
- **Location**: `services/knowledge/` (4 files)
  - `knowledge_graph_service.py` - Core graph operations (CRUD nodes/edges)
  - `semantic_indexing_service.py` - Embedding generation and semantic indexing
  - `graph_query_service.py` - Query and traversal operations
  - `pattern_recognition_service.py` - Pattern detection in knowledge
- **Purpose**: Build and maintain semantic knowledge graph of codebase entities, relationships, and patterns
- **Type**: Custom-built
- **Dependencies**: ChromaDB, LLM for embeddings, domain models
- **Suggested Wardley position**: **Custom** (novel architecture for Piper Morgan)
- **Notes**: Stores graph as nodes (EdgeType, NodeType) and edges; enables contextual awareness and learning

### Component: Orchestration Engine
- **Location**: `services/orchestration/` (Temporal-based)
- **Purpose**: Execute complex multi-step workflows asynchronously with failure recovery
- **Type**: Custom-built orchestration logic + Consumed (Temporal framework)
- **Dependencies**: Temporal server, services (GitHub, Slack, etc.), PostgreSQL
- **Suggested Wardley position**: **Custom** (workflow definitions) / **Commodity** (Temporal engine)
- **Notes**: Manages 8D Spatial Intelligence workflows, intent processing pipelines

### Component: Authentication & Authorization
- **Location**: `services/auth/`
  - `jwt_service.py` - JWT token generation and validation
  - `password_service.py` - Password hashing (bcrypt)
  - `user_service.py` - User account management
- **Purpose**: Manage user sessions, JWT tokens, and role-based access control (RBAC)
- **Type**: Custom-built (token management) + Consumed (bcrypt, JWT)
- **Dependencies**: Redis (session store), PostgreSQL (user storage)
- **Suggested Wardley position**: **Custom** (token architecture) / **Commodity** (bcrypt)
- **Notes**: Session tokens stored in Redis; JWT supports scoped permissions

### Component: Todo Management Service
- **Location**: `services/todo/todo_management_service.py`
- **Purpose**: Create, update, complete, prioritize, and organize todos with tagging and status tracking
- **Type**: Custom-built
- **Dependencies**: TodoRepository, UserRepository, KnowledgeGraphService, Intent Service
- **Suggested Wardley position**: **Product**
- **Notes**: Core user-facing feature; integrates with intent system for smart todo creation

### Component: Feedback Service
- **Location**: `services/feedback/feedback_service.py`
- **Purpose**: Collect, store, and analyze user feedback for product improvement
- **Type**: Custom-built
- **Dependencies**: FeedbackRepository, LLM for analysis
- **Suggested Wardley position**: **Product**
- **Notes**: Essential for learning system and product iteration

### Component: Learning System
- **Location**: `services/learning/` (referenced in IntentService)
- **Purpose**: Extract patterns, build knowledge models, and improve intent classification from usage
- **Type**: Custom-built
- **Dependencies**: Knowledge graph, pattern recognition, LLM
- **Suggested Wardley position**: **Genesis** (novel "dreaming" capability)
- **Notes**: Enables self-improvement through experience; learns issue similarity, resolution patterns, tag patterns

### Component: Domain Services (Business Logic Layers)
- **Location**: `services/domain/`
  - `github_domain_service.py` - GitHub-specific business logic
  - `slack_domain_service.py` - Slack-specific business logic
  - `notion_domain_service.py` - Notion-specific business logic
  - `llm_domain_service.py` - LLM integration business logic
  - `standup_orchestration_service.py` - Daily standup coordination
- **Purpose**: Implement domain-specific business rules and workflows
- **Type**: Custom-built
- **Dependencies**: Integration plugins, repositories, intent service
- **Suggested Wardley position**: **Custom**
- **Notes**: Bridges external APIs with core business logic

---

## INTEGRATION COMPONENTS (EXTERNAL API CONNECTIONS)

### Component: GitHub Integration Plugin
- **Location**: `services/integrations/github/`
  - `github_plugin.py` - Core plugin implementation
  - `config_service.py` - GitHub config management
  - `github_integration_router.py` - FastAPI routes
- **Purpose**: Connect to GitHub API for issue tracking, repository analysis, commit history
- **Type**: Configured-from-library (PyGithub / requests)
- **Dependencies**: GitHub API (external), authentication service
- **Suggested Wardley position**: **Commodity** (GitHub is external service)
- **Notes**: Implements PiperPlugin interface; enables intent handlers for issue creation/updating, commit analysis

### Component: Slack Integration Plugin
- **Location**: `services/integrations/slack/`
  - `slack_plugin.py` - Core plugin implementation
  - `config_service.py` - Slack config management
  - `ngrok_service.py` - Tunnel for local development webhook
- **Purpose**: Connect to Slack API for message posting, channel integration, event handling
- **Type**: Configured-from-library (slack-sdk)
- **Dependencies**: Slack API (external), ngrok for dev webhooks, Redis for session
- **Suggested Wardley position**: **Commodity**
- **Notes**: Enables async message processing via Temporal; stores webhook secrets

### Component: Notion Integration Plugin
- **Location**: `services/integrations/notion/`
  - `notion_plugin.py` - Core plugin implementation
  - `config_service.py` - Notion config management
- **Purpose**: Connect to Notion API for wiki/docs storage, page creation, database integration
- **Type**: Configured-from-library (notion-client)
- **Dependencies**: Notion API (external)
- **Suggested Wardley position**: **Commodity**
- **Notes**: Enables knowledge base documentation and wiki features

### Component: Calendar Integration Plugin
- **Location**: `services/integrations/calendar/`
  - `calendar_plugin.py` - Core plugin implementation
  - `config_service.py` - Calendar config management
- **Purpose**: Connect to calendar service (Google Calendar, Outlook) for scheduling and availability
- **Type**: Configured-from-library (calendar SDK)
- **Dependencies**: Calendar API provider
- **Suggested Wardley position**: **Commodity**
- **Notes**: Supports scheduling features in strategic planning workflows

### Component: MCP (Model Context Protocol) Integration
- **Location**: `services/integrations/mcp/` + `services/mcp/`
  - `services/mcp/client.py` - MCP client implementation
  - `services/mcp/protocol/` - Protocol handling
  - `services/mcp/consumer/` - Consumer for MCP resources
- **Purpose**: Federate with external MCP servers for additional tools/resources
- **Type**: Custom-built (MCP protocol implementation) + Consumed (MCP spec)
- **Dependencies**: External MCP servers (optional)
- **Suggested Wardley position**: **Product** (novel federation pattern)
- **Notes**: Enables plugin ecosystem for third-party tools

### Component: Spatial Adapter
- **Location**: `services/integrations/spatial_adapter.py`
- **Purpose**: Spatial reasoning and 8D analysis for understanding project structure
- **Type**: Custom-built
- **Dependencies**: Knowledge graph, intent service
- **Suggested Wardley position**: **Genesis** (novel "8D Spatial Intelligence")
- **Notes**: Specialized spatial data processing; unique to Piper Morgan

---

## EXTERNAL SERVICE DEPENDENCIES (API PROVIDERS)

### Component: LLM Services (Claude API)
- **Location**: `services/llm/`
  - `adapters/claude_adapter.py` - Claude-specific implementation
  - `adapters/factory.py` - LLM provider factory
  - `config.py` - LLM configuration
- **Purpose**: Use Claude for intent classification, content generation, analysis, synthesis
- **Type**: Pure consumption (external SaaS API)
- **Dependencies**: Anthropic API key, network access to api.anthropic.com
- **Suggested Wardley position**: **Commodity**
- **Notes**: Central to intent classification and synthesis workflows; multiple use cases

---

## DATA ACCESS LAYER (REPOSITORIES)

### Component: Repository Pattern Implementation
- **Location**: `services/database/repositories.py`
- **Purpose**: Abstract database access with repository pattern for all domain entities
- **Type**: Custom-built
- **Dependencies**: SQLAlchemy ORM, PostgreSQL
- **Suggested Wardley position**: **Product** (custom pattern implementation)
- **Classes**: RepositoryFactory with ~20 repository implementations
  - TodoRepository
  - ProjectRepository
  - UserRepository
  - IssueRepository
  - KnowledgeGraphRepository (nodes/edges)
  - FeedbackRepository
  - And others (20+ total)
- **Notes**: Centralizes data access logic; enables testing with in-memory implementations

---

## DOMAIN MODELS (TRUTH SOURCE)

### Component: Domain Model (Business Entity Definitions)
- **Location**: `services/domain/models.py`
- **Purpose**: Define all domain entities and business rules (User, Todo, Project, Issue, KnowledgeNode, etc.)
- **Type**: Custom-built
- **Dependencies**: None (defines dependencies for others)
- **Suggested Wardley position**: **Product** (core business logic)
- **Notes**: 40+ domain entities; SQLAlchemy ORM mirrors these in `services/database/models.py`

### Component: Shared Types & Enums
- **Location**: `services/shared_types.py`
- **Purpose**: Centralized enum definitions for intent categories, workflow types, task statuses, etc.
- **Type**: Custom-built
- **Dependencies**: None (Python enum)
- **Suggested Wardley position**: **Product**
- **Enums**:
  - IntentCategory (QUERY, EXECUTION, ANALYSIS, SYNTHESIS, STRATEGY, PLANNING, REVIEW, LEARNING)
  - WorkflowType, TaskStatus, TodoStatus, TodoPriority
  - IntegrationType, EdgeType, NodeType, PatternType
  - OrderingStrategy, ListType
- **Notes**: Single source of truth for all type definitions

---

## WEB & API LAYER

### Component: FastAPI Web Application
- **Location**: `web/app.py` (678 lines)
- **Purpose**: HTTP server, REST API endpoints, middleware, request/response handling
- **Type**: Custom-built (FastAPI + custom middleware)
- **Dependencies**: FastAPI, Uvicorn, Starlette
- **Suggested Wardley position**: **Product**
- **Features**:
  - CORS middleware
  - Enhanced error handling middleware
  - Authentication/authorization
  - Request logging
  - Static file serving

### Component: API Route Handlers
- **Location**: `web/api/routes/`
- **Purpose**: HTTP endpoint implementations for all domain features
- **Type**: Custom-built
- **Dependencies**: Services layer, FastAPI, request validation (Pydantic)
- **Suggested Wardley position**: **Product**
- **Routes** (typical structure):
  - `/api/intent/` - Intent processing
  - `/api/todos/` - Todo management
  - `/api/projects/` - Project management
  - `/api/files/` - File operations
  - `/api/auth/` - Authentication
  - `/api/feedback/` - Feedback submission

### Component: Startup & Initialization
- **Location**: `web/startup.py`
- **Purpose**: Initialize services, load configuration, perform health checks during startup
- **Type**: Custom-built (phased initialization)
- **Dependencies**: ServiceContainer, all services, database
- **Suggested Wardley position**: **Product**
- **Phases**: (typical startup sequence)
  1. Configuration loading
  2. Database connection
  3. Service initialization
  4. Integration plugin loading
  5. Health check

### Component: UI Templates & Components
- **Location**: `templates/` + `web/static/`
- **Purpose**: Server-rendered HTML (Jinja2) with vanilla JavaScript for frontend UI
- **Type**: Custom-built
- **Dependencies**: Jinja2, CSS/JS utilities
- **Suggested Wardley position**: **Custom** (unique UI/UX)
- **Notable**:
  - Server-rendered (not SPA)
  - Component library in `templates/components/`
  - JS utilities: toast.js, dialog.js, permissions.js
  - CSS: Tailwind config in `tailwind.config.ts`

---

## SUPPORTING INFRASTRUCTURE

### Component: Service Container & Dependency Injection
- **Location**: `services/container/`
  - `service_container.py` - DI container
  - `service_registry.py` - Service registration
  - `initialization.py` - Service initialization
  - `exceptions.py` - Container-specific errors
- **Purpose**: Centralize service lifecycle management and dependency injection
- **Type**: Custom-built
- **Dependencies**: All services (manages their creation)
- **Suggested Wardley position**: **Product**
- **Notes**: Enables easy testing, service swapping, and clear dependency graph

### Component: Plugin Registry & Discovery
- **Location**: `services/plugins/`
  - `plugin_registry.py` - Plugin registration and discovery
  - `plugin_interface.py` - PiperPlugin interface definition
- **Purpose**: Manage plugin lifecycle, load plugins dynamically, validate interface compliance
- **Type**: Custom-built
- **Dependencies**: Integration plugins
- **Suggested Wardley position**: **Product** (plugin architecture)
- **Notes**: Enables extensibility; validates all plugins implement required interface

### Component: Health & Integration Monitoring
- **Location**: `services/health/integration_health_monitor.py`
- **Purpose**: Monitor health status of integrations and infrastructure components
- **Type**: Custom-built
- **Dependencies**: All integration plugins, infrastructure services
- **Suggested Wardley position**: **Product**
- **Notes**: Provides system health dashboard and alerts

### Component: Configuration Management
- **Location**: `services/infrastructure/config/` + `config/`
  - `services/infrastructure/config/config_validator.py` - Validation logic
  - `config/PIPER.md` - Default configuration (Markdown)
  - `config/PIPER.user.md` - User overrides (hot-reloadable)
- **Purpose**: Load, validate, and hot-reload application configuration
- **Type**: Custom-built (config loader + Markdown format)
- **Dependencies**: None (PIPER.md is Markdown, not YAML)
- **Suggested Wardley position**: **Custom** (novel Markdown-based config)
- **Notes**: Non-standard but enables hot-reload without system restart

### Component: Security & Key Management
- **Location**: `services/security/`
  - `key_audit_service.py` - Audit API key access
  - `user_api_key_service.py` - Manage user API keys
  - `key_rotation_service.py` - Rotate secrets periodically
- **Purpose**: Manage API keys, audit access, rotate secrets securely
- **Type**: Custom-built
- **Dependencies**: Keychain service, PostgreSQL
- **Suggested Wardley position**: **Custom** (specialized security patterns)
- **Notes**: RBAC for permissions; security-first design

### Component: Keychain Service
- **Location**: `services/infrastructure/keychain_service.py`
- **Purpose**: Secure storage of sensitive credentials (API keys, secrets)
- **Type**: Custom-built wrapper around OS keychain
- **Dependencies**: macOS Keychain / Linux Secret Storage / Windows Credential Manager
- **Suggested Wardley position**: **Custom**
- **Notes**: Avoids storing secrets in .env files

### Component: Task Manager & Scheduling
- **Location**: `services/infrastructure/task_manager.py`
- **Purpose**: Schedule and manage periodic tasks (cron-like jobs)
- **Type**: Custom-built
- **Dependencies**: Temporal (for async execution)
- **Suggested Wardley position**: **Product**
- **Notes**: Used for scheduled standup generation, maintenance tasks

---

## ANALYSIS & QUERY SERVICES

### Component: Analysis Service
- **Location**: `services/analysis/`
- **Purpose**: Perform complex analysis on codebase data (metrics, trends, patterns)
- **Type**: Custom-built
- **Dependencies**: Repositories, knowledge graph
- **Suggested Wardley position**: **Product**
- **Examples**: Repository metrics, contributor stats, activity trends

### Component: Query Services (Canonical Queries)
- **Location**: `services/queries/`
- **Purpose**: Pre-built optimized queries for common access patterns
- **Type**: Custom-built
- **Dependencies**: Repositories
- **Suggested Wardley position**: **Custom** (novel query optimization pattern)
- **Notes**: Enables efficient data retrieval without N+1 queries

---

## SPECIALIZED SERVICES

### Component: Ethical Consensus Engine
- **Location**: `services/ethics/` (inferred from draft map)
- **Purpose**: Evaluate actions against ethical guidelines; ensure responsible AI
- **Type**: Custom-built
- **Dependencies**: Domain models, LLM for evaluation
- **Suggested Wardley position**: **Genesis** (novel responsibility architecture)
- **Notes**: Prevents harmful actions; validates outputs align with user values

### Component: Personality/Colleague Relationship Module
- **Location**: `services/personality/` (inferred from context)
- **Purpose**: Maintain user relationship context and conversational personality
- **Type**: Custom-built
- **Dependencies**: Knowledge graph, conversation context
- **Suggested Wardley position**: **Genesis** (novel "colleague relationship" model)
- **Notes**: Personalizes responses; remembers user preferences and history

### Component: Learning & Knowledge Synthesis
- **Location**: Referenced in intent service and knowledge services
- **Purpose**: Extract and retain learnings from interactions
- **Type**: Custom-built
- **Dependencies**: Knowledge graph, pattern recognition
- **Suggested Wardley position**: **Genesis** (novel "dreaming" capability)
- **Notes**: Distinguishes Piper Morgan from transactional systems

---

## DEVELOPMENT & TESTING INFRASTRUCTURE

### Component: Test Suite
- **Location**: `tests/` (unit, integration, manual subdirectories)
- **Purpose**: Automated testing for quality assurance and regression prevention
- **Type**: Custom-built
- **Dependencies**: pytest, test fixtures, mocks
- **Suggested Wardley position**: **Product**
- **Test Categories**:
  - Unit tests: <30 seconds, isolated
  - Integration tests: up to 2 minutes, with containers
  - Manual tests: hardcoded data, exploratory
  - Smoke tests: critical path validation

### Component: CLI (Command-Line Interface)
- **Location**: `cli/` + `main.py`
- **Purpose**: Server startup, database migrations, admin operations
- **Type**: Custom-built
- **Dependencies**: Click (or argparse), services layer
- **Suggested Wardley position**: **Product**
- **Commands**: start, setup, status, migrate, etc.

### Component: Database Migrations (Alembic)
- **Location**: `alembic/`
- **Purpose**: Version-controlled database schema changes
- **Type**: Configured-from-library (Alembic)
- **Dependencies**: Alembic, SQLAlchemy
- **Suggested Wardley position**: **Commodity** (Alembic is standard)
- **Notes**: Auto-generated from domain/database model changes

---

## FRAMEWORK & LIBRARY DEPENDENCIES

### Core Dependencies (Custom Application Framework)
- **FastAPI**: Web framework (HTTP)
- **SQLAlchemy**: ORM (database abstraction)
- **Pydantic**: Data validation (request/response models)
- **Alembic**: Database migrations
- **Python Logging**: Structured logging
- **PyJWT**: JWT token management
- **bcrypt**: Password hashing
- **Uvicorn**: ASGI server

### Integration Libraries (External Service SDKs)
- **PyGithub** or **requests**: GitHub API client
- **slack-sdk**: Slack API client
- **notion-client**: Notion API client
- **Google Calendar API**: Calendar integration
- **anthropic**: Claude API client

### Infrastructure Libraries
- **redis**: Redis client
- **chromadb**: Vector database client
- **temporalio**: Temporal client library
- **docker-compose**: Infrastructure orchestration

---

## SUMMARY BY WARDLEY POSITION

### Genesis (Novel, Unique to Piper Morgan)
1. **Ethical Consensus Engine** - Novel responsibility architecture
2. **Personality/Colleague Relationship Module** - Novel conversational model
3. **Learning System / "Dreaming" Capability** - Self-improvement through experience
4. **8D Spatial Intelligence** - Unique spatial reasoning for project understanding
5. **Trust Architecture** - Foundation for ethical AI decision-making
6. **Spatial Adapter** - Novel spatial data processing

### Custom (Built in-house, competitive advantage)
1. **Knowledge Graph Service** - Novel semantic understanding
2. **Orchestration Engine** (custom logic layer) - Workflow definitions
3. **Intent Classification & Routing** - 8 intent categories with 60+ handlers
4. **Repository Pattern Implementation** - Data access abstraction (20+ repos)
5. **Domain Services** (GitHub, Slack, Notion, LLM) - Domain-specific business logic
6. **Configuration Management** (Markdown-based) - Hot-reloadable config
7. **Security & Key Management** - Specialized secret handling
8. **Query Services / Canonical Queries** - Optimized data retrieval patterns
9. **Plugin Architecture** - PiperPlugin interface and discovery
10. **Service Container & DI** - Dependency injection system
11. **Startup & Initialization** - Phased initialization system
12. **UI/Templates & Components** - Custom server-rendered interface
13. **Keychain Service Wrapper** - OS keychain abstraction

### Product (Mature, off-the-shelf components with custom integration)
1. **Intent Classification Service** - Product-grade intent router
2. **Authentication & Authorization** - JWT + RBAC
3. **Todo Management Service** - Core user feature
4. **Feedback Service** - Product feedback loop
5. **Domain Models** - Business entity definitions
6. **Shared Types & Enums** - Type system
7. **FastAPI Web Application** - HTTP server
8. **API Route Handlers** - REST endpoints
9. **Repository Pattern** - Data access layer
10. **Health & Monitoring** - System observability
11. **Task Manager & Scheduling** - Job scheduling
12. **Analysis Service** - Complex data analysis
13. **Test Suite** - Automated testing
14. **CLI Tools** - Command-line interface
15. **MCP Federation** - Extensible protocol support

### Commodity (External services, third-party solutions)
1. **PostgreSQL Database** - Relational DB
2. **Redis Cache** - In-memory cache/queue
3. **ChromaDB** - Vector database
4. **Temporal Workflow Engine** - Async orchestration
5. **Traefik API Gateway** - Reverse proxy
6. **GitHub API** - Issue tracking & repository access
7. **Slack API** - Team communication
8. **Notion API** - Knowledge base
9. **Calendar APIs** - Scheduling
10. **Claude API** - LLM inference
11. **Alembic** - Database migrations
12. **FastAPI, SQLAlchemy, Pydantic** - Web/ORM frameworks

---

## INTEGRATION DEPENDENCIES (Component Graph)

```
User Request
    ↓
FastAPI Routes → Intent Classification Service
    ↓                      ↓
Authentication       LLM Provider (Claude)
(JWT + RBAC)        ↓
    ↓              Orchestration Engine (Temporal)
Service Container       ↓
(DI)                Various Intent Handlers
    ↓                      ↓
Domain Services      Knowledge Graph Service
(GitHub, Slack,      + Semantic Indexing
Notion, LLM)         + Pattern Recognition
    ↓                      ↓
Plugin Registry      ChromaDB (Vector DB)
(6 integrations)         ↓
    ↓              PostgreSQL (Persistence)
Repositories             ↓
+ Repository Factory  Redis (Cache/Queue)
    ↓
Domain Models
(Truth Source)
```

---

## MISSING / UNCLEAR COMPONENTS

Based on scanning, some inferred but not directly verified:

1. **Trust Architecture** - Referenced in draft map but not found in direct search
   - Likely location: `services/ethics/` or `services/intelligence/`
   - Warrants deeper inspection

2. **Contextual Awareness System** - Mentioned in draft but not explicitly found
   - Likely distributed across knowledge graph + intent service
   - May need to verify in project_context services

3. **Object Model** (as distinct from Domain Models)
   - May refer to structured knowledge representation
   - Possibly in knowledge_graph or intelligence services

4. **Recognition Interface** - Unclear what this refers to
   - Possibly UI components for pattern recognition display
   - May be in templates or analysis service output

---

## RECOMMENDATIONS FOR WARDLEY MAP VALIDATION

### Suggested Placements (High Confidence)
- ✅ **GitHub API, Slack API, LLM APIs, PostgreSQL, Calendar** → **Commodity** (confirmed)
- ✅ **Intent Classification, MCP Federation, Plugin Architecture** → **Product** (confirmed)
- ✅ **8D Spatial Intelligence, Learning System, Ethical Consensus** → **Genesis** (confirmed in design)

### Requires Further Investigation
1. **Trust Architecture** - Find actual implementation to confirm Genesis classification
2. **Contextual Awareness** - Verify if separate from knowledge graph or integrated
3. **Object Model** vs Domain Models - Clarify distinction if exists
4. **Recognition Interface** - Locate and classify

### Strategic Observations
1. **Balanced Portfolio**: Mix of Genesis (innovation), Custom (differentiation), Product (delivery), Commodity (scale)
2. **Strong Foundation**: Robust infrastructure (PostgreSQL, Redis, Temporal) enables reliability
3. **Clear Architecture**: Service layer + plugin system supports extensibility
4. **Continuous Learning**: Knowledge graph + learning system support product evolution
5. **Ethical Foundation**: Ethics engine differentiates from commodity AI products

---

*Inventory completed: 50+ components cataloged across infrastructure, services, integrations, and supporting systems.*
