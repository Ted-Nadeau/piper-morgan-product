# Task 3: Authentication Integration - Standup API

**Agent**: Claude Code (Programmer)
**Issue**: #162 (CORE-STAND-MODES-API)
**Task**: 3 of 7 - Authentication Integration
**Sprint**: A4 "Standup Epic"
**Date**: October 19, 2025, 4:05 PM
**Estimated Effort**: Small-Medium (1-1.5 hours)

---

## Mission

Fix the JWT service bug, enable authentication on standup endpoints, generate test tokens, and verify protected endpoints work correctly with real JWT tokens.

**Scope**:
- Fix JWT service bug (found during Task 2)
- Enable REQUIRE_AUTH=true for production use
- Generate test JWT tokens
- Verify all endpoints require valid auth
- Test with real tokens (not optional auth)

**NOT in scope**:
- OpenAPI docs (Task 4)
- Comprehensive testing (Task 6)
- Any new auth features

---

## Context

- **GitHub Issue**: #162 (CORE-STAND-MODES-API) - Multi-modal API
- **Current State**:
  - ✅ JWT auth implemented in Task 1
  - ✅ Service integration tested in Task 2 (with auth optional)
  - ⚠️ JWT service has pre-existing bug
  - ⚠️ REQUIRE_AUTH currently defaults to false
- **Target State**:
  - JWT bug fixed
  - REQUIRE_AUTH=true for production
  - All endpoints protected
  - Working with real tokens
- **Dependencies**:
  - JWT service (services/auth/jwt_service.py)
  - Auth middleware (services/auth/auth_middleware.py)
  - ADR-012: Protocol-Ready JWT Authentication
- **User Data Risk**: None - auth verification only
- **Infrastructure Verified**: Yes - JWT system exists from Phase 1

---

## STOP Conditions (EXPANDED TO 17)

If ANY of these occur, STOP and escalate to PM immediately:

1. **Infrastructure doesn't match gameplan** - JWT service structure different
2. **Method implementation <100% complete** - All auth flows must work
3. **Pattern already exists in catalog** - Check before creating new patterns
4. **Tests fail for any reason** - Auth must work with real tokens
5. **Configuration assumptions needed** - Don't guess JWT config
6. **GitHub issue missing or unassigned** - Verify #162 still assigned
7. **Can't provide verification evidence** - Must show auth working
8. **ADR conflicts with approach** - Follow ADR-012 exactly
9. **Resource not found after searching** - JWT files must exist
10. **User data at risk** - Though none expected here
11. **Completion bias detected** - Auth must actually work, not "should work"
12. **Rationalizing gaps as "minor"** - No auth shortcuts allowed
13. **GitHub tracking not working** - Issue updates must work
14. **Single agent seems sufficient** - This IS single agent task
15. **Git operations failing** - All commits must work
16. **Server state unexpected** - Verify API behavior
17. **UI behavior can't be visually confirmed** - Use curl with tokens

**Remember**: STOP means STOP. Don't try to work around it. Ask PM.

---

## Evidence Requirements (CRITICAL - EXPANDED)

### For EVERY Claim You Make:

- **"Fixed JWT bug"** → Show before/after token generation working
- **"Auth enabled"** → Show unauthorized requests rejected (401)
- **"Generated test tokens"** → Show actual tokens created
- **"Protected endpoints work"** → Show curl with valid token succeeds
- **"Invalid tokens rejected"** → Show curl with bad token fails (401)
- **"All modes protected"** → Show auth required for each mode

### Completion Bias Prevention (CRITICAL):

- **Never guess! Always verify first!**
- **NO "should work"** - only "here's proof it works"
- **NO "probably fixed"** - only "here's evidence it's fixed"
- **NO assumptions** - only verified facts with terminal output
- **NO rushing to claim done** - evidence first, claims second

### Git Workflow Discipline:

After ANY code changes:
```bash
git status
git add [files]
git commit -m "[descriptive message]"
git log --oneline -1  # MANDATORY - show this output
```

### Server State Awareness:

Before claiming auth works:
```bash
# Test unauthorized request (should fail)
curl -X POST http://localhost:8001/api/standup/generate \
  -H "Content-Type: application/json" \
  -d '{"mode": "standard", "format": "json"}' -v

# Test with invalid token (should fail)
curl -X POST http://localhost:8001/api/standup/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer invalid_token" \
  -d '{"mode": "standard", "format": "json"}' -v

# Test with valid token (should succeed)
curl -X POST http://localhost:8001/api/standup/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VALID_TOKEN" \
  -d '{"mode": "standard", "format": "json"}' | jq '.'
```

---

## Related Documentation

- **resource-map.md** - ALWAYS CHECK FIRST for service locations
- **stop-conditions.md** - When to stop and ask for help
- **anti-80-pattern.md** - Understanding completion bias prevention
- **ADR-012** - Protocol-Ready JWT Authentication (FOLLOW THIS)
- **Pattern-014** - Error Handling Pattern (for auth errors)
- **Task 1 work** - JWT auth already implemented

---

## REMINDER: Methodology Cascade

This prompt carries our methodology forward. You are responsible for:

1. **Verifying infrastructure FIRST** (no wrong assumptions)
2. **Ensuring 100% completeness** (no 80% pattern)
3. **Checking what exists NEXT** (no reinventing)
4. **Preserving user data ALWAYS** (though none at risk here)
5. **Checking resource-map.md FIRST** (for JWT service locations)
6. **Following ALL verification requirements**
7. **Providing evidence for EVERY claim**
8. **Creating auth flow enumeration** (unauthorized, invalid, valid)
9. **Stopping when assumptions are needed**
10. **Maintaining architectural integrity** (ADR-012)
11. **Updating GitHub with progress** (in descriptions!)
12. **Creating session logs in .md format**
13. **Verifying git commits with log output**
14. **Checking server state before/after changes**
15. **Providing visual proof for auth claims** (curl outputs)
16. **Never guessing - always verifying first!**
17. **Never rationalizing incompleteness!**

**Security failures are critical. Evidence is mandatory.**

---

## Task Requirements

### 1. Locate and Understand JWT Bug

**Investigation Required**:
```bash
# Find JWT service
ls -la services/auth/jwt_service.py

# Read the error you encountered
# (You mentioned AttributeError in dataclass fields iteration)

# Understand what's broken
cat services/auth/jwt_service.py | grep -A 10 "def.*token"
```

**Document**:
- What is the exact error?
- Where in the code does it occur?
- What is the root cause?
- What's the fix?

**If unclear**: STOP (condition #9 - resource not found after searching)

---

### 2. Fix JWT Service Bug

**Expected Issue**: AttributeError in dataclass fields iteration

**Common Causes**:
```python
# BAD - Python 3.11+ changed this
from dataclasses import fields
for field in fields(some_class):  # Fails if not instance
    ...

# GOOD - Use correct approach
from dataclasses import fields
for field in fields(SomeClass):  # Pass class, not instance
    ...

# OR
import dataclasses
if dataclasses.is_dataclass(obj):
    for field in dataclasses.fields(obj):
        ...
```

**Fix the Bug**:
1. Identify exact line causing error
2. Understand why it's failing
3. Implement correct fix
4. Test token generation works

**Evidence Required**:
```bash
# Show it was broken
$ python -c "from services.auth.jwt_service import JWTService; JWTService().create_token({'sub': 'test'})"
# (Should show error before fix)

# Show your fix
$ git diff services/auth/jwt_service.py

# Show it's fixed
$ python -c "from services.auth.jwt_service import JWTService; print(JWTService().create_token({'sub': 'test'}))"
# (Should show token after fix)
```

---

### 3. Create Token Generation Utility

**For testing purposes**, create a simple script:

```python
# scripts/generate_test_token.py
"""Generate test JWT tokens for API testing"""

from services.auth.jwt_service import JWTService
import sys

def generate_token(user_id: str = "test_user", **claims):
    """Generate a test JWT token"""
    jwt_service = JWTService()

    token_claims = {
        "sub": user_id,  # Subject (user ID)
        **claims
    }

    token = jwt_service.create_token(token_claims)
    return token

if __name__ == "__main__":
    user_id = sys.argv[1] if len(sys.argv) > 1 else "test_user"
    token = generate_token(user_id)
    print(token)
```

**Usage**:
```bash
# Generate test token
$ python scripts/generate_test_token.py
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Generate token for specific user
$ python scripts/generate_test_token.py "user123"
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Evidence Required**: Show token generation working

---

### 4. Enable Authentication in Production

**Update web/api/routes/standup.py**:

```python
# Change REQUIRE_AUTH default to true
REQUIRE_AUTH = os.getenv("REQUIRE_AUTH", "true").lower() == "true"

# Note: Now defaults to true (auth required)
# Can still disable for testing: export REQUIRE_AUTH=false
```

**Also update the dependency**:

```python
async def get_current_user_optional():
    """
    Optional auth for development (now defaults to REQUIRED).

    When REQUIRE_AUTH=true (DEFAULT/PRODUCTION):
    - Full JWT validation required
    - Returns user info or raises 401

    When REQUIRE_AUTH=false (testing only):
    - Auth bypassed
    - Returns None
    """
    if not REQUIRE_AUTH:
        return None  # Auth disabled for testing only

    # JWT validation (your existing code from Task 1)
    # Make sure this works with real tokens!
    ...
```

**Evidence Required**: Show REQUIRE_AUTH=true is now default

---

### 5. Verify Unauthorized Access Rejected

**Test without token**:
```bash
# Should get 401 Unauthorized
$ curl -X POST http://localhost:8001/api/standup/generate \
  -H "Content-Type: application/json" \
  -d '{"mode": "standard", "format": "json"}' -v

# Expected response:
HTTP/1.1 401 Unauthorized
{
  "detail": "Authentication required"
}
```

**Evidence Required**: Show 401 response for unauthorized requests

---

### 6. Verify Invalid Token Rejected

**Test with fake token**:
```bash
# Should get 401 Unauthorized
$ curl -X POST http://localhost:8001/api/standup/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer invalid_token_12345" \
  -d '{"mode": "standard", "format": "json"}' -v

# Expected response:
HTTP/1.1 401 Unauthorized
{
  "detail": "Invalid token"
  # Or similar message
}
```

**Evidence Required**: Show 401 response for invalid tokens

---

### 7. Verify Valid Token Accepted

**Generate and test with real token**:
```bash
# Generate valid token
$ export TEST_TOKEN=$(python scripts/generate_test_token.py)
$ echo $TEST_TOKEN

# Test with valid token - should succeed
$ curl -X POST http://localhost:8001/api/standup/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TEST_TOKEN" \
  -d '{"mode": "standard", "format": "json"}' | jq '.'

# Expected: 200 OK with standup content
{
  "success": true,
  "standup": {
    "content": { ... },
    ...
  }
}
```

**Evidence Required**: Show 200 response with valid token

---

### 8. Test All Endpoints Protected

**Verify each endpoint requires auth**:

```bash
# /generate (should require auth)
$ curl -X POST http://localhost:8001/api/standup/generate \
  -H "Content-Type: application/json" \
  -d '{"mode": "standard"}' -v
# Expected: 401

# /modes (public - no auth needed)
$ curl http://localhost:8001/api/standup/modes
# Expected: 200 OK
# (This one can be public)

# /formats (public - no auth needed)
$ curl http://localhost:8001/api/standup/formats
# Expected: 200 OK
# (This one can be public)

# /health (public - no auth needed)
$ curl http://localhost:8001/api/standup/health
# Expected: 200 OK
# (Always public for monitoring)
```

**Auth Requirements**:
- `/generate` - MUST require auth (protected resource)
- `/modes` - Can be public (just lists available modes)
- `/formats` - Can be public (just lists available formats)
- `/health` - Should be public (monitoring needs this)

**Evidence Required**: Show auth applied appropriately

---

## Verification Steps

### Step 1: Fix JWT Bug

```bash
# Test token generation
$ python scripts/generate_test_token.py
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Verify token structure
$ echo "eyJ..." | cut -d. -f2 | base64 -d 2>/dev/null | jq '.'
{
  "sub": "test_user",
  "exp": 1234567890,
  ...
}
```

**Expected**: Token generated successfully

**If fails**: STOP (condition #4 - tests fail)

---

### Step 2: Enable Auth

```bash
# Restart API with auth enabled (default now)
$ uvicorn main:app --reload --port 8001

# Verify REQUIRE_AUTH is true
$ grep "REQUIRE_AUTH" web/api/routes/standup.py
REQUIRE_AUTH = os.getenv("REQUIRE_AUTH", "true").lower() == "true"
```

**Expected**: Auth enabled by default

---

### Step 3: Test Auth Flows

**Flow 1: No token (unauthorized)**
```bash
$ curl -X POST http://localhost:8001/api/standup/generate \
  -H "Content-Type: application/json" \
  -d '{"mode": "standard"}' -v 2>&1 | grep "401"
```

**Expected**: 401 Unauthorized

**Flow 2: Invalid token**
```bash
$ curl -X POST http://localhost:8001/api/standup/generate \
  -H "Authorization: Bearer fake_token" \
  -H "Content-Type: application/json" \
  -d '{"mode": "standard"}' -v 2>&1 | grep "401"
```

**Expected**: 401 Unauthorized

**Flow 3: Valid token**
```bash
$ export TOKEN=$(python scripts/generate_test_token.py)
$ curl -X POST http://localhost:8001/api/standup/generate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"mode": "standard"}' | jq '.success'
```

**Expected**: true (success)

---

### Step 4: Test All Modes with Auth

```bash
# Generate token once
$ export TOKEN=$(python scripts/generate_test_token.py)

# Test each mode
for mode in standard issues documents calendar trifecta; do
  echo "Testing $mode mode..."
  curl -X POST http://localhost:8001/api/standup/generate \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"mode\": \"$mode\"}" \
    2>&1 | grep -q '"success": true' && echo "✅ $mode" || echo "❌ $mode"
done
```

**Expected**: All modes ✅

**Evidence Required**: Show all modes work with valid auth

---

## Success Criteria

Task 3 is complete when:

- [ ] JWT service bug identified and documented
- [ ] JWT service bug fixed with evidence
- [ ] Token generation script created and working
- [ ] REQUIRE_AUTH defaults to true (production ready)
- [ ] Unauthorized requests return 401 (evidence shown)
- [ ] Invalid tokens return 401 (evidence shown)
- [ ] Valid tokens work correctly (evidence shown)
- [ ] All 5 modes tested with valid auth (evidence shown)
- [ ] Public endpoints still public (/health, /modes, /formats)
- [ ] Protected endpoints require auth (/generate)
- [ ] Code committed with git log output shown
- [ ] Session log updated in .md format
- [ ] Auth flow enumeration complete (unauthorized/invalid/valid = 3/3)
- [ ] No security gaps or shortcuts
- [ ] ADR-012 followed correctly

---

## Self-Check Before Claiming Complete

### Ask Yourself:

1. **Does JWT bug fix actually work?** (Token generation succeeds)
2. **Is auth truly enabled by default?** (Not just "should be")
3. **Did I test unauthorized access?** (401 response shown)
4. **Did I test invalid tokens?** (401 response shown)
5. **Did I test valid tokens?** (200 + success shown)
6. **Are all modes protected?** (Tested each with auth)
7. **Is there a gap between claims and reality?** (Evidence matches)
8. **Did I verify git commits?** (Shown `git log --oneline -1`)
9. **Is auth actually secure?** (Not just bypassed for convenience)
10. **Am I rationalizing any gaps?** (No "good enough" shortcuts)
11. **Do I have objective proof?** (Curl outputs for all flows)
12. **Did I follow ADR-012?** (JWT implementation correct)
13. **Am I guessing or do I have evidence?** (Evidence for everything)

### If Uncertain About Anything:

- Test the auth flows yourself
- Show actual curl outputs
- Generate real tokens
- Verify security actually works
- Ask for help if stuck
- **Never guess about security!**

---

## Files to Modify

### Primary Files

- `services/auth/jwt_service.py` - Fix JWT bug
- `web/api/routes/standup.py` - Enable auth by default

### New Files

- `scripts/generate_test_token.py` - Token generation utility

### Session Log

- `dev/2025/10/19/HHMM-prog-code-log.md` - Your session log

---

## Deliverables

### 1. JWT Bug Fix

**Modified**: services/auth/jwt_service.py

**Evidence**:
```bash
# Before (broken)
$ python -c "..." # Show error

# After (fixed)
$ python scripts/generate_test_token.py
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

$ git diff services/auth/jwt_service.py
$ git log --oneline -1
```

### 2. Auth Flow Enumeration

**Table**:

| Flow | Test Command | Expected | Actual | Status |
|------|-------------|----------|---------|--------|
| No token | curl (no auth header) | 401 | 401 | ✅ |
| Invalid token | curl (bad token) | 401 | 401 | ✅ |
| Valid token | curl (real token) | 200 | 200 | ✅ |

**Target**: 3/3 = 100% ✅

### 3. Protected Endpoints Verification

**Table**:

| Endpoint | Auth Required | Tested | Status |
|----------|---------------|--------|--------|
| /generate | YES | ✅ | 401 without auth, 200 with |
| /modes | NO | ✅ | 200 always |
| /formats | NO | ✅ | 200 always |
| /health | NO | ✅ | 200 always |

**Target**: 4/4 = 100% ✅

### 4. Evidence Report

**Terminal outputs showing**:
- JWT bug before/after
- Token generation working
- 401 responses for unauthorized/invalid
- 200 responses for valid auth
- All 5 modes work with auth
- Git commit confirmed

### 5. Session Log

**In dev/2025/10/19/HHMM-prog-code-log.md**:
- JWT bug details (what, where, why)
- Fix explanation
- Auth flow testing results
- Security verification
- Time spent

---

## Security Notes

### Critical Security Requirements:

1. **Never expose secrets** in logs or errors
2. **Always validate tokens** - no shortcuts
3. **Use proper HTTP status codes** - 401 for auth failures
4. **Follow ADR-012** - established JWT patterns
5. **Test negative cases** - unauthorized, invalid, expired
6. **Document security decisions** clearly

### Common Security Anti-Patterns to AVOID:

- ❌ "Auth works for valid tokens, assuming it blocks invalid"
- ❌ "Testing with auth disabled is good enough"
- ❌ "Probably blocks unauthorized requests"
- ❌ Exposing token details in error messages
- ❌ Assuming security without testing

### Do This Instead:

- ✅ Test ALL auth flows (unauthorized, invalid, valid)
- ✅ Show evidence for each security claim
- ✅ Verify tokens are actually validated
- ✅ User-friendly errors without security details
- ✅ Security through testing, not assumptions

---

## Remember

- **Security is not negotiable** - Test thoroughly
- **Evidence = confidence** - Show all auth flows work
- **STOP conditions protect you** - Use for any uncertainty
- **100% means 100%** - All 3 auth flows must work
- **ADR-012 is your guide** - Follow the established pattern

**Auth is critical infrastructure. Get it right!** 🔒

---

*Template Version: 8.0*
*Based on: agent-prompt-template.md*
*All methodology sections included*
*Task-specific sections customized for security*
*Ready for deployment*
