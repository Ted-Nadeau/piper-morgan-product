# Release Notes: v0.8.4.1

**Release Date**: January 13, 2026
**Release Type**: Patch Release (Bug Fixes + Architecture Improvement)

---

## Overview

This patch release fixes several bugs discovered during alpha testing and introduces a foundational architecture improvement for identity handling. The fixes address chat persistence, standup routing, and unified request context management.

**Key improvements in this release:**
- **Chat persistence**: Conversations now auto-load on page refresh
- **Standup routing**: `/standup` command correctly routes to interactive handler
- **Identity architecture**: New `RequestContext` model provides unified user/session handling (ADR-051)

---

## Bug Fixes

### Issue #583: Chat Persistence
**Problem**: Conversation history was lost on page refresh - users had to manually reload their conversation.

**Fix**: Chat now automatically loads the current conversation on page refresh (`693ae13b`).

### Issue #585: Standup Routing
**Problem**: The `/standup` command and portfolio onboarding were conflicting, causing routing issues.

**Fix**: Explicit `/standup` command now correctly routes to the interactive `StandupConversationHandler`, while greeting-based onboarding triggers `PortfolioOnboardingHandler` (`f666884a`).

### Issue #582: UserContextService Database Connection
**Problem**: User context service wasn't connecting to database projects properly.

**Fix**: Connected `UserContextService` to database projects for proper user context retrieval (`c7d58927`).

### Issue #581: Chat Sidebar Sync
**Problem**: Clicking a conversation in the sidebar didn't sync with the chat input.

**Fix**: Chat input now correctly syncs with sidebar conversation selection (`90f39287`).

### Issue #574: Conversation History Sidebar
**Problem**: Conversation history sidebar wasn't correctly switching between conversations.

**Fix**: Sidebar now properly switches conversations and loads corresponding history (`faf305c7`).

---

## Architecture Improvements

### Issue #584: Unified Request Context (ADR-051)

**Problem**: The codebase had 14 different ID concepts with type inconsistencies - `user_id` varied between UUID and string, and `session_id` was overloaded for three different purposes.

**Solution**: Introduced `RequestContext` - a single, immutable context object that serves as the source of truth for identity:

```python
@dataclass(frozen=True)
class RequestContext:
    user_id: UUID           # Authenticated user's database PK
    conversation_id: UUID   # Database PK for conversation record
    request_id: UUID        # Unique per-request for tracing
    user_email: str         # User's email for logging
    timestamp: datetime     # Request timestamp (UTC)
    workspace_id: Optional[UUID] = None  # Future multi-tenant
```

**Implementation**: 4-phase migration completed:
1. `RequestContext` model added with factory method (`6ee40118`)
2. Intent route creates context at HTTP boundary (`f18497d3`)
3. `IntentService` accepts context parameter (`46cfec51`)
4. Documentation updated with new patterns (`e46976c2`)

**Benefits**:
- Type safety: UUID internally, string conversion only at boundaries
- Single source of truth for identity
- Foundation for future multi-tenant support
- 12 new unit tests for context handling

---

## Test Results

```
=============== 1705 passed, 26 skipped ================
```

- All existing tests continue to pass
- 12 new tests added for `RequestContext`

---

## Upgrade Notes

- **No database migrations required**
- **No configuration changes required**
- **Backwards compatible**: Old `session_id`/`user_id` parameters still work

---

## Related Issues

| Issue | Type | Description |
|-------|------|-------------|
| #583 | Bug | Chat persistence on page refresh |
| #585 | Bug | Standup/Portfolio routing conflict |
| #584 | Architecture | Unified identity model (ADR-051) |
| #582 | Bug | UserContextService database connection |
| #581 | Bug | Chat sidebar sync |
| #574 | Bug | Conversation history switching |

---

## What's Next

- Continue alpha testing with focused manual test scenarios
- Monitor calendar integration (potential issue with "no events" responses)
- Incremental adoption of `RequestContext` in other routes/services

---

**Full Changelog**: [v0.8.4...v0.8.4.1](https://github.com/mediajunkie/piper-morgan-product/compare/v0.8.4...v0.8.4.1)
