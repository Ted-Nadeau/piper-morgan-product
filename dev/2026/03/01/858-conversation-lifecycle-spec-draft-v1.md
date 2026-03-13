# Conversation Lifecycle Specification

**Issue**: #858 — SPEC: Conversation lifecycle specification
**Status**: DRAFT v1.1
**Date**: March 1, 2026
**Author**: Lead Developer
**Informed by**: CXO memo (Feb 28), PPM memo (Feb 28), Research report (Feb 28)
**Feeds into**: #715 (MUX-HOME-CONVERSATIONS-LIFECYCLE, M2)
**Compatible with**: ADR-050 (graph model), PDR-002 (conversational glue), PDR-101 (multi-entity conversations), MultiChat PRD v1.0 (Ted Nadeau)

---

## 1. Design Principles

These principles constrain all sections of this specification. When in doubt about a design choice, return to these.

### P1. The Colleague Test

Users don't think about conversation "lifecycle." They think: "that time I talked to Piper about quarterly planning" and "what we discussed yesterday." Our UX language must match natural speech, not internal system terminology.

- Internal states (ACTIVE, ARCHIVED, COMPOSTED) inform Piper's behavior
- User-visible states are simpler: conversations are there, older, or gone
- Piper never says "your RATIFIED conversation" — she says "what we talked about"

### P2. Entity Surface, Not Conversation Archive

The right sidebar (History) is the **entity surface** — the UI home for Layer 2 of the Three-Layer Context Persistence Model (ADR-054). Conversations appear here first because they are the first entity type users form through work with Piper.

Future entity types (WorkItems, Features, Documents) will also surface here. **Do not design the sidebar as "conversation archive" — design it as "user work objects with lifecycle state."**

### P3. Multi-Entity Compatibility

This spec uses language that does not preclude multi-participant conversations (PDR-101, MultiChat PRD v1.0):

| Avoid | Use Instead | Reason |
|-------|------------|--------|
| "My chat with Piper" | "Conversation about X" | Topic-centric, not participant-centric |
| "User's conversation" | "Conversation owner" / `created_by` | Supports multiple participants |
| "Piper and I discussed" | "This conversation covered" | Agent-neutral |
| `user_id` (in new code) | `created_by` (in spec language) | Compatible with PDR-101 |

### P4. State Is Visual, Not Nominal

Conversation names stay stable across lifecycle transitions. The *presentation* changes — not the name.

- "M0 Planning" with normal appearance (active)
- "M0 Planning" dimmed/grouped (archived)
- Never: "Archived: M0 Planning"

### P5. Extensible Boundaries

Conversation boundaries must accommodate future evolution — branching, forking, and multi-participant models — even if the current answer is "not yet." The boundary definition should be a policy, not a hardcoded assumption.

### P6. Anti-Flattening Checklist

Before any implementation of this spec, verify:

- [ ] Right sidebar is "entity surface," not "conversation archive"
- [ ] Internal lifecycle states are distinct from user-visible states
- [ ] Conversation naming is by topic, not by state
- [ ] Language supports future multi-participant model
- [ ] Boundary definition allows for branching/forking evolution
- [ ] Conversation boundary definition is extensible (PPM addition)

---

## 2. Lifecycle State Machine

### 2.1 Internal States

Conversations move through three internal states. These states inform Piper's behavior and system operations but are **not directly exposed in the UI**.

```
               calendar-day         time-based
               boundary or          distillation
               user action          (automated)

  [Creation] ──► ACTIVE ──────────► ARCHIVED ──────────► COMPOSTED
                   │                   │
                   │   user deletes    │   user deletes
                   ▼                   ▼
                DELETED             DELETED
```

| Internal State | Maps to Entity Lifecycle | Description |
|----------------|-------------------------|-------------|
| **ACTIVE** | RATIFIED | Current, accessible. User is engaged or recently was. |
| **ARCHIVED** | ARCHIVED | Preserved for reference. Searchable. Not in active use. |
| **COMPOSTED** | COMPOSTED | Content distilled into Piper's learning. Original conversation no longer directly surfaced. See 2.1.1. |
| **DELETED** | (soft delete) | Removed by user action. Not visible anywhere. Soft-deleted in DB with `deleted_at` timestamp for data retention policy compliance. |

#### 2.1.1 COMPOSTED Content Retention

COMPOSTED conversations retain their original content in the database but are no longer directly accessible to users. The content is available for Piper's cross-session memory synthesis (ADR-054 Layer 3) but not surfaced in sidebars or search. Actual content deletion after distillation is a future policy decision, not part of MVP.

### 2.2 User-Visible States

| What User Sees | Internal State | Visual Treatment | Where Visible |
|---------------|----------------|------------------|---------------|
| **(just there)** | ACTIVE | Normal appearance | Left sidebar, right sidebar |
| **"Older conversations"** | ARCHIVED | Dimmed or grouped separately | Right sidebar only |
| **"Piper remembers things"** | COMPOSTED | Not visible | Implicit in Piper's responses |
| **(gone)** | DELETED | Simply disappears | Nowhere |

**COMPOSTED visibility**: COMPOSTED conversations are not visible in either sidebar and do not appear in search results. Users who need to review old conversations should do so before the composting period elapses. Composted content influences Piper's responses through the memory system but is not directly browsable.

### 2.3 State Transitions

| Transition | Trigger | Reversible? | Notes |
|-----------|---------|-------------|-------|
| Creation → ACTIVE | New conversation created (any path) | N/A | See Section 3 |
| ACTIVE → ARCHIVED | **Soft close**: calendar day boundary passes with no new user messages | Yes (user can reactivate) | See Section 7.2 |
| ACTIVE → ARCHIVED | **Hard close**: user explicitly archives from UI | Yes | Right sidebar action |
| ARCHIVED → ACTIVE | User sends a new message in archived conversation | Yes | Explicit continuation |
| ARCHIVED → COMPOSTED | Automated: conversation content distilled into learning after configurable period (default: 90 days) | No | Layer 3 of persistence model. See 2.3.1. |
| ACTIVE → DELETED | User explicitly deletes | No (from user perspective) | Soft delete in DB |
| ARCHIVED → DELETED | User explicitly deletes | No (from user perspective) | Soft delete in DB |

#### 2.3.1 Composting Period Configuration

The composting period is configured at the system level via environment variable `PIPER_COMPOSTING_DAYS` (default: 90) or in `config/piper.user.md`. Per-user configuration is a future enhancement. The 90-day default is generous by design — it reduces user anxiety about conversations disappearing while still providing eventual cleanup.

### 2.4 Domain Model Changes

The `Conversation` domain entity needs a `lifecycle_state` field to replace the binary `is_active`:

```python
# Proposed addition to services/domain/models.py Conversation dataclass
class ConversationLifecycleState(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    COMPOSTED = "composted"
    DELETED = "deleted"

# On Conversation dataclass:
lifecycle_state: ConversationLifecycleState = ConversationLifecycleState.ACTIVE
is_active: bool = True  # DEPRECATED — retained for backward compatibility during migration
deleted_at: Optional[datetime] = None  # Set when state transitions to DELETED
archived_at: Optional[datetime] = None  # Set when state transitions to ARCHIVED
```

**Evolutionary note**: `lifecycle_state` applies to the conversation *container*, not the turn/node sequence inside it. Whether the conversation contains 50 linear turns or a 200-node graph (ADR-050 Phase 2), the lifecycle state is about the conversation as an entity.

### 2.5 `is_active` Migration Path

1. Add `lifecycle_state` column (default ACTIVE), `deleted_at`, `archived_at`
2. Backfill: all existing conversations with `is_active=True` → `lifecycle_state=ACTIVE`
3. Update all queries to use `lifecycle_state` instead of `is_active`
4. Deprecate `is_active` (keep as computed property for backward compatibility)
5. Remove `is_active` column after full migration verified

---

## 3. Creation Invariants

### 3.1 Creation Paths

Three paths currently create conversations. All must produce equivalent records.

| Path | Trigger | File | When It Fires |
|------|---------|------|--------------|
| **Explicit** | User clicks "+ New Chat" | `web/api/routes/conversations.py` → `create_conversation()` | User-initiated UI action |
| **Auto-create** | First message in a session with no conversation | `services/database/repositories.py:1151` → `ensure_conversation_exists()` | System-initiated, before turn save |
| **Lazy ensure** | Before saving turns when conversation_id provided but no DB record | Same function, different caller | System-initiated, FK constraint prevention |

### 3.2 Required Invariants (Post-Creation)

Every conversation, regardless of creation path, MUST have:

| Field | Invariant | Enforcement |
|-------|-----------|-------------|
| `id` | Non-empty UUID string | Generated at creation |
| `created_by` / `user_id` | Valid, authenticated user ID | **MUST NOT** be empty, null, or "unknown" (post-#840 fix) |
| `session_id` | Non-empty session identifier | Set at creation |
| `title` | Non-empty string | Default: "Conversation" (auto-titled after first turn via #598) |
| `lifecycle_state` | ACTIVE | Default on creation |
| `created_at` | Server-generated timestamp | Set at creation |
| `updated_at` | Server-generated timestamp | Set at creation, updated on each turn |
| `last_activity_at` | Server-generated timestamp | Updated on each user message |

### 3.3 Invariant Violations

If a required invariant cannot be satisfied, the creation path MUST:
1. **Log the violation** with structured logging (conversation_id, path, which invariant failed)
2. **Refuse to create** the conversation (not create a broken one)
3. **Surface the failure** to the caller (not silently swallow)

This is the lesson of #840: `ensure_conversation_exists` used to silently create conversations with `user_id="unknown"`, making them permanently invisible. The post-#840 fix correctly refuses creation when `user_id` is missing.

### 3.4 Evolutionary Note

Current creation paths assume a single owner (`user_id`). The spec uses `created_by` language to remain compatible with PDR-101's multi-participant model, where conversations may be created by facilitator agents or other participants. The creation invariants above apply to the conversation owner; additional participants are added after creation (Phase 2+).

---

## 4. Auth Contract

### 4.1 Principle: No Silent Failures

When authentication fails during a conversation session, the system MUST inform the user with a clear action path. Silent failures — where the user continues typing but nothing persists — are the most confusing UX pattern and are explicitly prohibited.

### 4.2 Auth Failure Scenarios

| Scenario | Current Behavior (post-#840) | Specified Behavior |
|----------|------------------------------|-------------------|
| **Token expired during session** | `ensure_conversation_exists` refuses creation (no user_id) → turn save fails on FK constraint | Surface to user: "Your session expired — please log in to continue." Preserve unsent message in UI. |
| **Cookie missing on sidebar fetch** | `fetchHistoryConversations()` now includes `credentials: 'include'` | Return 401 → sidebar shows "Sign in to see history" (not empty list) |
| **Token expired between sessions** | Redirect to login | Redirect to login. On successful re-auth, restore last conversation state. |
| **Intent endpoint without auth** | Currently requires auth | Continues to require auth. Unauthenticated requests return 401 with redirect URL. |

### 4.3 Conversation State Preservation

When auth expires mid-session:
1. Any message the user has typed but not sent MUST be preserved in the UI (client-side)
2. Turns already persisted MUST NOT be lost (they're in the DB with valid user_id)
3. After re-authentication, the user should return to their conversation, not a blank screen

### 4.4 Token Refresh Contract

Per #857 (auth token management), conversation-related endpoints should:
- Accept auth tokens via cookie (`credentials: 'include'` on all fetch calls)
- Return 401 (not 403) when token is expired (allows client-side refresh logic)
- Include `X-Auth-Redirect` header with login URL on 401 responses

---

## 5. Sidebar Identity & Refresh Contract

### 5.1 Two Sidebars, Two Purposes

| | Left Sidebar | Right Sidebar |
|---|-------------|---------------|
| **Purpose** | Navigation | Retrieval (entity surface) |
| **Mental model** | "Switch to that other thing" | "Find something from before" |
| **Shows** | Recent ACTIVE conversations | All conversations (ACTIVE + ARCHIVED), searchable |
| **Lifecycle filter** | `lifecycle_state = ACTIVE` | `lifecycle_state IN (ACTIVE, ARCHIVED)` |
| **Entity types** | Conversations only (for now) | Conversations now; WorkItems, Features, etc. later |
| **Persistence model layer** | Layer 1 (Conversational Memory, ~24hr window) | Layer 2 (User History, all time, searchable) |
| **Ordering** | Most recent activity first | Grouped by time period (Today, Yesterday, This Week, Older) |

### 5.2 Right Sidebar Is the Entity Surface

The right sidebar will eventually surface all hardened entities — not just conversations. Current implementation (conversations only) is a starting point. Design and API contracts should not assume conversations are the only entity type.

**API design implication**: The right sidebar endpoint should be named/structured to accommodate additional entity types (e.g., `/api/v1/history` rather than `/api/v1/conversations/history`).

### 5.3 Refresh Triggers

| Event | Left Sidebar | Right Sidebar |
|-------|-------------|---------------|
| User sends message | Update `last_activity_at` in current entry | Update `last_activity_at` in current entry |
| New conversation created | Add to top of list | Add to "Today" group |
| User switches conversation | Highlight selected | Highlight selected |
| Conversation archived | Remove from list | Move to "Older" group, apply dimmed style |
| Conversation deleted | Remove from list | Remove from list |
| Page navigation | Full re-fetch | Full re-fetch |
| Timer/polling | Not required for MVP | Not required for MVP |
| Server-sent events | Not required for MVP | Not required for MVP |

### 5.4 API Endpoints

**Current state**: Both sidebars call `GET /api/v1/conversations` with the same data. This is the "two-sidebar identity crisis" identified in the sidebar archaeology report.

**Specified behavior**:

| Endpoint | Purpose | Returns |
|----------|---------|---------|
| `GET /api/v1/conversations?state=active` | Left sidebar | ACTIVE conversations, ordered by `last_activity_at` DESC |
| `GET /api/v1/conversations?state=active,archived` | Right sidebar | ACTIVE + ARCHIVED conversations, grouped by time period |
| `GET /api/v1/conversations?q={search}` | Right sidebar search | Conversations matching title or content, across all non-deleted states |

Filtering by `lifecycle_state` differentiates the two sidebars at the API level while reusing the same endpoint.

---

## 6. Representation Inventory

### 6.1 ConversationTurn: Three Definitions

| # | File | Fields | Purpose | Canonical? |
|---|------|--------|---------|------------|
| 1 | `services/domain/models.py:1641` | id, conversation_id, turn_number, user_message, assistant_response, intent, entities, references, context_used, metadata, processing_time, created_at, completed_at | **Persistence/database model** — full turn record for storage and retrieval | **Yes — this is the canonical persistence representation** |
| 2 | `services/intent_service/conversation_context.py:51` | id, timestamp, message, intent (Intent enum), temporal_reference, entity_references, topic, lens | **In-session context window** — lightweight turn for the 10-turn sliding window used during intent processing | Derived — maps to Turn #1's `user_message` + `intent` + `entities` subset |
| 3 | `services/intelligence/conversation_aware.py:28` | user_message, questions_asked (List[ClarifyingQuestion]), timestamp | **Intelligence layer** — minimal turn for clarifying question tracking | Derived — maps to Turn #1's `user_message` + metadata subset |

### 6.2 Mapping Between Representations

```
Turn #1 (domain/models.py)         Turn #2 (conversation_context.py)    Turn #3 (conversation_aware.py)
─────────────────────────          ──────────────────────────────────    ──────────────────────────────
id                          ←──── id                                    (not mapped)
conversation_id                    (held by parent ConversationContext)  (not mapped)
turn_number                        (implicit by position in list)       (not mapped)
user_message                ←──── message                        ←──── user_message
assistant_response                 (not captured)                       (not captured)
intent (str)                ←──── intent (Intent enum)                  (not captured)
entities (list[str])        ←──── entity_references (list[str])        (not captured)
                                   temporal_reference                   (not captured)
                                   topic                               (not captured)
                                   lens                                (not captured)
metadata                           (not mapped)                  ←──── questions_asked
created_at                  ←──── timestamp                      ←──── timestamp
```

### 6.3 Consolidation Recommendation

**Do not unify into a single class.** The three representations serve genuinely different purposes at different system layers. Unification would either bloat the lightweight context-window turn or strip fields from the persistence model.

**Do**:
- Document the mapping above in code comments on each class
- Rename Turn #3 to `ClarifyingQuestionTurn` or `IntelligenceTurn` to reduce name collision confusion
- Ensure ADR-050 compatibility note: Turn #1 is "a shorthand for a message Node and its assistant response Node linked by 'reply'" — when the graph model arrives, Turn #1 decomposes into two nodes

### 6.4 ConversationContext: Two Definitions

| # | File | Fields | Purpose | Canonical? |
|---|------|--------|---------|------------|
| 1 | `services/intent_service/conversation_context.py:80` | session_id, user_id, turns (list of Turn #2), max_turns, max_age_minutes, lens_stack, last_offer | **In-session state** — rich context for intent processing with lens tracking, offer tracking, pruning | **Yes for in-session context** |
| 2 | `services/conversation/conversation_manager.py:24` | conversation_id, turns (list of Turn #1), created_at, updated_at, metadata | **Persistence-layer context** — bounded window of persisted turns for retrieval | **Yes for persisted context** |

### 6.5 ConversationContext Naming Recommendation

Two classes with the same name in the same subsystem is a naming collision. Recommend:

| Current Name | Proposed Name | Rationale |
|-------------|--------------|-----------|
| `conversation_context.py::ConversationContext` | `SessionConversationContext` | Emphasizes its role as in-session, ephemeral state |
| `conversation_manager.py::ConversationContext` | `PersistedConversationContext` | Emphasizes its role as DB-backed, durable state |

This rename is low-risk (each is used within its own module) and prevents confusion when both appear in the same discussion or code path.

---

## 7. Scope & Boundary

### 7.1 What Is a Conversation?

A conversation is a **bounded sequence of interactions** between a user and Piper (and, in the future, other participants) on a set of related topics. It is an entity with identity, lifecycle state, and persistence.

**Key properties**:
- Has a single `created_by` owner (the user who initiated it)
- Has a creation timestamp and lifecycle state
- Contains an ordered sequence of turns (currently linear; future: graph)
- Has a topic-based name (assigned by Piper or the user)
- Is bounded by time (see 7.2) and can be bounded by user action

**What a conversation is NOT**:
- It is not a session (sessions are auth-scoped; conversations are content-scoped)
- It is not permanent (conversations have lifecycle states and eventually compost)
- It is not a thread (conversations are top-level entities; threading is internal structure)

### 7.2 Conversation Boundaries: Start and End

#### When Does a Conversation Start?

A new conversation begins when:
1. **User creates explicitly**: clicks "+ New Chat" in the UI
2. **User sends first message** in a session with no active conversation
3. **Piper initiates proactively**: "Good morning, here's what's happening" (creates a new conversation for the proactive message)
4. **Calendar day boundary crossed** (see below)

#### When Does a Conversation End?

Users don't formally "end" conversations — they drift away. Like a colleague, Piper doesn't demand formal closure.

**Default: New calendar day = new conversation.**

After midnight (local time), the next user interaction starts a new conversation. The previous day's conversation transitions to ARCHIVED.

This is simpler than an inactivity timer (no "was it 24 or 48 hours?") and aligns with Piper's "good morning" greeting pattern. If a user sends a message at 11:59 PM and another at 12:01 AM, that's a new conversation by default.

**Exception: Explicit continuation.** A user can continue yesterday's conversation by:
- Selecting it in the right sidebar and sending a message (reactivates from ARCHIVED → ACTIVE)
- This is "Option A" (explicit sidebar action) per PPM guidance

**Future: Piper prompt (Option B).** Piper may eventually offer: "Good morning! Want to pick up where we left off yesterday, or start fresh?" This requires context awareness and is polish, not MVP.

**Future: Magic continuation (Option C).** "What were we talking about yesterday?" is handled by M0 Conversational Glue — lens tracking and reference resolution — without requiring formal conversation continuation. The user starts a new conversation but references the old one.

### 7.3 Conversation-Session Relationship

Currently, conversations are coupled to sessions via `session_id`. This coupling should be loosened:

| Current | Specified |
|---------|-----------|
| `session_id` used as conversation identifier | `session_id` tracks auth session; `conversation_id` is independent |
| One session = one conversation (implicit) | One session may span multiple conversations (e.g., user archives and starts new) |
| Session expiry = conversation uncertainty | Session expiry is an auth event; conversation state is preserved independently |

### 7.4 Branching and Forking

**Current answer: not yet.**

The spec acknowledges that conversations may eventually branch or fork (per Ted's model and ADR-050 Phase 2). The current boundary definition (one user + Piper + linear turns) does not assume these constraints are permanent:

- `conversation_id` is a standalone identifier, not derived from session
- Lifecycle states apply to the conversation container, not the turn sequence
- No schema assumptions prevent adding `parent_conversation_id` for branching (ADR-050 Phase 1: `parent_id` for threading)

---

## 8. Test Specifications

These test specifications define the verification criteria for implementing conversation lifecycle (#715). Each test includes enough detail to translate directly into pytest code.

### 8.1 State Machine Tests

#### T1: Fresh conversation has ACTIVE state

```
Given: An authenticated user
When: A conversation is created (any creation path)
Then: conversation.lifecycle_state == ACTIVE
  And: conversation.archived_at is None
  And: conversation.deleted_at is None
  And: conversation appears in left sidebar API response
  And: conversation appears in right sidebar API response
```

#### T2: Calendar day boundary archives conversation

```
Given: An ACTIVE conversation with last_activity_at = yesterday 23:00
  And: Current time is today 08:00
When: User sends a new message (not in this conversation)
Then: The old conversation.lifecycle_state == ARCHIVED
  And: old conversation.archived_at is set
  And: A new ACTIVE conversation is created for the new message
  And: Old conversation no longer appears in left sidebar
  And: Old conversation appears in right sidebar with archived visual treatment
```

**Implementation hint**: The archival transition should be triggered during conversation resolution (when the system determines which conversation a new message belongs to), not by a background cron job. Check: `is the active conversation from a previous calendar day?` If yes, archive it and create a new one.

#### T3: User explicitly archives a conversation

```
Given: An ACTIVE conversation
When: User sends archive action from the UI (e.g., PATCH /api/v1/conversations/{id}/state with body {"state": "archived"})
Then: conversation.lifecycle_state == ARCHIVED
  And: conversation.archived_at is set
  And: conversation removed from left sidebar
  And: conversation remains in right sidebar (dimmed/grouped)
```

#### T4: Reactivation by sending a message

```
Given: An ARCHIVED conversation
When: User selects it in the right sidebar and sends a message
Then: conversation.lifecycle_state == ACTIVE
  And: conversation.archived_at is cleared (or kept for history; implementation choice)
  And: conversation reappears in left sidebar
  And: The new turn is appended to the existing conversation
```

#### T5: User deletes a conversation

```
Given: A conversation in any state (ACTIVE or ARCHIVED)
When: User sends delete action (DELETE /api/v1/conversations/{id})
Then: conversation.lifecycle_state == DELETED
  And: conversation.deleted_at is set
  And: conversation removed from both sidebars
  And: conversation is NOT hard-deleted from DB (soft delete for data retention)
  And: GET /api/v1/conversations/{id} returns 404
```

#### T6: COMPOSTED conversations are invisible

```
Given: A conversation with lifecycle_state == COMPOSTED
When: User queries left sidebar (GET /api/v1/conversations?state=active)
  And: User queries right sidebar (GET /api/v1/conversations?state=active,archived)
  And: User searches (GET /api/v1/conversations?q=...)
Then: The composted conversation does NOT appear in any response
```

### 8.2 Creation Invariant Tests

#### T7: All creation paths produce equivalent records

```
Given: Three conversations created via:
  (a) POST /api/v1/conversations (explicit)
  (b) ensure_conversation_exists() during first message (auto-create)
  (c) ensure_conversation_exists() during turn save (lazy ensure)
Then: All three have:
  - Non-empty id (UUID format)
  - Valid user_id matching the authenticated user
  - Non-empty session_id
  - Non-empty title (default: "Conversation")
  - lifecycle_state == ACTIVE
  - created_at and updated_at set to server time
```

#### T8: Creation refuses without valid user_id

```
Given: A request to ensure_conversation_exists() with user_id=None
When: The function is called
Then: No conversation record is created
  And: A structured log entry is emitted with level ERROR
  And: The caller receives an indication of failure (not a silent creation)
```

### 8.3 Auth Contract Tests

#### T9: Token expiry surfaces to user (not silent)

```
Given: An authenticated user in an active conversation
When: Their auth token expires
  And: They send a new message
Then: The API returns 401 (not 200 with silent failure)
  And: The response includes a redirect URL or re-auth instruction
  And: Previously persisted turns are NOT lost
  And: The UI preserves the unsent message text (client-side)
```

#### T10: Sidebar fetch without auth returns 401

```
Given: A request to GET /api/v1/conversations without valid auth cookie
When: The request is made
Then: Response status is 401
  And: Response is NOT an empty conversation list (that would be a silent failure)
```

### 8.4 Sidebar Tests

#### T11: Left and right sidebars show different data

```
Given: 3 ACTIVE conversations and 2 ARCHIVED conversations for a user
When: Left sidebar is fetched (GET /api/v1/conversations?state=active)
  And: Right sidebar is fetched (GET /api/v1/conversations?state=active,archived)
Then: Left sidebar returns 3 conversations
  And: Right sidebar returns 5 conversations
  And: ARCHIVED conversations in right sidebar have distinct visual metadata (e.g., "archived": true in response)
```

#### T12: Sidebar refresh on new message

```
Given: An active conversation listed in both sidebars
When: User sends a new message in that conversation
Then: The conversation's last_activity_at is updated
  And: The conversation moves to the top of the left sidebar
  And: The conversation's timestamp updates in the right sidebar
```

#### T13: User can find old conversation via right sidebar search

```
Given: An ARCHIVED conversation titled "Q4 Planning Discussion"
When: User searches in right sidebar with query "Q4 Planning"
Then: The archived conversation appears in search results
  And: The conversation has archived visual treatment
  And: User can click to open and optionally continue it
```

### 8.5 End-to-End Integration Test

#### T14: Full lifecycle — create, converse, archive, search, continue

This is the critical end-to-end **happy path** integration test. It exercises the complete lifecycle path. Edge cases and failure modes are covered individually in T1-T13 and T15-T16.

```
Setup: Authenticated user, clean conversation state

Step 1 — Create:
  User sends: "Help me plan Q4"
  Assert: New conversation created with lifecycle_state=ACTIVE
  Assert: Conversation appears in left sidebar
  Assert: Conversation appears in right sidebar
  Assert: Piper responds with planning assistance

Step 2 — Name:
  Assert: After first substantive exchange, conversation has topic-based title
    (e.g., "Q4 Planning" — not "Chat #47" or "Conversation")

Step 3 — Continue same day:
  User sends: "What about the budget?"
  Assert: Message appends to same conversation (not new one)
  Assert: turn_number increments
  Assert: Conversation remains ACTIVE

Step 4 — Day boundary archive:
  Simulate: Clock advances past midnight
  User sends: "Good morning"
  Assert: Yesterday's "Q4 Planning" conversation is now ARCHIVED
  Assert: A new ACTIVE conversation is created for today
  Assert: "Q4 Planning" no longer in left sidebar
  Assert: "Q4 Planning" appears in right sidebar (archived treatment)

Step 5 — Search and find:
  User searches right sidebar: "Q4"
  Assert: "Q4 Planning" appears in results with archived treatment

Step 6 — Continue old conversation:
  User clicks "Q4 Planning" in right sidebar
  User sends: "Actually, let's revisit the timeline"
  Assert: "Q4 Planning" transitions back to ACTIVE
  Assert: "Q4 Planning" reappears in left sidebar
  Assert: The new turn is appended (not a new conversation)

Step 7 — Delete:
  User deletes today's empty conversation
  Assert: Conversation disappears from both sidebars
  Assert: Conversation still exists in DB with lifecycle_state=DELETED and deleted_at set
```

**Implementation note**: This test will likely need to mock the clock for the day boundary step. Use `freezegun` or equivalent to control `datetime.now()`. The important thing is that the day-boundary check happens in conversation resolution logic, not in a background job.

### 8.6 Naming Tests

#### T15: Conversation naming by topic

```
Given: A new conversation (default title "Conversation")
When: User sends a substantive message ("Help me plan the Q4 budget review")
  And: Piper responds
Then: Conversation title is updated to a topic-based name (e.g., "Q4 Budget Review")
  And: Title does NOT include state prefix ("Archived: ...")
  And: Title does NOT use numbered format ("Chat #47")
  And: Fallback (if topic unclear): date-based ("Mar 1 chat")
```

#### T16: Name stability across transitions

```
Given: A conversation titled "Q4 Budget Review" in ACTIVE state
When: Conversation transitions to ARCHIVED
Then: Title remains "Q4 Budget Review" (unchanged)
  And: Visual presentation changes (dimmed/grouped), not the name
```

---

## Appendix A: Relationship to #715

This specification defines **what** the conversation lifecycle is. Issue #715 implements **how** it appears in the UI.

| This Spec (#858) Defines | #715 Implements |
|--------------------------|----------------|
| ACTIVE / ARCHIVED / COMPOSTED / DELETED states | State indicators in Home view |
| State transitions and triggers | UI actions for archive/delete |
| Sidebar identity and refresh contract | Differentiated sidebar rendering |
| Naming conventions | Auto-titling behavior |
| Calendar day boundary | Day-change detection logic |
| API query parameters (`?state=`) | Frontend API calls with correct filters |

**Sequencing**: Spec first (#858), then implementation (#715). This spec should be approved before #715 work begins.

## Appendix B: Migration Considerations

### Database Changes

1. Add `lifecycle_state` VARCHAR(20) DEFAULT 'active' to `conversations` table
2. Add `archived_at` TIMESTAMP nullable to `conversations` table
3. Add `deleted_at` TIMESTAMP nullable to `conversations` table
4. Add `ConversationLifecycleState` enum to `services/shared_types.py`
5. Backfill: `UPDATE conversations SET lifecycle_state = 'active' WHERE is_active = TRUE`
6. Update `list_for_user()` query to filter by `lifecycle_state` instead of `is_active`

### API Changes

1. Add `state` query parameter to `GET /api/v1/conversations` (filter by lifecycle_state)
2. Add `PATCH /api/v1/conversations/{id}/state` for state transitions (archive, reactivate)
3. Change `DELETE /api/v1/conversations/{id}` to soft-delete (set lifecycle_state=DELETED)
4. Add search endpoint or `q` parameter to conversations list

### Backward Compatibility

- `is_active` remains as a computed property during migration: `is_active = (lifecycle_state == ACTIVE)`
- Existing API consumers that don't pass `?state=` get default behavior (ACTIVE only, matching current `is_active=True` filter)
- No breaking changes to frontend until #715 implements the new sidebar differentiation

## Appendix C: Source Documents

| Document | Path |
|----------|------|
| Research Report | `dev/2026/02/28/858-conversation-lifecycle-research.md` |
| CXO Memo | `mailboxes/lead/read/memo-from-cxo-to-ppm-lead-conversation-lifecycle-2026-02-28.md` |
| PPM Memo | `mailboxes/lead/read/memo-ppm-conversation-lifecycle-response-2026-02-28.md` |
| Entity Lifecycle Guide | `docs/internal/architecture/current/lifecycle-experience-guide.md` |
| ADR-050: Graph Model | `docs/internal/architecture/current/adrs/adr-050-conversation-as-graph-model.md` |
| ADR-054: Cross-Session Memory | `docs/internal/architecture/current/adrs/adr-054-cross-session-memory-architecture.md` |
| PDR-002: Conversational Glue v3 | `docs/internal/planning/conversational-glue/PDR-002-conversational-glue-v3.md` |
| PDR-101: Multi-Entity Conversation | `docs/internal/product/pdr/PDR-101-multi-entity-conversation.md` |
| MultiChat PRD v1.0 | `external/ted-multichat/multichat_prd_v1.md` |
| Issue #715 | MUX-HOME-CONVERSATIONS-LIFECYCLE (M2) |
| Issue #840 | BUG: Conversation not appearing in history sidebar |
| Issue #857 | Auth token management |

---

*Draft v1 — March 1, 2026*
*Draft v1.1 — March 1, 2026 (Architect R1-R4 revisions, PPM T14 note)*
*Prepared by Lead Developer*
*Approved by: Chief Architect (with revisions, applied), PPM*
