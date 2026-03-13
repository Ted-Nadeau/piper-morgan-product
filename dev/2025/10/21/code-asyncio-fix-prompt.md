# Fix Asyncio Test Failures: Quick Investigation & Resolution

**Agent**: Claude Code (Programmer)
**Task**: Fix 2 failing performance tests with asyncio errors
**Issue**: #227 CORE-USERS-JWT
**Date**: October 21, 2025, 5:17 PM
**Estimated Time**: 15-30 minutes

---

## Current Situation

**Working**:
- ✅ 17/17 core functionality tests passing
- ✅ 1/3 performance tests passing (critical lookup test)
- ✅ Performance target exceeded (1.423ms < 5ms)

**Failing**:
- ❌ 2/3 performance tests (asyncio event loop errors)
- Tests: Likely `test_blacklist_add_performance` and `test_concurrent_blacklist_operations`

**Your diagnosis**: "pytest-asyncio event loop issues" + "Fixture scope mismatch"

---

## Quick Investigation (5 minutes)

### Step 1: Get Exact Error Messages

```bash
# Run the failing tests with verbose output
pytest tests/performance/test_token_blacklist_performance.py -v -s

# Capture the EXACT error messages
# Look for patterns like:
# - "RuntimeError: Event loop is closed"
# - "RuntimeError: There is no current event loop"
# - "Task was destroyed but it is pending"
# - "Different event loop running"
```

**Show me the exact error output!**

---

## Common Asyncio Test Issues & Fixes

### Issue 1: Fixture Scope Mismatch

**Problem**: Fixture using `scope="session"` but needs `scope="function"`

**Check**:
```bash
grep -B 2 "@pytest.fixture" tests/performance/test_token_blacklist_performance.py
```

**Fix**:
```python
# BEFORE (causes issues)
@pytest.fixture(scope="session")
async def blacklist():
    ...

# AFTER (fixes issues)
@pytest.fixture(scope="function")
async def blacklist():
    ...
```

---

### Issue 2: Missing pytest-asyncio Configuration

**Problem**: pytest-asyncio not configured or wrong mode

**Check**:
```bash
# Look for pytest configuration
cat pytest.ini 2>/dev/null
cat pyproject.toml | grep -A 5 asyncio 2>/dev/null
cat setup.cfg | grep -A 5 asyncio 2>/dev/null
```

**Fix Option A** (pytest.ini):
```ini
[pytest]
asyncio_mode = auto
```

**Fix Option B** (pyproject.toml):
```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

---

### Issue 3: Missing @pytest.mark.asyncio Decorator

**Problem**: Async test functions not marked properly

**Check**:
```bash
# Look for async tests without decorator
grep -B 1 "async def test_" tests/performance/test_token_blacklist_performance.py
```

**Fix**:
```python
# BEFORE (might cause issues)
async def test_blacklist_add_performance(blacklist):
    ...

# AFTER (explicitly marked)
@pytest.mark.asyncio
async def test_blacklist_add_performance(blacklist):
    ...
```

---

### Issue 4: Event Loop Not Closed Properly

**Problem**: Previous tests leave event loop in bad state

**Check**:
```bash
# Look for event loop cleanup in fixtures
grep -A 10 "yield" tests/performance/test_token_blacklist_performance.py
```

**Fix**:
```python
@pytest.fixture(scope="function")
async def blacklist():
    # Setup
    bl = TokenBlacklist(...)
    await bl.initialize()

    yield bl

    # Teardown - ensure cleanup
    if hasattr(bl, 'cleanup'):
        await bl.cleanup()
```

---

### Issue 5: pytest-asyncio Version Issue

**Problem**: Old pytest-asyncio version with bugs

**Check**:
```bash
pip show pytest-asyncio
```

**Fix** (if version < 0.21.0):
```bash
pip install --upgrade pytest-asyncio
```

---

## Most Likely Fix (Based on "Fixture Scope Mismatch")

**Your diagnosis mentioned fixture scope**, so this is probably it:

### Quick Fix Steps:

**1. Find the performance test file**:
```bash
cat tests/performance/test_token_blacklist_performance.py
```

**2. Look for fixtures with wrong scope**:
```python
# Find this pattern
@pytest.fixture(scope="session")  # ← WRONG for async
async def blacklist():
    ...

# Or this pattern
@pytest.fixture(scope="module")   # ← ALSO WRONG for async
async def blacklist():
    ...
```

**3. Change to function scope**:
```python
# FIX: Use function scope for async fixtures
@pytest.fixture(scope="function")
async def blacklist():
    ...
```

**4. Re-run tests**:
```bash
pytest tests/performance/test_token_blacklist_performance.py -v
```

---

## Systematic Fix Process

### Phase 1: Identify Root Cause (5 min)

```bash
# Get exact errors
pytest tests/performance/test_token_blacklist_performance.py -v -s 2>&1 | tee /tmp/test_errors.txt

# Show me the output
cat /tmp/test_errors.txt
```

### Phase 2: Apply Fix (5 min)

**Most likely**: Change fixture scope to `function`

```bash
# Make the change
# Edit tests/performance/test_token_blacklist_performance.py
# Change fixture scopes from session/module to function
```

### Phase 3: Verify Fix (5 min)

```bash
# Run tests again
pytest tests/performance/test_token_blacklist_performance.py -v

# Should now see:
# test_blacklist_check_performance PASSED
# test_blacklist_add_performance PASSED  ← FIXED!
# test_concurrent_blacklist_operations PASSED  ← FIXED!
```

### Phase 4: Run All Tests (5 min)

```bash
# Verify nothing broke
pytest tests/services/auth/test_token_blacklist.py -v
pytest tests/performance/test_token_blacklist_performance.py -v

# Should see:
# 17 passed (core tests)
# 3 passed (performance tests)  ← ALL PASSING NOW!
```

---

## If Quick Fix Doesn't Work

**If fixture scope isn't the issue**, try these in order:

### 1. Add pytest.ini Configuration
```bash
cat > pytest.ini << 'EOF'
[pytest]
asyncio_mode = auto
EOF

pytest tests/performance/test_token_blacklist_performance.py -v
```

### 2. Upgrade pytest-asyncio
```bash
pip install --upgrade pytest-asyncio
pytest tests/performance/test_token_blacklist_performance.py -v
```

### 3. Check for Event Loop Conflicts
```bash
# Look for event loop creation in tests
grep -n "asyncio.new_event_loop\|asyncio.get_event_loop" tests/performance/
```

---

## Success Criteria

Tests are fixed when:

- [ ] All 3 performance tests passing
- [ ] No asyncio errors in output
- [ ] All 17 core tests still passing
- [ ] Test output clean (no warnings about event loops)

**Evidence required**:
```bash
pytest tests/performance/test_token_blacklist_performance.py -v
# Output should show:
# test_blacklist_check_performance PASSED
# test_blacklist_add_performance PASSED
# test_concurrent_blacklist_operations PASSED
# =================== 3 passed in X.XXs ===================
```

---

## Expected Timeline

**Optimistic** (if fixture scope issue): 10-15 minutes
- 5 min: Identify error
- 5 min: Change fixture scope
- 5 min: Verify all tests pass

**Realistic** (if configuration needed): 20-30 minutes
- 5 min: Identify error
- 10 min: Try fixes (scope, config, upgrade)
- 5 min: Verify all tests pass
- 5 min: Document solution

**Pessimistic** (if deeper issue): 45 minutes
- Would require STOP and ask PM at this point

---

## Communication Protocol

### When You Start:
```
🔧 Investigating asyncio test failures

Running: pytest tests/performance/test_token_blacklist_performance.py -v -s
[show exact error output]
```

### When You Find Root Cause:
```
🎯 Root cause identified: [description]

Issue: [what's wrong]
Fix: [what needs to change]
Applying fix now...
```

### When Fixed:
```
✅ Asyncio test failures FIXED!

Before: 1/3 performance tests passing
After: 3/3 performance tests passing ✅

Evidence:
[paste pytest output showing all 3 tests passing]

All 20 tests now passing (17 core + 3 performance)
```

### If Stuck After 30 Minutes:
```
⚠️ STOP - Need Help

Tried:
1. [what you tried]
2. [what you tried]
3. [what you tried]

Still seeing: [error]

Need PM guidance on next steps.
```

---

## Most Likely Solution (Prediction)

**I predict the fix is**:

```python
# In tests/performance/test_token_blacklist_performance.py

# Change this:
@pytest.fixture(scope="session")  # ← REMOVE
async def blacklist():
    ...

# To this:
@pytest.fixture(scope="function")  # ← ADD
async def blacklist():
    ...
```

**Rationale**:
- You diagnosed "fixture scope mismatch"
- Async fixtures need function scope for proper event loop management
- Session/module scope causes event loop conflicts between tests

---

## Action Items

1. **Get exact error messages** (5 min)
2. **Apply most likely fix** (fixture scope) (5 min)
3. **Verify all tests pass** (5 min)
4. **Report success** with evidence

**Total estimated time**: 15-20 minutes

---

**Let's fix these tests quickly and get to 100% completion!** 🚀

Start by showing me the exact error output from the failing tests.
