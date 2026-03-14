# MUX Objects & Views Discovery Report (#706)

**For**: PM (xian)
**Date**: 2026-03-14
**Purpose**: Inventory of existing domain objects, lifecycle states, views, and documentation — building on existing MUX vision rather than recreating.

---

## Executive Summary

Piper Morgan has **rich, well-documented MUX infrastructure** already in place. The philosophical vision (ADR-045), implementation protocols (ADR-055), 302 unit tests, and a full `services/mux/` module are all implemented. The gap is not in infrastructure — it's in **connecting domain objects to that infrastructure** and building the views that surface lifecycle state to users.

Currently:
- **4 domain objects** have lifecycle fields (`Feature`, `WorkItem`, `Todo`, `Project`)
- **1 domain object** has its own lifecycle state machine (`Conversation`)
- **2 domain objects** have specialized state machines (`StandupConversation`, `PortfolioOnboardingSession`)
- **3 HTML views** exist (standup, learning dashboard, personality preferences)
- **27 route modules** serve various domain objects
- **0 views** currently surface MUX lifecycle state to users

---

## Part 1: Existing MUX Documentation & Vision

### Core Philosophy (ADR-045: Object Model)
- **Grammar**: "Entities experience Moments in Places"
- **Ownership**: NATIVE (Piper's Mind), FEDERATED (Piper's Senses), SYNTHETIC (Piper's Understanding)
- **Lifecycle**: 8-stage state machine — EMERGENT → DERIVED → NOTICED → PROPOSED → RATIFIED → DEPRECATED → ARCHIVED → COMPOSTED
- **Anti-flattening principle**: 40+ tests prevent reducing rich concepts to mechanical schemas

### Implementation Spec (ADR-055: Object Model Implementation)
- `@runtime_checkable` Protocol pattern for role fluidity
- `EntityProtocol`, `MomentProtocol`, `PlaceProtocol`
- `Situation` context manager, `Perception` dataclass, 8 lens implementations
- Module: `services/mux/` — fully implemented Phase 1

### Key Design Principles (from existing docs)
1. **Experience framing required** — never raw data, always "You have 3 meetings today" not `{"meetings": 3}`
2. **Composting as transformation** — nothing disappears, it becomes wisdom
3. **Trust-gated surfacing** — learnings surface based on trust level (Stage 1-4)
4. **Role fluidity** — same object can be Entity AND Place (e.g., Team)
5. **Spiral lifecycle** — each cycle carries learning from previous cycles

### Existing Documentation Map

| Document | Location | Coverage |
|----------|----------|----------|
| Object Model Philosophy | `docs/internal/architecture/current/adrs/adr-045-object-model.md` | Core grammar, ownership, lifecycle stages |
| Implementation Spec | `docs/internal/architecture/current/adrs/adr-055-object-model-implementation.md` | Protocols, perception, lenses |
| Composting Architecture | `docs/internal/architecture/current/composting-learning-architecture.md` | Full pipeline spec (not yet implemented) |
| Feature-Object Map | `docs/internal/architecture/current/feature-object-model-map.md` | 16 features mapped to grammar |
| Consciousness Philosophy | `docs/internal/architecture/current/consciousness-philosophy.md` | The "why" behind the grammar |
| Consciousness Anti-Patterns | `docs/internal/architecture/current/consciousness-anti-patterns.md` | What NOT to do |
| Learning UX Design | `docs/internal/design/mux/MUX-VISION-LEARNING-UX-updated.md` | How learning surfaces to users |
| Insight Surfacing Rules | `docs/internal/design/mux/insight-surfacing-rules.md` | Pull/Passive/Push modes |
| MUX Tech Phase Specs | `docs/internal/design/mux/issue-MUX-TECH-PHASE*.md` | 4 phase implementation plans |
| Patterns 050-054 | `docs/internal/architecture/current/patterns/` | Morning Standup reference implementation |

### MUX Module Implementation (`services/mux/`)

| Module | What It Does | Test Count |
|--------|-------------|------------|
| `protocols.py` | EntityProtocol, MomentProtocol, PlaceProtocol | 101 |
| `situation.py` | Situation context manager | (included above) |
| `perception.py` | Perception, PerceptionMode | (included above) |
| `lifecycle.py` | LifecycleState enum (8 stages) | 69 |
| `lenses/` | 8 lens implementations | (included in 101) |
| `metadata.py` | 6 universal dimensions | 67 |
| `ownership.py` | Native/Federated/Synthetic | 25 |
| Anti-flattening tests | Consciousness preservation | 40 |
| **Total** | | **302** |

---

## Part 2: Domain Object Inventory

### Objects WITH Lifecycle Fields

These domain models already have `lifecycle_state: Optional[LifecycleState]` fields:

| Object | File:Line | Status Field | Lifecycle Field | `to_dict()` | Ownership |
|--------|-----------|-------------|-----------------|-------------|-----------|
| **Feature** | `models.py:203` | `status: str = "draft"` | `lifecycle_state` + `lifecycle_history` | Yes (includes lifecycle) | NATIVE |
| **WorkItem** | `models.py:263` | `status: str = "open"` | `lifecycle_state` + `lifecycle_history` | Yes (includes lifecycle) | FEDERATED |
| **Todo** | `models.py:1374` | `status: str = "pending"` | `lifecycle_state` | Yes | NATIVE |
| **Project** | `models.py:422` | (none) | `lifecycle_state` | Yes | NATIVE |

### Objects WITH Their Own State Machines

These have dedicated lifecycle enums, not the MUX LifecycleState:

| Object | File:Line | State Field | States | Ownership |
|--------|-----------|-------------|--------|-----------|
| **Conversation** | `models.py:1607` | `lifecycle_state: ConversationLifecycleState` | ACTIVE, PAUSED, RESOLVED, ARCHIVED | NATIVE |
| **StandupConversation** | `models.py:1697` | `state: StandupConversationState` | INITIATED, GATHERING, ANALYZING, PRESENTING, COMPLETE | NATIVE |
| **PortfolioOnboardingSession** | `models.py:1756` | `state: PortfolioOnboardingState` | INITIATED, GATHERING, CONFIRMING, COMPLETE | NATIVE |
| **Task** | `models.py:537` | `status: TaskStatus` | PENDING, IN_PROGRESS, COMPLETED, FAILED | NATIVE |
| **Workflow** | `models.py:580` | `status: WorkflowStatus` | PENDING, IN_PROGRESS, COMPLETED, FAILED | NATIVE |

### Objects WITHOUT Lifecycle (Potential Candidates)

| Object | File:Line | Key Fields | Notes |
|--------|-----------|------------|-------|
| **Product** | `models.py:185` | name, vision, strategy | Container for Features — may need lifecycle |
| **Stakeholder** | `models.py:249` | name, role, influence_level | Person — different lifecycle pattern |
| **Document** | `models.py:753` | (analysis model) | Analysis artifact, not persistent object |
| **List** | `models.py:1250` | name, items | Collection — could benefit from lifecycle |
| **ListItem** | `models.py:1338` | content, list_id | Child of List |
| **KnowledgeNode** | `models.py:1179` | content, node_type | Graph element |
| **KnowledgeEdge** | `models.py:1208` | source, target, relation | Graph relation |
| **Place** | `models.py:1046` | name, atmosphere | Already a MUX concept |
| **SpatialObject** | `models.py:960` | name, dimensions | Spatial system |

### Infrastructure Objects (Not Lifecycle Candidates)

| Object | Purpose |
|--------|---------|
| `RequestContext` | Per-request state |
| `ShareRole`, `SharePermission` | Access control |
| `ProjectIntegration` | Integration config |
| `Repository`, `ProjectRepositoryLink` | Git integration |
| `Event`, `FeatureCreated`, `InsightGenerated` | Domain events |
| `UploadedFile`, `FileTypeInfo` | File handling |
| `ValidationResult`, `AnalysisResult` | Analysis output |
| `TrustEvent`, `UserTrustProfile` | Trust system |

---

## Part 3: Views & Templates

### Existing HTML Views (Assets)

| View | File | Domain Objects | Lifecycle Visible? |
|------|------|---------------|-------------------|
| Morning Standup | `web/assets/standup.html` | StandupConversation | No (uses chat UI) |
| Learning Dashboard | `web/assets/learning-dashboard.html` | Insights, Learnings | No |
| Personality Preferences | `web/assets/personality-preferences.html` | Preference profile | No |

### Existing Templates (49 pages + 20+ components)

**Core Pages**: login, home, setup, todos, projects, project_detail, work_items, documents, files, lists, insights, standup, integrations, learning-dashboard, personality-preferences, privacy-settings, plus settings pages (github, slack, notion, calendar, projects, account, advanced)

**Lifecycle Components**: None exist yet. (The agent inventory mentioned `lifecycle_indicator.html`, `lifecycle_detail.html`, `lifecycle_notification.html` but these appear to be from design specs, not implemented files.)

**Other Relevant Components**: insight_card, insight_controls, reflection_summary, document_window, place_window, preference_suggestion, chat-widget, chat-inline, command_palette, greeting_context, channel_continuity, history_sidebar

### API Route Modules (27 total)

| Route Module | Domain Object(s) | CRUD | Lifecycle Ops |
|-------------|-------------------|------|--------------|
| `projects.py` | Project, Integration | Full CRUD + sharing | None |
| `todos.py` | Todo | Full CRUD + sharing | None |
| `conversations.py` | Conversation | CRUD + state update | `PATCH /{id}/state` |
| `work_items.py` | WorkItem | CRUD | None |
| `lists.py` | List, ListItem | CRUD | None |
| `documents.py` | Document | Analyze, search, summarize | None |
| `files.py` | UploadedFile | Upload, list, delete | None |
| `standup.py` | StandupConversation | Start, process | State transitions via chat |
| `knowledge_graph.py` | KnowledgeNode, Edge | CRUD | None |
| `learning.py` | Learnings | Read | None |
| `preferences.py` | Preferences | CRUD | None |
| `personality.py` | Personality profile | CRUD | None |
| `auth.py` | User | Login, logout, profile | None |
| `health.py` | System | Health checks | N/A |
| `intent.py` | Intent, Workflow | Process, status | None |
| `feedback.py` | Feedback | Submit, list | None |
| `integrations.py` | Integration health | Check | None |
| `repositories.py` | Repository | CRUD | None |
| `settings_integrations.py` | Settings | CRUD | None |
| `setup.py` | System setup | Initial config | None |
| `admin.py` | System | Monitoring | N/A |
| `api_keys.py` | API keys | CRUD | None |
| `ui.py` | UI elements | Serve | N/A |
| `debug.py` | Debug | Diagnostic | N/A |
| `loading_demo.py` | Demo | Demo | N/A |
| `conversation_context_demo.py` | Demo | Demo | N/A |

---

## Part 4: Gap Analysis

### Gap 1: Lifecycle State Not Surfaced in Any View
Four objects have `lifecycle_state` fields but **no view shows this to users**. No lifecycle UI components have been built yet.

### Gap 2: No Lifecycle Transition UI
`Conversation` has a `PATCH /{id}/state` endpoint, but no other object has API endpoints for lifecycle transitions. Feature, WorkItem, Todo, and Project lifecycle fields exist but can't be changed via API.

### Gap 3: Dual State Systems
Several objects have BOTH a domain-specific `status` field AND a MUX `lifecycle_state` field (Feature: draft/status + lifecycle_state; WorkItem: open/status + lifecycle_state; Todo: pending/status + lifecycle_state). The relationship between these is undefined. Which is authoritative?

### Gap 4: Conversation Has Its Own Lifecycle
`Conversation` uses `ConversationLifecycleState` (ACTIVE/PAUSED/RESOLVED/ARCHIVED) rather than the MUX `LifecycleState` (8-stage). Is this intentional? Should it map to the MUX lifecycle or remain independent?

### Gap 5: No Object Discovery/Catalog UI
There's no view where users can browse all objects, filter by lifecycle state, or see the "Objects in Places" grammar rendered visually.

### Gap 6: Composting Pipeline Not Implemented
Architecture doc exists (`composting-learning-architecture.md`) but no implementation. Objects can reach ARCHIVED/COMPOSTED state but nothing extracts learnings from them.

---

## Part 5: Decisions Needed (Collaborative Work)

These require PM input — they're design decisions, not implementation tasks:

### Decision 1: Status vs. Lifecycle — Which is authoritative?
Feature has both `status: "draft"` and `lifecycle_state: EMERGENT`. When a Feature moves from "draft" to "active", does lifecycle_state also change? Or are they independent dimensions?

**Options**:
- A) Lifecycle subsumes status (remove status, use lifecycle for everything)
- B) Status is domain-specific, lifecycle is cross-cutting (both coexist, different purposes)
- C) Status maps to lifecycle (status changes trigger lifecycle transitions)

### Decision 2: Which objects get MUX lifecycle treatment?
Current candidates with lifecycle fields: Feature, WorkItem, Todo, Project.
Objects that might benefit: Product, List, Conversation (convert from custom to MUX lifecycle?).
Objects that probably shouldn't: infrastructure objects, events, analysis results.

### Decision 3: What views do we need?
Possibilities:
- Object catalog (browse by type, filter by lifecycle state)
- Lifecycle timeline (visualize an object's journey through stages)
- Composting view (objects approaching end-of-life, extraction of learnings)
- Per-object lifecycle badge (add lifecycle indicators to existing views)

### Decision 4: Conversation lifecycle alignment
Keep `ConversationLifecycleState` (ACTIVE/PAUSED/RESOLVED/ARCHIVED) separate from MUX lifecycle? Or map it?
- ACTIVE → RATIFIED?
- PAUSED → DEPRECATED?
- RESOLVED → ARCHIVED?
- Archived → COMPOSTED?

### Decision 5: Priority ordering
Which objects get lifecycle views first? Suggested priority based on user value:
1. **Project** — users interact with this most
2. **Todo** — visible in daily workflow
3. **Feature** — PM workflow
4. **WorkItem** — federated from GitHub
5. **Conversation** — already has state management

---

## Part 6: What Exists vs. What's Needed

| Layer | Exists | Needs Work |
|-------|--------|------------|
| Philosophy & vision | Complete (ADR-045, ADR-055) | — |
| Protocols & grammar | Complete (services/mux/) | — |
| Lifecycle enum & stages | Complete (8 stages) | — |
| Anti-flattening tests | Complete (40+ tests) | — |
| Domain model lifecycle fields | Partial (4 of ~10 objects) | Decide which others get lifecycle |
| Lifecycle transition API | Minimal (Conversation only) | Add transition endpoints for other objects |
| Lifecycle views/UI | None | Build components and integrate into page templates |
| Status↔Lifecycle mapping | Undefined | Design decision needed |
| Composting pipeline | Architecture only | Implementation (Phase 4) |
| Object catalog/discovery | None | Design + build |

---

_Report prepared: 2026-03-14_
_Issue: #706 MUX-OBJECTS-VIEWS_
_Building on: ADR-045, ADR-055, existing services/mux/ module, 302 passing tests_
