# Gameplan: #782 Notion Config Tests Failing

**Issue**: #782 - Test needs update for Issue #734 user_id requirement
**Date**: 2026-02-06

## Problem Statement

All 19 tests in `tests/integration/test_notion_config_loading.py` fail because they call `get_config()` and `is_configured()` without the `user_id` parameter that Issue #734 made required.

## Five Whys Summary

Test/implementation drift from multi-tenancy migration. Tests were overlooked when `get_config()` signature changed.

## Files to Modify

| File | Change |
|------|--------|
| `tests/integration/test_notion_config_loading.py` | Add TEST_USER_ID, update all calls |

---

## Phase 1: Add Test User ID Constant

Add at top of file after imports:

```python
# Test user ID for multi-tenancy (Issue #734)
TEST_USER_ID = "test_user_notion_config"
```

---

## Phase 2: Update TestNotionConfigLoading (17 tests)

Update all `service.get_config()` calls to `service.get_config(TEST_USER_ID)`:

- `test_loads_from_piper_user_md` (line 57)
- `test_env_vars_override_user_config` (line 99)
- `test_defaults_when_no_config` (line 131)
- `test_graceful_fallback_when_piper_missing` (line 148)
- `test_graceful_fallback_when_yaml_malformed` (line 175)
- `test_authentication_section_parsing` (line 201)
- `test_missing_authentication_section` (line 226)
- `test_api_config_settings` (line 255)
- `test_environment_configuration` (line 280)
- `test_env_var_environment_override` (line 307)
- `test_configuration_priority_order_comprehensive` (line 346)
- `test_partial_configuration` (line 386)
- `test_empty_piper_user_md_file` (line 404)
- `test_notion_section_with_no_yaml_block` (line 427)
- `test_rate_limit_configuration` (line 450)
- `test_env_var_rate_limit_override` (line 477)
- (one more if I miscounted)

---

## Phase 3: Update TestNotionConfigServiceBasics (2 tests)

- `test_config_caching` (lines 505, 508) - two calls to `get_config()`
- `test_is_configured_method` (lines 531, 540) - two calls to `is_configured()`

---

## Phase Z: Verification

### Success Criteria

- [ ] All 19 tests pass
- [ ] No other tests break

### Test Plan

```bash
pytest tests/integration/test_notion_config_loading.py -v
```

### Rollback Plan

Revert changes to `tests/integration/test_notion_config_loading.py`.

---

## Work Characteristics

- **Scope**: Single file, mechanical find-replace with minor additions
- **Risk**: Low - test file only, no production code
- **Duration**: ~15 minutes
- **Worktree**: Skip (test maintenance)
