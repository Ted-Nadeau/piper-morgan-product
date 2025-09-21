# CLAUDE.md Archive - Verbose Content

This document preserves explanatory content from the original 921-line CLAUDE.md for human reference.
The active CLAUDE.md has been optimized for token efficiency (<150 lines).

## Excellence Flywheel Methodology - Detailed Explanation

The Excellence Flywheel represents our systematic approach to development excellence:

1. **Systematic Verification First**: Always verify the current state before implementing changes. This prevents assumption-based development and ensures we build on solid foundations.

2. **Test-Driven Development**: Write tests before implementation to ensure quality and prevent regressions.

3. **Multi-Agent Coordination**: Strategic deployment of specialized agents (Code, Cursor, Chief Architect, Lead Developer) for maximum efficiency.

4. **GitHub-First Tracking**: All work is tracked through GitHub issues for transparency and coordination.

### Why This Matters

False success reporting breaks the Excellence Flywheel by:
- Wasting time on non-existent solutions
- Destroying trust in systematic progress
- Creating compound errors across agent sessions
- Preventing learning from actual implementation issues

Honest reporting enables:
- Accurate progress tracking
- Effective debugging and problem-solving
- Compound learning across sessions
- Trust in systematic methodology

## Session Start Protocol - Detailed

### Time/Date/Location Confirmation
Acknowledge current time, date, and timezone from environment. This ensures proper context for time-sensitive operations and session continuity.

### Context Review Protocol
- Check for handoff documentation in docs/development/prompts/
- Review recent session logs for context
- Identify incomplete tasks or ongoing work
- Note any specific instructions or constraints

### Task Planning and Organization
For multi-step or complex tasks:
- Use TodoWrite tool immediately to organize work
- Break down tasks into specific, actionable items
- Set appropriate priorities and dependencies
- Track progress throughout session

## PM Issue Implementation Protocol - Detailed

### GitHub-First Implementation Approach

Before implementing any PM-XXX issue:

1. **Review GitHub Issue Completely**
   - Read the issue description and all comments
   - Look for preparation reports from other agents
   - Check for implementation roadmaps or strategic guidance
   - Verify current status and any recent updates

2. **Coordinate with Preparation Work**
   - Reference preparation findings in your implementation approach
   - Follow recommended implementation sequences when provided
   - Incorporate risk mitigation strategies from preparation reports
   - Build on analysis work rather than duplicating effort

3. **Verify Current Context**
   - Confirm issue hasn't been updated since your assignment
   - Check for dependencies or blockers mentioned in comments
   - Look for related issues or cross-references
   - Ensure you have the complete context before proceeding

## Systematic Verification First - Philosophy

Our biggest breakthrough: "Check First, Implement Second" has proven to be our most transformative approach, enabling 15-minute ADR migrations and 11-minute complete framework implementations.

### Pattern Library Reference

1. **Repository Pattern**: `services/repositories/*.py` - Standard async repository implementation
2. **Service Pattern**: `services/*/service.py` - Business logic encapsulation
3. **ADR Patterns**: `docs/architecture/adr-*.md` - Architectural decision implementations
4. **Test Patterns**: `tests/*/test_*.py` - Comprehensive test coverage approaches
5. **Jekyll Liquid Escaping**: `{% raw %}...{% endraw %}` - Escape double braces in GitHub Pages

### Why Verification Works

1. **Prevents Assumption-Based Development**: Eliminates "I think the pattern is..." → guarantees "I know the pattern is..."
2. **Ensures Architectural Consistency**: Identifies established patterns before creating new ones
3. **Accelerates Implementation**: Understanding existing structure eliminates false starts and rework
4. **Maintains Quality**: Leverages proven patterns rather than inventing new approaches
5. **Enables Excellence Flywheel**: Each implementation builds knowledge for accelerated future work

## Testing Strategy - Detailed

### Integration Test Patterns
- Integration tests use real database connections (PostgreSQL on port 5433)
- AsyncSessionFactory Test Fixtures: Use `async_session` and `async_transaction` fixtures
- Legacy Support: `db_session` fixture maintained for backward compatibility
- Tests automatically handle database cleanup between runs
- Asyncpg warnings during teardown are benign and can be ignored

### Testing Discipline Protocol

**MANDATORY: Dual Testing Strategy**
- **Unit Tests**: Fast feedback with strategic mocking
- **Reality Tests**: Full execution paths without critical mocks

**FORBIDDEN: Critical Path Over-Mocking**
- Never mock away the code you're testing
- Test real execution paths to catch actual bugs
- Production reality testing before any commits

## Architecture Philosophy

### Domain-Driven Design
All business logic flows from domain models in `services/database/models.py`. The database schema is generated from SQLAlchemy models, not the other way around.

**NO QUICK FIXES**: Always fix issues at the correct domain layer
**Layered Architecture**: Domain → Application → Infrastructure → Presentation
**Business logic belongs in domain services**, not UI or infrastructure layers

### AsyncSessionFactory Pattern
Standardized async session management across all components (2025-07-15 migration):
- **Session Scope**: `AsyncSessionFactory.session_scope()` for automatic session lifecycle management
- **Transaction Awareness**: Repository methods detect existing transactions to prevent double-scoping
- **Context Managers**: All database operations use async context managers for cleanup
- **Consistent Pattern**: Replaces legacy RepositoryFactory and direct session creation

### CQRS-lite Pattern
- Read operations: `services/queries/` (QueryRouter handles all read-only operations)
- Write operations: `services/orchestration/` (workflows and commands)
- Separation enables independent scaling and optimization

## Development Approach Philosophy

### Core Principles
- Question assumptions and explore alternatives
- Catch antipatterns before they take root
- Use decision points as teaching moments
- Keep responses "concise but complete"
- One actionable step at a time

### Key Constraints
- $0 software budget - use only free/open source tools
- Single developer bandwidth - optimize for maintainability
- Production-ready from start - no "we'll fix it later"

## Success Examples

### PM-015 Group 3 Implementation Success
- Code reviewed ADR-010 documentation before implementing
- Used fresh FeatureFlags utility from preparation work
- Achieved 100% test success by building on architectural guidance
- Implementation time minimized through preparation coordination

### PM-055 Preparation Coordination
- Cursor provided comprehensive implementation readiness report
- Code's blocker mitigation work informed by preparation analysis
- Wednesday implementation de-risked through systematic coordination
- GitHub issue became central coordination point for multi-agent work

These examples demonstrate how GitHub-first coordination amplifies agent effectiveness and accelerates systematic progress.
