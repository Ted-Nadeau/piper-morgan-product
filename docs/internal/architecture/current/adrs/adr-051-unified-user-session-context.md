# ADR-051: Unified User Session Context

**Status**: PROPOSED (Awaiting Chief Architect Review)
**Date**: 2026-01-13
**Authors**: Lead Developer (Claude Code)
**Issue**: #584
**Deciders**: Chief Architect

## Context

### Problem Statement

The codebase has accumulated significant technical debt around identity and context management. Investigation (Issue #584) revealed:

1. **14 different ID concepts** scattered across the codebase
2. **Type inconsistencies** for `user_id` (UUID in DB, str in routes, mixed in services)
3. **Semantic overloading** of `session_id` for three different purposes
4. **Broken propagation** where `user_id` doesn't flow through call chains

This has caused multiple bugs (#490, #582) and will continue to cause bugs as features are added.

### Root Cause Analysis

The issues stem from three interrelated problems:

**1. Model Problem (Foundational)**
Three distinct domain concepts are conflated:
- **User Identity**: Who is making the request (permanent)
- **Session Context**: Ephemeral request context (per-request)
- **Conversation Context**: Multi-turn state (per-conversation)

**2. Naming Problem (Semantic)**
`session_id` is used for:
- Request-level ephemeral context in routes
- Persistent conversation identity in ConversationManager
- User-context cache key in UserContextService

**3. Implementation Problem (Type System)**
`user_id` has 5+ different type representations:
- `UUID` in database models
- `UUID` in `JWTClaims.user_id` field
- `str` in `JWTClaims.sub` field (canonical JWT claim)
- `str` when extracted in routes (`current_user.sub`)
- Mixed `str`/`UUID` in service layer parameters

### Historical Context

This pattern emerged from:
1. Initial single-user architecture where `session_id` == user context
2. Multi-user retrofit (Issue #280) that added fallbacks rather than proper propagation
3. Feature accretion (onboarding, portfolio, standup) each handling IDs inconsistently
4. No unified identity layer as a single source of truth

### Current State Evidence

| File | Issue | Severity |
|------|-------|----------|
| `web/api/routes/intent.py:221` | Uses `.sub` instead of `.user_id` | HIGH |
| `services/user_context_service.py:49` | Falls back to session_id as user ID | CRITICAL |
| `services/intent/intent_service.py:140` | Uses session_id as conversation_id | MEDIUM |
| `services/intent_service/canonical_handlers.py:126` | `user_id: str = None` (wrong type) | HIGH |
| `services/intent_service/todo_handlers.py:37` | `user_id: UUID` (conflicting type) | HIGH |

## Decision

### Proposed Solution: Unified `RequestContext` Model

Create a single, immutable context object that flows through the entire request lifecycle:

```python
# services/domain/models.py

@dataclass(frozen=True)
class RequestContext:
    """
    Unified context for all request processing.

    This is the single source of truth for identity and context.
    Passed through all service calls - never optional, never reconstructed.
    """
    # User Identity (permanent)
    user_id: UUID                    # Authenticated user's database PK
    username: str                    # Display name

    # Conversation Context (persistent per-conversation)
    conversation_id: UUID            # Database PK for conversation record

    # Request Context (ephemeral)
    request_id: UUID                 # Unique per-request for tracing
    timestamp: datetime              # Request timestamp

    # Optional context
    workspace_id: Optional[UUID] = None  # For future multi-tenant support

    @classmethod
    def from_jwt_and_request(
        cls,
        claims: JWTClaims,
        conversation_id: UUID,
        request_id: Optional[UUID] = None,
    ) -> "RequestContext":
        """Factory method to create context from JWT claims and request data."""
        return cls(
            user_id=UUID(claims.sub),  # Canonical: JWT sub claim as UUID
            username=claims.username,
            conversation_id=conversation_id,
            request_id=request_id or uuid4(),
            timestamp=datetime.utcnow(),
            workspace_id=UUID(claims.workspace_id) if claims.workspace_id else None,
        )
```

### Propagation Pattern

```python
# In routes - create context once at boundary
@router.post("/intent")
async def process_intent(
    request: IntentRequest,
    current_user: JWTClaims = Depends(get_current_user),
):
    # Create context at request boundary - single source of truth
    context = RequestContext.from_jwt_and_request(
        claims=current_user,
        conversation_id=request.conversation_id,
    )

    # Pass context through all calls
    result = await intent_service.process(context, request.message)
    return result

# In services - always receive context, never reconstruct
class IntentService:
    async def process(self, ctx: RequestContext, message: str) -> IntentResult:
        # Use ctx.user_id for user-scoped operations
        user_context = await self.context_service.get(ctx.user_id)

        # Use ctx.conversation_id for conversation operations
        history = await self.conversation_repo.get_turns(ctx.conversation_id)

        # Pass context to downstream services
        return await self._route_intent(ctx, classified_intent)
```

### Type Consistency

Standardize on:
- **`UUID` internally** for all ID fields in domain models and services
- **`str` at boundaries** (HTTP requests/responses, JWT claims)
- **Explicit conversion** at boundary only, using `UUID(str_value)`

### Migration Strategy

**Phase 1: Add `RequestContext`** (non-breaking)
- Create the model in `domain/models.py`
- Add factory method
- Document in CLAUDE.md

**Phase 2: Route-level adoption** (incremental)
- Update routes to create `RequestContext`
- Pass to services alongside existing parameters
- Services accept both patterns during migration

**Phase 3: Service-level migration** (incremental)
- Update services to use `RequestContext`
- Remove old parameter patterns
- Update tests

**Phase 4: Cleanup** (breaking)
- Remove fallback patterns in `UserContextService`
- Remove `session_id` parameter from methods that should use `conversation_id`
- Enforce type consistency

## Alternatives Considered

### Alternative A: Request-Scoped Dependency Injection
Use FastAPI's dependency injection to provide context automatically.

**Pros**: Less explicit passing, cleaner signatures
**Cons**: Hidden dependencies, harder to test, magic behavior

**Decision**: Rejected - explicit is better than implicit for critical context

### Alternative B: Thread-Local / Context Variables
Use Python's `contextvars` for implicit context propagation.

**Pros**: No parameter passing needed
**Cons**: Hidden state, harder to reason about, async complexity

**Decision**: Rejected - explicit passing is more maintainable

### Alternative C: Keep Current Pattern, Just Document
Document the existing inconsistencies and establish conventions.

**Pros**: No code changes, immediate
**Cons**: Doesn't fix the bugs, conventions will drift

**Decision**: Rejected - documentation alone hasn't prevented bugs

## Consequences

### Positive
- Single source of truth for identity/context
- Type-safe ID handling
- Eliminates class of bugs around `user_id` propagation
- Clear audit trail (request_id tracing)
- Foundation for multi-tenant support

### Negative
- Significant refactoring effort
- All services need signature updates
- Tests need updates
- Learning curve for new pattern

### Risks
- Incomplete migration leaves two patterns
- Over-engineering if simpler solution exists
- Breaking changes during migration

## Questions for Chief Architect

1. **Is `RequestContext` the right abstraction?** Should it be split (e.g., `UserContext` + `ConversationContext` + `RequestMetadata`)?

2. **Type standardization**: Is `UUID` internally / `str` at boundaries the right choice? Or should we use `str` everywhere for simplicity?

3. **Migration approach**: Incremental (Phases 1-4) or big-bang refactor?

4. **Scope**: Should this include all 14 ID concepts, or focus on the core three (`user_id`, `session_id`, `conversation_id`)?

5. **Alternative patterns**: Are there patterns from other projects that handle this better?

## References

- Issue #584 - Original tech debt identification
- Issue #582 - Bug caused by missing `user_id` propagation
- Issue #490 - Portfolio onboarding bug (related to session/user confusion)
- ADR-049 - Conversational State (related context management)

---

_ADR created: 2026-01-13_
_Status: PROPOSED - Awaiting Chief Architect review_
