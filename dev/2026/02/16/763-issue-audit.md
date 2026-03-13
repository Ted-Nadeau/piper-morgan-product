# Audit: #763 (GLUE-FOLLOWUP) against feature.md template

**Date**: 2026-02-16
**Auditor**: Lead Developer (Claude Code)
**Phase**: Issue → Gameplan

---

## Audit Matrix

| # | Template Requirement | Status | Notes |
|---|---------------------|--------|-------|
| 1 | Priority | ✅ | P0 |
| 2 | Labels | ✅ | `PDR-002`, `glue` |
| 3 | Milestone | ❌ | Missing — no milestone specified |
| 4 | Epic | ✅ | #762 GLUE |
| 5 | Related | ⚠️ | Has #427, Pattern-011, ADR-049 — ADR-049 exists (confirmed), Pattern-011 confirmed |
| 6 | Problem Statement: Current State | ✅ | Clear before/after example of lost lens |
| 7 | Problem Statement: Impact | ❌ | No Blocks/User Impact/Technical Debt section |
| 8 | Problem Statement: Strategic Context | ❌ | Missing — why now? |
| 9 | Goal: Primary Objective | ❌ | No explicit one-sentence objective |
| 10 | Goal: Example User Experience | ✅ | Before/after calendar scenario provided |
| 11 | Goal: Not In Scope | ❌ | Missing — what's explicitly excluded? |
| 12 | What Already Exists: Infrastructure | ❌ | Missing — see code investigation below |
| 13 | What Already Exists: What's Missing | ❌ | Missing — see code investigation below |
| 14 | Requirements: Phase 0 | ❌ | No investigation phase defined |
| 15 | Requirements: Phased tasks | ⚠️ | Has 3 requirement areas but no phases with tasks/deliverables |
| 16 | Requirements: Phase Z | ❌ | Missing |
| 17 | Acceptance Criteria: Functionality | ✅ | 6 criteria with percentage targets |
| 18 | Acceptance Criteria: Testing | ❌ | No testing criteria |
| 19 | Acceptance Criteria: Quality | ❌ | No quality criteria |
| 20 | Acceptance Criteria: Documentation | ❌ | No documentation criteria |
| 21 | Completion Matrix | ❌ | Missing |
| 22 | Testing Strategy | ❌ | Missing |
| 23 | Success Metrics | ⚠️ | >90%/>85% targets serve this role but not structured per template |
| 24 | STOP Conditions | ❌ | Missing |
| 25 | Effort Estimate | ⚠️ | "3-5 days" at top but no phase breakdown |
| 26 | Dependencies | ❌ | Missing — does this depend on #766? Pattern-011? |
| 27 | Related Documentation | ⚠️ | Listed in header but not structured |
| 28 | Evidence Section | ❌ | Expected — pre-implementation |
| 29 | Completion Checklist | ❌ | Missing |

**Score: 5 ✅ / 5 ⚠️ / 19 ❌**

---

## Code Investigation: What Already Exists

### WORKING Infrastructure (ready to build on)

1. **Follow-up detection system** (`services/intent_service/conversation_context.py`)
   - `FollowUpType` enum: TEMPORAL_SHIFT, ENTITY_REFERENCE, CONFIRMATION, REFINEMENT, CONTINUATION, NEGATION
   - `detect_follow_up(message, context)` → pattern-matches against known follow-up patterns
   - `resolve_follow_up(follow_up_type, extracted_data, context)` → creates inherited Intent
   - Tests: `tests/unit/services/intent_service/test_classifier_follow_up.py` — all passing

2. **Rich ConversationContext** (`services/intent_service/conversation_context.py`)
   - Fields: session_id, user_id, turns (10-turn window), max_age_minutes (30)
   - Properties: `last_intent`, `last_temporal_reference`, `last_topic`, `is_active`
   - ConversationTurn stores: temporal_reference, entity_references, topic, intent

3. **Reference resolver** (`services/conversation/reference_resolver.py`)
   - Resolves pronouns: "it", "that", "the meeting"
   - Finds candidates from conversation history, scores, picks best

4. **Context tracker** (`services/conversation/context_tracker.py`)
   - Tracks: current_topic, active_entities, user_intent_history, conversation_flow

5. **Intent classifier integration** (`services/intent_service/classifier.py`)
   - `classify_conscious()` checks follow-ups FIRST, skips LLM if resolved
   - ConversationContext passed through to personality bridge

6. **ProcessRegistry** (ADR-049) — Handles guided multi-turn flows (onboarding, standup)

7. **MUX Lens system** (`services/mux/lenses/`) — Perception lenses exist (temporal, priority, etc.) but are for object analysis, not conversational tracking

### MISSING for #763

1. **`current_lens` field** — Neither ConversationContext has it
2. **Lens inference from intent** — No function to map intent → lens (e.g., `meeting_time` → `calendar_view`)
3. **Lens inheritance in follow-up resolution** — `resolve_follow_up()` doesn't preserve lens
4. **Lens-aware intent classification** — Classifier doesn't use lens to bias interpretation
5. **Explicit lens reset detection** — No patterns for "user changed dimensions"
6. **Multiple concurrent lenses** — Not implemented anywhere

### Key Architectural Insight

The follow-up system currently resolves **temporal shifts** excellently (pattern-matched, no LLM). But it cannot resolve **arbitrary perspective shifts** because it doesn't track what dimension/lens the user was viewing through. Adding `current_lens` to ConversationContext and wiring it through the existing follow-up → classifier → personality bridge pipeline should work without restructuring.

---

## Critical Discussion Points for PM

1. **Scope of "reference types"**: All 4 types (pronouns, elliptical, comparative, temporal) or subset?
2. **>90%/>85% accuracy measurement**: What test corpus? What's the baseline?
3. **"Multiple active lenses"**: Is this M0 scope or future?
4. **Lens taxonomy**: How many lens types for MVP? (calendar, issues, projects, ...?)
5. **LLM involvement**: Should lens inference be rule-based (fast, deterministic) or LLM-based (flexible, slower)?
