# Pattern-045: Green Tests, Red User

**Status**: Established
**Date**: December 25, 2025
**Category**: Testing Anti-Pattern (Development & Process)
**Related Issues**: #479 (CRUD failures), #485 (FK violations), #487 (Intent classification)

## Overview

An anti-pattern where unit tests pass with mocked dependencies but real user testing against actual infrastructure reveals systematic failures. Named for the testing dashboard showing "green" while users experience "red" errors.

**Part of the Completion Discipline Triad**: Patterns 045, 046, and 047 form a reinforcing system:
- Pattern-045 reveals the gap (tests pass, users fail)
- Pattern-046 prevents premature closure (Beads discipline)
- Pattern-047 enables pause when uncertain (Time Lord Alert)

## Problem Statement

Systems can achieve high test coverage and passing test suites while being fundamentally broken for real users due to:
- Mocked dependencies hiding integration issues
- Schema/model drift not caught by unit tests
- Type mismatches only enforced at database level
- Temporal bugs (operations before entities exist)
- Configuration differences between test and production

## Pattern Manifestations

### Case 1: UUID Type Mismatch (Dec 7, 2025)
- **Tests**: 705 unit tests passing
- **Reality**: All CRUD operations failing
- **Root Cause**: Schema defined `owner_id` as `uuid`, models as `String`
- **Why Escaped**: PostgreSQL type checking bypassed by mocks
- **Debug Time**: 24 hours across 6 layers

### Case 2: FK Violations (Dec 17-18, 2025)
- **Tests**: All tests passing
- **Reality**: Setup wizard crashes with FK violations
- **Root Causes**:
  - `store_user_key()` commits before user exists
  - `learned_patterns` uses hardcoded user_id
- **Why Escaped**: Test fixtures pre-create users
- **Debug Time**: Multiple sessions

### Case 3: Intent Classification (Dec 20, 2025)
- **Tests**: Intent tests passing
- **Reality**: "Menu of services" returns generic response
- **Root Cause**: Missing patterns, over-greedy matching
- **Why Escaped**: No discovery scenario tests
- **Debug Time**: 12+ hour overnight session

## Prevention Strategies

### 1. Integration Testing Requirements
```python
# Bad: Unit test with mocks
def test_create_todo_mocked():
    repo = Mock()
    repo.create.return_value = Todo(...)
    assert repo.create(name="Test")

# Good: Integration test with real DB
@pytest.mark.integration
async def test_create_todo_real():
    async with real_database() as db:
        todo = await TodoRepository(db).create(name="Test")
        assert todo.id is not None
```

### 2. Schema Validation on Startup
```python
class SchemaValidator:
    def validate_on_startup(self):
        """Compare DB schema with SQLAlchemy models"""
        for model in Base.metadata.tables:
            db_columns = inspector.get_columns(model)
            for column in model.columns:
                if not types_compatible(column.type, db_columns[column.name]):
                    raise SchemaValidationError(...)
```

### 3. Fresh Install Testing
```python
@pytest.fixture
def fresh_database():
    """Database with no pre-existing data"""
    # No users, no setup flags, virgin state
    yield empty_db

def test_setup_wizard_fresh_install(fresh_database):
    """Test the actual first-time user experience"""
    # Should work without any pre-existing entities
```

### 4. E2E Scenario Testing
Test actual user workflows, not just components:
- Setup → Login → Create Todo → View Todo
- Fresh Install → API Key Validation → First Query
- Discovery queries without prior context

### 5. Critical Path Smoke Tests
Before marking issues "done":
- Test in browser, not just API
- Test with fresh database
- Test complete user journey
- Verify against production-like environment

## Acceptance Criteria Updates

All issues should include:
- [ ] Unit tests pass
- [ ] Integration tests against real PostgreSQL
- [ ] Fresh install scenario tested
- [ ] Browser verification completed
- [ ] No hardcoded IDs or assumptions

## Detection Signals

Watch for these warning signs:
- High unit test coverage with user complaints
- "Works on my machine" syndrome
- Tests that only pass with fixtures
- No integration test markers
- Missing fresh install scenarios
- Hardcoded test data (user IDs, etc.)

## Cultural Practices

### "Done" Means User-Verified
- Code complete ≠ Done
- Tests passing ≠ Done
- **User can accomplish task = Done**

### The Five Whys Protocol
When user failures occur:
1. Why did it fail for the user?
2. Why didn't tests catch it?
3. Why were tests inadequate?
4. Why wasn't integration tested?
5. Why was this gap acceptable?

### Verification-First Development
From Pattern-006: Write verification before implementation
- Define how you'll know it works for users
- Create integration test scenarios first
- Mock as little as possible

## Implementation Checklist

When implementing new features:
- [ ] Create integration tests first
- [ ] Test fresh install scenario
- [ ] Test with real database
- [ ] Verify schema compatibility
- [ ] Test complete user journey
- [ ] Browser verification
- [ ] No hardcoded assumptions

## Related Patterns

- **Pattern-006**: Verification-First Development
- **Pattern-010**: Cross-Validation Protocol
- **Pattern-042**: Investigation-Only Protocol
- **Pattern-043**: Defense-in-Depth Prevention
- **Pattern-046**: Beads Completion Discipline (prevents declaring done prematurely)
- **Pattern-047**: Time Lord Alert (enables pause when uncertain)

## Anti-Pattern Remediation

If you discover Green Tests, Red User:
1. Stop and create integration test that fails
2. Fix the integration issue
3. Add schema validation if applicable
4. Add fresh install test
5. Document in Pattern-045 instances
6. Update acceptance criteria going forward

## Historical Impact

- **Dec 7**: 24-hour debugging marathon
- **Dec 17-18**: Multiple FK violation sessions
- **Dec 20**: 12+ hour overnight fix

**Cumulative Time Lost**: ~40+ hours of debugging that integration tests would have prevented

## Quotes

> "The discipline is to mark it 'done' when a user can use it." - Lead Developer, Dec 3

> "Schema defined owner_id as uuid, models as String. PostgreSQL rejected operations with type mismatch error. Root cause why ALL CRUD failed." - Dec 7 Omnibus

> "Unit tests with mocks passed; real database revealed the truth." - Dec 22 Memo

---

*Last Updated: December 27, 2025*
*Instances: 3 major (UUID mismatch, FK violations, Intent classification)*
*Prevention: Integration tests, schema validation, fresh install scenarios*
