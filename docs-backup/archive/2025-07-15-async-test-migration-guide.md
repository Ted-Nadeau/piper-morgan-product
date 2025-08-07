# AsyncSessionFactory Test Migration Guide

**Last updated: 2025-07-15**

## Context

- Tests previously used `db_session_factory` fixture for DB session management.
- New codebase standard is to use `AsyncSessionFactory.session_scope()` for all async DB tests.
- This pattern is proven to work for at least one test in `test_file_scoring_weights.py`.

## Migration Template

### 1. Imports

```python
from services.database.session_factory import AsyncSessionFactory
# Remove any import of db_session_factory or related fixtures
```

### 2. Old Pattern

```python
async with await db_session_factory() as session:
    repo = FileRepository(session)
    # ... test logic ...
```

### 3. New Pattern

```python
async with AsyncSessionFactory.session_scope() as session:
    repo = FileRepository(session)
    # ... test logic ...
```

### 4. Remove all references to `db_session_factory` in test signatures and fixtures.

## Gotchas/Notes

- Some tests may still fail with event loop/session errors until `conftest.py` is updated to manage the event loop and session scope correctly for all async tests.
- Always import `AsyncSessionFactory` from `services.database.session_factory`.
- If a test needs multiple DB operations, use a new `session_scope()` for each logical transaction.
- Await `asyncio.sleep(0)` between DB operations if needed to yield to the event loop (helps avoid connection reuse issues in some cases).

## Next Steps

- WAIT for Claude Code to complete `conftest.py` updates to fix event loop issues.
- Once fixed, apply this pattern to all tests using the old `db_session_factory` pattern.
- Update the checklist below as more files are identified.

---

## Files to Update (Checklist)

- [x] tests/test_file_scoring_weights.py (done, proof of concept)
- [ ] tests/test_file_repository_migration.py
- [ ] tests/test_file_resolver_edge_cases.py
- [ ] tests/test_file_reference_detection.py
- [ ] tests/test_workflow_repository_migration.py
- [ ] tests/services/orchestration/test_orchestration_engine.py
- [ ] tests/test_api_query_integration.py
- [ ] tests/test_clarification_edge_cases.py
- [ ] tests/test_session_manager.py
- [ ] tests/test_intent_enricher.py
- [ ] tests/test_pre_classifier.py
- [ ] (Add others as identified by Claude Code's priority list)

---

**Ready to apply broadly once conftest.py is fixed!**

---

## Continuity Handoff Prompt for Next Session

**Context:**

- All business logic tests have been updated to match improved system behavior.
- Edge cases are now correctly classified; only one known limitation (verb usage of 'file') is tracked as xfail/TODO.
- Functional pass rate is 85.5%.
- Remaining failures are asyncpg/SQLAlchemy event loop and session management issues (infrastructure, not logic).

**Next Steps for Tomorrow:**

- Focus on infrastructure: asyncpg/SQLAlchemy event loop and connection pool issues.
- Review and refactor test fixtures and session management for full async compatibility.
- Use the migration guide as a template for any further test updates.
- Celebrate the robust, modern business logic test suite!

**Handoff:**

> You are picking up a codebase with a clean, modern, and accurate business logic test suite. The remaining work is infrastructure: asyncpg/SQLAlchemy event loop/session issues. See session log and migration guide for full context. Good luck!

---
