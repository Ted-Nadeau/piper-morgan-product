# Cursor: Directive for Issue #283 - Option 2 (APIError Exception Handler)

## Your Discovery: Correct and Important

You've identified the real architectural constraint: FastAPI's dependency injection executes BEFORE middleware can intercept exceptions. This is accurate.

**Your refactoring work was NOT wasted**:
- ✅ Using APIError is structurally correct
- ✅ Infrastructure exists (UserFriendlyErrorService)
- ✅ You identified the real blocker

**Now we need the right solution for the architecture we have.**

---

## Directive: Option 2 - Add APIError Exception Handler

**Why Option 2 (not Option 1)**:
- Option 1 (move auth out of Depends): Too invasive, breaks FastAPI patterns
- Option 2 (exception handler): Simple, clean, uses existing infrastructure
- We CONTROL APIError (unlike HTTPException), so handler will work

**This is DIFFERENT from the HTTPException handler that failed**:
- HTTPException: FastAPI's built-in type (their handling takes precedence)
- APIError: OUR exception class (we control the handling)
- This distinction is critical

---

## Implementation: Add APIError Exception Handler

### Step 1: Verify APIError Structure (5 min)

First, confirm APIError has the fields we need:

```bash
# Check the APIError class definition
grep -A 20 "class APIError" services/exceptions.py
```

**Expected fields**:
- `message`: Error message identifier (e.g., "authentication_required")
- `status_code`: HTTP status code (e.g., 401)
- `context`: Optional additional context

If APIError doesn't have these fields, we may need to adjust, but likely it does.

### Step 2: Add Exception Handler to web/app.py (15 min)

**Add this AFTER app creation, BEFORE mounting routers**:

```python
# web/app.py
from fastapi import Request
from fastapi.responses import JSONResponse
from services.exceptions import APIError
from services.ui_messages.user_friendly_errors import UserFriendlyErrorService
import structlog

logger = structlog.get_logger()

@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
    """
    Handle APIError exceptions with user-friendly messages.

    This catches APIError raised anywhere in the application,
    including from FastAPI dependencies like get_current_user.

    Since dependencies execute before middleware, this exception
    handler is the appropriate layer to convert APIError to
    friendly messages for users.
    """
    error_service = UserFriendlyErrorService()

    # Get friendly message based on error type
    if hasattr(exc, 'message'):
        # If APIError has a message identifier, use it
        friendly_message = error_service.get_friendly_message(
            exc.message,
            exc.status_code if hasattr(exc, 'status_code') else 500
        )
    else:
        # Fallback: use status code to determine message
        if exc.status_code == 401:
            friendly_message = error_service.authentication_required()
        elif exc.status_code == 403:
            friendly_message = error_service.permission_denied()
        elif exc.status_code == 404:
            friendly_message = error_service.resource_not_found()
        else:
            friendly_message = error_service.system_error()

    # CRITICAL: Log technical details for debugging
    logger.error(
        "api_error",
        error_type=exc.__class__.__name__,
        message=getattr(exc, 'message', str(exc)),
        status_code=getattr(exc, 'status_code', 500),
        path=request.url.path,
        context=getattr(exc, 'context', {})
    )

    # Return friendly message to user
    return JSONResponse(
        status_code=getattr(exc, 'status_code', 500),
        content={"message": friendly_message}
    )
```

**Key Points**:
1. This catches APIError at FastAPI level (includes dependencies)
2. Integrates with existing UserFriendlyErrorService
3. Logs technical details (preserves debugging info)
4. Returns friendly message to user

### Step 3: Verify auth_middleware Still Raises APIError (5 min)

```bash
# Check that auth_middleware.py raises APIError
grep -A 5 "raise APIError" web/middleware/auth_middleware.py
```

**Expected**: Should see APIError being raised for auth failures

If not raising APIError, that needs to be fixed first (but you said you already did this).

### Step 4: Test ALL 6 Error Types (30 min)

**Now test with the exception handler in place**:

```bash
# Start server fresh
python main.py

# Get auth token
TOKEN=$(curl -s -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"xian","password":"test123456"}' \
  | jq -r '.token')

echo "Token: $TOKEN"
```

#### Test 1-4: Should Still Work (Middleware Layer)

```bash
# Test 1: Empty Input
curl -X POST http://localhost:8001/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": ""}' | jq .
# Save to: test-option2-1-empty.txt
# Expected: Still works (middleware catches)

# Test 2: Unknown Input
curl -X POST http://localhost:8001/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "xyzabc123qwerty"}' | jq .
# Save to: test-option2-2-unknown.txt
# Expected: Still works (middleware catches)

# Test 3: Timeout (if testable)
# Expected: Still works (middleware catches)

# Test 4: Unknown Intent
# Expected: Still works (middleware catches)
```

#### Test 5-6: SHOULD NOW WORK (Exception Handler Layer)

```bash
# Test 5: Invalid Auth - SHOULD NOW SHOW FRIENDLY MESSAGE ✅
curl -X POST http://localhost:8001/chat \
  -H "Authorization: Bearer INVALID_TOKEN_12345" \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}' | jq .
# Save to: test-option2-5-invalid-auth.txt
# Expected: {"message": "Let's try logging in again. Your session may have expired."}
# NOT: "Invalid token" or "Authentication required"

# Test 6: No Auth - SHOULD NOW SHOW FRIENDLY MESSAGE ✅
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}' | jq .
# Save to: test-option2-6-no-auth.txt
# Expected: {"message": "Let's try logging in again. Your session may have expired."}
# NOT: "Authentication required"
```

**Critical**: Tests 5 and 6 MUST show friendly messages now. If they don't, the exception handler isn't catching APIError properly.

### Step 5: Check 404 Handling (10 min)

**404 may need special handling**:

```bash
# Test 7: 404 Not Found
curl -X GET http://localhost:8001/nonexistent/route \
  -H "Authorization: Bearer $TOKEN" | jq .
# Save to: test-option2-7-not-found.txt
```

**If still showing "Not Found"**:
- 404 may come from FastAPI route matching (before any handler)
- May need separate @app.exception_handler(404) or custom 404 handler
- Document this as a separate case if needed

**If showing friendly message**: Great! Count as 6/6.

### Step 6: Create COMPLETE Matrix (15 min)

```markdown
## Issue #283 Error Handling - COMPLETE STATE (Option 2)

| Error Type | Layer | Handler Type | User Sees Friendly | Test Status | Evidence |
|------------|-------|--------------|-------------------|-------------|----------|
| Empty Input | Middleware | EnhancedErrorMiddleware | ✅ YES | ✅ PASSING | test-option2-1-empty.txt |
| Unknown Action | Middleware | EnhancedErrorMiddleware | ✅ YES | ✅ PASSING | test-option2-2-unknown.txt |
| Timeout | Middleware | EnhancedErrorMiddleware | ✅ YES | ✅ PASSING | test-option2-3-timeout.txt |
| Unknown Intent | Middleware | EnhancedErrorMiddleware | ✅ YES | ✅ PASSING | test-option2-2-unknown.txt |
| 401 Auth | Dependency | APIError Exception Handler | ✅ YES | ✅ PASSING | test-option2-5-invalid-auth.txt |
| 404 Not Found | Route | [TBD based on test] | ❓ TESTING | ❓ | test-option2-7-not-found.txt |

**CURRENT: 5/6 or 6/6 depending on 404 test**

**Architecture**:
- Middleware layer: Catches exceptions in route handlers
- Exception handler layer: Catches exceptions in dependencies
- Two-tier approach necessary due to FastAPI architecture
```

### Step 7: Commit & Update (15 min)

```bash
git add web/app.py
git commit -m "fix: Add APIError exception handler for friendly messages (#283)"
git push

# Update GitHub
gh issue comment 283 --body "
## Option 2 Implementation Complete

### Architectural Discovery
- Dependencies execute BEFORE middleware (FastAPI design)
- Cannot catch dependency exceptions in middleware
- Solution: Exception handler at FastAPI level

### Implementation
- Added @app.exception_handler(APIError)
- Integrates with UserFriendlyErrorService
- Two-tier error handling:
  - Middleware: Route handler exceptions
  - Exception handler: Dependency exceptions

### Test Results
[Paste all curl outputs showing friendly messages]

### Completion Matrix
[Paste matrix showing 5/6 or 6/6]

**Status**: 5/6 confirmed, investigating 404 handling
"
```

---

## Timeline: 1-1.5 Hours

- Step 1: Verify APIError (5 min)
- Step 2: Add exception handler (15 min)
- Step 3: Verify auth raises APIError (5 min)
- Step 4: Test 6 error types (30 min)
- Step 5: Check 404 (10 min)
- Step 6: Create matrix (15 min)
- Step 7: Commit & update (15 min)
- Buffer: 15 min

**Total: ~1.5 hours**

---

## Acceptance Criteria

- [ ] APIError exception handler added to web/app.py
- [ ] Handler integrates with UserFriendlyErrorService
- [ ] auth_middleware confirmed raising APIError
- [ ] Test 1-4: Friendly messages (middleware layer) - still working
- [ ] Test 5: Invalid auth shows friendly (exception handler) - NOW WORKING
- [ ] Test 6: No auth shows friendly (exception handler) - NOW WORKING
- [ ] Test 7: 404 tested and documented (may need separate handling)
- [ ] Complete matrix created (5/6 or 6/6)
- [ ] Commit pushed with evidence
- [ ] GitHub issue updated
- [ ] Technical logging verified (logs show details, users see friendly)

**DO NOT CLAIM COMPLETE WITHOUT ALL 11 CHECKBOXES**

---

## Why This Will Work

**The Previous HTTPException handler failed because**:
- HTTPException is FastAPI's type
- FastAPI handles it with built-in logic
- Our handler never got invoked

**This APIError handler will work because**:
- APIError is OUR type (services/exceptions.py)
- We control the handling completely
- FastAPI will route it to our handler
- No built-in handling to conflict with

**This is the architecturally correct solution**:
- Middleware: For route-level exceptions
- Exception handler: For dependency-level exceptions
- Two-tier approach matches FastAPI's two-tier execution

---

## STOP Conditions

**If exception handler still doesn't catch APIError**:
1. Check APIError import in app.py (correct path?)
2. Check exception handler registration (before routers?)
3. Check APIError is actually being raised (log output?)
4. Report findings - may need deeper architectural investigation

**If 404 still shows technical message**:
- Document as separate issue
- May need custom 404 handler
- Could still be 5/6 complete with 404 as known limitation

---

## Start Now

Begin with Step 1: Verify APIError has message/status_code fields

Report back when exception handler is added and ready to test.

**Target: 5/6 minimum, 6/6 if 404 works**
