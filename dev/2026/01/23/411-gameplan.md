# Gameplan: #411 MUX-INTERACT-RECOGNITION

**Issue**: #411 MUX-INTERACT-RECOGNITION
**Created**: 2026-01-23
**Agent**: Lead Developer (single agent - sequential work)

---

## Overview

Build the recognition UI layer that presents contextual options to users when intent classification has low confidence. This builds on #410's orientation system (RecognitionOptions) to create the user-facing recognition experience.

**Core Insight**: Recognition > Recall. ~50% of users struggle to articulate precise queries. We help them recognize from context-aware options.

---

## Phase -1: Pre-Validation (Auto-STOP)

Before any work:
- [x] GitHub issue exists: #411 ✅
- [x] Issue assigned to milestone: I2 ✅
- [x] Dependencies complete: #410 (orientation) ✅ CLOSED
- [x] No blocking issues discovered

---

## Phase 0: Investigation & Setup

**Objective**: Understand existing infrastructure and integration points

### Tasks
1. [ ] Review RecognitionOptions API from #410
   - RecognitionOption dataclass
   - RecognitionOptions dataclass
   - RecognitionGenerator.generate()
   - RecognitionGenerator.format_for_display()

2. [ ] Review pre_classifier.py confidence scoring
   - How confidence is computed
   - Current thresholds used

3. [ ] Map integration point in intent pipeline
   - Where recognition should trigger
   - How to return recognition response vs normal response

4. [ ] Document integration approach

### Deliverables
- Investigation notes in session log
- Integration approach documented

### STOP Conditions
- RecognitionOptions API unavailable or broken
- Pre-classifier confidence unavailable
- Pipeline architecture unclear

---

## Phase 0.7: Conversation Design

**Purpose**: Recognition is conversational - user sees options, makes selection

### Part A: Happy Path Script

```
Turn 1:
  User: "check on things"
  [Low confidence detected, triggers recognition]
  Piper: "I can check a few things for you:
    • Your standup status (meeting in 45 min)
    • The API PR waiting for review
    • Your todo list for today

  Which would help most? Or something else entirely?"
  State: NORMAL → RECOGNITION_OFFERED

Turn 2a (Selection):
  User: "standup"
  Piper: [Routes to standup handler, returns standup result]
  State: RECOGNITION_OFFERED → NORMAL

Turn 2b (None of these):
  User: "something else"
  Piper: "Sure! What would be most helpful right now?"
  State: RECOGNITION_OFFERED → CLARIFYING

Turn 3 (After clarification):
  User: "check my email"
  Piper: [Attempts normal classification with clarified input]
  State: CLARIFYING → NORMAL
```

### Part B: Edge Cases Table

| User Input | Current State | Expected Behavior | Response |
|------------|---------------|-------------------|----------|
| Exact option match ("standup") | RECOGNITION_OFFERED | Route to handler | Handler response |
| Partial match ("stand") | RECOGNITION_OFFERED | Accept as match | Handler response |
| "none" / "something else" | RECOGNITION_OFFERED | Prompt clarification | "What would help?" |
| Numeric selection ("1") | RECOGNITION_OFFERED | Accept by position | Handler response |
| New query unrelated | RECOGNITION_OFFERED | Treat as new input | Re-classify |
| Empty/whitespace | RECOGNITION_OFFERED | Re-show options | Repeat options |

### Part C: State Machine

```
NORMAL
    └── [low confidence] → RECOGNITION_OFFERED

RECOGNITION_OFFERED
    ├── [select option] → NORMAL (execute handler)
    ├── [none of these] → CLARIFYING
    └── [new unrelated query] → NORMAL (re-classify)

CLARIFYING
    ├── [clear input] → NORMAL (re-classify)
    └── [still unclear] → RECOGNITION_OFFERED (may loop once)
```

### Part D: Design Decisions

1. **No trust penalty for "none of these"** - User clarifying is positive engagement
2. **One loop maximum** - If still unclear after clarification, use best guess or fall back
3. **Selection matching is fuzzy** - "stand" matches "standup status"
4. **Numeric selection allowed** - "1" selects first option

---

## Phase 1: Recognition Response Service

**Objective**: Create service that formats recognition options for user presentation

### Tasks
1. [ ] Create `services/mux/recognition_response.py`

2. [ ] Implement `RecognitionResponseService`:
   ```python
   class RecognitionResponseService:
       def format_for_channel(recognition: RecognitionOptions, config: ArticulationConfig) -> str
       def format_for_web(recognition: RecognitionOptions) -> str
       def format_for_slack(recognition: RecognitionOptions) -> str
       def handle_selection(selection: str, options: RecognitionOptions) -> Optional[str]
       def handle_none_of_these() -> str
   ```

3. [ ] Implement channel-specific formatting:
   - Web: Full narrative with explanation
   - Slack: Compressed format

4. [ ] Implement trust-aware language:
   - Stage 1-2: More cautious phrasing
   - Stage 3+: More confident suggestions

5. [ ] Create unit tests
   - Test channel formatting
   - Test option limit
   - Test escape hatch presence
   - Test trust-aware language

### Deliverables
- `services/mux/recognition_response.py`
- `tests/unit/services/mux/test_recognition_response.py` (≥15 tests)

### Acceptance Criteria
- [ ] Channel formatting works (web vs Slack)
- [ ] Option limit (2-4) enforced
- [ ] Escape hatch always present
- [ ] Trust-aware language applied
- [ ] All tests passing

---

## Phase 2: Pipeline Integration

**Objective**: Integrate recognition triggering into intent classification

### Tasks
1. [ ] Define confidence threshold (recommend 0.6 or 0.7)

2. [ ] Create `RecognitionTrigger` class:
   ```python
   class RecognitionTrigger:
       def should_trigger(confidence: float, context: IntentClassificationContext) -> bool
       def generate_recognition(context: IntentClassificationContext) -> RecognitionOptions
   ```

3. [ ] Modify `classify_conscious()` or create wrapper:
   - Check confidence after classification
   - If below threshold, generate recognition
   - Return recognition response

4. [ ] Handle recognition state in conversation:
   - Track that recognition was offered
   - Enable selection handling

5. [ ] Create unit tests for triggering logic

### Deliverables
- `services/mux/recognition_trigger.py` or modified classifier
- Integration tests

### Acceptance Criteria
- [ ] Low confidence triggers recognition
- [ ] High confidence bypasses recognition
- [ ] Recognition state tracked

---

## Phase 3: Handler Integration

**Objective**: Handle user selection from recognition options

### Tasks
1. [ ] Create recognition selection handler:
   ```python
   def handle_recognition_selection(selection: str, original_message: str, context: Dict) -> Response
   ```

2. [ ] Route selection to appropriate intent handler

3. [ ] Handle "none of these" flow:
   - Prompt for clarification
   - Don't penalize in trust computation

4. [ ] Create end-to-end test

### Deliverables
- Recognition handler integration
- E2E test

### Acceptance Criteria
- [ ] Selection routes to correct handler
- [ ] "None of these" prompts clarification
- [ ] No trust penalty for clarification

---

## Phase Z: Final Bookending & Handoff

### Tasks
1. [ ] Run full test suite - verify no regressions
2. [ ] Update GitHub issue description:
   - Check all acceptance criteria boxes
   - Fill completion matrix with evidence
   - Add test output to evidence section
3. [ ] Add closing comment with implementation summary
4. [ ] "Experience" check: Does recognition feel helpful?
5. [ ] Update session log

### Verification Command
```bash
python -m pytest tests/unit/services/mux/test_recognition*.py -v
python -m pytest tests/unit/services/intent_service/ -v
python -m pytest tests/unit/ -v
```

### STOP Conditions
- Any test failures
- Latency exceeds 100ms
- Recognition feels corrective, not helpful

---

## Success Criteria

### Quantitative
- ≥20 new tests
- <100ms latency for recognition
- 0 test regressions

### Qualitative
- Options feel contextually relevant
- Language sounds helpful, not corrective
- User can always escape to clarification

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| RecognitionOptions API changed | Review #410 code first |
| Confidence scoring unclear | Document during Phase 0 |
| Pipeline integration complex | Small changes, test frequently |
| Recognition feels "corrective" | Use CXO-approved language patterns |

---

## Estimated Effort

- Phase 0: 1 hour (investigation)
- Phase 1: 2-3 hours (service + tests)
- Phase 2: 2-3 hours (integration)
- Phase 3: 1-2 hours (handler)
- Phase Z: 1 hour (verification)
- **Total**: 7-10 hours

---

## Agent Notes

- Single agent (sequential work, tightly coupled to #410)
- Build on RecognitionOptions, don't reinvent
- Use CXO language patterns ("I can help with..." not "Did you mean...")
- Test incrementally - each phase should have passing tests

---

_Gameplan created: 2026-01-23_
_Template version: 9.3_
