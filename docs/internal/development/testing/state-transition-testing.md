# State Transition Testing Pattern

**Issue**: #485
**Date**: December 17, 2025
**Status**: Active Pattern

## Overview

State transition testing catches bugs that occur during system state changes, such as:
- Fresh install → first use
- Anonymous → authenticated
- Setup incomplete → setup complete

These bugs are missed by traditional tests that always start from a "working state."

## The Problem This Solves

### Root Cause: Happy Path Bias

Our standard test fixtures pre-create users and other required data. This means tests always run against a "steady state" system where:
- Users exist
- Sessions are valid
- API keys are stored

But real users don't start in steady state. They start with **nothing** and go through **transitions**:

```
Empty Database → Setup Wizard → User Created → API Keys Stored → First Use
```

When any step in this sequence has a bug, users hit errors that tests don't catch.

### Example: Issue #485 FK Violation

The setup wizard validated API keys by calling `store_user_key()` which created database records. But the FK constraint required users to exist first. Since tests pre-created users, this bug was never caught.

**Symptom**: FK violation during API key validation in setup wizard
**Root Cause**: Operations happening in wrong temporal order
**Why Tests Missed It**: Tests didn't model the transition from "no users" to "first user"

## How to Use State Transition Testing

### 1. The `fresh_database` Fixture

Use this fixture when testing flows that start from an empty state:

```python
@pytest.mark.integration
@pytest.mark.transition
@pytest.mark.asyncio
async def test_setup_works_on_fresh_install(fresh_database):
    """Test that setup wizard completes without FK violations."""
    # fresh_database has NO users, NO sessions, NO api_keys
    # This simulates a brand new installation

    result = await complete_setup_flow(fresh_database)
    assert result.success
```

### 2. The `transition_state` Helper

Use this helper to verify what database changes occurred:

```python
@pytest.mark.integration
@pytest.mark.transition
@pytest.mark.asyncio
async def test_validation_doesnt_create_records(fresh_database, transition_state):
    """Validation-only operations should not modify database."""

    # Capture state before
    await transition_state.capture_before(fresh_database)

    # Do the operation
    await validate_api_key(session=fresh_database, store=False)

    # Capture state after
    await transition_state.capture_after(fresh_database)

    # Assert no new records
    transition_state.assert_no_new_records('user_api_keys', 'audit_logs')
```

### 3. The `@pytest.mark.transition` Marker

Mark state transition tests so they can be run as a group:

```bash
# Run all state transition tests
pytest -m transition -v

# Run transition tests in verbose mode with no capture
pytest -m transition -xvs
```

## When to Write State Transition Tests

Write transition tests when:

1. **Adding setup/onboarding flows** - Test the complete journey from empty state
2. **Adding auth/session flows** - Test transitions between auth states
3. **Adding features that depend on prior state** - Test what happens without that state
4. **After finding a temporal bug** - Add regression test using `fresh_database`

## Fixtures Reference

### `fresh_database`

```python
@pytest_asyncio.fixture(scope="function")
async def fresh_database(db_session):
    """Database with schema but NO user data."""
    # Clears: users, user_api_keys, learned_patterns,
    #         learning_settings, user_sessions, audit_logs
```

### `transition_state`

```python
@pytest.fixture
def transition_state():
    """Helper for tracking database changes."""
    # Methods:
    #   await capture_before(session)  - Snapshot table counts
    #   await capture_after(session)   - Snapshot after operation
    #   assert_no_new_records(*tables) - Assert no changes
    #   assert_new_records(table, count=1) - Assert N new records
```

## Test File Location

State transition tests live in:
```
tests/integration/test_fresh_install_flow.py  # Fresh install flows
tests/integration/test_auth_transitions.py    # Auth state changes (future)
tests/integration/test_setup_transitions.py   # Setup wizard flows (future)
```

## Best Practices

1. **Always use the `transition` marker** - Makes it easy to run all transition tests
2. **Use `fresh_database` for empty-state tests** - Don't manually delete data
3. **Use `transition_state` to assert database changes** - Don't query tables manually
4. **Test both happy path and error paths** - Include tests for:
   - Operation succeeds (correct order)
   - Operation fails gracefully (wrong order)
   - Operation is idempotent (repeated calls)

## Related Documents

- [E2E Bug Investigation Report Template](e2e-bug-investigation-report-template.md)
- [E2E Bug Fix Execution Protocol](e2e-bug-fix-execution-protocol.md)
- GitHub Issue: #485 (original bug that motivated this pattern)
