# Gameplan: #649 TRUST-LEVELS-3 Discussability

**Issue**: TRUST-LEVELS-3: Discussability (TrustExplainer & Intent Handlers)
**Epic**: #413 (MUX-INTERACT-TRUST-LEVELS)
**Date**: 2026-01-23
**Author**: Lead Developer (Claude Code Opus)

---

## Phase -1: Infrastructure Verification

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Trust infrastructure: services/trust/trust_computation_service.py (from #647)
- [x] ProactivityGate: services/trust/proactivity_gate.py (from #648)
- [x] OutcomeClassifier: services/trust/outcome_classifier.py (from #648)
- [x] SignalDetector: services/trust/signal_detector.py (from #648)
- [x] TrustIntegration: services/trust/trust_integration.py (from #648)
- [x] Existing explain_trust_state(): Already in TrustComputationService
- [x] 244 passing tests in services/trust/

**My understanding of the task**:
- Create TrustExplainer service for rich natural language explanations
- Create ExplanationDetector for "why did you do that?" pattern detection
- Create explanation handler to wire detection → explainer
- Ensure explanations pass Contractor Test (professional, not robotic)

### Part A.2: Work Characteristics Assessment

**Worktree Assessment**:
- [x] Single agent, sequential work
- [x] Tightly coupled trust service files
- [x] ~2.5 hour estimate

**Assessment**: SKIP WORKTREE - Single agent, sequential work, tightly coupled trust service files

### Part B: PM Verification Required

**What needs verification**:
1. Should explanations be registered as a new IntentCategory or handled separately?
2. Does existing explain_trust_state() need replacement or augmentation?
3. Any specific phrases beyond ADR-053 templates to include?

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Infrastructure from #647/#648 verified, can investigate during Phase 0

---

## Phase 0: Initial Bookending

### Tasks
- [ ] Review existing explain_trust_state() implementation
- [ ] Review ADR-053 explanation templates
- [ ] Check SignalDetector patterns (may be reusable for query detection)
- [ ] Update GitHub issue with investigation status

### Investigation Commands
```bash
# Verify trust services work
python -c "from services.trust import TrustComputationService, ProactivityGate; print('OK')"

# Check existing explain_trust_state
grep -A 30 "def explain_trust_state" services/trust/trust_computation_service.py

# Check SignalDetector patterns (reuse opportunity)
grep -A 20 "ESCALATION_PHRASES\|COMPLAINT_PHRASES" services/trust/signal_detector.py
```

### STOP Conditions
- #648 infrastructure not importable
- ADR-053 templates don't exist or are incomplete

---

## Phase 0.5: Frontend-Backend Contract Verification

**SKIP** - This issue is backend-only (explanations returned as text)

---

## Phase 0.6: Data Flow & Integration Verification

### User Context Propagation

| Layer | Needs user_id? | Source |
|-------|----------------|--------|
| ExplanationDetector | No | Just analyzes text |
| TrustExplainer | Yes | Parameter from handler |
| ExplanationHandler | Yes | From RequestContext |

### Integration Points

| Caller | Callee | Verified? |
|--------|--------|-----------|
| ExplanationHandler | TrustExplainer | [ ] |
| TrustExplainer | TrustComputationService | [ ] |
| TrustExplainer | UserTrustProfileRepository | [ ] |

---

## Phase 0.7: Conversation Design

### Explanation Templates (from ADR-053)

**Stage 1 (NEW)**:
> "We're still getting to know each other. I'll wait for you to ask before offering suggestions, so I can learn what's helpful to you."

**Stage 2 (BUILDING)**:
> "We've been working together for a bit. I'll occasionally mention related things I can help with, but I'll always ask before acting."

**Stage 3 (ESTABLISHED)**:
> "We have a good working relationship. I'll proactively point out things I notice that might need your attention, but I'll still check before doing anything significant."

**Stage 4 (TRUSTED)**:
> "You've given me latitude to handle routine things. I'll take care of what I can and let you know what I did. Just tell me if you'd prefer I check first on anything."

### Contractor Test Criteria
- No internal jargon ("Stage 2", "TrustStage.BUILDING")
- Professional but warm tone
- References shared history naturally
- Offers agency ("let me know if...")

---

## Phase 0.8: Post-Completion Integration

### Side Effects

| Side Effect | Who/What Needs to Know |
|-------------|------------------------|
| New trust/* files | __init__.py exports |
| Explanation queries detected | Could be logged for analytics |

### Downstream Behavior Changes

| What Changes | When It Happens | Who's Affected |
|--------------|-----------------|----------------|
| Trust queries get answers | User asks "why" questions | All users |
| Proactive actions explained | User questions action | Stage 3-4 users |

---

## Phase 1: TrustExplainer Service

### Tasks
- [ ] Create `services/trust/trust_explainer.py`
- [ ] Implement stage explanation methods
- [ ] Implement proactive action explanation
- [ ] Implement "why not proactive" explanation
- [ ] Write unit tests

### Deliverables
- `services/trust/trust_explainer.py`
- `tests/unit/services/trust/test_trust_explainer.py`

### Acceptance Criteria
- [ ] explain_current_stage() returns natural language for all 4 stages
- [ ] explain_proactive_action() references the action taken
- [ ] explain_why_not_proactive() is appropriate for Stage 1-2
- [ ] No internal jargon in any output
- [ ] 15+ unit tests passing

### Test Strategy
```
test_trust_explainer.py:
- test_explain_stage_new_natural_language
- test_explain_stage_building_mentions_progress
- test_explain_stage_established_mentions_relationship
- test_explain_stage_trusted_mentions_autonomy
- test_explain_proactive_action_includes_context
- test_explain_why_not_proactive_for_new_user
- test_explanations_no_jargon
- test_handles_missing_profile
```

---

## Phase 2: ExplanationDetector Service

### Tasks
- [ ] Create `services/trust/explanation_detector.py`
- [ ] Implement query type detection
- [ ] Reuse patterns from SignalDetector where applicable
- [ ] Write unit tests

### Query Patterns to Detect

| Pattern Type | Examples |
|--------------|----------|
| WHY_ACTION | "Why did you do that?", "Why did you just..." |
| WHY_NO_ACTION | "Why don't you just...", "Why are you so cautious?" |
| TRUST_LEVEL | "How much do you trust me?", "What's our relationship?" |
| BEHAVIOR_QUESTION | "Why do you always ask?", "Why don't you decide?" |

### Deliverables
- `services/trust/explanation_detector.py`
- `tests/unit/services/trust/test_explanation_detector.py`

### Acceptance Criteria
- [ ] Detects all 4 query types
- [ ] No false positives on normal conversation
- [ ] Returns query type enum for routing
- [ ] 15+ unit tests passing

### Test Strategy
```
test_explanation_detector.py:
- test_detects_why_did_you_do_that
- test_detects_why_dont_you_just
- test_detects_why_so_cautious
- test_detects_trust_question
- test_no_false_positives_normal_text
- test_handles_variations
- test_returns_correct_query_type
```

---

## Phase 3: ExplanationHandler Integration

### Tasks
- [ ] Create `services/trust/explanation_handler.py`
- [ ] Wire detector → handler → explainer
- [ ] Handle edge cases (no profile, error states)
- [ ] Update `services/trust/__init__.py` exports
- [ ] Write unit tests

### Deliverables
- `services/trust/explanation_handler.py`
- Updated `services/trust/__init__.py`
- `tests/unit/services/trust/test_explanation_handler.py`

### Acceptance Criteria
- [ ] Routes queries to correct explainer method
- [ ] Handles unknown query types gracefully
- [ ] Returns explanation + optional follow-up offer
- [ ] 10+ unit tests passing

### Test Strategy
```
test_explanation_handler.py:
- test_routes_why_action_to_explain_proactive
- test_routes_why_no_action_to_explain_why_not
- test_routes_trust_level_to_explain_stage
- test_handles_unknown_query
- test_includes_followup_offer
- test_handles_missing_profile
```

---

## Phase Z: Final Bookending

### Tasks
- [ ] Run full trust test suite
- [ ] Run full unit test suite (check for regressions)
- [ ] Update issue with completion evidence
- [ ] Update session log
- [ ] Verify all exports in __init__.py

### Evidence Required
```bash
# Trust tests
pytest tests/unit/services/trust/ -v
# Expected: 280+ passed (244 existing + 40+ new)

# Full regression check
pytest tests/unit/ --tb=short
# Expected: 3370+ passed (3332 + 40 new)
```

---

## Completion Matrix

| Component | Status | Evidence |
|-----------|--------|----------|
| TrustExplainer service | ⏳ | |
| Explanation templates | ⏳ | |
| ExplanationDetector | ⏳ | |
| ExplanationHandler | ⏳ | |
| __init__.py exports | ⏳ | |
| Unit tests (explainer) | ⏳ | |
| Unit tests (detector) | ⏳ | |
| Unit tests (handler) | ⏳ | |

---

## STOP Conditions

1. ADR-053 templates incomplete or unclear → clarify
2. Existing explain_trust_state() conflicts → reconcile first
3. SignalDetector incompatible for reuse → build from scratch
4. Test failures in existing trust tests → fix first
5. Explanation templates fail Contractor Test → revise

---

## Agent Assignment

**Single Agent**: Lead Developer

**Rationale**: Sequential work, tightly coupled files, ~2.5 hour estimate. No parallel work opportunities.

---

## Duration Estimates

| Phase | Estimate |
|-------|----------|
| Phase 0: Investigation | 15 min |
| Phase 1: TrustExplainer | 45 min |
| Phase 2: ExplanationDetector | 30 min |
| Phase 3: Handler | 30 min |
| Phase Z: Completion | 15 min |
| **Total** | ~2.5 hours |
