# Cursor Agent: Issue #283 Phase 2 - STRICT Validation (REVISED v2)

## Critical Context

**Your Phase 1 claim**: "All 5 error types covered ✅"

**Your Phase 2 discovery**: HTTPException (401, 404, 403) bypasses middleware - only ~85% working

**This is the 80% completion pattern we're fighting against.**

---

## Mission: Complete Issue #283 to 100%

**Option A (85% solution) is UNACCEPTABLE** - represents core failure of our purpose.

**You will do Option B**: Add HTTPException handler + REAL validation with #290-style matrices

**There is no other work to do until this is complete** - no bounty in skipping steps.

---

## Completion Matrix Standard (From Issue #290)

Your matrices must follow the proven #290 pattern that caught the 80% pattern on Nov 1:

**Multi-Column Breakdown** (not vague "Implemented" column):
- Separate columns for each component
- Explicit PASSING/FAILING status (not just ✅)
- Evidence column with actual file names or line numbers
- TOTAL line showing N/M = X%

**Before/After Evolution** (show the gap closing):
- Current incomplete state first
- Target complete state as goal
- Makes progress toward 100% visible

---

## Step 1: Current State Matrix (BEFORE - 15 minutes)

**Create this EXACT matrix documenting current state**:

```markdown
## Issue #283 Error Handling - CURRENT STATE (BEFORE)

| Error Type | Middleware Mounted | Python Exception Caught | HTTPException Caught | User Sees Friendly | Test Status | Evidence |
|------------|-------------------|------------------------|---------------------|-------------------|-------------|----------|
| Empty Input | ✅ YES | ✅ YES | N/A | ✅ YES | ✅ PASSING | Middleware handles |
| Unknown Action | ✅ YES | ✅ YES | N/A | ✅ YES | ✅ PASSING | Middleware handles |
| Timeout | ✅ YES | ✅ YES | N/A | ✅ YES | ✅ PASSING | Middleware handles |
| Unknown Intent | ✅ YES | ✅ YES | N/A | ✅ YES | ✅ PASSING | Middleware handles |
| 401 Auth | ✅ YES | N/A | ❌ BYPASS | ❌ NO | ❌ FAILING | Shows "Authentication required" |
| 404 Not Found | ✅ YES | N/A | ❌ BYPASS | ❌ NO | ❌ FAILING | Shows "Not Found" |

**TOTAL: 4/6 = 67% INCOMPLETE**

**Root Cause**: FastAPI's HTTPException bypasses middleware exception handling
**Blocking**: Auth errors (401) and Not Found (404) show technical messages to users
```

**Commit this matrix** to session log before proceeding.

---

## Step 2: Add HTTPException Handler (30 minutes)

**The Problem You Identified**: FastAPI's HTTPException bypasses middleware

**The Solution**: Custom HTTPException handler in web/app.py

```python
# web/app.py - Add after app creation, BEFORE mounting routers

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from services.ui_messages.user_friendly_errors import UserFriendlyErrorService
import structlog

logger = structlog.get_logger()

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Convert FastAPI HTTPException to user-friendly messages.

    This handler intercepts FastAPI's built-in error responses
    and converts them using UserFriendlyErrorService.
    """
    error_service = UserFriendlyErrorService()

    # Map status codes to friendly messages
    friendly_message = None

    if exc.status_code == 401:
        # Authentication errors
        friendly_message = error_service.authentication_required()
    elif exc.status_code == 403:
        # Permission errors
        friendly_message = error_service.permission_denied()
    elif exc.status_code == 404:
        # Not found errors
        friendly_message = error_service.resource_not_found()
    elif exc.status_code == 422:
        # Validation errors
        friendly_message = error_service.validation_failed(str(exc.detail))
    elif exc.status_code >= 500:
        # Server errors
        friendly_message = error_service.system_error()
    else:
        # Fallback - check if we have a friendly version
        friendly_message = error_service.get_friendly_message(
            exc.status_code,
            str(exc.detail)
        )

    # CRITICAL: Log technical details server-side (preserve debugging info)
    logger.error(
        "http_exception",
        status_code=exc.status_code,
        detail=str(exc.detail),
        path=request.url.path
    )

    # Return friendly message to user
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": friendly_message or str(exc.detail)}
    )
```

**Commit this with**: "fix: Add HTTPException handler for friendly error messages (#283)"

**Evidence required**:
```bash
git add web/app.py
git commit -m "fix: Add HTTPException handler for friendly error messages (#283)"
git log --oneline -1
git show HEAD --stat
```

**Document in session log**:
- Commit hash
- Files changed
- Lines added/removed

---

## Step 3: MANDATORY Manual Validation - ALL 6 ERROR TYPES (1 hour)

**You will test EVERY error type and document ACTUAL terminal outputs.**

**"Tests pass" is NOT evidence. Curl outputs showing friendly messages are evidence.**

### Setup

```bash
# Start server fresh
python main.py

# In another terminal, get auth token
TOKEN=$(curl -s -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"xian","password":"test123456"}' \
  | jq -r '.token')

echo "Token: $TOKEN"  # Verify you got a token
```

### Test 1: Empty Input (MANDATORY)

```bash
curl -X POST http://localhost:8001/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": ""}' | jq .

# Save full output to session log
# Expected: Friendly message from UserFriendlyErrorService
# NOT: "validation error" or technical message
```

**Evidence**: Paste actual JSON response showing friendly message

### Test 2: Unknown/Gibberish Input (MANDATORY)

```bash
curl -X POST http://localhost:8001/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "xyzabc123qwerty"}' | jq .

# Save full output to session log
# Expected: "I'm not sure I understood" or "I'm still learning"
# NOT: "no handler" or technical error
```

**Evidence**: Paste actual JSON response showing friendly message

### Test 3: Timeout (if testable) (MANDATORY)

```bash
# If you can trigger a timeout scenario, test it
# Otherwise document why not testable in current setup
# Expected: "That's complex - let me reconsider" message
```

**Evidence**: Paste actual response OR explanation why not testable

### Test 4: Invalid Auth Token - 401 (MANDATORY - THIS IS THE FIX)

```bash
curl -X POST http://localhost:8001/chat \
  -H "Authorization: Bearer INVALID_TOKEN_12345" \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}' | jq .

# Save full output to session log
# BEFORE fix: "Invalid token" or "Authentication required" (technical)
# AFTER fix: Friendly message from error_service.authentication_required()
```

**Evidence**: Paste actual JSON response showing friendly message (NOT "Authentication required")

### Test 5: No Auth Token - 401 (MANDATORY - THIS IS THE FIX)

```bash
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}' | jq .

# Save full output to session log
# BEFORE fix: "Authentication required" (technical)
# AFTER fix: Friendly message from error_service.authentication_required()
```

**Evidence**: Paste actual JSON response showing friendly message (NOT "Authentication required")

### Test 6: 404 Not Found (MANDATORY - THIS IS THE FIX)

```bash
curl -X GET http://localhost:8001/nonexistent/route \
  -H "Authorization: Bearer $TOKEN" | jq .

# Save full output to session log
# BEFORE fix: "Not Found" (technical)
# AFTER fix: Friendly message from error_service.resource_not_found()
```

**Evidence**: Paste actual JSON response showing friendly message (NOT "Not Found")

---

## Step 4: Create COMPLETE State Matrix (AFTER - 15 minutes)

**After all tests pass, create this matrix showing 100% completion**:

```markdown
## Issue #283 Error Handling - COMPLETE STATE (AFTER)

| Error Type | Middleware Mounted | Python Exception Caught | HTTPException Caught | User Sees Friendly | Test Status | Evidence |
|------------|-------------------|------------------------|---------------------|-------------------|-------------|----------|
| Empty Input | ✅ YES | ✅ YES | N/A | ✅ YES | ✅ PASSING | test-1-empty-input.txt |
| Unknown Action | ✅ YES | ✅ YES | N/A | ✅ YES | ✅ PASSING | test-2-unknown-action.txt |
| Timeout | ✅ YES | ✅ YES | N/A | ✅ YES | ✅ PASSING | test-3-timeout.txt OR "Not testable in current setup" |
| Unknown Intent | ✅ YES | ✅ YES | N/A | ✅ YES | ✅ PASSING | test-2-unknown-action.txt (same test) |
| 401 Auth | ✅ YES | N/A | ✅ NOW CAUGHT | ✅ YES | ✅ PASSING | test-4-invalid-auth.txt |
| 404 Not Found | ✅ YES | N/A | ✅ NOW CAUGHT | ✅ YES | ✅ PASSING | test-6-not-found.txt |

**TOTAL: 6/6 = 100% ✅ COMPLETE**

**Fix Applied**: HTTPException handler catches 401 and 404 before FastAPI's default handler
**Result**: All error types now show user-friendly messages
```

**NO CLAIMING COMPLETE WITHOUT THIS 6/6 MATRIX**

---

## Step 5: Verify Technical Logging Still Works (15 minutes)

```bash
# While running tests above, check server logs
tail -f logs/piper-morgan.log  # or wherever logs go

# Or check console output if running in foreground
python main.py

# Verify logs show:
# - "http_exception" entries with status_code and detail
# - Technical exception details (for debugging)
# - While user receives friendly messages
```

**Evidence**: Log excerpt showing technical details preserved

**Example log entry you should see**:
```
[error] http_exception status_code=401 detail="Invalid token" path="/chat"
```

**While user sees**: `{"message": "Let's try logging in again. Your session may have expired."}`

---

## Step 6: Before/After Comparison Table (15 minutes)

**Create this table showing the improvement**:

```markdown
## Issue #283 Before/After Comparison

| Error Scenario | Before (Technical) | After (Friendly) | Status |
|----------------|-------------------|------------------|--------|
| Empty Input | 30s timeout then generic error | "I didn't quite catch that..." | ✅ |
| Unknown Action | "No handler for action: X" | "I'm still learning how to help with that" | ✅ |
| Invalid Auth (401) | "Invalid token" | "Let's try logging in again..." | ✅ |
| No Auth (401) | "Authentication required" | "Let's try logging in again..." | ✅ |
| Not Found (404) | "Not Found" | "I couldn't find that..." | ✅ |
| Timeout | "Operation timed out" | "That's complex - let me reconsider..." | ✅ |
```

---

## Step 7: Update GitHub Issue #283 (15 minutes)

**Edit the issue description** to mark ALL acceptance criteria:

```bash
gh issue view 283  # See current state

# Update with all checkboxes marked
gh issue edit 283 --body "
[paste full issue description with all ✓ checked]

## Completion Evidence

### Before/After Matrices
- Current state: 4/6 = 67% (middleware works, HTTPException bypassed)
- Complete state: 6/6 = 100% (HTTPException handler added)

### Commit
- Commit: [hash from git log]
- Files: web/app.py (+50 lines)
- HTTPException handler catches 401, 404 before FastAPI default

### Manual Test Results
- Test 1 (Empty): ✅ Friendly message
- Test 2 (Unknown): ✅ Friendly message
- Test 3 (Timeout): ✅ Friendly message OR not testable
- Test 4 (Invalid Auth): ✅ Friendly message (was 'Invalid token')
- Test 5 (No Auth): ✅ Friendly message (was 'Authentication required')
- Test 6 (404): ✅ Friendly message (was 'Not Found')

### Technical Logging
- ✅ Server logs preserve technical details
- ✅ Users see friendly messages only

**COMPLETE: 6/6 = 100%**
"
```

**Add evidence comment**:

```bash
gh issue comment 283 --body "
## Phase 2 Validation COMPLETE - 100%

### HTTPException Handler Added
- Commit: [paste commit hash]
- File: web/app.py (+50 lines)
- Catches HTTPException before FastAPI's default handler
- Maps all status codes to UserFriendlyErrorService

### Completion Matrix: 6/6 = 100%

**BEFORE** (4/6 = 67%):
- Empty Input: ✅ Working
- Unknown Action: ✅ Working
- Timeout: ✅ Working
- Unknown Intent: ✅ Working
- 401 Auth: ❌ Technical message
- 404 Not Found: ❌ Technical message

**AFTER** (6/6 = 100%):
- Empty Input: ✅ Working
- Unknown Action: ✅ Working
- Timeout: ✅ Working
- Unknown Intent: ✅ Working
- 401 Auth: ✅ Friendly message
- 404 Not Found: ✅ Friendly message

### All 6 Test Outputs Documented

[Paste curl outputs from all 6 tests]

### Technical Logging Verified

[Paste log excerpt showing technical details preserved]

**Issue #283 is now 100% complete and ready for PM final approval.**
"
```

---

## Acceptance Criteria - ALL 11 REQUIRED

- [ ] Current state matrix (BEFORE) created showing 4/6 = 67%
- [ ] HTTPException handler added to web/app.py
- [ ] Handler committed with evidence (git log + git show)
- [ ] Test 1 (empty): curl output documented, friendly message confirmed
- [ ] Test 2 (unknown): curl output documented, friendly message confirmed
- [ ] Test 3 (timeout): curl output OR explanation why not testable
- [ ] Test 4 (invalid auth): curl output showing friendly NOT "Invalid token"
- [ ] Test 5 (no auth): curl output showing friendly NOT "Authentication required"
- [ ] Test 6 (404): curl output showing friendly NOT "Not Found"
- [ ] Complete state matrix (AFTER) created showing 6/6 = 100%
- [ ] Before/After comparison table created
- [ ] Technical logging verified (log excerpt provided)
- [ ] GitHub issue #283 description updated with all criteria checked
- [ ] GitHub issue #283 has evidence comment with matrices and outputs
- [ ] Session log updated with full Phase 2 completion

**DO NOT CLAIM COMPLETE WITHOUT ALL 15 CHECKBOXES**

---

## Critical Reminders

**Complete means COMPLETE**:
- Not 67% (current state)
- Not 85% (middleware only)
- 6/6 = 100% with HTTPException handler
- Multi-column matrices showing component breakdown
- Before/After evolution documented

**Evidence means ACTUAL OUTPUTS**:
- Not "it should work"
- Not "tests pass so it works"
- Actual curl outputs showing friendly messages
- Actual log excerpts showing technical details preserved
- Before/After comparison visible

**No bounty in skipping steps**:
- There is no other work to do
- This must be done right
- Option A (85%) represents core failure
- Complete = 6/6 with matrices

**Matrix Standard**:
- Multi-column breakdown (not vague "Implemented")
- Explicit PASSING/FAILING status
- Evidence column with file names or line numbers
- TOTAL line showing N/M = X%
- Before/After evolution visible

---

## Session Log Format

Continue your existing log: `dev/2025/11/03/2025-11-03-0620-prog-cursor-log.md`

Add Phase 2 completion with:
- Current state matrix (BEFORE: 4/6 = 67%)
- HTTPException handler implementation
- All 6 curl test outputs
- Complete state matrix (AFTER: 6/6 = 100%)
- Before/After comparison table
- Technical logging verification
- GitHub updates

---

## You Said In Phase 1

> "Status: Issue #283 Phase 1 COMPLETE & SHIPPED"

**But it wasn't complete** - HTTPException wasn't handled (4/6 = 67%).

**Phase 2 is your chance to make it actually complete: 6/6 = 100%**

**Follow the #290 pattern that worked**:
1. Show current incomplete state (4/6 = 67%)
2. Add the fix (HTTPException handler)
3. Test ALL 6 error types manually
4. Document EVERY curl output
5. Show complete state (6/6 = 100%)
6. Create Before/After comparison

**Then and only then: "Issue #283 COMPLETE - 6/6 = 100%"**

---

**Start with Step 1: Create BEFORE matrix showing 4/6 = 67%. Report back with matrix in session log.**
