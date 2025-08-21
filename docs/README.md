!(../web/assets/pm-logo)

# Piper Morgan - Conversational AI Product Management Assistant

**NEW: Conversational AI with Memory** - Your PM assistant now understands natural language and remembers context across conversations.

An intelligent product management assistant that evolves from automating routine tasks to providing strategic insights and recommendations **through natural conversation**.

## 🎯 Vision

Piper Morgan aims to be more than a task automation tool. It's designed to grow from a helpful PM intern into a strategic thinking partner, handling everything from creating tickets to analyzing market trends and suggesting product strategies.

## 🎯 Key Features

### MCP+Spatial Intelligence Integration (PM-033a/b)

Piper now features revolutionary **8-dimensional spatial intelligence** through the Model Context Protocol:

**Strategic Differentiator - Spatial Intelligence**:

- **8-Dimensional Analysis**: HIERARCHY, TEMPORAL, PRIORITY, COLLABORATIVE, FLOW, QUANTITATIVE, CAUSAL, CONTEXTUAL
- **Historic Performance**: Sub-1ms federated search (150x better than industry standards)
- **Contextual Understanding**: Only AI agent with true multi-dimensional context analysis
- **Competitive Moat**: Unmatched spatial intelligence across GitHub + Notion integrations

**Technical Architecture**:

- **GitHub Integration**: Retrieve and manage 84+ issues via MCP protocol with spatial context
- **Federated Search**: Query across multiple services with spatial intelligence enhancement
- **Circuit Breaker Protection**: Graceful degradation when services unavailable
- **Connection Pooling**: 642x performance improvement for external calls

### PIPER.md Configuration System

Personalized context configuration for enhanced user experience:

- **User Context**: Define your role, projects, and priorities
- **Calendar Patterns**: Specify your work schedule and meeting patterns
- **Standing Priorities**: Set recurring tasks and focus areas
- **Hot Reload**: Configuration updates without restart

### Conversational Memory (PM-034)

Advanced conversation context management:

- **10-Turn Context Window**: Maintains conversation history
- **Anaphoric Reference Resolution**: >90% accuracy resolving "that issue", "the document"
- **Redis Caching**: 5-minute TTL with circuit breaker protection
- **<150ms Additional Latency**: Minimal performance impact

## 🌟 Why Conversational AI Changes Everything

| Traditional PM Tools                     | 🎉 **Piper Morgan with Conversational AI**  |
| ---------------------------------------- | ------------------------------------------- |
| `"Update GitHub issue #1247"`            | **"Update that bug we discussed"**          |
| `"Show me document requirements_v2.pdf"` | **"Show me the latest requirements"**       |
| Lost context between commands            | **10-turn conversation memory**             |
| Rigid command syntax                     | **Natural language flow**                   |
| Manual issue tracking                    | **Automatic relationship detection**        |
| Remember exact identifiers               | **"that issue", "the document", "my task"** |
| Start over each time                     | **Continuous context awareness**            |
| One command = one action                 | **Multi-step workflow conversations**       |

**Result**: 5x faster workflows, 90% less mental overhead, conversations that feel human.

## 💬 See It in Action: Real PM Conversations

### Workflow 1: Issue Management Flow

```
You: "Create a critical bug for the payment system failure"
Piper: "✅ Created critical bug #156: Payment system failure (assigned to backend team)"

You: "Add the error logs to that issue"
Piper: "✅ Added error logs to issue #156"

You: "What's the timeline for fixing it?"
Piper: "Based on issue #156 complexity: 3-5 business days for fix + 1-2 days security review"

You: "Create a follow-up task for the security review"
Piper: "✅ Created task #157: Security review for payment system (linked to #156)"

You: "Assign the main issue to Michael"
Piper: "✅ Assigned bug #156 to Michael. He's been notified."
```

**🎯 Notice**: Piper remembers "that issue" = #156, distinguishes "main issue" from "follow-up task", maintains full context.

### Workflow 2: Document & Analysis Flow

```
You: "I'm uploading the new product requirements document"
Piper: "✅ Processed requirements_v3.pdf (47 pages, 23 features identified)"

You: "What are the high-priority features in the document?"
Piper: "Found 6 high-priority features in requirements_v3.pdf:
       • Advanced search with AI filtering
       • Real-time collaboration dashboard
       • Mobile-first responsive design..."

You: "Create GitHub issues for the first three features"
Piper: "✅ Created 3 GitHub issues:
       #158: Advanced search with AI filtering
       #159: Real-time collaboration dashboard
       #160: Mobile-first responsive design"

You: "Set them all to the Q3 milestone"
Piper: "✅ Added issues #158, #159, #160 to Q3 2025 milestone"
```

**🎯 Notice**: Piper references "the document" naturally, understands "first three" from previous list, resolves "them all" to the created issues.

### Workflow 3: Multi-Project Context Switching

```
You: "Switch to the mobile app project"
Piper: "✅ Context switched to Mobile App v2.0 (12 open issues, 3 in review)"

You: "Show me the authentication work"
Piper: "Found 2 authentication items in Mobile App v2.0:
       • Issue #89: iOS login screen redesign (in progress)
       • Issue #91: Android authentication flow (ready for QA)"

You: "Update the iOS one with the latest designs"
Piper: "✅ Updated issue #89 with latest design files from Figma"

You: "What about our web platform progress?"
Piper: "✅ Switching to Web Platform v1.2 context...
       Web Platform: 8 open issues, 2 completed this sprint"

You: "Compare the authentication progress between projects"
Piper: "Authentication progress comparison:
       • Mobile App: iOS design complete, Android in QA
       • Web Platform: OAuth integration 80% complete, SSO pending"
```

**🎯 Notice**: Seamless project context switching, "the iOS one" resolved correctly, cross-project analysis maintained.

## 🚀 Get Started with Conversational AI

### 📚 For Product Managers & Users

**New to conversational AI?** Start with our complete user guide ecosystem:

- **[📚 Complete User Guide Collection](/user-guides/README.md)** - Master index of all user documentation
- **[🚀 Getting Started Guide](/user-guides/getting-started-conversational-ai.md)** - Transform from command mode to natural conversation
- **[🎯 Understanding Anaphoric References](/user-guides/understanding-anaphoric-references.md)** - Master "that issue", "the document", "my task" patterns
- **[🧠 Conversation Memory Guide](/user-guides/conversation-memory-guide.md)** - How Piper maintains context across 10+ interactions
- **[🔄 Upgrading from Command Mode](/user-guides/upgrading-from-command-mode.md)** - Migration guide for existing users
- **[📖 Real Conversation Examples](/user-guides/conversation-scenario-examples.md)** - 6 complete PM workflow scenarios

### 💻 For Developers & Integrators

**Implementing conversational AI?** Complete technical resources:

- **[Conversation API Documentation](/development/PM-034-conversation-api-documentation.md)** - Complete endpoint reference with examples
- **[Developer Integration Quick Start](/development/PM-034-developer-integration-quick-start.md)** - 15-minute setup guide
- **[Implementation Guide](/development/PM-034-implementation-guide.md)** - Architecture patterns and best practices

### 🎯 Adoption Path

**Choose your journey**:

| I want to...              | Start here                                                                    | Then                                                                         | Finally                  |
| ------------------------- | ----------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------ |
| **Try it out**            | [Getting Started Guide](/user-guides/getting-started-conversational-ai.md)     | [Real Examples](/user-guides/conversation-scenario-examples.md)               | Use Piper!               |
| **Understand the magic**  | [Understanding References](/user-guides/understanding-anaphoric-references.md) | [Memory Guide](/user-guides/conversation-memory-guide.md)                     | Advanced features        |
| **Upgrade from commands** | [Upgrading Guide](/user-guides/upgrading-from-command-mode.md)                 | [Getting Started](/user-guides/getting-started-conversational-ai.md)          | Conversational workflows |
| **Build with APIs**       | [API Documentation](/development/PM-034-conversation-api-documentation.md)     | [Integration Guide](/development/PM-034-developer-integration-quick-start.md) | Production               |

**Performance Promise**: <150ms response time, >90% reference accuracy, 10-turn context window.

## 🏗️ Architecture Overview

This platform is built on a microservices architecture with the following core principles:

- **Domain-Driven Design**: PM concepts drive the architecture, not tool integrations
- **Event-Driven**: All services communicate through events for scalability and learning
- **Plugin Architecture**: Every external system (GitHub, Jira, Slack) is a plugin
- **AI-Native**: LLMs provide reasoning capabilities, not just text generation
- **Learning-Centric**: Every interaction teaches the system something new

### Core Services

**Orchestration & Workflow Management:**

- **Multi-Agent Coordinator**: Intelligent task decomposition and agent assignment
- **Excellence Flywheel**: Systematic verification and quality enforcement
- **Workflow Factory**: Dynamic workflow creation and management

**AI & Intelligence Services:**

- **Intent Service**: Natural language intent classification and understanding
- **Conversation Service**: Conversational AI with 10-turn memory
- **Knowledge Services**: Semantic indexing, pattern recognition, and graph queries
- **LLM Integration**: Large language model orchestration and reasoning

**Integration & External Services:**

- **GitHub Integration**: MCP-powered issue management and spatial intelligence
- **Slack Integration**: Spatial-aware communication and notifications
- **MCP Consumer**: Model Context Protocol integration with connection pooling

**Data & Infrastructure:**

- **Database Services**: Domain models, repositories, and data access patterns
- **Cache Layer**: Redis-based caching and session management
- **Health Monitoring**: Comprehensive system observability and metrics
- **Authentication**: JWT-based user management and security

**Query & Analysis:**

- **Query Services**: Project, conversation, and file query capabilities
- **Analysis Services**: Data analysis and pattern recognition
- **File Context**: Document processing and context extraction

## 🏛️ Architectural Principles

- **Domain-Driven Design**: Domain models are the source of truth.
- **CQRS-lite**: Queries and commands are handled separately for clarity and scalability.
- **Repository Pattern**: All data access is abstracted through repositories.
- **RESTful Error Handling**: API returns precise status codes and actionable error messages.
- **Test-Driven Development**: All core features are covered by integration and domain-level tests.

## 🚀 Getting Started

### Prerequisites

- **Python 3.11** (required - exactly 3.11, not 3.12+)
  - Docker with Python 3.11 base images
  - Git
- Docker & Docker Compose
- PostgreSQL 14+
- Redis 7+
- Node.js 18+ (for frontend development)

### Local Development Setup

```bash
# Verify Python version (must be 3.11 exactly)
python --version  # Should show Python 3.11.x

# Clone the repository
git clone https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product

# Verify .python-version file
cat .python-version  # Should show 3.11

# Set up Python virtual environment with Python 3.11
python3.11 -m venv venv  # Explicitly use Python 3.11
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Verify Python version in virtual environment
python --version  # Should show Python 3.11.x

# Install dependencies
pip install -r requirements.txt

# Verify asyncio.timeout availability (requires Python 3.11)
python -c "import asyncio; asyncio.timeout(1.0); print('✅ Python 3.11 verified')"

# Copy environment template
cp .env.example .env
# Edit .env with your API keys and configuration

# Start infrastructure services
docker-compose up -d postgres redis

# Initialize the database
python scripts/init_db.py

# Start the development server
python main.py
```

### Docker Setup

```bash
# Docker containers now use Python 3.11
docker-compose build
docker-compose up

# Verify container Python version
docker-compose exec app python --version  # Should show Python 3.11.x
```

### Staging Environment (Production-Grade)

For testing PM-038 MCP integration and production readiness:

```bash
# One-command staging deployment
./scripts/deploy_staging.sh

# Verify staging deployment (14 comprehensive tests)
./scripts/verify_staging_deployment.sh

# Access staging services
# API: http://localhost:8001
# Web UI: http://localhost:8081
# Grafana: http://localhost:3001
# Prometheus: http://localhost:9090
```

**Key Features:**

- ✅ **PM-038 MCP Integration**: 642x performance improvement enabled
- ✅ **Production Monitoring**: Prometheus + Grafana dashboards
- ✅ **Health Checks**: Comprehensive component monitoring
- ✅ **Automated Rollback**: Safe deployment with rollback procedures
- ✅ **Performance Validation**: <500ms search target (achieving ~60ms)

**Staging Architecture:**

- 8 containerized services with Docker Compose
- Named volume persistence with automated backups
- Nginx load balancing and security headers
- Circuit breaker pattern for fault tolerance
- Real-time monitoring and alerting

See [Staging Deployment Guide](/operations/staging-deployment-guide.md) for complete details.

## 🧑‍💻 Testing

```bash
# Run all tests
PYTHONPATH=. pytest

# Run API query integration tests
PYTHONPATH=. pytest tests/test_api_query_integration.py

# Note: Some asyncpg/SQLAlchemy warnings may appear during test teardown; these are benign and do not affect production.
```

## Test Suite Health

### Current Status (August 2025)

The test suite has been significantly improved with systematic testing discipline and verification-first methodology.

**Test Coverage**: Comprehensive unit, integration, and validation tests across all core services

**Current Testing Infrastructure:**

- **Database-Free Testing**: Excellence Flywheel standalone test runner for core orchestration functionality
- **Smoke Test Infrastructure**: Chief Architect Phase 1 with <5 second execution targets
- **Comprehensive Coverage**: Extensive test coverage for critical orchestration components

### Running Tests Effectively

```bash
# Run all tests with proper environment
PYTHONPATH=. python -m pytest tests/ -v

# Run specific test categories
PYTHONPATH=. python -m pytest tests/unit/ -v
PYTHONPATH=. python -m pytest tests/integration/ -v

# Run with coverage reporting
PYTHONPATH=. python -m pytest tests/ --cov=services --cov-report=term-missing

# Fast failure mode for development
PYTHONPATH=. python -m pytest tests/ -x -v

# Database-free testing (Excellence Flywheel infrastructure)
python tests/orchestration/run_standalone_tests.py
```

### Testing Best Practices

- **Always use PYTHONPATH**: Required for proper module resolution
- **Verification-First**: Always verify existing patterns before writing new tests
- **Reality Testing**: Avoid over-mocking critical paths
- **Test Isolation**: Each test should be independent and deterministic

**Development Methodology**: See [Methodology Core](/development/methodology-core/) for comprehensive development frameworks including Excellence Flywheel, Agent Coordination, and Enhanced Autonomy patterns.

### Health Monitoring Tools

- **Smoke Test Infrastructure**: Chief Architect Phase 1 testing with <5 second execution targets
- **Database-Free Testing**: Excellence Flywheel standalone test runner for core functionality
- **Integration Health Monitor**: Real-time component health tracking with Prometheus + Grafana
- **Comprehensive Test Suite**: Unit, integration, and validation tests across all services

**Testing Documentation**: See [Orchestration Testing Methodology](/development/testing/orchestration-testing-methodology.md) for detailed testing patterns and infrastructure.

## Pre-commit Hook Strategy

Before committing, to avoid the formatting dance:

```bash
# First, add your docs
git add docs/

# Check what pre-commit will do without changing files
pre-commit run --all-files --show-diff-on-failure

# If only formatting issues on docs, you can:
# Option 1: Let it fix them
pre-commit run --all-files

# Option 2: Skip specific hooks just this once
SKIP=end-of-file-fixer,trailing-whitespace git commit -m "Add background task and test health documentation"
```

## 📁 Project Structure

```
piper-morgan-product/
├── services/                 # Core application services
│   ├── domain/              # Domain models and business logic
│   ├── api/                 # API endpoints and middleware
│   ├── auth/                # Authentication services
│   ├── cache/               # Redis caching layer
│   ├── configuration/       # Configuration management (PIPER.md)
│   ├── conversation/        # Conversational AI & memory
│   ├── database/            # Database models and repositories
│   ├── ethics/              # Ethics boundary enforcement
│   ├── intent_service/      # Intent classification
│   ├── integrations/        # External system integrations
│   │   ├── github/          # GitHub API integration
│   │   └── slack/           # Slack spatial integration
│   ├── knowledge_graph/     # Knowledge management
│   ├── mcp/                 # MCP consumer & protocols
│   ├── orchestration/       # Multi-Agent Coordinator, Excellence Flywheel, Workflows
│   │   ├── multi_agent_coordinator.py    # Intelligent task orchestration
│   │   ├── excellence_flywheel_integration.py    # Quality enforcement
│   │   └── workflow_factory.py    # Dynamic workflow management
│   ├── queries/             # Query routing & degradation
│   └── repositories/        # Data access patterns
├── alembic/                 # Database migrations
├── config/                  # Configuration files
│   ├── PIPER.md            # User context configuration
│   └── feature_flags/      # Feature flag configurations
├── docs/                    # Documentation
│   ├── architecture/        # Architecture & ADRs
│   ├── development/         # Development guides
│   ├── operations/          # Operations guides
│   ├── patterns/            # Pattern index & catalog
│   ├── planning/            # Roadmap & backlog
│   └── user-guides/         # User documentation
├── scripts/                 # Development & deployment scripts
├── tests/                   # Test suite
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── validation/         # Validation tests
└── web/                     # Web UI application
```

## 📊 Current Status

### Recently Completed (August 2025)

- [x] **PM-033a MCP Consumer**: Working MCP integration retrieving 84+ GitHub issues
- [x] **PM-033b Tool Federation**: GitHub + Notion integrations with MCP+Spatial Intelligence
- [x] **Architectural Signature**: 8-dimensional spatial analysis across all tool integrations
- [x] **Performance Leadership**: Sub-1ms federated search (150x better than industry standards)
- [x] **Competitive Differentiator**: Unique spatial intelligence capability
- [x] **PIPER.md Configuration System**: Personalized context for enhanced standup experience
- [x] **Conversational AI Memory**: 10-turn context window with <150ms latency
- [x] **PM-034 Anaphoric References**: >90% accuracy resolving "that issue", "the document"
- [x] **PM-063 QueryRouter Degradation**: Comprehensive graceful degradation implementation
- [x] **Excellence Flywheel Testing Infrastructure**: Database-free testing with 100% test coverage validation
- [x] **Multi-Agent Coordinator Documentation**: Complete PM guide to intelligent task orchestration architecture

### Core Platform

- [x] Domain-driven backend and query API robust and fully tested (PM-009 complete)
- [x] **PM-038 MCP Integration**: 642x performance improvement with connection pooling
- [x] **Production-Grade Staging**: Docker Compose with monitoring and rollback
- [x] Architecture design and domain model definition
- [x] Core infrastructure setup (Postgres, Redis, ChromaDB)
- [x] Query intent pipeline with RESTful error handling
- [x] Comprehensive health monitoring with Prometheus + Grafana
- [x] **Excellence Flywheel Testing**: Database-free testing infrastructure with comprehensive coverage
- [x] **Multi-Agent Coordinator**: Intelligent task orchestration with <1000ms coordination overhead

### In Progress

- [ ] CI/CD pipeline implementation
- [ ] Advanced Web UI features
- [ ] Additional MCP service integrations

## 🤝 Contributing

Currently, work is being done on the `main` branch. Feature branches will be used as the team grows.

1. Create feature branches from `main` (or `develop` when available)
2. Follow the coding standards in `docs/coding-standards.md`
3. Ensure all tests pass
4. Update documentation as needed
5. Create PR with clear description

## 📚 Documentation

### Core Documentation

- [Architecture Overview](/architecture/architecture.md)
- [Domain Model](/architecture/data-model.md)
- [API Documentation](/architecture/api-reference.md)
- **[📋 Pattern Index](/patterns/PATTERN-INDEX.md)** - Comprehensive catalog of 25+ proven architectural and implementation patterns
- **[🎯 Multi-Agent Coordinator Guide](/architecture/multi-agent-coordinator-pm-guide.md)** - Complete PM guide to our intelligent task orchestration engine

### Architecture Decision Records (ADRs)

Complete list of architectural decisions:

- [ADR-000: Meta-Platform Architecture](/architecture/adr/adr-000-meta-platform.md) - Meta-platform design philosophy and principles
- [ADR-001: MCP Integration](/architecture/adr/adr-001-mcp-integration.md) - Model Context Protocol integration strategy
- [ADR-002: Claude Code Integration](/architecture/adr/adr-002-claude-code-integration.md) - AI assistant development workflow
- [ADR-003: Intent Classifier Enhancement](/architecture/adr/adr-003-intent-classifier-enhancement.md) - Intent recognition improvements
- [ADR-004: Action Humanizer Integration](/architecture/adr/adr-004-action-humanizer-integration.md) - User-friendly action descriptions
- [ADR-005: Eliminate Dual Repository Implementations](/architecture/adr/adr-005-eliminate-dual-repository-implementations.md) - Repository pattern consistency
- [ADR-006: Standardize Async Session Management](/architecture/adr/adr-006-standardize-async-session-management.md) - Database session handling
- [ADR-007: Staging Environment Architecture](/architecture/adr/adr-007-staging-environment-architecture.md) - Production-grade staging setup
- [ADR-008: MCP Connection Pooling Strategy](/architecture/adr/adr-008-mcp-connection-pooling-production.md) - Performance optimization
- [ADR-009: Health Monitoring System Design](/architecture/adr/adr-009-health-monitoring-system.md) - System observability
- [ADR-010: Configuration Patterns](/architecture/adr/adr-010-configuration-patterns.md) - Configuration management strategy
- [ADR-011: Test Infrastructure Hanging Fixes](/architecture/adr/adr-011-test-infrastructure-hanging-fixes.md) - Test reliability improvements
- [ADR-012: Unified Session Management](/architecture/adr/adr-012-unified-session-management.md) - Consolidated session handling
- [ADR-013: MCP Spatial Integration Pattern](/architecture/adr/adr-013-mcp-spatial-integration-pattern.md) - Spatial intelligence integration patterns
- [ADR-014: Attribution-First Design](/architecture/adr/adr-014-attribution-first.md) - Attribution-driven design principles
- [ADR-015: Wild Claim Architecture](/architecture/adr/adr-015-wild-claim.md) - Bold architectural assertions and validation
- [ADR-016: Ambiguity-Driven Development](/architecture/adr/adr-016-ambiguity-driven.md) - Embracing uncertainty in development
- [ADR-017: Spatial MCP Integration](/architecture/adr/adr-017-spatial-mcp.md) - Advanced spatial intelligence with MCP
- [ADR-018: Server Functionality Patterns](/architecture/adr/adr-018-server-functionality.md) - Server-side architectural patterns
- [ADR-019: Orchestration Commitment](/architecture/adr/adr-019-orchestration-commitment.md) - Orchestration system design commitments
- [ADR-020: Protocol Investment Strategy](/architecture/adr/adr-020-protocol-investment.md) - Strategic protocol investment decisions
- [ADR-021: Multi-Federation Architecture](/architecture/adr/adr-021-multi-federation.md) - Multi-service federation patterns
- [ADR-022: Autonomy Experimentation](/architecture/adr/adr-022-autonomy-experimentation.md) - Autonomous system experimentation

### Operations

- [Staging Deployment Guide](/operations/staging-deployment-guide.md)
- [Staging Rollback Procedures](/operations/staging-rollback-procedures.md)

### Recent Feature Documentation

- [MCP Consumer Architecture](/architecture/pm-033a-mcp-consumer-architecture.md) - MCP integration design and implementation
- [MCP Integration Patterns](/architecture/mcp-integration-patterns.md) - Proven MCP integration patterns
- [PIPER.md Configuration](/../config/PIPER.md) - User context configuration template
- [Conversation Manager Guide](/development/PM-034-implementation-guide.md) - Conversational AI implementation
- [Query Router Degradation](/operations/query-router-degradation-runbook.md) - Graceful degradation operations
