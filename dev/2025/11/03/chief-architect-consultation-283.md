# Chief Architect Consultation: Issue #283 - Error Message UX

**Date**: November 3, 2025
**From**: PM (Christian Crumlish)
**Issue**: #283 - User-Friendly Error Messages
**Current State**: 4/6 = 67% proven achievable
**Decision Required**: Accept limitation or pursue complex solutions

---

## The Question

**Should we accept 4/6 = 67% completion for Issue #283, given the empirical evidence of FastAPI architectural constraints?**

More specifically:

1. **User Experience**: What do users actually see when they hit the 2/6 failing scenarios?
2. **Frequency**: How often will users encounter 401 auth errors vs the 4 working error types?
3. **Impact**: Does the technical message for auth errors meaningfully harm UX?
4. **Trade-offs**: Are the complex solutions (ASGI middleware, dependency refactor) worth the effort?
5. **Completion Definition**: Does 4/6 within architectural constraints satisfy "complete means complete"?

---

## Context Summary

### What Works (4/6 = 67%)

**These show friendly messages**:
- Empty input: "I didn't quite catch that. Could you try again?"
- Unknown action: "I'm still learning how to help with that"
- Timeout: "That's complex - let me reconsider my approach"
- Unknown intent: "I'm not sure I understood. Could you rephrase?"

**Mechanism**: EnhancedErrorMiddleware catches exceptions in route handlers

### What Doesn't Work (2/6 = 33%)

**These show technical messages**:
- Invalid auth token: `{"detail": "Invalid token"}` ❌
- No auth token: `{"detail": "Authentication required"}` ❌

**Mechanism**: FastAPI's dependency resolution phase returns error before our handlers can intercept

### User Experience Impact

**Working scenarios (4/6)**:
```
User: [sends empty message]
Response: "I didn't quite catch that. Could you try again?" ✅
```

**Failing scenarios (2/6)**:
```
User: [session expires mid-conversation]
Response: {"detail": "Invalid token"} ❌

Expected: "Let's try logging in again. Your session may have expired." ✅
```

**Question for you**: How often do users encounter auth errors vs other error types? If auth errors are rare, 4/6 may be "good enough."

---

## The Empirical Evidence

Cursor provided actual test outputs (not theory):

**Test 1 - Invalid Token**:
```bash
$ curl http://localhost:8001/auth/me -H "Authorization: Bearer INVALID_TOKEN"
{"detail": "Invalid token"}
```

**Test 2 - No Token**:
```bash
$ curl http://localhost:8001/auth/me
{"detail": "Authentication required"}
```

**Expected if handler worked**:
```json
{"message": "Let's try logging in again. Your session may have expired."}
```

**Evidence**: Response structure proves exception handler not invoked
- Our handler returns `{"message": "..."}`
- Actual response has `{"detail": "..."}`
- FastAPI extracting and returning `APIError.details` directly

**Full Analysis**: `dev/active/issue-283-empirical-proof.md`

---

## The Architectural Constraint

**FastAPI Request Processing Order**:

```
[Phase 1] Dependency Resolution
    ↓ get_current_user() raises APIError HERE
    ↓ FastAPI's dependency error handler catches it
    ↓ Extracts APIError.details dict
    ↓ Returns it directly as JSON
    ✗ NEVER reaches @app.exception_handler(APIError)
    ✗ NEVER reaches route handler
    ✗ NEVER reaches middleware

[Phase 2] Route Handler Execution
    ↓ Our exception handlers work HERE
    ↓ Our middleware works HERE
    ✓ This is where the 4/6 errors are caught
```

**Key Insight**: Exception handlers and middleware only see exceptions from Phase 2 (route handlers). Dependencies execute in Phase 1, before our handlers are in scope.

**Attempts Made**:
1. ✅ HTTPException handler - doesn't work (FastAPI's type)
2. ✅ APIError handler - doesn't work (dependency phase)
3. ✅ Auth refactored to raise APIError - correct but still bypassed
4. ✅ Empirical testing - proves limitation is real

---

## Options for Achieving 6/6 = 100%

### Option A: Move Auth Out of Dependencies (Invasive)

**Approach**: Refactor authentication from `Depends(get_current_user)` into route handler bodies

**Pros**:
- ✅ Would allow middleware/handlers to catch auth errors
- ✅ Achieves 6/6 = 100%

**Cons**:
- ❌ Violates FastAPI patterns (Depends() is idiomatic)
- ❌ Requires modifying 20+ protected routes
- ❌ Increases code duplication
- ❌ Makes auth logic less centralized
- ❌ Higher risk of breaking existing functionality

**Estimate**: 4-6 hours, moderate risk

### Option B: ASGI-Level Middleware (Complex)

**Approach**: Implement custom Starlette middleware at ASGI level (below FastAPI abstraction)

**Pros**:
- ✅ Could intercept responses before FastAPI processing
- ✅ Maintains FastAPI patterns (no route changes)

**Cons**:
- ❌ Very complex (low-level ASGI protocol)
- ❌ Performance concerns (intercepts ALL requests)
- ❌ May conflict with other middleware
- ❌ Difficult to test and maintain
- ❌ Uncertain if it would even work
- ❌ Outside team's ASGI expertise

**Estimate**: 8-12 hours, high risk, uncertain outcome

### Option C: Accept 4/6 = 67% (Pragmatic)

**Approach**: Document architectural limitation, accept what's achievable

**Pros**:
- ✅ Honest about constraints
- ✅ 4/6 error types provide good UX
- ✅ Focus effort on higher-value features
- ✅ Maintains clean FastAPI patterns
- ✅ Zero additional risk

**Cons**:
- ❌ Auth errors still show technical messages
- ❌ Feels incomplete (4/6 vs 6/6)
- ❌ May confuse users during auth failures

**Estimate**: 0 hours, zero risk

---

## My Questions for You

### 1. User Experience Priority

**How bad is it that auth errors show technical messages?**

Scenarios users encounter:
- Token expires during long session → sees `{"detail": "Invalid token"}`
- User pastes chat link without being logged in → sees `{"detail": "Authentication required"}`

vs. the working scenarios:
- User sends empty message → sees "I didn't quite catch that"
- User asks unintelligible question → sees "I'm still learning how to help with that"

**Question**: Does the auth error UX meaningfully harm the product, or is it acceptable given the architectural constraints?

### 2. Frequency Analysis

**How often do users hit auth errors vs other error types?**

If auth errors are 5% of all errors → maybe accept 4/6
If auth errors are 40% of all errors → maybe worth Option A or B

**Question**: Can we estimate the relative frequency of these 6 error types in production?

### 3. Completion Philosophy

**Does "complete within architectural constraints" satisfy our standards?**

We've established: "Complete means 100%, not 80%"

But this is: "100% of what's architecturally achievable (4/4), not 100% of the original scope (4/6)"

**Question**: Is this distinction meaningful, or should we only close issues at 6/6 regardless of constraints?

### 4. Risk vs Reward

**Are Options A or B worth the effort and risk?**

- Option A: 4-6 hours, invasive refactor, breaks patterns
- Option B: 8-12 hours, complex ASGI code, uncertain outcome
- Option C: 0 hours, accept limitation, clear documentation

**Question**: Given other priorities, is achieving 6/6 worth the investment?

### 5. Documentation Strategy

**If we accept 4/6, how do we document this?**

Options:
- Close issue with "4/6 complete - auth errors architectural limitation"
- Keep issue open with "2/6 blocked by FastAPI architecture" label
- Create new issue "Investigate ASGI middleware for auth error UX"

**Question**: What's the right way to represent architectural ceilings in our issue tracking?

---

## My Inclination

I'm **pragmatically inclined toward Option C** (accept 4/6) based on:

1. **Gödel-incomplete universe**: Not unwilling to accept limitations
2. **Good enough**: 4/6 coverage is meaningful improvement
3. **Risk**: Options A/B introduce complexity for marginal gain
4. **Patterns**: Maintaining clean FastAPI patterns has value
5. **Priorities**: Other features may deliver more user value

**But I need your architectural perspective on**:
- Whether 4/6 is truly the ceiling (any creative solutions?)
- User impact severity (how bad are technical auth errors?)
- Precedent this sets (are we lowering our completion bar?)
- Long-term maintainability (will we regret not doing A or B?)

---

## Recommendation Request

**Please advise on**:

1. **Decision**: Accept 4/6, pursue Option A, pursue Option B, or other approach?
2. **Rationale**: Why this is the architecturally sound choice
3. **User Impact**: Assessment of auth error UX harm
4. **Documentation**: How to represent this in Issue #283
5. **Precedent**: How this affects future "architectural limitation" scenarios

**Evidence Available**:
- `dev/active/issue-283-empirical-proof.md` - Full technical analysis
- Cursor's session logs - Complete implementation attempts
- Test outputs - Empirical proof of limitation

**Timeline**: No urgency - quality decision more important than speed

---

## Bottom Line

**I'm not unwilling to accept 4/6 if that's the right call**, but I want to ensure:
1. We understand what users will actually experience
2. We're not giving up prematurely (is there a creative Option D?)
3. We set the right precedent for future architectural constraints
4. We document this in a way that's clear for future maintainers

**Your architectural judgment requested.**
