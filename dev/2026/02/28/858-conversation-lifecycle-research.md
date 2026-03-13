# Research Report: Conversation Lifecycle — Current State of Docs & Code

**Issue**: #858 — SPEC: Conversation lifecycle specification
**Prepared by**: Documentation Management Specialist
**Date**: February 28, 2026
**Purpose**: Inform CXO and PPM engagement on conversation lifecycle specification work

---

## Executive Summary

There is **no unified specification for conversation lifecycle** in the Piper Morgan codebase or documentation. The conversation system was built incrementally across 22+ issues by different agents over 7 weeks, producing a functional but fragile pipeline with no documented invariants, no state machine, and no end-to-end contract. This report synthesizes findings from four research tracks — entity lifecycle docs, MUX design docs, sidebar development history, and codebase audit — to paint a complete picture of what exists, what's missing, and what #858 should deliver.

**Key finding**: The entity lifecycle model (8 stages, EMERGENT through COMPOSTED) was designed for domain objects like features and work items. Conversations were explicitly identified as needing "a simpler lifecycle subset" (#715) but that subset was never defined. Meanwhile, the conversation system accumulated 22+ issues including 13 bug fixes, many addressing the same structural root cause: no specification.

**Additional finding (per PM direction)**: Ted Nadeau's MultiChat PRD v1.0 (927 lines) and ADR-050 define the accepted evolutionary path toward a graph-based conversation model with multi-participant support. The lifecycle spec must be designed with awareness of this trajectory — specifically, lifecycle states should attach to the conversation container (not the turn sequence), creation should not assume single-user ownership, and conversation boundaries should be defined in a way that accommodates future branching and forking. Section E details the compatibility analysis.

---

## Section A: Entity Lifecycle Documentation

### What Exists

The **Lifecycle Experience Guide** (`docs/internal/architecture/current/lifecycle-experience-guide.md`, implemented via #408, last updated Jan 22, 2026) defines an 8-stage lifecycle model:

| Stage | Experience Phrase | Meaning |
|-------|------------------|---------|
| EMERGENT | "I just noticed..." | Something forming, uncategorized |
| DERIVED | "I figured out from..." | Inferred from other information |
| NOTICED | "I'm aware of..." | Explicitly brought to attention |
| PROPOSED | "I think we should..." | Suggested for action |
| RATIFIED | "We're doing..." | Confirmed, in active use |
| DEPRECATED | "This used to be..." | Still exists but no longer active |
| ARCHIVED | "I remember when..." | Preserved for reference |
| COMPOSTED | "I learned that..." | Transformed into learning |

Implementation lives in `services/mux/lifecycle.py`. The model is designed for **domain objects** — features, work items, projects, tasks — things that Piper tracks on behalf of the user.

### The Conversation Gap

Issue **#715** (MUX-HOME-CONVERSATIONS-LIFECYCLE, still OPEN) explicitly recognizes the gap:

> "Conversations likely use a **simpler lifecycle** (RATIFIED, ARCHIVED, COMPOSTED) rather than full 8 stages."

The issue notes that conversations are **entities (hard objects)** with identity and persistence, not soft objects. ConversationTurns are **components** (part of conversation, not independent). Transcripts are **artifacts** (derived/exported forms).

But #715 is scoped as "Post-MUX MVP (before Beta)" and its checklist is entirely unchecked:
- [ ] Determine appropriate lifecycle subset for Conversations
- [ ] Design conversation state display in Home view
- [ ] Wire indicators to `home.html` template
- [ ] Consider conversation naming conventions

**Assessment**: The lifecycle framework exists and is well-designed, but its application to conversations is explicitly deferred. The only lifecycle state a conversation can currently have is `is_active: bool`.

---

## Section B: MUX Design Docs Regarding Conversations

### Documents Found

| Document | Path | Status | Relevance |
|----------|------|--------|-----------|
| ADR-050: Conversation as Graph Model | `adrs/adr-050-conversation-as-graph-model.md` | Accepted Jan 21, not implemented | High — defines conversation structure vision |
| ADR-049: Hierarchical Intent Architecture | `adrs/adr-049-conversational-state-hierarchical-intent.md` | Accepted | Medium — state management within conversations |
| ADR-054: Cross-Session Memory Architecture | `adrs/adr-054-cross-session-memory-architecture.md` | Accepted | Medium — defines 3-layer persistence model |
| ADR-048: ServiceContainer Lifecycle | `adrs/adr-048-service-container-lifecycle.md` | Accepted | Low — infrastructure, not conversation lifecycle |
| PDR-002: Conversational Glue v3 | `conversational-glue/PDR-002-conversational-glue-v3.md` | Active | High — defines Discovery/Context/Proactivity |
| PDR-101: Multi-Entity Conversation | `pdr/PDR-101-multi-entity-conversation.md` | Draft | Medium — entity participant model |
| PM-034: Conversation API | (referenced in PDR-002) | Active | Medium — documents existing API |
| Conversational Glue Implementation Guide | `conversational-glue/conversational-glue-implementation-guide.md` | DRAFT v1, Feb 1 2026 | High — 1,048 lines, most comprehensive |

### Maturity Assessment

| Capability | Design Status | Code Status |
|------------|--------------|-------------|
| Linear turn model | Documented | Implemented ✅ |
| Graph model (typed nodes/edges) | ADR-050 accepted | Not implemented ⏳ |
| Process-level state | ADR-049 accepted | ProcessRegistry implemented ✅ |
| Turn-level context window | PDR-002 | 10-turn ConversationContext ✅ |
| Reference resolution | PDR-002 | Implemented ✅ |
| Entity tracking in conversations | PDR-101 | Not implemented ⏳ |
| Hierarchical memory (3 layers) | ADR-054 | Layer 1 only ✅ |
| Confidence tiers | PDR-002 | Not implemented ⏳ |
| Offer tracking | PDR-002 | WorkflowOfferService ✅, contextual offers via #852 ✅ |
| Conversation lifecycle states | #715 scoped | Not implemented ❌ |

### Key Observations

1. **ADR-050** envisions conversations as graphs with typed nodes (MESSAGE, TASK, WHISPER, DECISION, QUESTION) and explicit links (REPLY, REFERENCE, BLOCKING). Phase 0 = "no changes yet." This is the long-term vision but provides no guidance for current implementation.

2. **PDR-002** defines three components — Discovery (what's relevant?), Context (what should Piper know?), and Proactivity (what should Piper do?) — but doesn't address conversation birth, death, archival, or naming.

3. **The Implementation Guide** (1,048 lines, DRAFT v1) is the most comprehensive document, covering the full conversational glue system, but is focused on *within-conversation* behavior, not *conversation lifecycle*.

4. **No document defines**: When a conversation starts. When it ends. What happens to it over time. How it's named. What states it can be in. When it should be archived. What "inactive" means operationally.

**Assessment**: MUX design docs are rich on *what happens inside a conversation* but silent on *the conversation as an entity with a lifecycle*. This is the exact gap #858 identifies.

---

## Section C: Sidebar Development History

### Three Waves of Development

The conversation sidebar has generated **22+ issues** across three development waves spanning 7 weeks.

**Wave 1: Initial Build (Jan 10-18)** — 11 issues

Epic #314 (CONV-UX-PERSIST) spawned #563-#566 as a rapid build. Four child issues opened and closed on Jan 11 alone. Then came 6 bug fixes over the next week: #574 (wrong lookup method), #581 (chat ignoring sidebar selection), #583 (replies not persisting on refresh), #587 (wrong date grouping), #598 (auto-titling), #604 (editable titles).

**Wave 2: Alpha Testing Regression (Jan 28 — Feb 6)** — 10 issues

Alpha tester discovered sidebar completely non-functional. Issues #726, #729, #731, #732, #735 addressed the immediate breakage. Then #780 (wrong API endpoint), #785-#788 addressed a second round of failures.

Key finding: The right History sidebar component (`history_sidebar.html`) was built in #425 with 56 passing unit tests but `HistorySidebar.mount()` was never called. Issues #729 and #735 existed solely to wire up what was already built.

**Wave 3: Systemic Failures (Feb 21-28)** — 3 issues

Issue #840 revealed three *compounding* auth failures that made the history sidebar non-functional for ALL users:
1. `fetchHistoryConversations()` lacked `credentials: 'include'`
2. `ensure_conversation_exists()` used `user_id or "unknown"` fallback
3. Silent token expiry let users chat while auth was lapsed

This was the investigation that led to filing #858.

### Recurring Patterns

| Pattern | Description | Occurrences |
|---------|-------------|-------------|
| **Independent systems** | `chat.js` and sidebar tracked conversation identity separately with no shared state | #574, #581, #583, #731 |
| **Partial fixes** | Bug fixed in one endpoint but not others (e.g., `Z` suffix for timestamps) | #587, #788 |
| **Masked by testing** | Page refresh during testing hid real-time update failures | #731 |
| **Built but not wired** | Component existed with passing tests but was never mounted | #729, #735 |
| **Silent failure** | `try/except` blocks swallowed errors, making conversations invisible | #840 |
| **Two-sidebar identity crisis** | Left (#565) and right (#425) sidebars show same data from same endpoint | #785, #786 |

### The Structural Root Cause

From the #840 investigation (Lead Developer, Feb 25):

> "This feature was built incrementally across 11+ issues without a unifying specification. Each issue added a capability but no issue defined the end-to-end contract."

From the PPM (Feb 1):

> "Right sidebar was designed for richer 'User History' but currently just shows conversations. Both sidebars now show essentially the same data with different UI. The distinction between 'conversation list' and 'history archive' collapsed in implementation."

**Assessment**: The sidebar's chronic instability is a symptom, not the disease. The disease is the absence of a conversation lifecycle specification. Each bug fix addressed a symptom without establishing invariants, guaranteeing recurrence.

---

## Section D: Codebase Reality

### Conversation Domain Model

```python
# services/domain/models.py lines 1595-1629
@dataclass
class Conversation:
    id: str  # UUID
    user_id: UUID
    session_id: str
    title: str
    context: Dict[str, Any]
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    last_activity_at: Optional[datetime] = None
    mux_ownership: Optional[OwnershipMetadata] = None
```

No lifecycle state field. No status enum. The only state distinction is `is_active: bool`.

### Three Conversation Creation Paths

| Path | Trigger | File | Guarantees |
|------|---------|------|------------|
| **Explicit** | User clicks "+ New Chat" | `web/api/routes/conversations.py` POST `/api/v1/conversations` | Creates DB record immediately, returns ID to frontend |
| **Auto-create** | First message in intent handler | `ensure_conversation_exists()` in `repositories.py:1151-1194` | Creates if missing; **refuses without valid user_id** (post-#840 fix) |
| **Lazy ensure** | Before saving turns | Same function, different caller | Same guarantees as auto-create |

The `ensure_conversation_exists` function (post-#840 fix) now raises `ValueError` if `user_id` is missing. Before the fix, it silently fell back to `"unknown"`, creating orphaned conversations invisible to `list_for_user()`.

### ConversationTurn: Three Definitions

| File | Fields | Purpose |
|------|--------|---------|
| `services/domain/models.py` | Full dataclass: conversation_id, turn_number, user_message, assistant_response, intent, entities, references, timestamps, metadata | Persistence/database model |
| `services/intent_service/conversation_context.py` | Minimal: role, content | 10-turn sliding window for LLM context |
| `services/intent_service/conversation_aware.py` | Dict with intent_result fields | Intent processing intermediate |

This fragmentation means "conversation turn" means different things in different parts of the system with no mapping between representations.

### Conversations API

`web/api/routes/conversations.py` exposes:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/conversations` | GET | List conversations for user |
| `/api/v1/conversations` | POST | Create new conversation |
| `/api/v1/conversations/latest` | GET | Get most recent conversation |
| `/api/v1/conversations/{id}` | GET | Get single conversation |
| `/api/v1/conversations/{id}/title` | PATCH | Update title |
| `/api/v1/conversations/{id}/turns` | GET | Get turns for conversation |

No endpoint for archiving, deleting, or changing conversation state. No endpoint for conversation lifecycle transitions.

### ConversationContext: Two Definitions

| File | Class | Purpose |
|------|-------|---------|
| `services/intent_service/conversation_context.py` | `ConversationContext` | 10-turn sliding window with lens_stack, last_offer, pending_entity — rich in-conversation state |
| `services/intent_service/conversation_manager.py` | `ConversationContext` | Simpler version — conversation_id + list of turns |

Two classes with the same name serving different purposes in the same subsystem.

### Alembic Migration (Designed, Not Applied)

Migration `601_mux_multichat_phase0` was designed as part of ADR-050 but has **not been applied**. The database schema has no conversation lifecycle fields beyond `is_active`.

**Assessment**: The code reflects the incremental accretion pattern described in Section C. No state machine, no lifecycle states, fragmented representations of core concepts, and duplicate class names creating confusion.

---

## Section E: Multi-Entity Conversation Evolution Path (Ted Nadeau / MultiChat)

### Why This Matters for #858

Per PM direction, the conversation lifecycle spec must remain open to the evolutionary path defined by Ted Nadeau's MultiChat architecture (PDR-101, ADR-050, MultiChat PRD v1.0). This isn't about implementing multi-entity now — it's about not designing invariants today that block us tomorrow.

### Ted's Conversation Model

Ted's MultiChat PRD v1.0 (927 lines, `external/ted-multichat/multichat_prd_v1.md`) defines a conversation as a **graph of typed element nodes and element links**, not a linear sequence. Key structural concepts:

| Concept | Ted's Model | Our Current Model | Compatibility Risk |
|---------|------------|-------------------|-------------------|
| **Conversation container** | `conversation` table with `created_by` (entity = human or AI) | `Conversation` dataclass with `user_id` | **Medium** — `user_id` assumes single owner. Ted's model supports multiple participants with distinct `created_by`. |
| **Conversation elements** | Typed `element_node` (message, annotation, edit_proposal, task, question, answer, decision, rule, summary, domain-specific) | `ConversationTurn` (user_message + assistant_response) | **High** — Our turn model bakes in 1:1 alternation. Ted's model has independent typed nodes from any participant. ADR-050 already notes: "ConversationTurn is a shorthand for a message Node and its response Node linked by 'reply'." |
| **Relationships** | `element_link` with typed relationships (replies_to, answers, refutes, supports, variant_of, domain-specific) | None — turns are implicitly sequential | **High** — No relationship model exists. |
| **Participants** | Multiple humans + personal agents + facilitator agents per conversation | Single `user_id` per conversation | **High** — Single-user assumption is structural. |
| **Ordering** | LEXORANK for efficient reordering without renumbering | `turn_number` sequential integer | **Low** — LEXORANK is an implementation detail, not a lifecycle concern. |
| **Lifecycle** | Not defined (Ted's PRD focuses on structure, not lifecycle) | `is_active: bool` | **N/A** — This is the gap #858 fills. Ted's model needs lifecycle too. |
| **Views** | "One model, many views" — Timeline, Thread, Tasks, Questions, Agreements, Domain-specific | Single chronological view | **Low for lifecycle** — View invariance means lifecycle states work regardless of view projection. |
| **Versioning** | Immutable nodes preferred ("we don't care about storage") | Mutable turns, no version history | **Medium** — Lifecycle states should work with either versioning model. |

### Design Constraints for #858

Based on this analysis, the conversation lifecycle spec should:

1. **Not assume single-user conversations.** Even though we only support 1:1 today, lifecycle states like ARCHIVED and COMPOSTED should make sense for multi-participant conversations. Use "conversation owner" (or "created_by") language rather than "user" where possible. PDR-101 already establishes the Conversation Owner role.

2. **Not assume linear turns.** Lifecycle states should apply to the conversation *container*, not to the turn sequence inside it. Whether the conversation contains 50 linear turns or a 200-node graph, the lifecycle state is about the conversation as an entity.

3. **Not assume a single creation path.** Ted's model supports creating conversations programmatically (facilitator-initiated) and through participant action. Our three creation paths are a degenerate case of this. The lifecycle spec should document current paths but not enshrine them as the only paths.

4. **Be compatible with typed elements.** If a conversation contains typed nodes (tasks, decisions, questions), lifecycle transitions might eventually consider whether all tasks are closed, all questions answered, etc. The spec doesn't need to implement this, but shouldn't preclude it.

5. **Address "conversation scope" vs "conversation state".** Ted's model supports parallel conversations, branching, and forking. The lifecycle spec should define what constitutes a single conversation's boundary — this is important for both the current 1:1 model and the future multi-participant model.

### ADR-050 Migration Path Implications

ADR-050 defines four phases:
- **Phase 0 (Current)**: No changes — methodology continues as prototype
- **Phase 1 (Participant Mode)**: Add `parent_id` for threading, `ConversationLink` table
- **Phase 2 (Host Mode)**: Full `ConversationNode` model, multiple views, multi-participant
- **Phase 3 (Personal Agents)**: `WhisperNode`, per-participant context

The lifecycle spec should work cleanly at Phase 0 and Phase 1. It should be *extensible* to Phase 2 (e.g., lifecycle transitions might gain new triggers when multiple participants exist) without requiring redesign.

**Assessment**: The multi-entity evolution path is well-documented and thoughtfully designed. The lifecycle spec is a missing foundation piece that both the current system and the future graph model need. Designing it with awareness of the target architecture prevents us from building lifecycle invariants that we'd have to tear down at Phase 1.

---

## Gap Analysis: Design vs Code vs User Experience

| Aspect | Design Intent | Code Reality | User Experience |
|--------|--------------|--------------|-----------------|
| **Conversation states** | 3-state subset: RATIFIED, ARCHIVED, COMPOSTED (#715) | Binary: `is_active` bool | No visible state — conversations just appear and remain |
| **Conversation creation** | Single clear path (implied by PDR-002) | 3 paths, 1 documented | User clicks New Chat or just types — unclear which path fires |
| **Naming** | Lifecycle-aware naming (#715 scope) | Auto-title after first turn (#598) | Generic "Chat #x" until first message, then AI-generated title |
| **Archival** | Part of lifecycle (#715) | No archive mechanism | Conversations accumulate indefinitely |
| **Deletion** | Not mentioned in any doc | No delete endpoint | Users cannot remove conversations |
| **Auth boundary** | Not specified | Fixed post-#840 but no contract | Silent failures if auth expires |
| **Sidebar purpose** | Left = session switching, Right = Layer 2 archive | Both call same endpoint, show same data | Two identical-looking panels confuse users |
| **End of conversation** | Not defined | `is_active` flag, never set to False | Conversations never "end" |
| **Graph model** | ADR-050: typed nodes and edges | Linear turn sequence | Sequential chat — no branching, threading, or typed messages |

### The Central Gap

No document in the codebase answers these questions:
1. **When does a conversation begin?** (Three answers currently, none canonical)
2. **When does a conversation end?** (Never, currently)
3. **What states can a conversation be in?** (`is_active` = True or False, but False is never set)
4. **What happens to old conversations?** (Nothing — they accumulate)
5. **How does the sidebar know to refresh?** (It doesn't — page navigation triggers re-fetch)
6. **What's the auth contract?** (Post-#840: require valid user_id. Pre-#840: silently break)
7. **What distinguishes the two sidebars?** (Nothing, currently)

---

## Proposed Updated Description for #858

Based on this research (including the Section E review of Ted's MultiChat architecture per PM direction), the current #858 description accurately identifies the problem but underscopes the solution. The specification should also address lifecycle states (connecting to #715, currently in M2), the two-sidebar identity question, conversation naming, and evolutionary compatibility with the multi-entity conversation path (ADR-050, PDR-101, MultiChat PRD v1.0).

### Proposed Description (Revised with Multi-Entity Compatibility)

```markdown
## Description

**Component**: Conversation Persistence Pipeline + Lifecycle
**Related**: #840 (3 overlapping root causes from underspecification), #715 (lifecycle states for conversations, M2)
**Informs**: ADR-050 (graph model), PDR-002 (conversational glue), PDR-101 (multi-entity conversations)
**Evolutionary Path**: MultiChat PRD v1.0 (Ted Nadeau) — lifecycle spec must remain compatible

### Problem

The conversation system was built incrementally across 22+ issues over 7 weeks without
a unifying specification. Each issue added a capability but none defined the end-to-end
contract. Three waves of development (Jan 10-18, Jan 28-Feb 6, Feb 21-28) produced
13 bug fixes for the same structural root cause: no specification for how conversations
are born, live, and die.

Specific manifestations:
- **Three creation paths** with no documented invariants (explicit, auto-create, lazy ensure)
- **Two sidebar components** built from different design tracks (#565 left, #425 right) now showing identical data
- **No lifecycle states** — conversations have only `is_active: bool`, never set to False
- **No end-of-conversation concept** — conversations accumulate indefinitely with no archival
- **Three different ConversationTurn representations** across the codebase
- **Two ConversationContext classes** with the same name serving different purposes
- **Auth boundary discovered by accident** (#840) — no documented auth contract
- **Design docs rich on in-conversation behavior** (ADR-050, PDR-002) but silent on conversation-as-entity lifecycle

### What's Needed

A **Conversation Lifecycle Specification** (ADR or lightweight design doc) covering:

#### 1. Conversation State Machine
- Define lifecycle states for conversations (connecting to #715's proposed RATIFIED/ARCHIVED/COMPOSTED subset of the 8-stage entity lifecycle model)
- Document state transitions and triggers (e.g., what makes a conversation "archived"?)
- Define what `is_active` means operationally vs. future lifecycle states
- Address conversation naming conventions at each lifecycle stage (#715 scope item)
- **Evolutionary constraint**: States must apply to the conversation *container*, not the turn/node sequence inside it — ensuring compatibility with ADR-050's graph model where turns become typed nodes

#### 2. Creation Invariants
- Canonical documentation of each creation path (explicit, auto-create, lazy ensure)
- What each path guarantees (user_id, session_id, title, timestamps)
- When each path fires (user action vs. system action)
- Single source of truth for "how a conversation begins"
- **Evolutionary constraint**: Don't assume single-user creation. Use "conversation owner" / "created_by" language compatible with PDR-101's multi-participant model (Phase 2+)

#### 3. Auth Contract
- What happens when auth expires during a session
- Token refresh expectations for conversation endpoints (see #857)
- Whether intent endpoint should work unauthenticated
- How auth failures surface to user (not silently)

#### 4. Sidebar Identity & Refresh Contract
- Define the distinct purposes of left sidebar (conversation switching) and right sidebar (history/archive)
- What data each sidebar shows and how it differs
- When sidebars refresh (on message, navigation, timer, server-sent event?)
- Shared vs. distinct API endpoints
- **Evolutionary constraint**: Right sidebar's original design intent was Layer 2 of the Three-Layer Context Persistence Model (ADR-054) — a searchable archive that would eventually surface domain objects with lifecycle states. Spec should acknowledge this trajectory even if current implementation is simpler.

#### 5. Representation Consolidation (Inventory)
- Inventory the three ConversationTurn representations and document the mapping between them
- Inventory the two ConversationContext classes and clarify naming
- Determine which representations are canonical vs. derived
- **Evolutionary constraint**: ADR-050 establishes that "ConversationTurn is a shorthand for a message Node and its assistant response Node linked by 'reply'." The inventory should note which representations map cleanly to the graph model and which will need transformation.

#### 6. Conversation Scope & Boundary
- Define what constitutes a single conversation's boundary (important for both current 1:1 model and future multi-participant model)
- Address whether conversations can be forked, branched, or merged (even if answer is "not yet")
- Define the relationship between conversation and session (currently coupled via `session_id`)
- **Evolutionary constraint**: Ted's model supports parallel conversations with branching. The boundary definition should be extensible.

#### 7. Integration Test Coverage
- At least one test exercising: message → persist → sidebar refresh → conversation appears
- Test for auth expiry scenario: token expires → next action → user informed (not silent)
- Test for creation path consistency: each path produces equivalent Conversation records

### Research Basis

This specification is informed by a research report (Feb 28, 2026) covering:
- **Entity lifecycle docs**: lifecycle-experience-guide.md (8-stage model), #715 (conversation lifecycle subset — OPEN, M2)
- **MUX design docs**: ADR-050, ADR-049, ADR-054, PDR-002, PDR-101, conversational-glue-implementation-guide
- **Multi-entity evolution**: MultiChat PRD v1.0 (Ted Nadeau, 927 lines), ADR-050 migration phases
- **Sidebar history**: 22+ issues across 3 development waves, 13 bug fixes, sidebar archaeology report (Feb 1)
- **Codebase audit**: Conversation model, 3 creation paths, API routes, ConversationTurn × 3, ConversationContext × 2

Full report: `dev/2026/02/28/858-conversation-lifecycle-research.md`

### Acceptance Criteria

- [ ] Conversation state machine defined (states, transitions, triggers)
- [ ] Each creation path documented with invariants
- [ ] Auth failure contract specified
- [ ] Sidebar identity and refresh contract defined
- [ ] Representation inventory completed (ConversationTurn × 3, ConversationContext × 2)
- [ ] Conversation scope and boundary defined
- [ ] Multi-entity compatibility reviewed (spec checked against ADR-050 phases and PDR-101)
- [ ] At least one integration test for end-to-end path
- [ ] Relationship to #715 clarified — spec feeds #715 implementation (sequential: spec first, then wiring)

### Priority

Not blocking M0. Prevents recurrence of #840-class integration boundary bugs and establishes
foundation for ADR-050 graph model and #715 lifecycle wiring. Once spec is complete,
#715 (currently M2) may be a candidate for promotion to M0.

### Relationships

- **Feeds into**: #715 (MUX-HOME-CONVERSATIONS-LIFECYCLE, M2) — spec defines states, #715 implements them in UI
- **Informed by**: #840 investigation, sidebar archaeology report (Feb 1), MultiChat PRD v1.0
- **Prerequisite for**: ADR-050 Phase 1 implementation, PDR-101 multi-entity support
- **Compatible with**: Ted Nadeau's graph-based conversation model (element_node + element_link)
- **Adjacent**: #857 (auth token management)

---

_Filed: Feb 25, 2026 — updated Feb 28, 2026 with research findings_
_Research report: `dev/2026/02/28/858-conversation-lifecycle-research.md`_
```

---

## Recommendations for CXO/PPM Engagement

1. **#858 → #715 sequencing (PM-confirmed)**: #858 writes the spec, #715 (currently M2) implements the lifecycle states in the UI. Sequential: spec first, then wiring. Once the spec is complete, PM will evaluate whether #715 should be promoted from M2 to M0.

2. **Two-sidebar question**: The CXO and PPM should decide whether the two sidebars should remain as distinct components with differentiated purposes, or merge into one. Currently they are functionally identical, and the PPM identified this as "classic flattening" on Feb 1. The right sidebar's original intent (Layer 2 archive with domain object surfacing) is architecturally valuable but not reflected in implementation. This decision affects the sidebar refresh contract in Section 4 of the spec.

3. **Naming conventions**: Issue #715 raised conversation naming as a design consideration (unclear topic → "Chat #x", spawned → inherit parent name, topic clarified → Piper renames). This should be part of the lifecycle spec as naming is lifecycle-stage-dependent behavior.

4. **Multi-entity compatibility (PM-directed)**: Ted Nadeau's MultiChat PRD v1.0 defines a rich graph model (element_node + element_link) that is the accepted future direction (ADR-050). The lifecycle spec must remain open to this evolutionary path. Specific constraints: (a) lifecycle states on the conversation container not the turn sequence, (b) "conversation owner" language not "user", (c) creation paths should be extensible, (d) boundary definitions should accommodate future branching/forking. See Section E for detailed compatibility analysis.

5. **The 22-issue pattern**: The conversation subsystem generated 22+ issues, 13 of them bugs, across 3 development waves over 7 weeks. Each wave fixed symptoms without establishing invariants, guaranteeing recurrence. This is the strongest argument for "spec first, then build" and should feature prominently in the CXO/PPM discussion. The #840 investigation that surfaced this pattern (Feb 25) led directly to filing #858.

6. **Representation cleanup opportunity**: The codebase has 3 different `ConversationTurn` representations and 2 different classes named `ConversationContext`. The spec's representation inventory (Section 5) will expose which are canonical and which are drift. ADR-050 already provides the mapping: "ConversationTurn is a shorthand for a message Node and its response Node linked by 'reply'." This alignment work reduces technical debt while preparing the codebase for the graph model migration.

7. **Conversation scope/boundary question**: Neither the current code nor the design docs define what constitutes a single conversation's boundary. When does one conversation end and another begin? Can conversations fork? This question matters now (for archival/lifecycle transitions) and matters more in the multi-entity future (where parallel conversations with branching are part of Ted's model). The CXO and PPM should address this in the spec.

---

## Appendix: Source Documents Referenced

| Document | Path | Status |
|----------|------|--------|
| Lifecycle Experience Guide | `docs/internal/architecture/current/lifecycle-experience-guide.md` | Implemented (#408) |
| ADR-050: Conversation as Graph Model | `docs/internal/architecture/current/adrs/adr-050-conversation-as-graph-model.md` | Accepted, not implemented |
| ADR-049: Hierarchical Intent Architecture | `docs/internal/architecture/current/adrs/adr-049-conversational-state-hierarchical-intent.md` | Accepted |
| ADR-054: Cross-Session Memory | `docs/internal/architecture/current/adrs/adr-054-cross-session-memory-architecture.md` | Accepted |
| ADR-046: Moment.type Agent Architecture | `docs/internal/architecture/current/adrs/adr-046-moment-type-agent-architecture.md` | Proposed |
| PDR-002: Conversational Glue v3 | `docs/internal/planning/conversational-glue/PDR-002-conversational-glue-v3.md` | Active |
| PDR-101: Multi-Entity Conversation | `docs/internal/product/pdr/PDR-101-multi-entity-conversation.md` | Draft v2 |
| MultiChat PRD v1.0 (Ted Nadeau) | `external/ted-multichat/multichat_prd_v1.md` | v1.0 |
| Sidebar Archaeology Report | `docs/internal/design/audits/2026-02-history-sidebar-design-archaeology.md` | Complete |
| Conversational Glue Implementation Guide | `docs/internal/planning/conversational-glue/conversational-glue-implementation-guide.md` | DRAFT v1 |
| Domain Models Reference | `docs/internal/architecture/current/models/domain-models.md` | Active |
| Issue #715 | MUX-HOME-CONVERSATIONS-LIFECYCLE | OPEN (M2) |
| Issue #840 | BUG: Conversation not appearing in history sidebar | CLOSED |
| Issue #857 | Auth token management | Reference |

---

*Research compiled February 28, 2026*
*Revised with multi-entity compatibility analysis per PM direction (Section E added)*
*Sources: 14 architecture/design documents, 22+ GitHub issues, session logs, codebase symbols via Serena, MultiChat PRD v1.0*
