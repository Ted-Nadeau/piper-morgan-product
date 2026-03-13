# Gameplan: #648 TRUST-LEVELS-2 Integration

**Issue**: TRUST-LEVELS-2: Integration (Intent Pipeline & ProactivityGate)
**Epic**: #413 (MUX-INTERACT-TRUST-LEVELS)
**Date**: 2026-01-23
**Author**: Lead Developer (Claude Code Opus)

---

## Phase -1: Infrastructure Verification

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Trust infrastructure: services/trust/trust_computation_service.py (from #647)
- [x] Repository: services/repositories/user_trust_profile_repository.py
- [x] Domain models: TrustStage, TrustEvent, UserTrustProfile
- [x] Database: user_trust_profiles table exists
- [x] Intent service: services/intent_service/ (need to investigate structure)

**My understanding of the task**:
- Wire trust computation into intent processing
- Create ProactivityGate for stage-based behavior gating
- Create OutcomeClassifier for intent→outcome mapping
- Create SignalDetector for escalation/complaint phrases
- Integrate welcome back pattern for inactivity regression

### Part A.2: Work Characteristics Assessment

**Worktree Assessment**:
- [x] Single agent, sequential work
- [x] Tightly coupled files requiring atomic commits
- [x] ~2-3 hour estimate

**Assessment**: SKIP WORKTREE - Single agent, sequential work, tightly coupled trust service files

### Part B: PM Verification Required

**What needs verification**:
1. Where does intent processing complete? (Where to hook trust recording)
2. Do any proactive features exist yet that need gating?
3. Is there existing outcome classification we should follow?

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Infrastructure from #647 verified, can investigate integration points during Phase 0

---

## Phase 0: Initial Bookending

### Tasks
- [ ] Verify #647 infrastructure is accessible
- [ ] Find intent processing pipeline entry points
- [ ] Identify where responses are generated
- [ ] Check for existing proactive features
- [ ] Update GitHub issue with investigation status

### Investigation Commands
```bash
# Verify trust service works
python -c "from services.trust.trust_computation_service import TrustComputationService; print('OK')"

# Find intent processing flow
grep -rn "IntentCategory" services/intent_service/ --include="*.py" | head -20

# Find where responses are generated
grep -rn "assistant_response\|generate_response" services/ --include="*.py" | head -20

# Check for proactive features
grep -rn "proactive\|suggest\|offer" services/ --include="*.py" | head -10
```

### STOP Conditions
- #647 infrastructure not importable
- Intent pipeline architecture completely unclear

---

## Phase 0.5: Frontend-Backend Contract Verification

**SKIP** - This issue is backend-only (no UI changes)

---

## Phase 0.6: Data Flow & Integration Verification

### User Context Propagation

| Layer | Needs user_id? | Source |
|-------|----------------|--------|
| Intent Service | Yes | From RequestContext or session |
| TrustComputationService | Yes | Parameter from intent service |
| Repository | Yes | Parameter from service |

### Integration Points

| Caller | Callee | Verified? |
|--------|--------|-----------|
| Intent handler | TrustComputationService | [ ] |
| ProactivityGate | TrustComputationService.get_trust_stage | [ ] |
| SignalDetector | TrustComputationService.progress_to_trusted | [ ] |

---

## Phase 0.7: Conversation Design

**SKIP** - This issue is not a conversational feature

---

## Phase 0.8: Post-Completion Integration

### Completion Side-Effects

| Side Effect | Table/Field | Value |
|-------------|-------------|-------|
| Trust recorded | user_trust_profiles | event added |
| Stage may change | user_trust_profiles.current_stage | 1-4 |

### Downstream Behavior Changes

| Feature | Before | After |
|---------|--------|-------|
| Responses | Static | May include proactive hints (Stage 2+) |
| Suggestions | None | Context-based suggestions (Stage 3+) |

---

## Phase 1: ProactivityGate Service

### Objective
Create the gate that decides what behaviors are allowed at each trust stage.

### Tasks
- [ ] Create `services/trust/proactivity_gate.py`
- [ ] Implement gate methods:
  - `can_offer_capability_hints(stage)` → bool
  - `can_proactive_suggest(stage)` → bool
  - `can_act_without_asking(stage)` → bool
  - `get_proactivity_config(stage)` → dict
  - `get_max_suggestions_per_session(stage)` → int
- [ ] Write unit tests

### Deliverables
- `services/trust/proactivity_gate.py`
- `tests/unit/services/trust/test_proactivity_gate.py`

### Acceptance Criteria
- [ ] Stage 1 (NEW) blocks all proactive behavior
- [ ] Stage 2 (BUILDING) allows hints only
- [ ] Stage 3 (ESTABLISHED) allows suggestions
- [ ] Stage 4 (TRUSTED) allows autonomous actions
- [ ] All gate methods tested

---

## Phase 2: OutcomeClassifier

### Objective
Classify intent processing outcomes for trust recording.

### Tasks
- [ ] Create `services/trust/outcome_classifier.py`
- [ ] Implement classification rules per ADR-053:
  - User expressed thanks → successful
  - Follow-up question → successful
  - Command execution → successful
  - Topic change without ack → neutral
  - "Not what I wanted" → negative
- [ ] Write unit tests

### Deliverables
- `services/trust/outcome_classifier.py`
- `tests/unit/services/trust/test_outcome_classifier.py`

### Acceptance Criteria
- [ ] All classification rules implemented
- [ ] Edge cases handled (ambiguous input → neutral)
- [ ] Unit tests for each rule

---

## Phase 3: SignalDetector

### Objective
Detect conversational signals for trust escalation and complaints.

### Tasks
- [ ] Create `services/trust/signal_detector.py`
- [ ] Implement trust escalation detection:
  - "Just handle it"
  - "Do that automatically"
  - "I trust you to..."
  - "You don't need to ask"
- [ ] Implement complaint detection:
  - "stop doing that"
  - "don't", "I didn't ask"
  - Explicit "no" to proactive offer
- [ ] Write unit tests

### Deliverables
- `services/trust/signal_detector.py`
- `tests/unit/services/trust/test_signal_detector.py`

### Acceptance Criteria
- [ ] Escalation phrases detected correctly
- [ ] Complaint patterns detected correctly
- [ ] No false positives on normal conversation
- [ ] Unit tests for all patterns

---

## Phase 4: Intent Pipeline Integration

### Objective
Wire trust components into the intent processing flow.

### Tasks
- [ ] Identify integration point (after intent handling)
- [ ] Add trust recording call with outcome
- [ ] Check for escalation/complaint signals
- [ ] Add ProactivityGate checks where appropriate
- [ ] Implement welcome back message for regression
- [ ] Write integration tests

### Deliverables
- Modified intent handling code
- `tests/integration/services/trust/test_trust_integration.py`

### Acceptance Criteria
- [ ] Trust recorded after each interaction
- [ ] Stage progression works end-to-end
- [ ] Complaints trigger regression
- [ ] Welcome back message shows once after regression
- [ ] Integration tests pass

---

## Phase Z: Final Bookending

### Tasks
- [ ] Run all unit tests (expect ~80+ new tests)
- [ ] Run full test suite (confirm no regressions)
- [ ] Update GitHub issue with evidence
- [ ] Update session log
- [ ] Request PM approval

### Evidence Required
- Test output showing new tests pass
- Test output showing no regressions
- Database showing trust changes work

---

## Completion Matrix

| Component | Status | Evidence |
|-----------|--------|----------|
| ProactivityGate | ❌ | |
| OutcomeClassifier | ❌ | |
| SignalDetector | ❌ | |
| Pipeline Integration | ❌ | |
| Welcome Back | ❌ | |
| Unit Tests | ❌ | |
| Integration Tests | ❌ | |

---

## STOP Conditions

- Intent pipeline architecture unclear → investigate more
- Existing proactive features not found → may need to defer gating
- Classification rules seem incomplete → get PM input
- Tests fail → fix before proceeding
- Performance concerns with trust lookups → discuss with PM

---

## Agent Assignment

**Single Agent**: Lead Developer (Claude Code Opus)

**Rationale**: Sequential work with tightly coupled components. Each phase builds on the previous. ProactivityGate and OutcomeClassifier are independent but SignalDetector and Integration depend on them.

---

## Estimated Duration

| Phase | Estimate |
|-------|----------|
| Phase 0 | 15-30 min |
| Phase 1 | 30-45 min |
| Phase 2 | 45-60 min |
| Phase 3 | 45-60 min |
| Phase 4 | 60-90 min |
| Phase Z | 15-30 min |
| **Total** | ~3-4 hours |

---

*Gameplan created: 2026-01-23 11:00 AM*
