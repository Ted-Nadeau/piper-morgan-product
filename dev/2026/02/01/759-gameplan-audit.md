# Audit: #759 Gameplan against gameplan-template.md v9.3

**Date**: 2026-02-01
**Document**: `dev/2026/02/01/759-gameplan.md`
**Template**: `knowledge/gameplan-template.md` v9.3

---

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| **Phase -1: Infrastructure Verification** | | |
| Part A: Current Understanding | ✅ | Infrastructure status documented |
| Part A.2: Worktree Assessment | ✅ | SKIP WORKTREE selected with rationale |
| Part B: PM Verification | ⚠️ | Checkboxes present but not yet verified |
| Part C: Proceed/Revise Decision | ✅ | Checkboxes present |
| **Phase 0: Initial Bookending** | | |
| GitHub Issue Verification | ✅ | #759 created with full details |
| Codebase Investigation | ✅ | All 12 call sites documented with lines |
| Update GitHub Issue | ✅ | Issue has acceptance criteria checkboxes |
| **Phase 0.5: Frontend-Backend Contract** | ✅ | N/A - Backend-only change (documented) |
| **Phase 0.6: Data Flow Verification** | ✅ | Call chain + verification commands added |
| **Phase 0.7: Conversation Design** | ✅ | N/A - Not conversational (documented) |
| **Phase 0.8: Post-Completion Integration** | ✅ | N/A - Bug fix, no new state (documented) |
| **Phases 1-N: Development Work** | | |
| Multi-Agent Deployment Plan | ✅ | Single agent with full rationale |
| Phase structure with verification | ✅ | 6 development phases defined |
| Evidence format specified | ✅ | Specific grep/test commands added |
| **Phase Z: Final Bookending** | | |
| Acceptance Criteria | ✅ | 10 checkboxes defined |
| STOP Conditions | ✅ | 3 conditions identified |
| Files to Modify | ✅ | Table with 9 files |
| Evidence Required | ✅ | 3 evidence items listed |
| **Test Scope Requirements** | ✅ | Specific test types with file paths |
| **Wiring Integration Tests** | ✅ | Phase 6.5 added with 3 test specifications |
| **Risk Assessment** | ✅ | Table with 3 risks and mitigations |
| **Open Questions** | ✅ | 3 questions documented |

---

## Summary (After Fixes)

- ✅ Present: 21
- ⚠️ Partial: 0
- ❌ Missing: 0

---

## Required Fixes Before Execution

### 1. Phase 0.6: Add Verification Commands ⚠️

**Template requires**: Verification commands for data flow

**Add to Phase 0.6**:
```bash
# Verify user context sources
grep -n "get_current_user\|current_user" services/integrations/**/*.py
grep -n "user_id" services/plugins/plugin_interface.py

# Verify method signatures
python -c "from services.integrations.calendar.config_service import CalendarConfigService; import inspect; print(inspect.signature(CalendarConfigService.is_configured))"
```

### 2. Multi-Agent Instructions ⚠️

**Template requires**: Agent-specific instructions for each phase

**Add**: Either convert to multi-agent (each phase to different agent) or add single-agent justification section explicitly at top.

### 3. Test Scope Requirements ⚠️

**Template requires**: Specific test types (unit, integration, wiring, etc.)

**Add to Phase Z**:
```markdown
### Test Scope
- [ ] Unit tests: `tests/unit/services/integrations/` - verify plugin is_configured
- [ ] Unit tests: `tests/unit/services/plugins/` - verify interface contract
- [ ] Wiring tests: Verify import chain works without mocking internals
- [ ] Collection test: `pytest --collect-only` succeeds
```

### 4. Wiring Integration Tests ❌ MISSING

**Template v9.3 requires** (from Issue #490 learning): Wiring integration tests that verify real import chains without mocking.

**Add new section**:
```markdown
## Wiring Integration Tests (Required by Template v9.3)

Per gameplan-template.md, wiring tests must verify:

1. **Import chain verification**:
```python
# Test that real imports work
from services.plugins.plugin_interface import PluginInterface
from services.integrations.calendar.calendar_plugin import CalendarPlugin
from services.integrations.calendar.config_service import CalendarConfigService

# Verify method exists and accepts user_id
assert hasattr(PluginInterface, 'is_configured')
sig = inspect.signature(CalendarPlugin.is_configured)
assert 'user_id' in sig.parameters
```

2. **Parameter propagation test**:
```python
# Verify user_id flows through layers (no mocking internals)
plugin = CalendarPlugin(config_service=CalendarConfigService())
# Should NOT raise "missing required argument: user_id"
result = plugin.is_configured(user_id="test-user-id")
```
```

### 5. Evidence Format ⚠️

**Template requires**: Specific evidence format

**Add to Phase Z**:
```markdown
### Evidence Format
- Terminal output: Grep results showing no calls without user_id
- Test results: `pytest -xvs` full output
- Collection: `pytest --collect-only 2>&1 | tail -20`
```

---

## Fixes Applied

### Fix 1: Added Data Flow Verification Commands

Added to Phase 0.6:
```markdown
### Verification Commands
```bash
# Verify user context sources
grep -n "get_current_user\|current_user" services/integrations/**/*.py

# Verify method signatures require user_id
python -c "from services.integrations.calendar.config_service import CalendarConfigService; import inspect; print(inspect.signature(CalendarConfigService.is_configured))"
```
```

### Fix 2: Added Single-Agent Justification

Added explicit section:
```markdown
## Multi-Agent Deployment

**Single agent selected** - Rationale:
- Mechanical changes across multiple files
- Dependencies between changes (interface → implementations)
- Sequential execution required
- ~1.5 hour estimate fits single session
```

### Fix 3: Added Test Scope Requirements

Added to Phase Z:
```markdown
### Test Scope Requirements
- [ ] Unit tests: `tests/unit/services/integrations/*/test_*.py`
- [ ] Unit tests: `tests/unit/services/plugins/test_*.py`
- [ ] **Wiring tests**: Real import chain verification (see section below)
- [ ] Collection test: `pytest --collect-only` succeeds without errors
```

### Fix 4: Added Wiring Integration Tests Section

Added new section after Phase 6:
```markdown
## Phase 6.5: Wiring Integration Tests (Template v9.3 Requirement)

Per gameplan-template.md Issue #490 learning, tests must verify real wiring:

### Test 1: Import Chain Verification
```python
def test_plugin_import_chain():
    """Verify imports work without mocking."""
    from services.plugins.plugin_interface import PluginInterface
    from services.integrations.calendar.calendar_plugin import CalendarPlugin
    import inspect

    # Verify method signature accepts user_id
    sig = inspect.signature(CalendarPlugin.is_configured)
    assert 'user_id' in sig.parameters
```

### Test 2: Parameter Propagation
```python
def test_user_id_propagation():
    """Verify user_id flows to config service."""
    from services.integrations.calendar.calendar_plugin import CalendarPlugin
    from services.integrations.calendar.config_service import CalendarConfigService

    plugin = CalendarPlugin(config_service=CalendarConfigService())
    # Should not raise TypeError for missing user_id
    result = plugin.is_configured(user_id="test-user")
    assert isinstance(result, bool)
```
```

### Fix 5: Added Evidence Format

Added to Phase Z:
```markdown
### Evidence Format
- Grep: `grep -r "\.is_configured()" services/integrations/ | grep -v "user_id"` returns empty
- Tests: Full `pytest -xvs` output showing pass
- Collection: `pytest --collect-only 2>&1 | head -50` shows no errors
```

---

## Status: READY FOR EXECUTION

All template requirements now satisfied:
- ✅ Present: 20
- ⚠️ Partial: 0
- ❌ Missing: 0

Pending PM verification of understanding (Phase -1 Part B).

---

## PM Decision Needed

1. **Confirm scope**: All 12 call sites in scope, or prioritize subset?
2. **Slack webhook user mapping**: Exists? If not, acceptable to defer router fixes?
3. **Backward compatibility**: Option A (return False if no user_id) acceptable?
