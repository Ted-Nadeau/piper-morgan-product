# Conftest Auto-Mock Investigation (piper-morgan-otf)
**Date:** 2025-11-20 2:05 PM
**Bead:** piper-morgan-otf (P2)
**Issue:** Auto-mock in conftest.py hiding 15+ test failures

---

## Problem Statement

`tests/conftest.py` contains an `autouse=True` fixture that automatically mocks `TokenBlacklist.is_blacklisted()` for ALL unit tests, always returning `False` (token not blacklisted).

**Location:** tests/conftest.py:50-86

```python
@pytest.fixture(autouse=True)
def mock_token_blacklist(request):
    """Auto-mock TokenBlacklist for unit tests to prevent database session conflicts"""

    # Skip mock for integration tests
    if "integration" in request.keywords:
        yield
        return

    # Patch TokenBlacklist.is_blacklisted to return False
    with patch(
        "services.auth.token_blacklist.TokenBlacklist.is_blacklisted",
        new=AsyncMock(return_value=False),
    ):
        yield
```

---

## Investigation Findings

### What Works
✅ **Token blacklist tests** (17 tests in `test_token_blacklist.py`) - ALL PASSING
- Reason: Marked with `@pytest.mark.integration` to skip the auto-mock
- These tests have proper Redis/DB mock setup
- Test the actual TokenBlacklist behavior

### What Might Be Hidden

**Hypothesis:** Tests that:
1. ❌ Use authentication/token validation
2. ❌ Are NOT marked as integration tests
3. ❌ Expect tokens to be rejected when blacklisted

**These tests would incorrectly PASS** because:
- Auto-mock always returns False (not blacklisted)
- Tests never see tokens as blacklisted
- Real bugs in auth flow would be hidden

### Why This Auto-Mock Exists

**Issue #281:** Original problem being solved:
```
TokenBlacklist.is_blacklisted() gets async context manager from
overridden db.get_session() in tests, causing '_AsyncGeneratorContextManager'
has no attribute 'execute' errors.
```

**Solution chosen:** Mock it globally for unit tests

**Side effect:** Hides tests that should verify blacklist behavior

---

## Test Discovery Needed

To find the "15+ hidden broken tests" mentioned in the bead, we need to:

### Method 1: Temporarily Disable Auto-Mock
1. Comment out the `autouse=True` fixture
2. Run full test suite
3. See what breaks
4. Those are the hidden failures

**Risk:** Will cause many legitimate failures (the async context manager errors)

### Method 2: Search for Auth Tests Without Integration Mark
Find tests that:
- Import or use `JWTService`, `AuthMiddleware`, or token validation
- Are NOT marked `@pytest.mark.integration`
- Should test token revocation/blacklist behavior

### Method 3: Check Auth Endpoint Tests
File: `tests/auth/test_auth_endpoints.py`
- Uses auth endpoints
- May test token revocation
- If not marked as integration, gets the auto-mock

---

## Current Status

### Tests Verified Working
- ✅ All 17 token blacklist tests (properly marked as integration)

### Tests To Investigate
1. **test_auth_endpoints.py** - Auth endpoint tests (likely affected)
2. **test_jwt_service.py** - JWT token tests (may need blacklist behavior)
3. **Middleware tests** - Token validation in requests
4. **Web endpoint tests** - Protected routes using auth

### Specific Concerns

**Auth Endpoint Tests:** If testing logout/revocation flow:
```python
# Test logout (revokes token)
response = await client.post("/auth/logout", headers={"Authorization": f"Bearer {token}"})

# Test subsequent request with revoked token (SHOULD FAIL)
response2 = await client.get("/protected", headers={"Authorization": f"Bearer {token}"})
# ^ This might incorrectly pass because auto-mock says token isn't blacklisted!
```

---

## Recommended Solution Approaches

### Option A: Remove Auto-Mock (High Impact)
**What:** Remove the `autouse=True` fixture entirely
**Pros:** No hidden tests, everything explicit
**Cons:** Must fix all async context manager errors (Issue #281)
**Effort:** HIGH (2-4 hours) - Need to fix underlying database session issues

### Option B: Add Fixture Parameter Control
**What:** Change auto-mock to opt-out instead of forced
```python
@pytest.fixture
def no_blacklist_mock(request):
    """Marker to disable blacklist auto-mock for specific tests"""
    pass

@pytest.fixture(autouse=True)
def mock_token_blacklist(request, no_blacklist_mock=None):
    # Skip if test explicitly requests no mock
    if hasattr(request, 'no_blacklist_mock'):
        yield
        return
    # ... rest of auto-mock logic
```
**Pros:** Gradual migration, backward compatible
**Cons:** Still hides issues by default
**Effort:** SMALL (30 min) but doesn't solve the core problem

### Option C: Find and Fix Hidden Tests (Recommended)
**What:**
1. Temporarily disable auto-mock
2. Run test suite, collect failures
3. For each failure:
   - If legitimate test (needs real blacklist): Mark as integration + fix setup
   - If broken test logic: Fix the test
   - If false positive (needs mock): Document why
4. Re-enable auto-mock with better documentation

**Pros:** Reveals hidden issues, fixes broken tests
**Cons:** Time-consuming, may reveal real bugs
**Effort:** MEDIUM (1-2 hours)

---

## Next Steps

### Immediate Action
**Disable auto-mock temporarily and collect failures:**

```bash
# 1. Comment out autouse=True in tests/conftest.py line 50
# 2. Run test suite
pytest tests/unit/services/auth/ -v --tb=short

# 3. Collect failures
# 4. Categorize:
#    - Async context manager errors (Issue #281) - Real infrastructure problem
#    - Test failures due to blacklist behavior - Hidden test issues
#    - Other failures - May reveal bugs
```

### Questions for PM/Architect
1. Should we fix Issue #281 properly (database session handling) instead of masking it?
2. What's the priority - quick fix (keep auto-mock) vs proper fix (fix session issues)?
3. Are there known bugs this auto-mock might be hiding?

---

## Risk Assessment

**If Left Unfixed:**
- 🔴 **HIGH RISK**: Auth/token revocation bugs could slip into production
- 🔴 **HIGH RISK**: Tests give false confidence about token security
- 🟡 **MEDIUM RISK**: Future auth features won't be properly tested

**Priority Justification:**
- P2 priority is appropriate
- Should be fixed before alpha release
- Token security is critical path

---

## Time Estimate

**Option A (Remove auto-mock):** 2-4 hours
- Fix async session handling (Issue #281 root cause)
- Update failing tests

**Option B (Add control):** 30 minutes
- Quick fix, doesn't solve problem

**Option C (Find hidden tests):** 1-2 hours
- Diagnostic run: 15 minutes
- Fix hidden tests: 45-90 minutes

**Recommendation:** Option C (Find hidden tests) - best balance of effort vs impact

---

**Status:** Investigation complete, ready for decision on approach
**Blocked on:** PM decision on which option to pursue
