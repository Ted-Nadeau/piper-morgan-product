# Chief Architect Context - Database Fallback Pattern Question

## Current Architecture Pattern

We've implemented **graceful database degradation** in several components:
- `main.py`: Intent enrichment falls back to unenriched intent
- `OrchestrationEngine`: Has `test_mode` parameter for database-independent operation
- Workflow status endpoint: Gracefully degrades to in-memory workflows

## The Pattern Gap

**QueryRouter** (`services/queries/query_router.py`) requires database connectivity:
```python
async with AsyncSessionFactory.session_scope() as session:
    project_repo = ProjectRepository(session)
    # ... requires active database connection
```

**User Impact**: "List projects" fails with 500 error when database unavailable, while "Create issue" works perfectly.

## Architectural Decision Point

**Question**: Should we extend the graceful degradation pattern to QueryRouter?

**Options Considered**:
1. **Extend pattern**: Add database fallback to QueryRouter (returns helpful "Database unavailable" messages)
2. **Accept limitation**: Document that QUERY intents require database connectivity
3. **Redesign**: Create database-independent query service architecture

**Design Pattern Concern**: Avoiding "litter of singletons" - ensuring consistent approach to database fallback across services rather than ad-hoc solutions.

**Context**: This enables development/testing without Docker while maintaining user experience consistency between EXECUTION and QUERY intents.

**Trade-offs**: Pattern consistency vs. development convenience vs. architectural complexity.
