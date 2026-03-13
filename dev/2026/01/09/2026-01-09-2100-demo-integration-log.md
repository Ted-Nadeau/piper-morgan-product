# Session Log: Demo Integration Investigation

**Bead:** piper-morgan-7ik
**Date:** 2026-01-09 21:00
**Agent:** Claude Code (Opus 4.5)
**Task:** Investigate why 'Demo' integration appears in Piper's identity response

## Investigation Summary

### Problem Statement
When users ask Piper about its capabilities/identity, a "Demo" integration appears in the response. Users don't recognize this integration and it causes confusion.

### Root Cause Analysis

**Flow traced:**
1. User asks "Who are you?" or similar identity query
2. `CanonicalHandlers._handle_identity_query()` is called (line 167)
3. It calls `_get_dynamic_capabilities()` (line 60-111)
4. This method queries `get_plugin_registry().get_status_all()` and includes plugins where `configured=True` OR `active=True`
5. The Demo plugin (`services/integrations/demo/`) auto-registers at import time
6. `DemoConfigService.is_configured()` returns `self.enabled`
7. `self.enabled = os.getenv("DEMO_ENABLED", "true").lower() == "true"` - **default is TRUE**

**The bug:** Demo plugin's `DEMO_ENABLED` environment variable defaults to `"true"`, making it always appear as configured and thus included in identity responses.

### Files Involved

| File | Relevance |
|------|-----------|
| `services/integrations/demo/config_service.py` | Contains the problematic default |
| `services/integrations/demo/demo_plugin.py` | Auto-registers plugin |
| `services/intent_service/canonical_handlers.py` | Queries plugin registry for identity responses |

### Key Code Snippets

**The problematic default (config_service.py line 23):**
```python
self.enabled = os.getenv("DEMO_ENABLED", "true").lower() == "true"
```

**Plugin inclusion logic (canonical_handlers.py lines 85-87):**
```python
is_configured = status.get("configured", False)
is_active = status.get("active", False) or status.get("status") == "active"
if is_configured or is_active:
```

### Recommendation

**Fix:** Change the default value of `DEMO_ENABLED` from `"true"` to `"false"`.

**Rationale:**
- The Demo plugin is a developer template, not a user-facing feature
- Developers creating new integrations can explicitly set `DEMO_ENABLED=true` for testing
- Production environments should never show "Demo integration template for developers" to users
- This is the minimal, targeted fix with lowest risk of regression

### Alternative Considered (Not Recommended)

Adding filtering in `_get_dynamic_capabilities()` to exclude "demo" was considered but rejected because:
- It adds special-case logic to the canonical handlers
- The root cause is the inappropriate default, not the inclusion logic
- Better to fix at the source than add workarounds

## Fix Applied

### Code Changes

**1. `services/integrations/demo/config_service.py`:**
- Changed default from `os.getenv("DEMO_ENABLED", "true")` to `os.getenv("DEMO_ENABLED", "false")`
- Updated docstring for `is_configured()` to clarify new behavior

**2. `services/integrations/demo/tests/test_demo_plugin.py`:**
- Updated 3 tests to expect `is_configured() == False` by default
- Added comments explaining the fix references bead piper-morgan-7ik

**3. `tests/unit/services/integrations/demo/test_demo_plugin.py`:**
- Updated 3 tests to match new behavior (duplicate test file in unit test directory)

## Testing

- [x] Run tests for demo plugin: `python -m pytest services/integrations/demo/tests/ -v` - **9 passed**
- [x] Run identity/canonical handler tests: `python -m pytest tests/unit/services/intent_service/ -v -k "identity or canonical"` - **204 passed**
- [x] Run smoke tests: `python -m pytest tests/unit/ -m smoke` - **614 passed, 1 skipped**
- [ ] Manual verification: Start server, ask "who are you?", confirm Demo is not listed

## Files Modified

1. `services/integrations/demo/config_service.py` - Changed default DEMO_ENABLED to "false"
2. `services/integrations/demo/tests/test_demo_plugin.py` - Updated test expectations
3. `tests/unit/services/integrations/demo/test_demo_plugin.py` - Updated test expectations

## Status

- [x] Investigation complete
- [x] Root cause identified
- [x] Fix implemented
- [x] Tests verified (all passing)
- [x] Ready for commit

## Commit Message

```
fix(demo-plugin): Disable Demo integration by default (bead piper-morgan-7ik)

The Demo integration was appearing in Piper's identity responses because
DEMO_ENABLED defaulted to "true". This caused user confusion as they saw
"Demo: Demo integration template for developers" in capabilities.

Changes:
- Set DEMO_ENABLED default to "false" in DemoConfigService
- Update tests to expect disabled-by-default behavior
- Add docstring clarifying the new default

Developers can still enable the demo plugin for testing by setting
DEMO_ENABLED=true in their environment.
```
