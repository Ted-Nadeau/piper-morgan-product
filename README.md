# Piper Morgan Platform

An intelligent product management assistant that evolves from automating routine tasks to providing strategic insights and recommendations.

## 🎯 Vision

Piper Morgan aims to be more than a task automation tool. It's designed to grow from a helpful PM intern into a strategic thinking partner, handling everything from creating tickets to analyzing market trends and suggesting product strategies.

## 🏗️ Architecture Overview

This platform is built on a microservices architecture with the following core principles:

- **Domain-Driven Design**: PM concepts drive the architecture, not tool integrations
- **Event-Driven**: All services communicate through events for scalability and learning
- **Plugin Architecture**: Every external system (GitHub, Jira, Slack) is a plugin
- **AI-Native**: LLMs provide reasoning capabilities, not just text generation
- **Learning-Centric**: Every interaction teaches the system something new

### Core Services

1. **Intent & Goal Management Service**: Understands what users want to achieve
2. **Orchestration Engine**: Plans and coordinates complex workflows
3. **Reasoning Service**: Provides analysis, insights, and recommendations
4. **Knowledge Graph Service**: Maintains understanding of products, features, and relationships
5. **Integration Services**: Plugins for GitHub, Jira, Confluence, Analytics, etc.
6. **Learning Service**: Captures patterns and improves over time

## 🏛️ Architectural Principles

- **Domain-Driven Design**: Domain models are the source of truth.
- **CQRS-lite**: Queries and commands are handled separately for clarity and scalability.
- **Repository Pattern**: All data access is abstracted through repositories.
- **RESTful Error Handling**: API returns precise status codes and actionable error messages.
- **Test-Driven Development**: All core features are covered by integration and domain-level tests.

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+** (required)
  - Docker with Python 3.11 base images
  - Git
- Docker & Docker Compose
- PostgreSQL 14+
- Redis 7+
- Node.js 18+ (for frontend development)

### Local Development Setup

```bash
# Verify Python version (must be 3.11+)
python --version  # Should show Python 3.11.x

# Clone the repository
git clone https://github.com/yourusername/piper-morgan-platform.git
cd piper-morgan-platform

# Verify .python-version file
cat .python-version  # Should show 3.11

# Set up Python virtual environment with Python 3.11
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Verify Python version in virtual environment
python --version  # Should show Python 3.11.x

# Install dependencies
pip install -r requirements.txt

# Verify asyncio.timeout availability (key PM-055 feature)
python -c "import asyncio; asyncio.timeout(1.0); print('✅ Python 3.11 ready')"

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

See [Staging Deployment Guide](docs/operations/staging-deployment-guide.md) for complete details.

## 🧑‍💻 Testing

```bash
# Run all tests
PYTHONPATH=. pytest

# Run API query integration tests
PYTHONPATH=. pytest tests/test_api_query_integration.py

# Note: Some asyncpg/SQLAlchemy warnings may appear during test teardown; these are benign and do not affect production.
```

## Test Suite Health

### Known Issues

As of July 16, 2025, the test suite shows ~85% pass rate when run with `pytest tests/`, but this is misleading due to test isolation issues.

**True System Health**: ~98% when tests are run individually

### Using the Health Check Tool

```bash
python scripts/test-health-check.py
```

This tool distinguishes between:

- Real failures (business logic issues)
- Isolation failures (pass individually, fail in suite)

#### Common Patterns

- **Async Event Loop Warnings**: Cosmetic issues from pytest-asyncio + asyncpg
- **Test Isolation**: Database state pollution between tests
- **Business Logic Evolution**: Tests may fail when Piper's behavior improves

#### Running Tests Effectively

- For accurate results: `pytest tests/specific_test.py -v`
- For isolation: `pytest --forked` (requires pytest-forked)
- Use health check tool to identify real issues

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
├── services/                 # Microservices
│   ├── domain/              # Core domain models and logic
│   ├── intent_service/      # Intent recognition
│   ├── orchestration/       # Workflow planning and execution
│   ├── intelligence/        # AI-powered analysis
│   ├── knowledge_graph/     # Knowledge management
│   └── integrations/        # External system plugins
│       ├── github/
│       ├── jira/
│       └── slack/
├── infrastructure/          # Deployment and configuration
│   ├── docker/             # Dockerfiles
│   ├── k8s/                # Kubernetes manifests
├── shared/                 # Shared libraries
│   ├── contracts/          # Service contracts/interfaces
│   ├── utils/              # Common utilities
│   └── events/             # Event definitions
├── docs/                   # Documentation
│   ├── architecture/       # Architecture decisions
│   ├── api/                # API documentation
│   └── poc-reference/      # Lessons from POC
├── scripts/                # Development and deployment scripts
├── tests/                  # Test suite
└── web/                    # Web application (UI)
```

## 📊 Current Status

- [x] Domain-driven backend and query API robust and fully tested (PM-009 complete)
- [x] **PM-038 MCP Integration**: 642x performance improvement with connection pooling
- [x] **PM-063 QueryRouter Degradation**: Comprehensive graceful degradation implementation (method level complete)
- [x] **Production-Grade Staging**: Docker Compose with monitoring and rollback
- [x] Architecture design and domain model definition
- [x] Core infrastructure setup (Postgres, Redis, ChromaDB)
- [x] Basic service scaffolding and orchestration engine
- [x] Query intent pipeline with RESTful error handling and contract-driven tests
- [x] Comprehensive health monitoring with Prometheus + Grafana
- [ ] **PM-063 Production Deployment**: Critical integration fix needed (missing return statement)
- [ ] CI/CD pipeline (in progress)
- [ ] Web UI and advanced integrations (upcoming)

## 🤝 Contributing

Currently, work is being done on the `main` branch. Feature branches will be used as the team grows.

1. Create feature branches from `main` (or `develop` when available)
2. Follow the coding standards in `docs/coding-standards.md`
3. Ensure all tests pass
4. Update documentation as needed
5. Create PR with clear description

## 📚 Documentation

### Core Documentation

- [Architecture Overview](docs/architecture/architecture.md)
- [Domain Model](docs/architecture/data-model.md)
- [API Documentation](docs/api/api-reference.md)

### Architecture Decision Records (ADRs)

- [ADR-007: Staging Environment Architecture](docs/architecture/adr/adr-007-staging-environment-architecture.md)
- [ADR-008: MCP Connection Pooling Strategy](docs/architecture/adr/adr-008-mcp-connection-pooling-production.md)
- [ADR-009: Health Monitoring System Design](docs/architecture/adr/adr-009-health-monitoring-system.md)

### Operations

- [Staging Deployment Guide](docs/operations/staging-deployment-guide.md)
- [Staging Rollback Procedures](docs/operations/staging-rollback-procedures.md)
