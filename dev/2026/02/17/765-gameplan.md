# Gameplan: #765 GLUE-SLOTFILL — Natural Slot Filling Without Interrogation

**Issue**: #765
**Branch**: `claude/m0-conversational-glue`
**Depends on**: #763 ✅ (lens system), #766 ✅ (ProcessRegistry)
**Estimated effort**: 2-3 days
**Date**: 2026-02-17

---

## Phase -1: Infrastructure Verification ✅

**Completed via investigation** (see `dev/2026/02/17/765-issue-audit.md` and session log 1:05 entry).

**Infrastructure Status**:
- [x] Web framework: FastAPI
- [x] ProcessRegistry: `services/process/registry.py` — operational, accepts new ProcessType handlers
- [x] GuidedProcess Protocol: operational, used by onboarding + standup
- [x] State machines: PortfolioOnboardingState (5 states), StandupConversationState (7 states)
- [x] Adapter pattern: `services/process/adapters.py` — template exists
- [x] Testing framework: pytest with async support
- [x] ConversationContext: 10-turn window, lens tracking (#763)

**Understanding of the task**:
- Build a reusable slot-filling framework that any workflow can use
- Framework handles: multi-slot extraction, skip-filled-slots, grouped prompting
- Integrates with ProcessRegistry as a Tier 1 handler
- First consumer: a "schedule meeting" demo workflow (proves the framework works)

**Worktree Assessment**: SKIP — single agent, sequential work, same branch as #763.

---

## Phase 0.7: Conversation Design

### Happy Path Script

```
Turn 1:
  User: "Set up a meeting with Sarah Tuesday at 2pm"
  [classify_conscious() → intent: EXECUTION/schedule_meeting]
  [SlotFilling activates: template "schedule_meeting" has 4 slots]
  [Multi-slot extraction: attendee=Sarah, day=Tuesday, time=2pm, topic=?]
  Piper: "Got it — meeting with Sarah, Tuesday at 2pm. What's the topic?"
  State: EXTRACTING → PROMPTING (1 missing required slot)

Turn 2:
  User: "Q3 planning"
  [SlotFilling handles: extracts topic=Q3 planning]
  [All required slots filled → confirmation]
  Piper: "Done — Q3 planning with Sarah, Tuesday at 2pm. Want me to send the invite?"
  State: PROMPTING → CONFIRMING

Turn 3:
  User: "Yes"
  Piper: "Invite sent!"
  State: CONFIRMING → COMPLETE
```

### Partial Input Script (user gives minimal info)

```
Turn 1:
  User: "Schedule a meeting"
  [classify_conscious() → intent: EXECUTION/schedule_meeting]
  [SlotFilling activates: template "schedule_meeting" has 4 slots]
  [Multi-slot extraction: no slots filled]
  Piper: "Sure! Who should attend, and when works?"
  State: EXTRACTING → PROMPTING (grouped: attendee + time)

Turn 2:
  User: "Sarah and Jake, Thursday morning"
  [SlotFilling: attendee=[Sarah, Jake], day=Thursday, time=morning, topic=?]
  Piper: "Meeting with Sarah and Jake, Thursday morning. What's the topic?"
  State: PROMPTING → PROMPTING (1 remaining)

Turn 3:
  User: "Sprint review"
  Piper: "Sprint review with Sarah and Jake, Thursday morning. Sound good?"
  State: PROMPTING → CONFIRMING
```

### Slot Update Script

```
Turn 1:
  User: "Set up a 1:1 with Sarah tomorrow at 3"
  Piper: "Got it — 1:1 with Sarah, tomorrow at 3pm. What's the topic?"

Turn 2:
  User: "Actually make it 4pm"
  [SlotFilling: detects update to time slot, overrides 3pm → 4pm]
  Piper: "Updated to 4pm. What's the topic?"
```

### Edge Cases

| User Input | State | Expected Behavior |
|------------|-------|-------------------|
| "Never mind" / "Cancel" | ANY | Exit gracefully, clear slots |
| "Yes" (ambiguous confirmation) | PROMPTING | Treat as "I don't have more info" — prompt again specifically |
| "Change Sarah to Jake" | PROMPTING/CONFIRMING | Update slot, re-confirm |
| Very long message with all slots | EXTRACTING | Fill all slots, skip to CONFIRMING |
| Gibberish | PROMPTING | Re-prompt for current missing slot |

---

## Phase 1: SlotTemplate + SlotFillingState (0.5 day)

### Objective
Define the data model for slot specifications and the state machine for slot-filling conversations.

### Tasks
- [ ] Add `SlotFillingState` enum to `services/shared_types.py`
  - EXTRACTING, PROMPTING, CONFIRMING, COMPLETE, CANCELLED
- [ ] Create `services/slot_filling/slot_template.py`
  - `SlotDefinition` dataclass: name, display_name, required (bool), slot_type (text/datetime/entity/choice), extraction_hint (optional), group (optional int for grouped prompting)
  - `SlotTemplate` dataclass: name, display_name, slots (list), confirmation_style (implicit/explicit)
  - `SlotState` dataclass: template ref, filled_slots (dict), current_prompt_group (int)
  - `MEETING_TEMPLATE` — first consumer template with 4 slots (attendee, day, time, topic)
- [ ] Create `services/slot_filling/__init__.py`

### Tests
- [ ] `tests/unit/services/slot_filling/test_slot_template.py`
  - SlotDefinition construction
  - SlotTemplate validation (at least 1 required slot)
  - SlotState: filled/unfilled/missing_required queries
  - MEETING_TEMPLATE sanity checks

### Deliverables
- Data model files created
- 15-20 tests passing
- No integration yet — pure data model

---

## Phase 2: Slot Extraction + Skip Logic (0.75 day)

### Objective
Build the core extraction engine that parses user messages for slot values, and the skip-filled logic.

### Tasks
- [ ] Create `services/slot_filling/slot_extractor.py`
  - `extract_slots(message: str, template: SlotTemplate, llm_service) -> dict[str, Any]`
  - LLM-based extraction: prompt with template slots + message → JSON slot values
  - Graceful fallback: if LLM fails, return empty dict (will prompt manually)
  - `update_slot_state(state: SlotState, extracted: dict) -> SlotState`
  - `get_missing_required(state: SlotState) -> list[SlotDefinition]`
  - `get_next_prompt_group(state: SlotState) -> list[SlotDefinition]` (max 2-3 slots)
- [ ] Create `services/slot_filling/slot_prompts.py`
  - `format_confirmation(state: SlotState) -> str` — "Got it — meeting with Sarah, Tuesday at 2pm"
  - `format_prompt(missing: list[SlotDefinition]) -> str` — "What's the topic?"
  - `format_grouped_prompt(missing: list[SlotDefinition]) -> str` — "Who should attend, and when works?"
  - Implicit vs explicit confirmation based on template setting

### Tests
- [ ] `tests/unit/services/slot_filling/test_slot_extractor.py`
  - Extraction from full message (all slots filled)
  - Extraction from partial message (some slots)
  - Empty extraction (no slots parseable)
  - Slot update (override existing value)
  - Missing required detection
  - Next prompt group selection (respects grouping, max 2-3)
- [ ] `tests/unit/services/slot_filling/test_slot_prompts.py`
  - Confirmation formatting
  - Single missing slot prompt
  - Grouped prompt (2-3 missing slots)
  - All-filled → confirmation only

### Deliverables
- Extraction engine with LLM integration (mocked in tests)
- Skip-filled logic working
- Grouped prompting logic working
- 25-30 tests passing

---

## Phase 3: SlotFillingManager + ProcessRegistry Integration (0.75 day)

### Objective
Build the state machine manager and wire it into ProcessRegistry as a Tier 1 handler.

### Tasks
- [ ] Create `services/slot_filling/slot_filling_manager.py`
  - `SlotFillingManager` class
  - `start_filling(user_id, session_id, template, initial_message) -> SlotFillingResponse`
  - `handle_turn(user_id, session_id, message) -> SlotFillingResponse`
  - State machine: EXTRACTING → PROMPTING → CONFIRMING → COMPLETE/CANCELLED
  - Session storage (in-memory dict, keyed by session_id — same pattern as onboarding)
  - Decline/cancel detection
  - Slot update detection during PROMPTING/CONFIRMING states
- [ ] Add `SLOT_FILLING = "slot_filling"` to `ProcessType` in `services/process/registry.py`
- [ ] Create `services/slot_filling/slot_filling_adapter.py`
  - `SlotFillingProcessAdapter` implementing GuidedProcess protocol
  - `check_active()`: checks if session has active slot-filling
  - `handle_message()`: delegates to manager, returns ProcessCheckResult
- [ ] Register adapter in ProcessRegistry initialization
- [ ] Wire `classify_conscious()` to trigger slot-filling when intent matches a template
  - After classification: if intent action has a registered SlotTemplate, start filling

### Tests
- [ ] `tests/unit/services/slot_filling/test_slot_filling_manager.py`
  - Full happy path (all slots in first message)
  - Partial path (2 turns)
  - Cancel mid-flow
  - Slot update mid-flow
  - Session isolation
- [ ] `tests/unit/services/slot_filling/test_slot_filling_adapter.py`
  - Adapter delegates correctly
  - check_active returns true/false correctly
  - ProcessCheckResult formatting

### Deliverables
- State machine manager operational
- Registered in ProcessRegistry
- Wiring tests verify real objects (not mocks) per #490 learning
- 20-25 tests passing

---

## Phase 4: Colleague Test + Regression (0.5 day)

### Objective
Verify the system behaves like a competent colleague and doesn't break existing flows.

### Tasks
- [ ] Create `tests/unit/services/slot_filling/test_slot_filling_colleague.py`
  - Scenario 1: All slots in one message → immediate confirmation
  - Scenario 2: Partial slots → prompt only for missing
  - Scenario 3: Slot update → accept change, re-confirm
  - Scenario 4: Cancel mid-flow → graceful exit
  - Scenario 5: Empty first message → grouped prompt for essentials
  - Scenario 6: Two-slot message → one follow-up for remaining
- [ ] Run regression: existing onboarding + standup + intent_service tests
- [ ] Run regression: #763 lens tests (152 tests)

### Deliverables
- 6 colleague scenarios passing
- Full regression green
- Evidence logged

---

## Phase Z: Commit + Handoff (0.25 day)

- [ ] Commit with proper message referencing #765
- [ ] Update #765 issue description with evidence
- [ ] Add closing comment with implementation evidence
- [ ] Update session log
- [ ] Handoff notes for #764 (GLUE-MULTIINTENT)

---

## Acceptance Criteria Mapping

| Criterion | Phase | Test |
|-----------|-------|------|
| Multi-slot input parsed correctly >90% | Phase 2 | test_slot_extractor: full/partial extraction |
| Never re-asks for provided information | Phase 2 | test_slot_extractor: skip-filled logic |
| Maximum 2-3 questions per exchange | Phase 2 | test_slot_prompts: grouped prompting |
| Slot updates accepted after initial fill | Phase 3 | test_slot_filling_manager: update mid-flow |
| Implicit confirmation default | Phase 2 | test_slot_prompts: confirmation formatting |
| Passes Colleague Test | Phase 4 | test_slot_filling_colleague: 6 scenarios |

---

## Architecture Decisions

### Why ProcessRegistry (not ConversationContext)?
The slot-filling framework operates at **Tier 1** (ADR-049) — it intercepts messages before classification when a slot-filling session is active. This is the same tier as onboarding and standup, and uses the same GuidedProcess protocol. ConversationContext is Tier 2 (per-turn metadata).

### Why LLM-based extraction (not regex)?
Natural language slot values are too varied for regex ("Tuesday at 2pm", "next week", "tomorrow morning", "the 15th"). LLM extraction with a structured prompt is more robust and matches the pattern used in the lens decoder (#763).

### Why in-memory session storage (not database)?
Same pattern as onboarding/standup. Slot-filling sessions are ephemeral (minutes, not days). Database persistence would be over-engineering for the M0 sprint.

### Why a framework (not just fixing onboarding)?
Multiple workflows need slot-filling (#767 GLUE-SOFTINVOKE depends on it). Building a reusable framework now prevents each workflow from re-implementing the same logic.

---

## STOP Conditions

- ProcessRegistry doesn't accept new ProcessType → STOP, investigate
- Onboarding adapter pattern doesn't generalize → STOP, rethink approach
- LLM extraction unreliable (>20% failure in tests) → STOP, consider hybrid approach
- Existing onboarding/standup tests fail → STOP, fix regression before proceeding
- Slot-filling interferes with lens tracking (#763) → STOP, resolve interaction

---

## Risk Assessment

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| LLM extraction quality | Medium | Graceful fallback to manual prompting; structured JSON prompt |
| ProcessRegistry conflict with existing handlers | Low | Priority system handles this; slot-filling gets lower priority than onboarding |
| Scope creep into actual calendar integration | Low | Explicit "Not In Scope" list; MEETING_TEMPLATE is demo-only |
| ConversationContext interference | Low | Slot-filling is Tier 1, lens is Tier 2; different layers |
