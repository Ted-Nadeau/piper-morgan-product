# Gameplan: #410 MUX-INTERACT-CANONICAL-ENHANCE

**Issue**: #410 - Evolve canonical queries to orientation system
**Created**: 2026-01-23
**Updated**: 2026-01-23 (post Arch/CXO guidance)
**Template Version**: v9.3

---

## Architectural Guidance (Received 2026-01-23)

**Chief Architect Decision** (memo: `memo-lead-dev-orientation-architecture-response-2026-01-23.md`):
- **Modified Option D**: Option A structure + Option D framing
- **Location**: `services/mux/orientation.py` - Part of MUX/consciousness domain, NOT a new bounded context
- **Grammar Alignment**: Through framing and documentation - "Piper perceiving the current Situation through multiple lenses"
- **Integration Point**: After PlaceDetector, before IntentClassifier
- **Trust Integration**: Include trust_context field NOW

**CXO Experience Guidance** (memo: `memo-lead-dev-orientation-response-2026-01-23.md`):
- **Trust Gradient**: Stage 1 = never proactive, Stage 3+ = "I notice..." OK
- **Articulation**: "looks like" not "seems to be"
- **Recognition Presentation**: Option C (narrative) as north star with channel adaptation
- **Channel Adaptation**: Web = full narrative, Slack = compressed
- **"None of these"**: Doesn't affect trust computation
- **Framing**: Observational for inferences, declarative for facts

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (verified)
- [x] MUX domain: services/mux/ (verified - consciousness.py exists)
- [x] Trust service: services/trust/ (verified - TrustComputationService complete)
- [x] Place detector: services/intent_service/place_detector.py (verified)
- [x] Intent classifier: services/intent_service/classifier.py (verified)
- [x] Testing framework: pytest (verified)
- [x] Shared types: services/shared_types.py (TrustStage enum exists)

**My understanding of the task** (updated per Arch guidance):
- I believe we need to: Create an orientation layer at `services/mux/orientation.py` that represents "Piper perceiving the current Situation through multiple lenses"
- The five pillars map to lenses: Identity (self-awareness), Temporal (temporal), Spatial (contextual + place), Agency (priority), Prediction (causal/anticipating)
- This is NOT a new bounded context - it's part of MUX/consciousness domain
- Trust integration happens NOW via trust_context field

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel on different files/features
- [x] Task duration >30 minutes (main branch may advance)
- [ ] Multi-component work (e.g., frontend + backend by different agents)
- [ ] Exploratory/risky changes where easy rollback is valuable
- [ ] Coordination queue prompt being claimed

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [ ] Small fixes (<15 min)
- [x] Tightly coupled files requiring atomic commits
- [ ] Time-critical work where setup overhead matters

**Assessment:**
- [x] **SKIP WORKTREE** - Single agent, tightly coupled MUX files, overhead exceeds benefit

### Part B: PM Verification ✅ RECEIVED

**Verified via Arch/CXO memos**:
1. ✅ Location: `services/mux/orientation.py` (Arch decision)
2. ✅ Integration point: After PlaceDetector, before IntentClassifier (Arch decision)
3. ✅ No existing orientation system (creating from scratch)
4. ✅ Trust integration NOW (PM + Arch decision)

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Guidance received, gameplan updated appropriately

---

## Phase 0: Initial Bookending - Investigation

### Purpose
Verify MUX/consciousness infrastructure and integration points per Arch guidance.

### Required Actions

1. **GitHub Issue Verification**
   - [x] Issue #410 exists and is assigned
   - [x] Description updated with full template (2026-01-23)

2. **Codebase Investigation**
   - [ ] Read existing MUX infrastructure: `services/mux/consciousness.py`
   - [ ] Verify PlaceDetector API: `services/intent_service/place_detector.py`
   - [ ] Verify IntentClassifier API: `services/intent_service/classifier.py`
   - [ ] Verify TrustContext access: `services/trust/trust_computation_service.py`
   - [ ] Check existing context dataclasses in `services/domain/models.py`

3. **Integration Point Analysis**
   ```bash
   # Where PlaceDetector is called
   grep -r "PlaceDetector\|place_detector" services/ --include="*.py"

   # Where IntentClassifier is called
   grep -r "IntentClassifier\|classifier" services/intent_service/ --include="*.py"

   # Current flow: Request → PlaceDetector → [orientation HERE] → IntentClassifier → Handler
   ```

### Deliverables
- Investigation notes in session log
- Integration approach documented
- PlaceDetector output format documented
- IntentClassifier input requirements documented

### STOP Conditions
- Orientation system already exists (complete it instead)
- PlaceDetector/IntentClassifier APIs incompatible with approach
- MUX consciousness architecture significantly different than expected

---

## Phase 0.5: N/A (No Frontend Work)

This issue is backend-only. Skip Phase 0.5.

---

## Phase 0.6: N/A (Single Layer)

This issue creates a new layer but doesn't involve complex multi-layer data flow. Skip Phase 0.6.

---

## Phase 0.7: N/A (Not Conversational)

This issue is not a conversational feature. Skip Phase 0.7.

---

## Phase 0.8: N/A (No Completion Side-Effects)

This issue creates infrastructure, not user-facing state changes. Skip Phase 0.8.

---

## Phase 1: Orientation State Model

### Objective
Create data model for Piper's orientation state per Arch decision.

### Agent Deployment
**Single Agent (Lead Developer)** - Tightly coupled dataclass work

### Tasks (per Arch structure)
- [ ] Create `services/mux/orientation.py`
- [ ] Define `OrientationPillarType` enum (IDENTITY, TEMPORAL, SPATIAL, AGENCY, PREDICTION)
- [ ] Define `OrientationPillar` dataclass per Arch spec:
  ```python
  @dataclass
  class OrientationPillar:
      pillar_type: OrientationPillarType
      lens_applied: str  # Which lens produced this perception
      perception: str    # What Piper perceives
      confidence: float
      source_context: str  # Where this came from (for debugging/audit)
  ```
- [ ] Define `OrientationState` dataclass per Arch spec:
  ```python
  @dataclass
  class OrientationState:
      identity: OrientationPillar      # Lens: self-awareness
      temporal: OrientationPillar      # Lens: temporal
      spatial: OrientationPillar       # Lens: contextual + place
      agency: OrientationPillar        # Lens: priority
      prediction: OrientationPillar    # Lens: causal (anticipating)
      situation_frame: Optional[str] = None
      trust_context: Optional["TrustContext"] = None
  ```
- [ ] Implement `OrientationState.gather()` classmethod per Arch spec
- [ ] Implement private `_perceive_*` methods for each pillar
- [ ] Add grammar-aligned docstrings (Entity, Perception, Situation, Lens vocabulary)

### Deliverables
- `services/mux/orientation.py` (new file)
- `tests/unit/services/mux/test_orientation.py` (≥10 tests)

### Acceptance Criteria (Phase 1)
- [ ] OrientationPillarType enum with 5 values
- [ ] OrientationPillar captures pillar_type, lens_applied, perception, confidence, source_context
- [ ] OrientationState has all 5 pillar fields + trust_context
- [ ] OrientationState.gather() constructs from available context
- [ ] Grammar-aligned docstrings reference ADR-055
- [ ] 10+ unit tests passing

---

## Phase 2: Articulation & Surfacing

### Objective
Create articulation layer that transforms orientation into natural language per CXO guidance.

### Agent Deployment
**Single Agent (Lead Developer)** - Sequential integration work

### Tasks (per CXO guidance)
- [ ] Add `articulate()` method to OrientationState or create ArticulationService
- [ ] Implement trust-aware surfacing logic:
  - Stage 1: Never surface unprompted (internal only)
  - Stage 2: Reactive-contextual (respond to "help" with informed options)
  - Stage 3+: Proactive-contextual ("I notice..." OK)
  - Stage 4: Anticipatory
- [ ] Implement articulation patterns per CXO:
  - Identity: "I'm here to help with [context]"
  - Temporal: "It's [time] — [implication]"
  - Spatial: "We're in [place], working on [topic]"
  - Agency: "Your top priority looks like [X]" (NOT "seems to be")
  - Prediction: "I can [relevant capabilities]"
- [ ] Implement channel adaptation:
  - Web: Full narrative
  - Slack: Compressed ("Busy morning — standup in 30")
- [ ] Use observational for inferences, declarative for facts

### Deliverables
- Articulation logic in `services/mux/orientation.py` (or new file)
- `tests/unit/services/mux/test_articulation.py` (≥8 tests)

### Acceptance Criteria (Phase 2)
- [ ] Trust-aware surfacing respects stage thresholds
- [ ] Articulation uses "looks like" not "seems to be"
- [ ] Channel adaptation works (web vs Slack)
- [ ] Observational/declarative distinction implemented
- [ ] 8+ unit tests passing

---

## Phase 3: Recognition Option Generation

### Objective
Generate recognition options from orientation state per CXO Option C (narrative) guidance.

### Agent Deployment
**Single Agent (Lead Developer)** - Builds on Phase 2

### Tasks (per CXO guidance)
- [ ] Define `RecognitionOption` dataclass
- [ ] Implement `generate_options(orientation, trust_stage, channel)` method
- [ ] Use Option C (narrative) framing - sounds like colleague, not menu:
  - Web: "It looks like a busy morning. Standup's in 30 minutes, and there's that API PR waiting. Want help with either, or should we check your priority list?"
  - Slack: "Busy morning — standup in 30, API PR waiting. Help with either?"
- [ ] Rank options by relevance (2-4 options)
- [ ] Add "escape hatch" per trust level:
  - Stage 1-2: Always offer "...or something else entirely?"
  - Stage 3-4: Optional (trusted users know they can redirect)
- [ ] Use open language: "Which feels most useful?" not "Select one"
- [ ] Framing varies by trust:
  - Stage 1-2: Explicit option offering ("Which would be helpful?")
  - Stage 3-4: Assumptive ("Want me to start with standup prep?")

### Deliverables
- Recognition option generation in `services/mux/orientation.py`
- `tests/unit/services/mux/test_recognition_options.py` (≥5 tests)

### Acceptance Criteria (Phase 3)
- [ ] RecognitionOption dataclass with label, description, intent
- [ ] Option C (narrative) framing implemented
- [ ] Trust-aware escape hatch logic
- [ ] Channel-appropriate compression
- [ ] 2-4 option limit enforced
- [ ] 5+ unit tests passing

---

## Phase 4: Pipeline Integration

### Objective
Integrate orientation into intent processing pipeline per Arch guidance.

### Agent Deployment
**Single Agent (Lead Developer)** - Careful integration work

### Tasks (per Arch integration point decision)
- [ ] Integration point: After PlaceDetector, before IntentClassifier
  ```
  Request
    → PlaceDetector
    → OrientationState.gather()    ← HERE
    → IntentClassifier
    → Handler
  ```
- [ ] Modify intent processing to call OrientationState.gather()
- [ ] Pass orientation to handlers for:
  1. Classification context (what Piper thinks you're asking)
  2. Response framing (how Piper should communicate)
- [ ] Ensure no breaking changes to existing flow
- [ ] Add integration test

### Deliverables
- Modified `services/intent_service/classifier.py` or entry point (minimal changes)
- Integration test verifying orientation flows through

### Acceptance Criteria (Phase 4)
- [ ] Orientation computed after PlaceDetector, before IntentClassifier
- [ ] OrientationState passed to handlers
- [ ] Existing flow unchanged for cases without orientation
- [ ] No regression in intent classification tests
- [ ] Integration test passing
- [ ] <50ms latency impact

---

## Phase Z: Final Bookending & Handoff

### Required Actions

1. **Test Verification**
   ```bash
   # Run all new MUX orientation tests
   python -m pytest tests/unit/services/mux/test_orientation*.py tests/unit/services/mux/test_articulation.py tests/unit/services/mux/test_recognition*.py -v

   # Run all MUX tests (no regression)
   python -m pytest tests/unit/services/mux/ -v

   # Run intent service tests (integration, no regression)
   python -m pytest tests/unit/services/intent_service/ -v

   # Full unit test suite
   python -m pytest tests/unit/ -v
   ```

2. **GitHub Final Update**
   - All acceptance criteria checkboxes checked
   - Completion matrix filled with evidence
   - Evidence section populated

3. **Documentation**
   - [ ] Docstrings complete with grammar vocabulary (Entity, Perception, Situation, Lens)
   - [ ] Reference ADR-055 in OrientationState docstring
   - [ ] Session log documents decisions
   - [ ] Write "experience" paragraph per Arch guidance (does it help Piper *experience* where it is?)

4. **Handoff to #411 and #412**
   - Document how orientation feeds recognition patterns
   - Note CXO articulation decisions for downstream
   - Document trust-aware surfacing thresholds

### Evidence Required
- Test counts and output
- Performance measurement (<50ms)
- No regression proof
- "Experience" check paragraph

---

## Multi-Agent Coordination Plan

### Agent Deployment Map

| Phase | Agent | Evidence Required |
|-------|-------|-------------------|
| 0 | Lead Dev | Investigation notes |
| 1 | Lead Dev | 10+ tests, `services/mux/orientation.py` |
| 2 | Lead Dev | 8+ tests, articulation logic |
| 3 | Lead Dev | 5+ tests, recognition options |
| 4 | Lead Dev | Integration test, no regression |
| Z | Lead Dev | Full test suite, documentation, "experience" check |

### Verification Gates
- [ ] Phase 1: OrientationState tests passing (≥10)
- [ ] Phase 2: Articulation tests passing (≥8)
- [ ] Phase 3: Recognition option tests passing (≥5)
- [ ] Phase 4: Integration test passing, no regression
- [ ] Phase Z: Full suite passing, documentation complete, "experience" check written

---

## STOP Conditions

Stop immediately and escalate if:
- Existing orientation/context system found (complete it instead)
- ADR-039 architecture incompatible
- Canonical handlers require significant modification
- Performance impact exceeds 100ms
- Intent classification accuracy degrades
- Import/method errors in integration

---

## Success Criteria

### Issue Completion Requires
- [ ] OrientationState captures all 5 pillars
- [ ] OrientationService computes orientation per request
- [ ] Recognition options generated from orientation
- [ ] Pipeline integration complete
- [ ] ≥23 new tests passing
- [ ] No regression in existing tests
- [ ] <50ms latency impact
- [ ] Documentation complete
- [ ] PM approval received

---

## Estimated Effort

| Phase | Estimate |
|-------|----------|
| Phase 0 | 1 hour |
| Phase 1 | 2-3 hours |
| Phase 2 | 2-3 hours |
| Phase 3 | 1-2 hours |
| Phase 4 | 2 hours |
| Phase Z | 1 hour |
| **Total** | **10-12 hours** |

---

_Gameplan created: 2026-01-23_
_Template version: v9.3_
