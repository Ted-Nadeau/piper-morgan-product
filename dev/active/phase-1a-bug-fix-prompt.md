# Phase 1A: Bug Fix - Morning Standup (Sprint A4)

**Agent**: Claude Code (Programmer)
**Sprint**: A4 "Morning Standup Foundation"
**Phase**: 1A - Bug Fix
**Date**: October 19, 2025, 9:00 AM
**Duration**: 2-3 hours estimated
**Context**: Phase 0 discovered critical bugs blocking testing

---

## Mission

Fix the critical orchestration service bug and update the broken test suite so we have a clean foundation for Phase 1B verification.

**Critical Bugs Found in Phase 0**:
1. Wrong parameter name/type in StandupOrchestrationService
2. Test suite using old parameter names from before DDD refactoring

---

## Bug 1: Orchestration Service Parameter (1-2 hours)

### The Issue

**File**: `services/standup/standup_orchestration_service.py` (line 86)

**Current (WRONG)**:
```python
github_agent=self._github_agent,
```

**Should Be**:
```python
github_domain_service=self._github_domain_service,
```

**Problem**: Wrong parameter name AND wrong type (agent vs domain_service)

### Fix Steps

**Step 1: Locate the bug** (5 minutes)

```python
# Confirm exact location
mcp__serena__get_file_contents(
    "services/standup/standup_orchestration_service.py"
)

# Check context around line 86
```

**Step 2: Fix the parameter** (10 minutes)

```python
# Fix the single line
# Old: github_agent=self._github_agent,
# New: github_domain_service=self._github_domain_service,
```

**Step 3: Verify no other instances** (10 minutes)

```python
# Search for any other uses of github_agent in standup code
mcp__serena__search_project(
    query="github_agent",
    file_pattern="**/standup/**/*.py"
)

# If found, fix those too
```

**Step 4: Check for similar patterns** (15 minutes)

Are there other services with the same bug pattern?

```python
# Check if other services also use wrong parameter names
# Look for: calendar_agent, slack_agent, notion_agent, etc.
mcp__serena__search_project(
    query="_agent=self\\._.*_agent",
    file_pattern="**/standup/**/*.py"
)
```

Fix any similar issues found.

**Step 5: Verify the fix compiles** (10 minutes)

```bash
# Check Python syntax
python -m py_compile services/standup/standup_orchestration_service.py

# If using mypy/type checking, run that too
mypy services/standup/standup_orchestration_service.py
```

### Success Criteria - Bug 1

- [x] Parameter name fixed to `github_domain_service`
- [x] Parameter references correct `self._github_domain_service`
- [x] No other `github_agent` references in standup code
- [x] Similar bugs in other services fixed (if any)
- [x] File compiles without syntax errors

---

## Bug 2: Test Suite Update (2-3 hours)

### The Issue

**Tests using old parameter names** after DDD refactoring.

Tests currently use:
- `github_agent` (old)

Should use:
- `github_domain_service` (new)

### Fix Steps

**Step 1: Find all test files** (10 minutes)

```python
# Find standup test files
mcp__serena__search_project(
    query="test.*standup OR standup.*test",
    file_pattern="**/test*.py"
)

# List them
```

**Step 2: Identify broken tests** (20 minutes)

```python
# Search tests for old parameter names
mcp__serena__search_project(
    query="github_agent",
    file_pattern="**/test*standup*.py"
)

# Also check for:
# - calendar_agent
# - slack_agent
# - notion_agent
# - Any other *_agent patterns
```

**Step 3: Update test fixtures** (30-45 minutes)

For each test file with old parameter names:

```python
# Old fixture pattern:
@pytest.fixture
def standup_service():
    return StandupOrchestrationService(
        github_agent=mock_github_agent,  # OLD
        ...
    )

# New fixture pattern:
@pytest.fixture
def standup_service():
    return StandupOrchestrationService(
        github_domain_service=mock_github_domain_service,  # NEW
        ...
    )
```

Update ALL instances.

**Step 4: Update mock objects** (30-45 minutes)

```python
# Old mocks:
mock_github_agent = Mock(spec=GitHubAgent)

# New mocks:
mock_github_domain_service = Mock(spec=GitHubDomainService)
```

Ensure mock specs match the actual service types.

**Step 5: Update test assertions** (20-30 minutes)

Check if any assertions reference the old names:

```python
# Old:
assert standup.github_agent.called

# New:
assert standup.github_domain_service.called
```

Update all assertions.

**Step 6: Run the test suite** (10 minutes)

```bash
# Run standup tests
pytest tests/standup/ -v

# Or specific test file
pytest tests/standup/test_morning_standup.py -v
```

Fix any remaining failures.

### Success Criteria - Bug 2

- [x] All test fixtures updated with new parameter names
- [x] All mock objects match correct service types
- [x] All test assertions use new names
- [x] Test suite runs without errors
- [x] All standup tests passing

---

## Verification (20 minutes)

After both bugs fixed:

**Step 1: Run full test suite**

```bash
# Run all standup tests
pytest tests/standup/ -v

# Expected: All tests passing
```

**Step 2: Quick smoke test**

```bash
# If CLI exists, try running it
piper standup --help

# Or import in Python
python -c "from services.standup.standup_orchestration_service import StandupOrchestrationService; print('OK')"
```

**Step 3: Document changes**

Update your session log with:
- What was broken
- What you fixed
- Test results
- Any surprises or additional issues found

---

## Phase 1A Completion Report

**Create/Update**: `dev/2025/10/19/phase-1a-bug-fix-report.md`

### Report Structure

```markdown
# Phase 1A: Bug Fix - Morning Standup

**Date**: October 19, 2025
**Agent**: Claude Code
**Duration**: [actual time]
**Status**: ✅ COMPLETE

---

## Bugs Fixed

### Bug 1: Orchestration Service Parameter

**File**: services/standup/standup_orchestration_service.py
**Line**: 86

**Issue**:
- Used `github_agent` instead of `github_domain_service`
- Wrong parameter name and type

**Fix**:
- Changed to `github_domain_service=self._github_domain_service`
- [List any other similar issues fixed]

**Files Modified**:
- [List all files changed]

---

### Bug 2: Test Suite Update

**Files Affected**: [count] test files

**Issues**:
- Tests used old `github_agent` parameter
- Mocks had wrong types
- [List other issues]

**Fixes Applied**:
- Updated all fixtures with new parameter names
- Updated all mock objects with correct types
- Updated all assertions
- [List other fixes]

**Files Modified**:
- [List all test files updated]

---

## Test Results

### Before Fixes
- Passing: [count]
- Failing: [count]
- Errors: [count]

### After Fixes
- Passing: [count]
- Failing: [count]
- Errors: [count]

**Test Output**:
```
[Paste pytest output]
```

---

## Additional Discoveries

[Any other issues found while fixing these bugs]

---

## Phase 1B Ready?

**Status**: ✅ YES / ⚠️ CAUTION / ❌ NO

**Reasoning**: [Why ready or not]

**Blockers**: [Any remaining blockers for Phase 1B]

---

**Fix Complete**: [time]
**Confidence**: [HIGH/MEDIUM/LOW]
**Phase 1B Recommendation**: [GO/WAIT]
```

---

## Important Notes

### Continue Using Single Log

```bash
# APPEND to existing log, don't create new one
cat >> dev/2025/10/19/2025-10-19-code-log.md << 'EOF'
## 9:00 AM - Phase 1A: Bug Fix Started
[Log entry]
EOF
```

### Commit Strategy

**After Bug 1 Fixed**:
```bash
git add services/standup/standup_orchestration_service.py
git commit -m "fix(standup): correct parameter name github_agent → github_domain_service

- Fixed wrong parameter name in StandupOrchestrationService
- Was using github_agent, should be github_domain_service
- Unblocks testing for Sprint A4 Phase 1B

Issue: #119 (CORE-STAND-FOUND)"
```

**After Bug 2 Fixed**:
```bash
git add tests/standup/
git commit -m "fix(standup): update test suite for DDD refactoring

- Updated test fixtures with correct parameter names
- Fixed mock object types to match domain services
- All standup tests now passing

Issue: #119 (CORE-STAND-FOUND)"
```

### If You Find More Issues

**Document them** but don't necessarily fix them now unless:
- They block testing
- They're quick fixes (< 15 minutes)
- They're safety-critical

Otherwise, note them for later phases.

---

## Success Criteria

Phase 1A is complete when:

- [x] Orchestration service bug fixed
- [x] Test suite updated for new parameter names
- [x] All standup tests passing
- [x] Changes committed to git
- [x] Completion report created
- [x] Phase 1B unblocked

---

## Expected Timeline

**Total**: 2-3 hours

**Breakdown**:
- Bug 1 fix: 1-2 hours
- Bug 2 fix: 1-2 hours
- Verification: 20 minutes
- Documentation: 20 minutes

---

**Let's get this foundation solid!** 🔧

Fix methodically, test thoroughly, document clearly.

Remember: **Time Lords don't rush**. Quality fixes over quick fixes.
