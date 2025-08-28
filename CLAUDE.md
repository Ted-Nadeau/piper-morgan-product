# CLAUDE.md

Guidance for Claude Code in this repository.

## Core Requirements

**SECURITY**: NEVER access .env files - credentials must be provided through approved environment setup only
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

- **NEVER access .env files** - use approved environment setup only
- Never create test_*.py files outside tests/ directory
- Never use bare pytest (always PYTHONPATH=. python -m pytest)
- Never claim tests pass without running them
- Never close GitHub issues with unchecked criteria
- Never skip verification before implementation
- Never mock critical execution paths in tests

## Issue Tracking Protocol

**CRITICAL**: Before creating any GitHub issue:
1. **Verify existing PM numbers** with `gh issue list --state all --limit 50 | grep "PM-"`
2. **Check CSV file** for highest PM number: `grep "PM-" docs/planning/pm-issues-status.csv | sort -V | tail -5`
3. **Never guess or fabricate PM numbers** - always verify first
4. **Use next sequential number only** after verification (current highest: PM-122, next: PM-123)
5. **Reference methodology-08-ISSUE-TRACKING.md** for complete protocol
6. **Update CSV file** when creating new PM numbers
7. **Cross-reference backlog.md** for planning alignment

**Current State**: Highest PM number is PM-122 (Issue #128), next valid is PM-123

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

- 3:03 PM and new plans:\
Chief Architect - Deployment Ready
Wednesday, August 20, 2025 - 3:00 PM Pacific
Perfect! Let's activate our hidden excellence and then build on solid, tested foundations.
Immediate Deployment Instructions
Phase 1: Test Infrastructure Activation (3:00-3:30 PM)
For Claude Code:
markdownMISSION: Activate our 599+ test infrastructure

TASKS:
1. Create scripts/run_tests.sh with smart test execution:
   - Smoke tests for quick feedback (<5 seconds)
   - Option for full suite
   - Clear pass/fail reporting

2. Create git hooks for test enforcement:
   - .git/hooks/pre-commit: Run smoke tests
   - .git/hooks/pre-push: Run integration tests
   - Include bypass instructions for emergencies

3. Update documentation:
   - Add test execution to README.md
   - Update BRANCH-MANAGEMENT.md with test requirements
   - Create TEST-GUIDE.md for new developers

SUCCESS CRITERIA:
- Running "git commit" triggers smoke tests
- Tests complete in <5 seconds
- Clear feedback on pass/fail
For Cursor (parallel):
markdownMISSION: Document Multi-Agent Coordinator usage

TASKS:
1. Create docs/development/HOW_TO_USE_MULTI_AGENT.md:
   - When to use multi-agent decomposition
   - Agent strength mapping (Code vs Cursor)
   - Real examples from our work

2. Create practical templates:
   - Task decomposition template
   - Agent assignment checklist
   - Synchronization point planning

3. Update Excellence Flywheel docs:
   - Add multi-agent patterns to Pillar 3
   - Include test activation in Pillar 4

SUCCESS CRITERIA:
- Clear guide for when/how to use multi-agent
- Practical examples we can follow
- Integrated with our methodology
Phase 2: Enhanced Autonomy - Persistent Context (3:30-7:30 PM)
For Code (4-hour autonomous session):
markdownMISSION: Build Persistent Context Foundation

SYSTEMATIC VERIFICATION FIRST:
- Check for existing persistence patterns
- Review user preference handling
- Understand session management

IMPLEMENTATION PRIORITIES:
1. User preferences storage (simple JSON to start)
2. Session context persistence between conversations
3. Basic memory retrieval system
4. NOT complex knowledge graphs (keep it simple but extensible)

ARCHITECTURE REQUIREMENTS:
- Must work with existing domain models
- Should support future expansion
- Include comprehensive tests (use our activated infrastructure!)
- Document patterns for future features

SUCCESS CRITERIA:
- User preferences persist between sessions
- Context carries over between conversations
- Tests pass using our new infrastructure
- Foundation ready for MVP features
The Meta-Pattern
Notice what we're doing:

Activating infrastructure we built but forgot
Documenting patterns so we don't forget again
Using our tools to build our tools
Testing as we go with our activated test suite

This addresses your blog's thesis directly - we're building the orchestration affordances we need, starting with our own development workflow.
Quick Check Before Launch
Ready to deploy both agents with:

✅ Test activation (Code)
✅ Multi-agent documentation (Cursor)
✅ Then Enhanced Autonomy on Persistent Context?

This gives us the "building right" approach - activated tests, documented patterns, then new foundations built on solid ground.
Shall we launch? 🚀
