# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Piper Morgan is an AI-powered Product Management Assistant platform that evolves from automating routine PM tasks to providing strategic insights. It's built with domain-driven design where PM concepts (Product, Feature, Intent, WorkItem) drive the technical architecture.

## Key Commands

### Development Setup
```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start infrastructure (PostgreSQL, Redis, ChromaDB, Temporal, Traefik)
docker-compose up -d

# Initialize database (only needed once)
python scripts/init_db.py

# Run main API server (port 8001)
python main.py

# Run web UI (port 8081)
cd web && python -m uvicorn app:app --reload --port 8081
```

### Testing
```bash
# Run all tests (always use PYTHONPATH)
PYTHONPATH=. pytest

# Run specific test file
PYTHONPATH=. pytest tests/test_api_query_integration.py

# Run tests for a specific component
PYTHONPATH=. pytest tests/test_intent_classification.py
```

### Common Development Tasks
```bash
# Check database connection
PYTHONPATH=. python -c "from services.database.connection import get_db_session; list(get_db_session())"

# Access PostgreSQL directly
docker exec -it piper-postgres psql -U piper -d piper_morgan

# View Redis cache
docker exec -it piper-redis redis-cli

# View logs
docker-compose logs -f [service_name]
```

## Architecture & Code Structure

### Core Design Patterns

1. **Domain-Driven Design**: All business logic flows from domain models in `services/database/models.py`. The database schema is generated from SQLAlchemy models, not the other way around.
   - **NO QUICK FIXES**: Always fix issues at the correct domain layer
   - **Layered Architecture**: Domain → Application → Infrastructure → Presentation
   - **Business logic belongs in domain services**, not UI or infrastructure layers

2. **CQRS-lite Pattern**: 
   - Read operations: `services/queries/` (QueryRouter handles all read-only operations)
   - Write operations: `services/orchestration/` (workflows and commands)

3. **Repository Pattern**: All data access through repositories in `services/repositories/`

4. **Workflow Orchestration**: 
   - Uses internal task handler pattern in `OrchestrationEngine`
   - Stateless `WorkflowFactory` with per-call context injection
   - Automatic repository context enrichment for workflows

### Key Service Components

- **Intent Service** (`services/intent_service/`): Classifies user messages into QUERY, EXECUTION, ANALYSIS, etc.
- **Orchestration Engine** (`services/orchestration/engine.py`): Manages complex multi-step workflows
- **Query Router** (`services/queries/query_router.py`): Handles all read operations with specialized query services
- **Knowledge Base** (`services/knowledge_base/`): Vector storage with 85+ PM documents
- **Analysis Services** (`services/analysis/`): Document and text analysis with file type detection

### API Endpoints

Main API (`main.py`, port 8001):
- `POST /api/v1/intent` - Process natural language messages
- `GET /api/v1/workflows/{id}` - Check workflow status
- `POST /api/v1/files/upload` - Upload documents for analysis

Web UI (`web/app.py`, port 8081):
- Chat interface for interacting with Piper Morgan
- File upload and analysis
- Real-time workflow status updates

### Integration Points

- **GitHub**: Fully functional issue creation and analysis (`services/integrations/github/`)
- **Multi-LLM Strategy**: Claude for reasoning, OpenAI for embeddings
- **Session Management**: Tracks user context and uploaded files

### Environment Configuration

Required environment variables in `.env`:
```
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
DATABASE_URL=postgresql://piper:dev_changeme_in_production@localhost:5433/piper_morgan
REDIS_URL=redis://localhost:6379
```

### Testing Strategy

- Integration tests use real database connections (PostgreSQL on port 5433)
- Tests automatically handle database cleanup between runs
- Asyncpg warnings during teardown are benign and can be ignored
- Always set `PYTHONPATH=.` when running tests

### Current Development Focus

Based on git status, active development includes:
- Multi-project context resolution (PM-009)
- File query routing and analysis
- Architecture Decision Records (ADRs) for MCP integration
- Enhanced document analysis capabilities

### Important Notes

1. **Docker Volumes**: Uses named volume `piper_postgres_data_v1` to persist data across container restarts
2. **Port Mappings**: PostgreSQL runs on 5433 (not default 5432) to avoid conflicts
3. **Linting**: No specific linting configuration found - follow existing code style
4. **File Uploads**: Stored in `uploads/` directory with timestamp prefixes