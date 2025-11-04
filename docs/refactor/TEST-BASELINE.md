# Test Baseline - Before Refactoring

**Date**: 2025-11-03 16:25 PM PT
**Collection Status**: 649 tests collected with `-k "todo"` filter
**Execution Status**: Unable to run due to import errors (unrelated to todos)

---

## Test Files

**Todo-specific test files found**:
1. `tests/integration/test_todo_intent_handlers.py`
2. `tests/repositories/test_todo_repository.py`

**Note**: Only 2 test files explicitly named for todos, but 649 tests collected with "todo" keyword suggests many tests touch todo functionality indirectly.

---

## Import Errors (Blocking Baseline)

**Error 1**: `tests/integration/test_api_degradation_integration.py`
```
ImportError: cannot import name 'app' from 'main'
```

**Error 2**: `tests/integration/test_api_query_integration.py`
```
[Similar import error]
```

**Assessment**: These are NOT todo-related errors. They're general test infrastructure issues that existed before this refactoring.

---

## Test Coverage Estimate

**Based on collection**:
- 649 tests match "todo" keyword
- 2 dedicated todo test files
- Coverage appears to include:
  - Integration tests (todo intent handlers)
  - Repository tests (todo repository)
  - Likely API tests, domain model tests mixed in

---

## Baseline Strategy

**Problem**: Can't establish clean baseline due to pre-existing import errors

**Solution**:
1. Document that import errors exist (not caused by refactoring)
2. After Phase 1 (creating primitives), fix import errors if still present
3. Use individual test file runs where possible
4. Focus on tests that CAN run

**Critical Tests to Watch** (when import errors fixed):
- Todo repository CRUD operations
- Todo intent handler parsing
- Todo domain model creation
- TodoList universal pattern delegation

---

## Mitigation

**To verify refactoring doesn't break things**:
1. Run tests file-by-file where possible
2. Create new integration tests for Item/Todo hierarchy
3. Manual testing of todo functionality
4. Compare behavior before/after at API level

---

## Action Items

**Before Phase 1**:
- [x] Document test baseline (this file)
- [x] Note that import errors pre-exist
- [ ] Optionally: Fix import errors in test infrastructure

**During Phase 1**:
- [ ] Create new tests for Item primitive
- [ ] Create tests for Todo(Item) hierarchy
- [ ] Ensure new tests pass

**After Phase 2**:
- [ ] Run todo repository tests (if import errors fixed)
- [ ] Run todo intent handler tests (if import errors fixed)
- [ ] Verify no regressions

---

## Notes

**Key Finding**: Test infrastructure has pre-existing issues unrelated to todos.

**Refactoring Strategy**: Don't let broken test infrastructure block progress. Create NEW tests for new functionality (Item primitive) that can run independently.

**Quality Assurance**:
- New Item/Todo tests will validate correctness
- Manual testing will verify API still works
- Integration tests (when fixed) will provide comprehensive coverage

---

*Test baseline documented. Import errors noted as pre-existing condition.*
