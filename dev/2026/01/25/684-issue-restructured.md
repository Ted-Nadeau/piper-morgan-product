# MUX-NAV-PLACES - Places as Windows Design

**Priority**: P1
**Labels**: `MUX-IMPLEMENT`, `places`, `federated`, `consciousness`
**Milestone**: Sprint P1 (Navigation Paradigm)
**Epic**: #418 MUX-IMPLEMENT
**Related**: #419 (Home State), #420 (Nav Utility), #421 (Command Palette), ADR-038 (Spatial Intelligence)

---

## Problem Statement

### Current State
Integration model treats external sources as destinations:
- "Go to GitHub" → user leaves Piper's context
- "Check Notion" → user must context-switch
- "View Calendar" → user loses conversational flow

No unified "Place" abstraction exists. Each integration is siloed.

### Impact
- **Blocks**: Trust-gated home (#419) needs Places to show in context; nav (#420) needs Place items
- **User Impact**: Users context-switch constantly; lose conversational flow with Piper
- **Technical Debt**: Inconsistent integration patterns; no Place-type vocabulary

### Strategic Context
P1 establishes navigation paradigm. Places reframe integrations as "Piper's windows into external world" rather than "links to leave." This is foundational for the colleague experience - Piper observes and interprets, doesn't just redirect.

---

## Goal

**Primary Objective**: Create a Place abstraction that renders external sources as inline "windows" Piper can show, with type-based atmospheres and confidence-based display.

**Example User Experience**:
```
BEFORE:
- User asks "what's happening in GitHub?"
- Piper says "Click here to go to GitHub"
- User leaves Piper, loses context

AFTER (Stage 3 user):
- User asks "what's happening in GitHub?"
- Piper shows inline window: "I see 3 PRs waiting for review"
- User can expand details OR click through
- Piper acknowledges "This is what I saw 5 minutes ago"
```

**Not In Scope** (explicitly):
- ❌ Full implementation of all 4 Place types (start with 2)
- ❌ Real-time sync / webhooks (polling for P1)
- ❌ Rich editing within Place windows (read-only)
- ❌ Mobile-specific Place UI (desktop first)
- ❌ AI-powered Place recommendations

---

## What Already Exists

### Infrastructure ✅
- `services/integrations/` - GitHub, Slack, Calendar connectors
- `services/spatial/` - Spatial intelligence patterns
- ADR-038 - Spatial intelligence architecture
- Trust computation from #419
- HardnessLevel enum for visibility gating

### What's Missing ❌
- Place abstraction model
- Place-type enum (IssueTracking, Communication, Temporal, Documentation)
- "Window" component for inline Place rendering
- Confidence-based display logic
- Type-based atmosphere styling
- Graceful degradation for unavailable sources

---

## Requirements

### Phase 0: Investigation & Design
**Objective**: Establish Place vocabulary and component design

**Tasks**:
- [ ] Survey existing integration response patterns
- [ ] Define PlaceType enum (4 types)
- [ ] Design window component structure
- [ ] Define confidence levels (high/medium/low)
- [ ] Create atmosphere color/style vocabulary

**Deliverables**:
- PlaceType enum definition
- Window component wireframe
- Atmosphere style guide (4 types)

### Phase 1: Place Domain Model
**Objective**: Create Place abstraction in domain layer

**Tasks**:
- [ ] Add PlaceType enum to `services/shared_types.py`
- [ ] Create Place dataclass in `services/domain/models.py`
- [ ] Define PlaceConfidence enum (HIGH, MEDIUM, LOW)
- [ ] Add place_type to integration configs
- [ ] Write domain model tests

**Deliverables**:
- `PlaceType` enum
- `Place` dataclass
- `PlaceConfidence` enum
- 10+ unit tests

### Phase 2: Window Component (First Type)
**Objective**: Implement window component for IssueTracking type (GitHub)

**Tasks**:
- [ ] Create `templates/components/place_window.html`
- [ ] Implement IssueTracking atmosphere styling
- [ ] Create PlaceService to fetch and transform integration data
- [ ] Implement confidence-based display (summary/expand/redirect)
- [ ] Add staleness indicator ("Piper saw this N ago")
- [ ] Write component tests

**Deliverables**:
- `place_window.html` component
- IssueTracking atmosphere CSS
- PlaceService
- 10+ tests

### Phase 3: Second Place Type (Temporal)
**Objective**: Implement Temporal type (Calendar)

**Tasks**:
- [ ] Apply Temporal atmosphere styling
- [ ] Transform calendar data to Place format
- [ ] Timeline-oriented display mode
- [ ] Conflict awareness display
- [ ] Write tests for Temporal type

**Deliverables**:
- Temporal atmosphere CSS
- Calendar → Place transformation
- 5+ tests

### Phase 4: Trust-Gated Visibility
**Objective**: Filter Places by trust stage

**Tasks**:
- [ ] Assign hardness to each Place type
- [ ] Filter visible Places by trust stage
- [ ] Stage 1-2: Basic Places only
- [ ] Stage 3-4: Full Place set
- [ ] Write visibility tests

**Deliverables**:
- Trust-gated Place filtering
- Visibility matrix documented
- 5+ tests

### Phase 5: Home & Nav Integration
**Objective**: Wire Places into home state and nav

**Tasks**:
- [ ] Add Place summary cards to home (#419)
- [ ] Add Place items to nav (#420)
- [ ] Wire palette Place commands (#421)
- [ ] Write integration tests

**Deliverables**:
- Home Place cards
- Nav Place items
- Palette Place commands
- Integration evidence

### Phase Z: Completion & Handoff
- [ ] All acceptance criteria met
- [ ] Evidence provided
- [ ] 2 Place types working (IssueTracking, Temporal)
- [ ] Session log completed
- [ ] GitHub issue updated

---

## Acceptance Criteria

### Functionality
- [ ] PlaceType enum with 4 types defined
- [ ] Place dataclass in domain model
- [ ] Window component renders inline
- [ ] IssueTracking type working (GitHub)
- [ ] Temporal type working (Calendar)
- [ ] Confidence-based display (summary/expand/redirect)
- [ ] Staleness indicator working
- [ ] Trust-gated visibility working

### Testing
- [ ] Unit tests for Place domain model
- [ ] Unit tests for PlaceService
- [ ] Unit tests for window component
- [ ] Unit tests for trust-gated visibility
- [ ] Full unit test suite passes

### Quality
- [ ] No regressions introduced
- [ ] Type atmospheres visually distinct
- [ ] Graceful degradation when source unavailable
- [ ] "Piper sees..." language (anti-flattening)

### Documentation
- [ ] PlaceType vocabulary documented
- [ ] Atmosphere style guide
- [ ] Usage patterns documented
- [ ] Session log complete

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Phase 0: Design | ⏸️ | |
| Phase 1: Domain Model | ⏸️ | |
| Phase 2: Window + IssueTracking | ⏸️ | |
| Phase 3: Temporal Type | ⏸️ | |
| Phase 4: Trust-Gating | ⏸️ | |
| Phase 5: Integration | ⏸️ | |
| Phase Z: Completion | ⏸️ | |
| All unit tests pass | ⏸️ | |
| No regressions | ⏸️ | |

---

## Testing Strategy

### Unit Tests
```
tests/unit/services/domain/test_place_model.py:
- test_place_type_enum_values
- test_place_dataclass_creation
- test_place_confidence_levels
- test_place_staleness_calculation

tests/unit/services/test_place_service.py:
- test_github_to_place_transformation
- test_calendar_to_place_transformation
- test_confidence_determination
- test_unavailable_source_handling

tests/unit/templates/test_place_window.py:
- test_window_renders_summary
- test_window_renders_expanded
- test_window_redirect_mode
- test_staleness_display
- test_atmosphere_styling

tests/unit/services/test_place_visibility.py:
- test_stage_1_sees_basic_places
- test_stage_4_sees_all_places
- test_hardness_filtering
```

### Integration Tests
Not required for P1 - unit tests sufficient.

### Manual Testing Checklist
**Scenario 1**: GitHub Place window
1. [ ] Navigate to home as Stage 3 user
2. [ ] See GitHub Place card with PR summary
3. [ ] Expand to see details
4. [ ] Note staleness indicator
5. [ ] Click through to GitHub

**Scenario 2**: Calendar Place window
1. [ ] Navigate to home
2. [ ] See Calendar Place with upcoming events
3. [ ] See conflict highlighting if present
4. [ ] Timeline display mode working

---

## Success Metrics

### Quantitative
- 2 Place types implemented
- 30+ new unit tests passing
- 0 regressions in existing tests
- Window renders in <200ms

### Qualitative
- Places feel like "windows" not "links"
- Piper language used ("I see...", "I noticed...")
- Atmospheres visually distinct
- Confidence communicated clearly

---

## STOP Conditions

**STOP immediately and escalate if**:
- Integration APIs unavailable
- Trust context unavailable (#419 incomplete)
- Atmosphere styling conflicts with brand
- Performance >500ms for Place fetch
- Anti-flattening test fails ("API returned" instead of "Piper sees")
- Tests fail for any reason

**When stopped**: Document the issue, provide options, wait for PM decision.

---

## Effort Estimate

**Overall Size**: Large (new paradigm + multi-integration)

**Breakdown by Phase**:
- Phase 0: Medium (design work)
- Phase 1: Small (domain model)
- Phase 2: Large (window component + first type)
- Phase 3: Medium (second type)
- Phase 4: Small (visibility filtering)
- Phase 5: Medium (integrations)
- Phase Z: Small (documentation)

**Complexity Notes**:
- New abstraction paradigm (Place)
- Two integration types (GitHub, Calendar)
- Atmosphere styling system is new
- Builds on #419 trust infrastructure

---

## Dependencies

### Required (Must be complete first)
- [x] #419 MUX-NAV-HOME (trust_stage context)
- [ ] #420 MUX-NAV-UTILITY (nav integration - can parallel)
- [ ] #421 MUX-NAV-PALETTE (palette integration - can parallel)

### Optional (Nice to have)
- [ ] Calendar integration fully operational
- [ ] GitHub integration fully operational

---

## Related Documentation

- **Architecture**: ADR-038 (Spatial Intelligence), ADR-045 (Object Model)
- **Philosophy**: `docs/internal/architecture/current/ownership-metaphors.md`
- **Integrations**: `services/integrations/`, `services/spatial/`
- **Mobile**: `dev/active/mobile-skunkworks-briefing.md`

---

## Evidence Section

[To be filled during implementation]

### Implementation Evidence
```bash
# Phase 0 evidence (design artifacts)
# Phase 1 evidence (domain model)
# Phase 2 evidence (window + IssueTracking)
# Phase 3 evidence (Temporal)
# Phase 4 evidence (trust-gating)
# Phase 5 evidence (integrations)
# Full test suite
```

---

## Completion Checklist

Before requesting PM review:
- [ ] All acceptance criteria met ✅
- [ ] Completion matrix 100% ✅
- [ ] Evidence provided for each criterion ✅
- [ ] Tests passing with output ✅
- [ ] 2 Place types working ✅
- [ ] No regressions confirmed ✅
- [ ] STOP conditions all clear ✅
- [ ] Session log complete ✅

**Status**: Not Started

---

## Design Principles (Preserved from Original)

### The Core Insight
> "What if Places aren't links you click to leave Piper, but windows that show you what Piper sees there?"

### Atmosphere Belongs to Place-TYPE, Not Vendor
- **Issue Tracking** (GitHub, Linear, Jira) → focused, status-oriented
- **Communication** (Slack, Email) → conversational, time-sensitive
- **Temporal** (Calendar, Scheduling) → timeline-oriented, conflict-aware
- **Documentation** (Notion, Confluence) → reference-oriented, searchable

### Summary vs. Portal Based on Confidence
- High confidence: Show summary inline ("3 PRs need review")
- Medium confidence: Offer to expand ("Want to see the GitHub details?")
- Low confidence: Suggest visiting source ("I'm not sure - check GitHub directly?")

### FEDERATED Epistemology
Places are FEDERATED sources - Piper's senses, not her mind:
- Piper *observes* these sources
- Piper *interprets* what she sees
- Piper *acknowledges* uncertainty about external state

### Anti-Patterns to Avoid
- Brand-centric styling (GitHub green) → use type atmospheres
- "Open in new tab" as primary → keep user in Piper context
- Over-confident summaries → acknowledge staleness
- Treating all Places equally → trust-gate by sensitivity

---

## Place Types Reference

| Type | Prototype | Atmosphere | Key Actions | Hardness |
|------|-----------|------------|-------------|----------|
| IssueTracking | GitHub | Focused, status | View, triage, link | HARD |
| Communication | Slack | Conversational | Read, respond | MEDIUM |
| Temporal | Calendar | Timeline | View, schedule | HARD |
| Documentation | Notion | Reference | Search, link | SOFT |

---

_Issue created: 2026-01-25_
_Last updated: 2026-01-25_
