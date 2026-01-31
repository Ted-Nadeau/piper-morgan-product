# Views & Objects Roadmap

**Issue**: #706 MUX-OBJECTS-VIEWS
**Created**: 2026-01-27
**Authors**: PM (xian), Lead Developer (Claude)

---

## Purpose

This document maps Piper's domain objects to UI views, establishing where lifecycle indicators should appear and prioritizing implementation work.

---

## Object Classification

### Hard Objects (Entities with Lifecycle)

Objects that evolve through states and benefit from lifecycle treatment.

| Object | Has lifecycle_state | to_dict() wired | Current View | Lifecycle UI |
|--------|---------------------|-----------------|--------------|--------------|
| **WorkItem** | Yes (#685) | Yes (#685) | None | Planned (MUX) |
| **Feature** | Yes (#685) | Yes (#705) | None | Deferred (needs Product modeling) |
| **Project** | No | Yes | Projects | Planned (MUX) |
| **Todo** | No (has status) | Yes | Todos | Planned (MUX) |
| **Document** | No | Yes | Documents | Deferred (needs File/Doc modeling) |
| **List** | No | Yes | Lists | Deferred |
| **ListItem** | No | Yes | Lists | Deferred |
| **Conversation** | No | Yes | Home | Deferred |

### Soft Objects (No Lifecycle)

Objects that are outputs, snapshots, or don't evolve.

| Object | Reason | Current View |
|--------|--------|--------------|
| File | Static upload | Files |
| Insight | Surfacing modes, not lifecycle (CXO/PPM decision) | Insights |
| StandupResult | Synthesized output | Standup |
| Perception | Ephemeral lens output | None |
| AnalysisResult | Derived snapshot | Learning Dashboard |

### Infrastructure Objects

System scaffolding, not user-facing content.

| Object | Purpose |
|--------|---------|
| RequestContext | Session context |
| SharePermission | Access control |
| Workflow | Process orchestration |
| Integration configs | External service settings |

---

## View Inventory

### Existing Views

| View | Template | Primary Objects | Lifecycle Treatment |
|------|----------|-----------------|---------------------|
| **Todos** | `todos.html` | Todo | MUX Sprint |
| **Projects** | `projects.html` | Project | MUX Sprint |
| **Documents** | `documents.html` | Document | Post-MUX (needs modeling) |
| **Lists** | `lists.html` | List, ListItem | Post-MUX |
| **Files** | `files.html` | File | None (soft object) |
| **Insights** | `insights.html` | Insight | None (surfacing, not lifecycle) |
| **Home** | `home.html` | Conversation | Post-MUX |
| **Standup** | `standup.html` | StandupResult | None (artifact) |
| **Learning Dashboard** | `learning-dashboard.html` | Metrics | None (aggregations) |

### New Views (Planned)

| View | Primary Objects | Priority | Rationale |
|------|-----------------|----------|-----------|
| **Work Items** | WorkItem | MUX Sprint | Completes loop for #685 |
| **Project Detail** | Project, WorkItem | MUX Sprint | Shows lifecycle in context |
| **Document Viewer** | Document | Post-MUX | Needs File/Document modeling |
| **Features** | Feature | Post-MVP | Needs Product concept modeling |

---

## Implementation Roadmap

### MUX Sprint (P3 Extended)

| # | Item | Type | Objects | Effort | Issue |
|---|------|------|---------|--------|-------|
| 1 | Todos lifecycle UI | Wire existing | Todo | Small | #708 |
| 2 | Projects lifecycle UI | Wire existing | Project | Small | #709 |
| 3 | Work Items View | New view | WorkItem | Medium | #710 |
| 4 | Project Detail View | New view | Project, WorkItem | Medium | #711 |

### Post-MUX MVP (Before Beta)

| # | Item | Type | Objects | Dependencies | Issue |
|---|------|------|---------|--------------|-------|
| 5 | Document Viewer | New view | Document | File/Document modeling | #712 |
| 6 | Documents lifecycle UI | Wire existing | Document | #712 complete | #713 |
| 7 | Lists lifecycle UI | Wire existing | List, ListItem | Staleness concept | #714 |
| 8 | Home/Conversations lifecycle | Wire existing | Conversation | Simpler lifecycle model | #715 |

### Post-MVP (Future)

| # | Item | Type | Objects | Dependencies | Issue |
|---|------|------|---------|--------------|-------|
| 9 | Features View | New view | Feature | Product concept modeling | #716 |
| 10 | Product modeling | Concept work | Product | Architecture decision | #717 |

---

## Key Principles

### Lifecycle Optionality

When an object has its own simple state machine (like Todo's `pending → completed`), the 8-stage lifecycle is **optional and additive**, not a replacement.

- Default: Object uses its native status/state
- Optional: `lifecycle_state: Optional[LifecycleState] = None`
- UI: Show lifecycle indicator only when `lifecycle_state` is present

### Hard vs Soft Objects

- **Hard Objects**: Entities with identity and agency that evolve through states
- **Soft Objects**: Outputs, snapshots, or observations that don't evolve
- Lifecycle indicators only apply to Hard Objects

### Not All States Apply to All Entities

The 8-stage lifecycle is a menu, not a mandate. Some entities may use a subset:

| Entity | Likely States | Notes |
|--------|---------------|-------|
| WorkItem | All 8 | Full lifecycle |
| Project | All 8 | Full lifecycle |
| Todo | RATIFIED, ARCHIVED, COMPOSTED | Simple items skip early stages |
| Conversation | RATIFIED, ARCHIVED, COMPOSTED | Simpler model |
| Document | Depends on genesis | Requested vs Seeded vs Derived |

---

## Object Model Details

### Document Model (Future Implementation)

```
Document (Entity with Lifecycle)
├── genesis: Genesis
│   ├── type: requested | seeded | derived
│   ├── source: Optional[File | Document]
│   ├── trigger: str
│   └── created_by: Entity
├── versions: List[DocumentVersion]
├── current_version: DocumentVersion
├── lifecycle_state: Optional[LifecycleState]
└── metadata: DocumentMetadata
```

**File vs Document Distinction**:
- **File**: Static upload, no lifecycle (FEDERATED ownership)
- **Document**: Evolving content, optional lifecycle (NATIVE ownership)

### Conversation Model (Future Implementation)

- **Conversation**: Entity (hard) - has identity, persists, fundamental to relationship
- **ConversationTurn**: Component - part of conversation, not independent
- **Transcript**: Artifact - rendered/exported form

Simpler lifecycle likely sufficient (RATIFIED, ARCHIVED, COMPOSTED).

---

## Related Documents

- **ADR-045**: Object Model ("Entities experience Moments in Places")
- **ADR-055**: Object Model Implementation
- **#685**: MUX-LIFECYCLE-OBJECTS (WorkItem/Feature backend)
- **#705**: Feature.to_dict() lifecycle serialization
- **#706**: MUX-OBJECTS-VIEWS (this discovery epic)
- **Insight Surfacing Rules**: `docs/internal/design/mux/insight-surfacing-rules.md`

---

## Decision Log

| Date | Decision | Participants |
|------|----------|--------------|
| 2026-01-27 | Insights do not use lifecycle (surfacing modes instead) | CXO, PPM, Lead Dev |
| 2026-01-27 | Todo uses hybrid model (simple status + optional lifecycle) | PM, Lead Dev |
| 2026-01-27 | File vs Document distinction adopted | PM, Lead Dev |
| 2026-01-27 | MUX Sprint scope: Todos, Projects, Work Items View, Project Detail | PM, Lead Dev |

---

*Document created: 2026-01-27*
*Last updated: 2026-01-27*
