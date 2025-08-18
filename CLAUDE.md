# CLAUDE.md

Guidance for Claude Code in this repository.

## Core Requirements

**Excellence Flywheel**: Verify first → Implement second → Evidence-based progress → GitHub tracking
**Python**: 3.11 required, venv activated
**Testing**: PYTHONPATH=. python -m pytest (never bare pytest)
**Evidence**: Never claim success without verification output

## Critical Commands

```bash
# Setup
source venv/bin/activate
docker-compose up -d

# Testing (ALWAYS with PYTHONPATH)
PYTHONPATH=. python -m pytest tests/unit/ -v
PYTHONPATH=. python -m pytest tests/integration/test_file.py::TestClass::test_method -v

# Running
python main.py  # API on 8001
cd web && python -m uvicorn app:app --reload --port 8081

# Database
docker exec -it piper-postgres psql -U piper -d piper_morgan
```

## Project Structure

```
services/
├── domain/models.py           # Source of truth - check first
├── shared_types.py            # All enums here
├── orchestration/             # Workflows, multi-agent coordination
├── queries/                   # Read operations (CQRS)
├── repositories/              # Data access only
└── integrations/              # GitHub, Slack, external

tests/
├── unit/                      # Fast, mocked
├── integration/               # Real DB (port 5433)
└── conftest.py               # Fixtures: async_session, async_transaction

docs/
├── architecture/             # ADRs, patterns
├── development/
│   ├── methodology-core/     # Excellence Flywheel docs
│   └── session-logs/         # Daily logs: YYYY-MM-DD-log.md
└── planning/                 # Roadmap, backlog
```

## Verification Requirements

**Before ANY implementation**:
```bash
grep -r "pattern" services/ --include="*.py" -A 3 -B 3  # Find existing patterns
cat services/domain/models.py | grep "class"            # Check domain models
find . -name "*.py" -exec grep -l "ADR-" {} \;         # Find architectural decisions
```

**Before claiming completion**:
```bash
gh issue view [number] --json body | grep "\\[[ x]\\]"  # Check acceptance criteria
PYTHONPATH=. python -m pytest [test] -v                 # Run actual tests
# See "X passed" before claiming success
```

## Session Protocol

1. Create log: `docs/development/session-logs/YYYY-MM-DD-log.md`
2. Check handoffs: `docs/development/prompts/*-handoff-*.md`
3. Complex tasks: Use TodoWrite tool
4. End session: Update GitHub issues with evidence

## Don'ts

- Never create test_*.py files outside tests/ directory
- Never use bare pytest (always PYTHONPATH=. python -m pytest)
- Never claim tests pass without running them
- Never close GitHub issues with unchecked criteria
- Never skip verification before implementation
- Never mock critical execution paths in tests

## Architecture Rules

- Domain models (models.py) drive everything - DB follows models
- AsyncSessionFactory.session_scope() for all DB operations
- Repositories for data access only - no business logic
- Services for business logic - no direct DB access
- All enums in shared_types.py only

## Environment Variables

```
ANTHROPIC_API_KEY=required
OPENAI_API_KEY=required
DATABASE_URL=postgresql://piper:dev_changeme_in_production@localhost:5433/piper_morgan
REDIS_URL=redis://localhost:6379
GITHUB_TOKEN=for_gh_commands
```

## MCP Integration

Context7 available for library docs: "use context7" in prompts

## Quick Patterns

**New test**: Use async_transaction fixture
**New repository**: Inherit from base, use AsyncSessionFactory
**New service**: Business logic only, inject repositories
**New enum**: Add to shared_types.py only
**Session logs**: First of day: YYYY-MM-DD-log.md, then add a,b,c suffix
