# Audit: #408 MUX-VISION-LIFECYCLE-SPEC

## Issue vs Infrastructure Gap Analysis

### What the Issue Requests

**Experience Phrases** (from issue table):
| Stage | Issue Specifies |
|-------|-----------------|
| EMERGENT | "I just noticed..." |
| DERIVED | "I figured out from..." |
| NOTICED | "I'm aware of..." |
| PROPOSED | "I think we should..." |
| RATIFIED | "We're doing..." |
| DEPRECATED | "This used to be..." |
| ARCHIVED | "I remember when..." |
| COMPOSTED | "I learned that..." |

### What Already Exists

**`services/mux/lifecycle.py`** has `LifecycleState.experience_phrase` property:

| Stage | Current Implementation |
|-------|----------------------|
| EMERGENT | "I sense something forming, though its shape is not yet clear" |
| DERIVED | "I recognize a pattern emerging from the noise" |
| NOTICED | "This has caught my attention - it seems significant" |
| PROPOSED | "I am considering this proposal for its merits" |
| RATIFIED | "This is now part of our established reality" |
| DEPRECATED | "This served us well, but its time is passing" |
| ARCHIVED | "This rests in memory, preserved though no longer active" |
| COMPOSTED | "This has transformed into nourishment for future growth" |

### Gap Analysis

| Aspect | Issue Wants | Current State | Gap? |
|--------|-------------|---------------|------|
| Experience phrases | Simple, actionable ("I just noticed...") | Poetic, abstract ("I sense something forming...") | **YES - TONE MISMATCH** |
| meaning property | Not mentioned | Exists, descriptive | OK |
| typical_objects | Not mentioned | Exists, examples per state | OK |
| Transition explanations | Required deliverable | Not implemented | **YES** |
| Composting narrative | Required deliverable | CompostingExtractor exists, no narrative | **YES** |
| Error state handling | Required deliverable | InvalidTransitionError exists, no user-facing | **YES** |
| Integration in handlers | Required | Not implemented | **YES** |

---

## Critical Finding: Phrase Tone Mismatch

The issue specifies **short, actionable phrases** for everyday use:
- "I just noticed..."
- "I think we should..."
- "We're doing..."

The current implementation has **poetic, philosophical phrases**:
- "I sense something forming, though its shape is not yet clear"
- "I am considering this proposal for its merits"
- "This is now part of our established reality"

**Contractor Test**: Would a colleague say "This is now part of our established reality"? No. They'd say "We're doing this now."

**Decision Point**: Do we:
1. **Replace** existing phrases with issue-specified ones?
2. **Add** a second property (e.g., `short_phrase`) alongside existing?
3. **Consult** CXO/PPM on tone preference?

**Recommendation**: Option 2 or 3. The existing phrases may serve a different purpose (documentation, introspection). The issue phrases are for conversational UI. Both may be valid for different contexts.

---

## Existing Infrastructure Summary

### `services/mux/lifecycle.py` (471 lines)

| Component | Status | Notes |
|-----------|--------|-------|
| `LifecycleState` enum | ✅ Complete | 8 states with properties |
| `meaning` property | ✅ Complete | Descriptive meanings |
| `experience_phrase` property | ⚠️ Tone issue | Poetic vs actionable |
| `typical_objects` property | ✅ Complete | Example objects per state |
| `VALID_TRANSITIONS` | ✅ Complete | Transition rules defined |
| `InvalidTransitionError` | ✅ Complete | Error class, no user-facing message |
| `LifecycleTransition` dataclass | ✅ Complete | Records transitions |
| `HasLifecycle` protocol | ✅ Complete | Interface for lifecycle objects |
| `LifecycleManager` | ✅ Complete | Manages transitions |
| `CompostResult` dataclass | ✅ Complete | Composting output |
| `CompostingExtractor` | ✅ Complete | Extracts wisdom |

### Missing Components

| Component | Description | Priority |
|-----------|-------------|----------|
| `conversation_phrase` | Short, actionable phrases for UI | HIGH |
| `transition_explanation()` | Why object moved states | HIGH |
| `composting_narrative()` | User-facing composting story | MEDIUM |
| `error_user_message()` | Friendly error for invalid transitions | MEDIUM |
| Integration helpers | Functions for intent handlers | HIGH |

---

## Acceptance Criteria Mapping

### Documentation Deliverables

| Criterion | Current State | Work Needed |
|-----------|---------------|-------------|
| Lifecycle experience guide | None | Create doc |
| Transition explanation patterns | None | Define and implement |
| Composting narrative | CompostingExtractor exists | Add user-facing narrative |
| Error state handling | InvalidTransitionError exists | Add friendly messages |

### Integration Points

| Criterion | Current State | Work Needed |
|-----------|---------------|-------------|
| Experience phrases in intent handlers | Not integrated | Find handlers, add phrases |
| Lifecycle state in entity descriptions | Not implemented | Add to entity formatters |
| Composting events surfaced | CompostResult exists | Surface in appropriate contexts |
| Learning extraction visible | _generate_lessons exists | Make visible to users |

### Quality Gates

| Criterion | Current State | Work Needed |
|-----------|---------------|-------------|
| All 8 states have consistent language | Yes but wrong tone | Fix tone |
| Transitions feel natural | Not tested | PM review |
| Composting metaphor tested | Not tested | PM review |
| No "deletion" language | Not verified | Audit all messaging |

---

## Questions for PM Before Gameplan

1. **Phrase Tone**: Replace existing poetic phrases, or add separate actionable phrases?

2. **Scope of Integration**: Which intent handlers should use lifecycle phrases?
   - All handlers that touch lifecycle objects?
   - Specific subset?
   - Need to audit which handlers exist?

3. **Documentation Location**:
   - `docs/internal/architecture/current/` (alongside ADRs)?
   - Inline in code?
   - Both?

4. **Composting Visibility**: When should users see composting happen?
   - Never (background only)?
   - On request?
   - Proactively for certain objects?

---

## Recommended Gameplan Structure

Assuming PM answers:

**Phase 1**: Phrase Layer
- Add `conversation_phrase` property (or update existing)
- Add `transition_explanation()` method
- Add `error_user_message()` to InvalidTransitionError
- Tests for all phrase generation

**Phase 2**: Composting Narrative
- Add narrative generation to CompostingExtractor
- User-facing story of object transformation
- Tests

**Phase 3**: Integration
- Audit intent handlers for lifecycle touchpoints
- Add phrase integration helpers
- Integration tests

**Phase 4**: Documentation
- Lifecycle experience guide
- Pattern documentation
- Quality gate verification

---

## Summary

**Good news**: Substantial infrastructure exists (LifecycleState, transitions, composting).

**Key gap**: Existing phrases are poetic/philosophical, issue wants actionable/conversational.

**Decision needed**: PM guidance on phrase approach before proceeding.
