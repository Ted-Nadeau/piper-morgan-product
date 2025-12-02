# Copilot Instructions for Piper Morgan

AI Product Management Assistant - Python/FastAPI backend with plugin architecture

## Core Architecture

**Entry Point**: `main.py` → NOT `web/app.py` directly
- Run: `python main.py` (starts server on http://localhost:8001)
- FastAPI app defined in `web/app.py` (~1066 lines)
- Service initialization via `ServiceContainer` (DDD pattern)

**Service Container Pattern** (Singleton with explicit lifecycle):
```python
from services.container import ServiceContainer
container = ServiceContainer()
await container.initialize()  # MUST call before using services
llm_service = container.get_service('llm')
```
⚠️ **Never bypass ServiceContainer** - it manages dependencies and initialization order

**Hub-and-Spoke Model**: `IntentService` (5200+ lines) orchestrates 39 domain models from `services/domain/models.py` (1312 lines - single source of truth)

## Critical File Locations

- **All Enums**: `services/shared_types.py` (IntentCategory, WorkflowType, TaskType, TodoStatus, etc.)
- **Domain Models**: `services/domain/models.py` (1300+ lines - truth source)
- **Intent Routing**: `services/intent/intent_service.py` (5200+ lines - 13 intent categories)
- **User Config**: `config/PIPER.user.md` (NOT YAML - Markdown-based configuration)
- **Personality**: `config/PIPER.md` (system identity and tone)

## Infrastructure (docker-compose.yml)

**Non-standard ports to avoid conflicts**:
- PostgreSQL: **port 5433** (NOT 5432!)
- Redis: port 6379
- ChromaDB: port 8000
- Temporal: port 7233
- Web: port 8001

Docker project name: `piper-morgan-stable` (survives directory renames)

## Development Commands

```bash
# Start application
python main.py                    # Normal startup
python main.py --verbose          # Detailed logging
python main.py --no-browser       # No auto-launch

# CLI commands
python main.py setup              # Interactive setup
python main.py status             # System health check
python main.py keys add openai    # Add API key

# Tests with pytest markers
pytest tests/unit/ -v             # Unit tests
pytest tests/ -m smoke            # Critical path (<5 sec)
pytest tests/ -m integration      # Integration tests
pytest tests/ -m llm              # Requires LLM keys
pytest tests/ -m contract         # Plugin compliance

# Database migrations
docker-compose up -d              # Start services
alembic upgrade head              # Run migrations
alembic revision --autogenerate -m "desc"

# Pre-commit CRITICAL
./scripts/fix-newlines.sh         # ALWAYS before commit
```

## Project-Specific Patterns

### Intent Handler Convention
Intent handlers in `IntentService` follow strict naming: `_handle_{intent_type}_intent()`

**8 Primary Intent Categories**:
- `_handle_query_intent()` - Read-only data retrieval (CQRS-lite)
- `_handle_execution_intent()` - Create/update operations
- `_handle_analysis_intent()` - Data analysis workflows
- `_handle_synthesis_intent()` - Content generation
- `_handle_strategy_intent()` - Strategic planning
- `_handle_learning_intent()` - Pattern learning
- `_handle_unknown_intent()` - Fallback handling
- `_handle_summarize()` - Document summarization

**Action Mapper**: Classifier action names ≠ handler method names (Issue #284)
- Maps external action names to internal handler methods
- Located in `services/intent_service/action_mapper.py`

### Plugin Architecture
All plugins extend `PiperPlugin` from `services/plugins/plugin_interface.py`:
- **Metadata**: name, version, description, author
- **Capabilities**: "routes", "webhooks", "spatial", "mcp", "background"
- **Contract Tests**: `@pytest.mark.contract` verifies interface compliance
- **7 Active Integrations**: slack, github, notion, calendar, demo, mcp, spatial
  - Each in `services/integrations/{integration_name}/`
  - Plugin registration via `PluginRegistry`
  - Version tracking for compatibility

### Two-Tier Response Pattern
- **Canonical Handlers**: Fast (<1ms) for direct queries - no orchestration
- **Workflow Handlers**: Complex (2-3s) synthesis/analysis via `OrchestrationEngine`

### Graceful Degradation (Pattern-007)
Web layer returns structured responses even on service failure:
```python
def _create_degradation_response(message: str, degradation_msg: str) -> dict:
    # Returns 200 OK with user-friendly message
    # Never expose technical details to users
```

## Testing Philosophy

**Marker hierarchy** (pytest.ini):
- `@pytest.mark.smoke` - Critical path, <5 sec total (highest priority)
- `@pytest.mark.unit` - Unit tests, <30 sec
- `@pytest.mark.integration` - Up to 2 minutes (database, external services)
- `@pytest.mark.llm` - Requires API keys (skipped in CI without keys)
- `@pytest.mark.contract` - Plugin interface compliance
- `@pytest.mark.performance` - Performance and benchmark tests

**Async configuration**: Session-scoped event loops prevent "Task attached to different loop" errors (Issue #290)
```ini
asyncio_mode = auto
asyncio_default_fixture_loop_scope = session
```

**Test Failure Protocol** (from CLAUDE.md):
- STOP immediately if ANY test fails
- DO NOT rationalize as "minor" or "not blocking"
- Report: failing count, passing count, exact errors, options
- Wait for PM decision

## Common Gotchas

1. **PostgreSQL Port**: Use 5433, not default 5432
2. **Entry Point**: Run `main.py`, not directly uvicorn
3. **Config Format**: User config is Markdown (`PIPER.user.md`), not YAML
4. **Enum Location**: ALL enums go in `services/shared_types.py`
5. **Pre-commit**: Run `./scripts/fix-newlines.sh` before committing to fix EOF newlines
6. **Repository URL**: `https://github.com/mediajunkie/piper-morgan-product` (NOT `Codewarrior1988/piper-morgan`)

## Service Structure

```
services/
├── container/          # ServiceContainer (DDD lifecycle)
├── domain/             # Domain models (models.py is truth)
├── shared_types.py     # ALL enums
├── intent/             # Intent classification & routing
├── intent_service/     # Canonical handlers, todo handlers
├── integrations/       # External plugins (7+ integrations)
├── llm/                # LLM providers & adapters
├── orchestration/      # Temporal workflow engine
├── plugins/            # Plugin interface & registry
├── knowledge/          # Knowledge graph & RAG
└── user_context/       # Multi-user config isolation
```

## Key Design Decisions

- **DDD with ServiceContainer**: Explicit lifecycle management over framework magic
- **Intent-driven routing**: 13 categories (EXECUTION, ANALYSIS, SYNTHESIS, QUERY, etc.)
- **Plugin system**: Standardized interfaces with version tracking
- **Multi-user context**: Service isolates user configuration per session
- **Personality injection**: Markdown config parsed and applied to LLM responses
- **Temporal orchestration**: Complex workflows use Temporal activities (not direct calls)

## Documentation & Navigation

**Essential Navigation**:
- `docs/NAVIGATION.md` - Role-based navigation hub (337 lines)
- `CLAUDE.md` - Agent protocols, debugging, anti-completion-bias (792 lines)
- `docs/TECHNICAL-DEVELOPERS.md` - Developer technical reference (575 lines)
- `docs/DATABASE_SCHEMA.md` - Complete SQL DDL for 28 tables
- `COMPREHENSIVE-TESTING-GUIDE.md` - Testing procedures and E2E protocols

**Role-Based Briefings** (Progressive Loading):
- `knowledge/BRIEFING-ESSENTIAL-{ROLE}.md` - Lead Dev, Architect, Chief of Staff, Agent
- Each briefing: 2-2.5K tokens (vs. 39K for full context)
- Load additional context progressively as needed

**Public Documentation**: https://pmorgan.tech

## When Adding Features

1. Check `services/shared_types.py` for existing enums
2. Extend domain models in `services/domain/models.py`
3. Add intent handler to `IntentService` if user-facing
4. Create plugin in `services/integrations/` if external integration
5. Add smoke test for critical path (`@pytest.mark.smoke`)
6. Update user docs at https://pmorgan.tech if user-facing

## Anti-Patterns to Avoid

- ❌ Don't create new enum files - use `shared_types.py`
- ❌ Don't bypass ServiceContainer - use `container.get_service()`
- ❌ Don't skip pre-commit newline fixes - causes CI failures
- ❌ Don't use port 5432 - PostgreSQL is on 5433
- ❌ Don't declare completion without passing tests (anti-completion-bias protocol)
- ❌ Don't fix symptoms - always find root cause (see CLAUDE.md debugging framework)
- ❌ Don't implement patterns without reading reference implementation
- ❌ Don't add multiple fixes at once - test after each change

## Agent Protocols (CRITICAL)

**From CLAUDE.md - MUST follow**:

1. **STOP Conditions**: 17 mandatory conditions that require immediate escalation
2. **No Exceptions Rule**: Get PM approval before breaking any rule
3. **Test Failure**: STOP immediately, report, await decision
4. **Root Cause First**: Never fix symptoms, always diagnose root cause
5. **Progressive Loading**: Use role-based briefings, load context as needed
6. **Time Lord Alert**: Say this when uncertain - it's your escape hatch

**Live System State** (Query with Serena MCP):
- Intent handlers: `mcp__serena__find_symbol("IntentService", depth=1)`
- Active plugins: `mcp__serena__list_dir("services/integrations")`
- Pattern catalog: `mcp__serena__list_dir("docs/internal/architecture/current/patterns")`
- Benefits: 79% token savings, always accurate
