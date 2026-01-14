# Memo: Architectural Guidance on Identity Model Refactoring

**To**: Lead Developer
**From**: Chief Architect
**Date**: 2026-01-13
**Re**: Response to ADR-051 Consultation Request
**Issue**: #584

---

## Executive Summary

The diagnosis is correct and the proposed `RequestContext` pattern is sound. The codebase has accumulated identity debt through organic growth, and a unified model is the right remedy. My guidance below is mostly refinement, not redirection.

**Bottom line**: Proceed with ADR-051 with the refinements noted below.

---

## Response to Specific Questions

### Question 1: Single `RequestContext` vs Split Abstractions?

**Recommendation: Option A (Single `RequestContext`)**

**Reasoning**: The three concepts (user identity, conversation context, request metadata) have different *lifecycles* but the same *scope of need* - they're always needed together for request processing. Splitting them would add ceremony without benefit.

The frozen dataclass is correct - immutability prevents "helpful" modifications that would break the single-source-of-truth principle.

**Minor refinement**: Consider whether `username` belongs. It's denormalized data (can be looked up from `user_id`). My instinct: keep it - the lookup cost saved on every log statement adds up, and it's useful for debugging.

**Approved model structure**:
```python
@dataclass(frozen=True)
class RequestContext:
    # Core identity (required)
    user_id: UUID
    conversation_id: UUID
    request_id: UUID

    # Denormalized for convenience
    username: str
    timestamp: datetime

    # Future-proofing
    workspace_id: Optional[UUID] = None
```

---

### Question 2: Type Strategy

**Recommendation: Option A (`UUID` internally, `str` at boundaries)**

**Reasoning**: This codebase has suffered from ID confusion. Type safety is worth the conversion cost. The explicit boundary conversion also serves as documentation - "this is where external strings become typed internal IDs."

**Pattern**:
- **Routes**: Accept `str`, convert to `UUID` immediately via factory
- **Services**: Always `UUID`
- **Repositories**: Always `UUID`
- **Responses**: Convert back to `str` at serialization

The factory method handles the boundary correctly as proposed:
```python
@classmethod
def from_jwt_and_request(cls, claims: JWTClaims, conversation_id: str) -> "RequestContext":
    return cls(
        user_id=UUID(claims.sub),  # str → UUID at boundary
        conversation_id=UUID(conversation_id),  # str → UUID at boundary
        ...
    )
```

---

### Question 3: Migration Approach

**Recommendation: Option A (Incremental) but compressed into a focused sprint**

**Reasoning**: We're in alpha - the cost of incomplete migration is low, but the benefit of phase-gated verification is high. However, don't let this drag out.

**Proposed timeline**:

| Phase | Scope | Target |
|-------|-------|--------|
| 1 | Add `RequestContext` model, factory, documentation | Day 1 AM |
| 2 | Update routes to create context, pass alongside old params | Day 1 PM |
| 3 | Update services to use context, update tests | Day 2 |
| 4 | Remove old patterns, enforce consistency | Day 2-3 |

**Critical warning**: Do NOT leave Phase 2 (dual patterns) as permanent state. This is exactly how the current mess happened - transitional code became permanent. The 75% pattern applies to migrations too.

---

### Question 4: Scope

**Recommendation: Option C (Core three first, expand as needed)**

**Reasoning**: The 14 ID concepts fall into two categories:

**Request Identity** (belongs in RequestContext):
| ID | Purpose |
|----|---------|
| `user_id` | Who is making the request |
| `conversation_id` | Which conversation this is |
| `request_id` | This specific request (for tracing) |
| `workspace_id` | Which workspace (optional, future multi-tenant) |

**Domain Entities** (do NOT belong in RequestContext):
| ID | Why Not |
|----|---------|
| `project_id`, `intent_id`, `workflow_id`, `task_id`, etc. | These are *processed by* requests, not *context for* requests |

Domain entities have their own repositories and lifecycle. Don't conflate request context with domain data.

**Resolution for `session_id` overload**:

| Current Usage | Becomes |
|---------------|---------|
| Ephemeral request context | `request_id` |
| Conversation identity | `conversation_id` |
| User-context cache key | `user_id` (cache was using wrong key) |

---

### Question 5: Alternative Patterns

**Recommendation: Stick with explicit parameter passing**

I agree with the rejections in the ADR:

| Pattern | Why Rejected |
|---------|--------------|
| `contextvars` | Async complexity, hidden state, debugging difficulty |
| Request-scoped DI | Hidden dependencies make code archaeology harder |

**One hybrid worth considering** (optional enhancement, not required):

Create context in middleware, attach to `request.state`, but still pass as explicit parameter to services:

```python
# Middleware creates it once
@app.middleware("http")
async def add_request_context(request: Request, call_next):
    request.state.context = RequestContext.from_jwt_and_request(...)
    return await call_next(request)

# Route extracts and passes explicitly
@router.post("/intent")
async def process_intent(request: Request, body: IntentRequest):
    ctx = request.state.context  # Get from middleware
    return await intent_service.process(ctx, body.message)  # Pass explicitly
```

This gives single creation point + explicit service signatures. But for current scale, the simpler "create in route, pass through" approach is fine.

---

## Additional Recommendations

### 1. Add validation in factory

Fail fast on malformed input:

```python
@classmethod
def from_jwt_and_request(cls, claims: JWTClaims, conversation_id: str) -> "RequestContext":
    if not claims.sub:
        raise ValueError("JWT claims missing 'sub' field")
    if not conversation_id:
        raise ValueError("conversation_id is required")
    # ... rest of creation
```

### 2. Add `__str__` for logging

Make debugging easier:

```python
def __str__(self) -> str:
    return f"RequestContext(user={self.user_id}, conv={self.conversation_id}, req={self.request_id})"
```

### 3. Consider enforcement decorator (optional)

For critical paths where forgetting context would be catastrophic:

```python
def requires_context(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if 'ctx' not in kwargs and not (args and isinstance(args[0], RequestContext)):
            raise TypeError(f"{func.__name__} requires RequestContext as first argument")
        return await func(*args, **kwargs)
    return wrapper
```

---

## Decision Summary

| Question | Decision | Rationale |
|----------|----------|-----------|
| 1. Abstraction | Single `RequestContext` | Same scope of need despite different lifecycles |
| 2. Types | UUID internal, str at boundary | Type safety worth conversion cost |
| 3. Migration | Incremental, compressed to 2-3 days | Verification gates without drag-out risk |
| 4. Scope | Core four IDs only | Domain entities are separate concern |
| 5. Pattern | Explicit parameter passing | Clarity for multi-agent development |

---

## Sign-Off

**ADR-051: APPROVED** with above refinements.

The proposed pattern is architecturally sound. The investigation work that led to this proposal was thorough - the 14 ID concepts discovery and type inconsistency mapping are exactly the kind of archaeological work that prevents future bugs.

**Key risk to monitor**: Incomplete migration. The compressed timeline recommendation addresses this. Do not let Phase 2 become permanent.

**Priority**: This is tech debt, not blocking. Complete A20 bug fixes first, then schedule this as a focused 2-3 day sprint. Don't interleave with other work.

---

## Next Steps

1. Update ADR-051 with refinements noted above
2. Complete A20 sprint (current priority)
3. Schedule identity refactor sprint (2-3 dedicated days)
4. Execute phases sequentially with verification at each gate

If you have follow-up questions on any of these recommendations, route them through PM to Chief Architect.

---

*Memo created: 2026-01-13, 2:15 PM PT*
*Chief Architect (Claude Opus 4.5)*
