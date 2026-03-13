# Gameplan: #763 GLUE-FOLLOWUP — Follow-up Recognition with Lens Inheritance

**Issue**: #763
**Branch**: `claude/m0-conversational-glue`
**Sprint**: M0 — Conversational Glue
**Sequence**: #766 ✅ → **#763** → #765 → #764 → #767 → #779

---

## Phase -1: Infrastructure Verification

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (confirmed)
- [x] Database: PostgreSQL 5433 (confirmed)
- [x] Testing framework: pytest (confirmed)
- [x] Follow-up detection: Working in `services/intent_service/conversation_context.py`
- [x] Intent classifier: `services/intent_service/classifier.py` with `classify_conscious()`
- [x] ConversationContext (rich): `services/intent_service/conversation_context.py` — has `last_intent`, `last_topic`, `last_temporal_reference` but NO `current_lens`
- [x] Reference resolver: `services/conversation/reference_resolver.py` — handles pronouns/entities
- [x] MUX lens system: `services/mux/lenses/` — perception lenses, NOT conversational lens tracking

**My understanding of the task**:
- Add conversational lens tracking to enable follow-up queries to inherit "what aspect the user is asking about"
- Currently "What about Thursday?" works (temporal shift) but "Tell me more" and "And Sarah?" fail (no lens context)
- Hybrid approach: keep rule-based patterns for simple cases, add LLM lens decoder for complex follow-ups
- Add `current_lens` + `lens_stack` to ConversationContext
- Wire through existing classifier → personality bridge pipeline

### Part A.2: Work Characteristics

**Worktree Assessment**: SKIP WORKTREE
- Single agent (Lead Developer), sequential work
- Tightly coupled files (ConversationContext → classifier → follow-up resolution)
- Already on sprint branch `claude/m0-conversational-glue`

### Part B: PM Verification (COMPLETED IN DISCUSSION)

- PM confirmed: All 4 reference types in scope (pronouns, elliptical, comparative, temporal)
- PM confirmed: Build test corpus for accuracy measurement
- PM confirmed: Single `current_lens` + `lens_stack` (not simultaneous multi-lens)
- PM confirmed: Hybrid approach (rules for simple, LLM for complex)

### Part C: Proceed/Revise

- [x] **PROCEED** — Understanding confirmed through discussion

---

## Phase 0: Initial Bookending

**Issue verified**: #763 exists, assigned to mediajunkie, labeled PDR-002/glue, parent epic #762.

**Codebase investigation complete** (see `dev/2026/02/16/763-issue-audit.md`):

### What Already Exists ✅

| Component | Location | What It Does |
|-----------|----------|--------------|
| Follow-up detection | `conversation_context.py:145-215` | Pattern-matches 6 follow-up types (TEMPORAL_SHIFT, ENTITY_REFERENCE, CONFIRMATION, REFINEMENT, CONTINUATION, NEGATION) |
| Follow-up resolution | `conversation_context.py:218-290` | Inherits intent category/action from last turn, updates temporal/entity context |
| Rich ConversationContext | `conversation_context.py` | Tracks `last_intent`, `last_topic`, `last_temporal_reference`, 10-turn window |
| Classifier integration | `classifier.py:453-472` | `classify_conscious()` checks follow-ups first, skips LLM if resolved |
| Reference resolver | `reference_resolver.py` | Resolves "it", "that", "the meeting" to specific entities |
| Context tracker | `context_tracker.py` | Tracks `current_topic`, `active_entities`, `user_intent_history` |
| Follow-up tests | `test_classifier_follow_up.py` | Tests temporal inheritance, confirmations, continuations |

### What's Missing ❌

1. `current_lens` field on ConversationContext
2. `lens_stack` for topic digression/restoration
3. Lens inference from intent (e.g., `meeting_time` → `calendar` lens)
4. LLM lens decoder for complex follow-ups
5. Lens inheritance in `resolve_follow_up()`
6. Lens-aware intent classification bias
7. Lens reset detection for explicit topic changes
8. Test corpus (30-50 conversation pairs)

### Existing Follow-Up Coverage vs. #763 Requirements

| Scenario Type | Rules Today | After #763 |
|--------------|-------------|------------|
| Temporal shift ("What about Thursday?") | ✅ Works | ✅ + lens |
| Temporal + topic ("next week's tasks?") | ✅ Works | ✅ + lens |
| Lens shift within topic ("Who's attending?") | ❌ Falls to LLM | ✅ LLM lens decoder |
| Parameter modification ("And the closed ones?") | ⚠️ Partial | ✅ LLM lens decoder |
| Continuation needing lens ("Tell me more") | ❌ Matches but loses context | ✅ Lens inheritance |
| Elliptical + pronoun ("And Sarah?") | ❌ Falls to LLM | ✅ LLM lens decoder |
| Action shift within lens ("Cancel the 2pm") | ❌ Falls to LLM | ✅ Lens-aware classification |
| Pronoun + lens shift ("Who owns that?") | ❌ Falls to LLM | ✅ LLM lens decoder |

---

## Phase 0.6: Data Flow & Integration Verification

### Data Flow: Lens Through the Pipeline

```
User message
  → classify_conscious() [classifier.py]
    → detect_follow_up() [conversation_context.py]  ← ADD: lens inheritance
    → (if no follow-up) classify() → LLM             ← ADD: lens context in prompt
    → extract_lens() [NEW]                            ← ADD: infer lens from result
    → add_turn() with lens [conversation_context.py]  ← ADD: store lens
  → IntentClassificationContext [intent_types.py]     ← ADD: current_lens field
  → personality_bridge.transform()                    ← receives lens via context
  → Response to user
```

### Integration Points

| Caller | Callee | What Changes |
|--------|--------|-------------|
| `classify_conscious()` | `detect_follow_up()` | Pass lens context, get lens-aware resolution |
| `classify_conscious()` | `add_turn()` | Store lens with each turn |
| `resolve_follow_up()` | (returns Intent) | Include `lens` in intent context dict |
| `classify_conscious()` | `classify()` | Include lens in LLM system prompt for bias |
| `ConversationContext` | (properties) | Add `current_lens`, `lens_stack` properties |

### Post-Completion Integration (Phase 0.8)

Lens tracking is **entirely in-memory** on `ConversationContext` (lives in the classifier's session dict, same as existing follow-up state). No database migrations, no schema changes, no persistence side-effects. Lens state expires with the 30-minute session timeout, same as existing conversation context.

**No downstream behavior changes to other features** — lens is additive context that enriches follow-up resolution. Features that don't use follow-ups are unaffected.

### Pattern Adaptation: Following Existing Follow-Up Pattern

| Aspect | Existing Follow-Up | Lens Enhancement | Why Different? |
|--------|-------------------|------------------|----------------|
| Detection | Regex patterns | Regex + LLM fallback | Lens shifts can't be pattern-matched |
| Resolution | Inherit category/action | Inherit category/action + lens | Lens is additional context dimension |
| Storage | `temporal_reference` in turn | `lens` in turn | Same mechanism, new field |
| Retrieval | `last_temporal_reference` property | `current_lens` property | Same pattern |

---

## Phase 0.7: Conversation Design

### Part A: Happy Path Scripts

**Script 1: Calendar lens inheritance (temporal shift)**
```
Turn 1: User: "What's on my calendar tomorrow?"
        Lens: calendar → action: meeting_time
Turn 2: User: "What about Thursday?"
        Lens: calendar (inherited) → temporal updated to Thursday
        ✅ Shows Thursday calendar
```

**Script 2: Calendar lens with nested question**
```
Turn 1: User: "What's on my calendar tomorrow?"
        Lens: calendar → action: meeting_time
Turn 2: User: "Who's in the standup?"
        Lens: calendar.attendance (shift within topic) → LLM decodes
        ✅ Shows standup attendees
Turn 3: User: "What about Thursday?"
        Lens: calendar (restored from stack) → temporal shift
        ✅ Shows Thursday calendar
```

**Script 3: Elliptical follow-up**
```
Turn 1: User: "How's the Alpha project going?"
        Lens: project_status → entity: Alpha
Turn 2: User: "And Sarah?"
        Lens: project_status (inherited) → entity: Sarah
        ✅ Shows Sarah's involvement in Alpha
```

**Script 4: Explicit lens reset**
```
Turn 1: User: "What's on my calendar tomorrow?"
        Lens: calendar
Turn 2: User: "Actually, show me my open issues"
        Lens: issues (explicit change — new topic, new lens)
        ✅ Shows open issues, calendar lens cleared
```

### Part B: Edge Cases

| User Input | Previous Lens | Expected Behavior |
|------------|---------------|-------------------|
| "Tell me more" | calendar | Expand calendar details (more meetings, notes) |
| "Tell me more" | (none) | "More about what? I can help with..." |
| "What about Thursday?" | (none) | Ambiguous — treat as new query, classify normally |
| "Cancel the 2pm" | calendar | Action shift within lens — keep calendar context |
| "Never mind" | any | Clear lens, return to neutral |

### Part C: Lens Types for MVP

Based on Piper's current capabilities:

```python
class ConversationalLens(str, Enum):
    CALENDAR = "calendar"          # Schedule, meetings, availability
    ISSUES = "issues"              # Tasks, bugs, work items
    PROJECTS = "projects"          # Project status, progress
    PEOPLE = "people"              # Team, contacts, availability
    GENERAL = "general"            # No specific lens
```

### Part D: Lens Lifecycle

```
NO LENS (initial state)
    ├── [explicit query] → LENS SET (inferred from intent)
    └── [greeting/chat] → NO LENS (stays neutral)

LENS SET
    ├── [follow-up, same domain] → LENS INHERITED (carry forward)
    ├── [follow-up, sub-topic] → LENS PUSHED (push current, set new)
    ├── [explicit new topic] → LENS RESET (clear stack, set new)
    ├── [back to previous] → LENS POPPED (restore from stack)
    └── [30min timeout] → NO LENS (session expired)
```

---

## Phase 1: ConversationContext Extension + Test Corpus

**Objective**: Add lens tracking to ConversationContext and build the test corpus that defines our acceptance criteria.

**Tasks**:
- [ ] Add `lens: Optional[str]` field to `ConversationTurn` dataclass
- [ ] Add `current_lens` property to `ConversationContext` (returns last turn's lens)
- [ ] Add `lens_stack: List[str]` field to `ConversationContext` for digression tracking
- [ ] Create `ConversationalLens` enum in `services/shared_types.py`
- [ ] Build test corpus: 40+ conversation pairs covering all 4 reference types
- [ ] Write baseline test: run corpus through existing system, measure current pass rate

**Files modified**:
- `services/intent_service/conversation_context.py` — ConversationTurn, ConversationContext
- `services/shared_types.py` — ConversationalLens enum
- `tests/unit/services/intent_service/test_lens_corpus.py` — New test corpus

**Deliverables**:
- ConversationContext with lens fields (backward compatible — lens defaults to None)
- Test corpus with expected behaviors documented
- Baseline measurement: "X% of corpus passes today"

**STOP if**: Existing ConversationContext changes break follow-up tests

---

## Phase 2: Lens Extraction + Rule-Based Enhancement

**Objective**: Infer lens from classified intents and enhance rule-based follow-up resolution with lens inheritance.

**Tasks**:
- [ ] Create `extract_lens_from_intent(intent: Intent) -> Optional[str]` function
- [ ] Map intent categories/actions → lens types (rule-based mapping table)
- [ ] Update `resolve_follow_up()` to inherit lens from previous turn
- [ ] Update `add_turn()` to store lens with each turn
- [ ] Update `classify_conscious()` to call `extract_lens()` after classification
- [ ] Write unit tests for lens extraction and inheritance

**Files modified**:
- `services/intent_service/conversation_context.py` — resolve_follow_up, add_turn
- `services/intent_service/classifier.py` — classify_conscious
- `services/intent_service/lens_inference.py` — New file: extract_lens_from_intent
- `tests/unit/services/intent_service/test_lens_inference.py` — New tests

**Wiring Tests** (per gameplan-template v9.3):
- [ ] Verify `classify_conscious()` → `extract_lens()` → `add_turn()` → `current_lens` property chain with real objects (not mocked internals)
- [ ] Verify lens flows through `IntentClassificationContext` to personality bridge

**Deliverables**:
- Lens automatically extracted from every classified intent
- Rule-matched follow-ups inherit lens from previous turn
- Wiring tests prove lens propagates through real code path
- Corpus improvement: from baseline to ~60% (temporal shifts + confirmations + lens)

**STOP if**: classify_conscious() changes break existing follow-up tests

---

## Phase 3: LLM Lens Decoder for Complex Follow-Ups

**Objective**: Add LLM-based follow-up resolution for cases rules can't handle (elliptical, comparative, lens shifts).

**Tasks**:
- [ ] Create `decode_follow_up_with_llm(message, context_turns, current_lens) -> Intent` function
- [ ] Design minimal LLM prompt: last 2-3 turns + current message → structured output (is_follow_up, lens, action, entities)
- [ ] Integrate into `classify_conscious()`: rules first → LLM decoder if no match but lens active → full classify if no lens
- [ ] Add lens context to normal `classify()` LLM prompt for lens-aware bias
- [ ] Write tests for LLM decoder (mock LLM responses for deterministic testing)
- [ ] Run corpus: measure improvement

**Files modified**:
- `services/intent_service/classifier.py` — classify_conscious flow
- `services/intent_service/lens_inference.py` — decode_follow_up_with_llm
- `tests/unit/services/intent_service/test_lens_llm_decoder.py` — New tests

**Decision flow in classify_conscious()**:
```
1. Check for active guided process (ProcessRegistry) → return if handled
2. Check rule-based follow-up patterns → return if matched (+ lens inheritance)
3. IF current_lens active AND message is short/ambiguous:
   → LLM lens decoder (lightweight, 2-3 turns context)
   → return if decoded as follow-up
4. Full classify() with lens context in system prompt
5. Extract lens from result, store in turn
```

**Deliverables**:
- LLM decoder handles elliptical, comparative, and lens-shift follow-ups
- Corpus improvement: from ~60% to target >85%
- Latency: rule-matched paths unchanged, LLM decoder adds ~200-500ms only when needed

**STOP if**: LLM decoder latency exceeds 1 second, or prompt costs are unreasonable

---

## Phase 4: Lens Reset + Stack + Edge Cases

**Objective**: Handle explicit topic changes, lens stacking for digressions, and edge cases.

**Tasks**:
- [ ] Implement lens reset detection (explicit new topic clears lens)
- [ ] Implement lens stack push/pop for nested topics
- [ ] Handle "no lens" state gracefully (don't force lens inference on greetings/chat)
- [ ] Handle 30-minute session timeout (clear lens)
- [ ] Handle lens ambiguity ("Tell me more" with no lens → ask for clarification)
- [ ] Run full corpus: measure final pass rates

**Files modified**:
- `services/intent_service/conversation_context.py` — lens stack logic
- `services/intent_service/lens_inference.py` — reset detection
- `tests/unit/services/intent_service/test_lens_edge_cases.py` — New tests

**Deliverables**:
- Lens persists across 3+ follow-up turns ✅
- Explicit topic change resets lens ✅
- Corpus pass rates: >90% for "What about X?" inheritance, >85% for elliptical/comparative

---

## Phase 5: Colleague Test + Integration

**Objective**: Verify the system feels natural in conversation, not just correct in tests.

**Tasks**:
- [ ] Run colleague test: 6 scenarios (the 8 from analysis minus the 2 that already work)
- [ ] Verify lens doesn't leak into unrelated conversations (session isolation)
- [ ] Verify lens doesn't interfere with onboarding/guided processes (ProcessRegistry takes precedence)
- [ ] Run full unit test suite — no regressions
- [ ] Run E2E onboarding tests — no regressions from #766

**Colleague Test Scenarios**:
1. Calendar → "What about Thursday?" (temporal + lens)
2. Calendar → "Who's attending?" (lens shift within topic)
3. Issues → "And the closed ones?" (parameter modification)
4. Project status → "And Sarah?" (elliptical)
5. Calendar → "Cancel the 2pm" (action shift within lens)
6. Blockers → "Who owns that?" (pronoun + lens shift)

**Deliverables**:
- All 6 scenarios produce natural, correct responses
- No regressions in existing test suite
- Passes Colleague Test acceptance criterion

---

## Phase Z: Completion & Handoff

- [ ] All acceptance criteria met with evidence
- [ ] Test corpus results documented (pass rates per category)
- [ ] Commit on `claude/m0-conversational-glue` branch
- [ ] GitHub issue #763 updated with implementation evidence
- [ ] Session log updated
- [ ] Handoff notes for #765 (GLUE-PARKED: Parked workflow awareness)

---

## Acceptance Criteria Mapping

| Criterion | Phase | Measurement |
|-----------|-------|-------------|
| "What about X?" queries inherit lens >90% | Phase 4 | Corpus: temporal_shift + entity_reference categories |
| Elliptical phrases expand correctly >85% | Phase 4 | Corpus: elliptical category |
| Comparative queries resolve >85% | Phase 4 | Corpus: comparative category |
| Lens persists across ≥3 follow-up turns | Phase 4 | Dedicated 4-turn test sequences in corpus |
| Explicit topic change resets lens | Phase 4 | Corpus: lens_reset category |
| Passes Colleague Test | Phase 5 | 6 scenarios, human-verified |

---

## STOP Conditions

- Existing follow-up tests break after ConversationContext changes
- LLM lens decoder latency exceeds 1 second consistently
- Lens inference causes regressions in normal (non-follow-up) classification
- ProcessRegistry/onboarding interaction breaks
- Corpus results plateau significantly below targets after Phase 3

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| LLM decoder adds too much latency | Low | High | Only called when rules don't match AND lens is active |
| Lens inference is wrong for edge cases | Medium | Medium | Test corpus catches these; graceful fallback to "no lens" |
| ConversationContext changes break existing tests | Low | High | Backward compatible (lens defaults to None) |
| 85% accuracy target too ambitious for MVP | Medium | Low | Corpus defines what "85%" means concretely; adjust if needed |

---

## Effort Estimate

- Phase 1: 0.5 day (context extension + corpus)
- Phase 2: 0.5 day (lens extraction + rule enhancement)
- Phase 3: 1 day (LLM decoder — prompt design is the hard part)
- Phase 4: 0.5 day (reset/stack/edge cases)
- Phase 5: 0.5 day (colleague test + integration)
- Phase Z: 0.25 day

**Total: ~3.25 days** (within 3-5 day estimate)
