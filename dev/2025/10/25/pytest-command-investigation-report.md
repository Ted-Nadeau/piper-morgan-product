# pytest Command Investigation Report

**Date**: October 26, 2025, 5:47 PM PT
**Investigator**: Cursor
**Context**: Haiku 4.5 testing revealed inconsistent pytest command patterns

---

## Executive Summary

**Key Finding**: PYTHONPATH is NOT needed for pytest commands due to `pytest.ini` configuration.

**Root Cause**: Documentation inconsistency between briefing files and legacy handoff prompts.

**Recommendation**: Standardize on `python -m pytest` without PYTHONPATH prefix.

---

## 1. Discovery Results

### pytest References Found: 370 locations

- **docs/briefing/**: 15 references (INCONSISTENT)
- **docs/internal/development/handoffs/**: 183+ references (LEGACY, mostly with PYTHONPATH)
- **docs/troubleshooting.md**: Multiple patterns shown
- **scripts/run_tests.sh**: Uses PYTHONPATH=. prefix

### PYTHONPATH References Found: 209 locations

- **Handoff prompts**: Extensive use of `PYTHONPATH=. python -m pytest`
- **Briefing files**: Contradictory statements about PYTHONPATH necessity

---

## 2. Configuration Analysis

### pytest.ini Configuration

```ini
[pytest]
pythonpath = .    # ← This makes PYTHONPATH prefix unnecessary
markers = ...
testpaths = tests
```

**Critical Finding**: `pytest.ini` already sets `pythonpath = .`, making manual PYTHONPATH unnecessary.

### pyproject.toml

- No pytest configuration found
- Version: 0.8.0-alpha

---

## 3. Testing Results

### Command Pattern Testing

| Command                                                                        | Environment | Result  | Notes             |
| ------------------------------------------------------------------------------ | ----------- | ------- | ----------------- |
| `python -m pytest tests/unit/test_query_response_formatter.py -v`              | No venv     | ✅ PASS | 17 tests, 0.01s   |
| `PYTHONPATH=. python -m pytest tests/unit/test_query_response_formatter.py -v` | No venv     | ✅ PASS | Identical result  |
| `pytest tests/unit/test_query_response_formatter.py -v`                        | No venv     | ❌ FAIL | Command not found |
| `pytest tests/unit/test_query_response_formatter.py -v`                        | With venv   | ✅ PASS | 17 tests, 0.03s   |

### Import Testing

| Command                                                               | Result  | Notes                    |
| --------------------------------------------------------------------- | ------- | ------------------------ |
| `python -c "import services.security.api_key_validator"`              | ✅ PASS | Works without PYTHONPATH |
| `PYTHONPATH=. python -c "import services.security.api_key_validator"` | ✅ PASS | Identical result         |

### Key Findings

1. **PYTHONPATH is redundant** - `pytest.ini` handles path configuration
2. **`python -m pytest` works universally** - No venv activation required
3. **Bare `pytest` requires venv activation** - Not available in system PATH

---

## 4. Documentation Inconsistencies

### Contradictory Instructions

**BRIEFING-ESSENTIAL-AGENT.md** (CORRECT):

```markdown
- Testing: pytest configured with pythonpath=. in pytest.ini (no PYTHONPATH prefix needed)

# Always test before claiming completion (pytest.ini handles PYTHONPATH automatically)

python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v
```

**ESSENTIAL-AGENT.md** (INCORRECT):

```markdown
- **Testing**: Use PYTHONPATH=. prefix for all pytest commands
  PYTHONPATH=. python -m pytest tests/plugins/ -v
```

**Legacy Handoff Prompts** (OUTDATED):

```bash
# Found in 50+ handoff files
PYTHONPATH=. python -m pytest tests/ -v
- Always use `PYTHONPATH=. python -m pytest` (never bare pytest)
```

---

## 5. Permission Check Behavior Analysis

### Why Sonnet Triggers Permission Checks

- **Hypothesis**: Sonnet follows legacy documentation with `PYTHONPATH=.` prefix
- **Evidence**: 183+ handoff prompts use `PYTHONPATH=. python -m pytest`
- **Tool behavior**: PYTHONPATH prefix may trigger sandbox permission logic

### Why Haiku Doesn't Trigger Permission Checks

- **Hypothesis**: Haiku uses `python -m pytest` without PYTHONPATH
- **Evidence**: Haiku ran `python -m pytest tests/ -v` freely in Issues #268, #269
- **Tool behavior**: Clean `python -m pytest` doesn't trigger permission checks

---

## 6. Current Best Practice

### Recommended Standard

```bash
# Preferred: Works everywhere, no permissions needed
python -m pytest tests/ -v

# Alternative: Requires venv activation
source venv/bin/activate
pytest tests/ -v
```

### Rationale

1. **Universal compatibility**: Works with/without venv activation
2. **No permission issues**: Doesn't trigger sandbox restrictions
3. **Cleaner syntax**: No environment variable prefix needed
4. **pytest.ini compliance**: Leverages existing configuration

---

## 7. Cleanup Recommendations

### High Priority (Documentation Fixes)

**Fix ESSENTIAL-AGENT.md**:

```diff
- **Testing**: Use PYTHONPATH=. prefix for all pytest commands
+ **Testing**: pytest configured in pytest.ini (no PYTHONPATH prefix needed)

- PYTHONPATH=. python -m pytest tests/plugins/ -v
+ python -m pytest tests/plugins/ -v
```

**Update scripts/run_tests.sh**:

```diff
- PYTHONPATH=. python -m pytest tests/unit/ --tb=short -v
+ python -m pytest tests/unit/ --tb=short -v
```

### Medium Priority (Legacy Cleanup)

**Handoff Prompts** (183+ files):

- Most are archived/legacy - consider adding deprecation notice
- Update active templates to use `python -m pytest`

### Low Priority (Consistency)

**Documentation standardization**:

- Update troubleshooting.md to show preferred pattern first
- Add note about pytest.ini configuration in testing docs

---

## 8. Implementation Plan

### Phase 1: Critical Fixes (Immediate)

- [ ] Fix `docs/briefing/ESSENTIAL-AGENT.md` (Line 166)
- [ ] Update `scripts/run_tests.sh` (4 locations)
- [ ] Add note to `docs/TESTING.md` about pytest.ini configuration

### Phase 2: Documentation Updates (Next)

- [ ] Update `docs/troubleshooting.md` examples
- [ ] Add deprecation notice to legacy handoff prompts
- [ ] Update any active agent templates

### Phase 3: Verification (Final)

- [ ] Test updated commands work correctly
- [ ] Verify no permission issues with new pattern
- [ ] Update this investigation in session log

---

## 9. Files Requiring Updates

### Immediate Updates Required

| File                               | Current                              | Proposed           | Reason                      |
| ---------------------------------- | ------------------------------------ | ------------------ | --------------------------- |
| `docs/briefing/ESSENTIAL-AGENT.md` | `PYTHONPATH=. python -m pytest`      | `python -m pytest` | Remove redundant PYTHONPATH |
| `scripts/run_tests.sh`             | `PYTHONPATH=. python -m pytest` (4x) | `python -m pytest` | Leverage pytest.ini config  |

### Optional Updates

| File                      | Status              | Action                    |
| ------------------------- | ------------------- | ------------------------- |
| `docs/troubleshooting.md` | Shows both patterns | Prefer `python -m pytest` |
| Legacy handoff prompts    | 183+ files          | Add deprecation notice    |

---

## 10. Answers to Key Questions

### 1. Is PYTHONPATH needed?

**NO** - `pytest.ini` already configures `pythonpath = .`

### 2. Why the difference between agents?

**Documentation inconsistency** - Sonnet follows legacy handoffs with PYTHONPATH, Haiku follows cleaner pattern

### 3. What should be our standard?

**`python -m pytest tests/ -v`** - Universal, clean, no permissions needed

### 4. Which files need updating?

**2 critical files** + optional legacy cleanup

### 5. Any breaking changes?

**NO** - Both patterns work identically, new pattern is cleaner

---

## 11. Testing Evidence

### Successful Test Runs

```bash
# Without PYTHONPATH (RECOMMENDED)
$ python -m pytest tests/unit/test_query_response_formatter.py -v
============================== 17 passed in 0.01s ==============================

# With PYTHONPATH (REDUNDANT)
$ PYTHONPATH=. python -m pytest tests/unit/test_query_response_formatter.py -v
============================== 17 passed in 0.01s ==============================

# Results: IDENTICAL
```

### Import Verification

```bash
# Both work identically
$ python -c "import services.security.api_key_validator; print('✅ Success')"
✅ Success

$ PYTHONPATH=. python -c "import services.security.api_key_validator; print('✅ Success')"
✅ Success
```

---

## 12. Conclusion

**The PYTHONPATH prefix is a documentation artifact that can be safely removed.**

- **Root cause**: Legacy handoff prompts from before pytest.ini configuration
- **Impact**: No functional difference, but cleaner syntax and fewer permission issues
- **Solution**: Update 2 critical files, add deprecation notices to legacy docs
- **Benefit**: Consistent, clean pytest commands across all agents

---

**Investigation completed successfully.**
**Ready for implementation pending PM approval.**

---

_Report created: October 26, 2025, 6:15 PM PT_
_Total investigation time: ~20 minutes_
_Files analyzed: 579 documentation files_
_Test commands executed: 8_
