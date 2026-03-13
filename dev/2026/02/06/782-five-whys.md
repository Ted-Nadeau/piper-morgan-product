# Five Whys Analysis: #782 Notion Config Tests Failing

**Date**: 2026-02-06
**Issue**: #782 - Test needs update for Issue #734 user_id requirement

## The Problem

All 19 tests in `tests/integration/test_notion_config_loading.py` fail with:
```
TypeError: NotionConfigService.get_config() missing 1 required positional argument: 'user_id'
```

## Five Whys

### 1. Why do the tests fail with TypeError?
They call `service.get_config()` without passing `user_id`.

### 2. Why does get_config() require user_id?
Issue #734 made `user_id` required for multi-tenancy - config is now per-user.

### 3. Why weren't the tests updated when #734 was implemented?
The tests were overlooked during the multi-tenancy migration.

### 4. Why were they overlooked?
Likely because:
- They're integration tests (not unit tests run frequently)
- No CI pipeline caught the failure
- The migration focused on runtime code, not test coverage

### 5. Why does this matter?
Integration tests exist to verify config loading from PIPER.user.md works correctly. With all tests failing, we have no verification that the config loading layer works.

## Root Cause

**Test/implementation drift**: Multi-tenancy migration (#734) changed the `get_config()` signature but didn't update the integration tests.

## Fix Approach

Add a test user_id constant and pass it to all `get_config()` and `is_configured()` calls:

```python
TEST_USER_ID = "test_user_notion_config"

# In tests:
config = service.get_config(TEST_USER_ID)
assert service.is_configured(TEST_USER_ID) is True
```

## Files to Modify

| File | Change |
|------|--------|
| `tests/integration/test_notion_config_loading.py` | Add TEST_USER_ID, update all 19 tests |

## Verification

All 19 tests should pass after the fix.
