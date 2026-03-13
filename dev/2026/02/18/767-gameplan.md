# Gameplan: #767 GLUE-SOFTINVOKE — Soft Workflow Invocation from Natural Language

**Issue**: #767
**Epic**: #762 GLUE
**Branch**: `claude/m0-conversational-glue`
**Author**: Lead Developer (Claude Code Opus)
**Date**: 2026-02-18

---

## Phase -1: Infrastructure Verification

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (port 8001)
- [x] Database: PostgreSQL (port 5433) + ChromaDB (port 8000)
- [x] Testing framework: pytest with asyncio
- [x] Intent classification pipeline: PreClassifier (rules) → IntentClassifier (LLM fallback) → classify_conscious()
- [x] ProactivityGate: Trust-stage-gated proactivity, 4 stages, per-session throttling
- [x] RecognitionTrigger: Moderate-confidence offer mechanism
- [x] ProcessRegistry: Two-tier guided process architecture

**Task**: Build pattern-based soft invocation detection + workflow offer generation that integrates with existing ProactivityGate throttling and IntentService flow.

### Part A.2: Worktree Assessment

- [x] Single agent, sequential work
- [x] Tightly coupled files requiring atomic commits
- **SKIP WORKTREE** — Single developer, sequential phases, ~5-8 files.

### Part B: PM Verification

Investigation completed. Key findings:
1. ProactivityGate exists but has no consumer — `should_suggest_now()` is called nowhere
2. DISCOVERY_PATTERNS handle explicit queries only ("What can you do?"), not implied needs
3. No natural expression → workflow offer mapping exists
4. ConversationContext tracks turns but not pending offers
5. IntentService `process_intent()` returns `IntentProcessingResult` which has `suggestions` field (list) — potential integration point

---

## Phase 0: Investigation (COMPLETE)

- Mapped ProactivityGate: 4 trust stages, `can_offer_hints()` (Stage 2+), `can_proactive_suggest()` (Stage 3+), `should_suggest_now()` (stage + session count check)
- Mapped RecognitionTrigger: Moderate-confidence recognition options
- Mapped classify_conscious() pipeline: Place → Orientation → Follow-up → Classify → Recognition → Understanding
- Mapped IntentService.process_intent(): classify_multiple → multi-intent check → canonical handlers → learning handlers → suggestions
- Identified integration point: After intent processing, before returning result, check for soft invocation opportunity

---

## Phase 0.7: Conversation Design

### Happy Path: Natural Expression → Soft Offer → Acceptance
```
User: "I need to get the team together Tuesday"
Piper: [answers normally] + "By the way, I could help set up a meeting. Want me to find a time?"
User: "Yes please"
Piper: "Great! Who should I invite?" [starts slot-filling workflow]
```

### Happy Path: Soft Offer → Decline
```
User: "This project is getting complicated"
Piper: [answers normally] + "I could help organize things — want to set up some structure?"
User: "No, just venting"
Piper: "Got it, no worries." [continues normal conversation]
```

### Edge Case: Throttled (already offered recently)
```
User: "Also worried about deadlines"
Piper: [answers normally, no offer — already offered this exchange window]
```

### Edge Case: Low trust (NEW user)
```
User: "I need to schedule something"
Piper: [answers normally, no offer — trust stage doesn't allow suggestions]
```

### Anti-Pattern: Over-eager
```
BAD: User: "What a busy week"
     Piper: "Want me to reorganize your calendar? Set up a standup? Create a project plan?"
GOOD: User: "What a busy week"
      Piper: "Sounds hectic! Let me know if there's anything I can help with."
```

---

## Phase 1: SoftInvocationDetector + WorkflowOffer Data Model

**Objective**: Pattern-based detection of implied workflow needs + data model for offers.

### Data Model

```python
@dataclass
class WorkflowOffer:
    workflow_type: str          # e.g., "meeting", "project_setup", "standup"
    trigger_pattern: str        # What matched
    offer_message: str          # "Want me to help set up a meeting?"
    decline_message: str        # "No worries, just let me know if you change your mind."
    confidence: float           # Pattern match confidence

@dataclass
class SoftInvocationResult:
    has_offer: bool
    offer: Optional[WorkflowOffer]
    throttled: bool             # True if offer was suppressed by ProactivityGate
    reason: str                 # Why offer was/wasn't generated
```

### SoftInvocationDetector

Pattern-based detector with 10+ expression groups:
- "I need to..." + team/meeting/schedule keywords → meeting offer
- "Help me..." + organize/structure/plan keywords → project setup offer
- "I'm worried about..." + deadline/timeline keywords → status check offer
- "Things are getting..." + complicated/messy/disorganized → structure offer
- "We should..." + meet/sync/catch up → meeting offer
- "Can someone..." + review/check/look at → review offer
- "It would be nice to..." + track/organize/schedule → capability offer
- "I keep forgetting to..." + update/check/follow up → reminder offer
- "The team needs..." + alignment/sync/coordination → standup offer
- "I don't know where..." + things stand/we are/progress → status offer

### Tests (20-25 expected)
- Pattern matching for each expression group
- Confidence scoring
- WorkflowOffer properties
- No false positives on casual conversation
- Edge cases: partial matches, ambiguous expressions

### Files
- `services/intent_service/soft_invocation.py` (NEW: ~200-250 lines)
- `tests/unit/services/intent_service/test_soft_invocation.py` (NEW)

---

## Phase 2: WorkflowOfferService + Throttling

**Objective**: Generate natural-language offers with decline paths, integrate with ProactivityGate.

### WorkflowOfferService

```python
class WorkflowOfferService:
    def __init__(self, proactivity_gate: ProactivityGate):
        ...

    def should_offer(self, trust_stage, offers_this_window, detection_result) -> bool:
        """Check ProactivityGate + exchange window throttling."""

    def format_offer(self, workflow_offer, base_response) -> str:
        """Append soft offer to existing response with natural transition."""

    def format_acceptance(self, workflow_type) -> str:
        """Generate workflow start message."""

    def format_decline(self) -> str:
        """Generate graceful decline acknowledgment."""
```

### Exchange Window Throttling

The requirement is "max 2 unsolicited offers per 5 exchanges." This extends ProactivityGate's session-level throttling with a sliding window:
- Track offers in conversation context (timestamp + turn number)
- Count offers in last 5 exchanges
- If >= 2, suppress new offers regardless of trust stage

### Acceptance/Decline Detection

Simple pattern detection for offer responses:
- Accept: "yes", "sure", "please", "go ahead", "sounds good", "let's do it"
- Decline: "no", "nah", "not now", "just venting", "never mind", "I'm good"

### Tests (15-20 expected)
- ProactivityGate integration (each trust stage)
- Exchange window throttling
- Offer formatting (natural transitions)
- Acceptance/decline detection
- Edge cases: ambiguous responses, mid-conversation offers

### Files
- `services/intent_service/soft_invocation.py` (extend with WorkflowOfferService)
- `tests/unit/services/intent_service/test_soft_invocation.py` (extend)

---

## Phase 3: IntentService Integration

**Objective**: Wire soft invocation into the existing IntentService pipeline.

### Integration Point

In `IntentService.process_intent()`, after intent classification and handling, before returning the result:

```python
# After building the response...
# Issue #767: Check for soft invocation opportunity
if self.soft_invocation_detector and result.success:
    detection = self.soft_invocation_detector.detect(message, intent)
    if detection.has_offer:
        offer_result = self.workflow_offer_service.should_offer(
            trust_stage=trust_stage,
            offers_this_window=offers_count,
            detection_result=detection,
        )
        if offer_result:
            result.message = self.workflow_offer_service.format_offer(
                detection.offer, result.message
            )
            result.pending_offer = detection.offer
```

### Pending Offer Handling

When a user responds to a pending offer:
1. Check if previous response had a pending_offer
2. Detect accept/decline in current message
3. If accepted → start relevant workflow (via ProcessRegistry or slot filling)
4. If declined → acknowledge and continue normally

### IntentProcessingResult Extension

Add field: `pending_offer: Optional[WorkflowOffer] = None`

### Tests (10-15 expected)
- End-to-end: natural expression → detection → offer in response
- Offer acceptance → workflow start
- Offer decline → normal flow continues
- No offer when ProactivityGate denies
- No offer on single-intent happy path (existing behavior preserved)
- Fallback: detection error → normal response (no offer)

### Files
- `services/intent/intent_service.py` (modify: add soft invocation check)
- `tests/unit/services/intent_service/test_soft_invocation_integration.py` (NEW)

---

## Phase 4: Colleague Test + Regression

**Objective**: Verify natural behavior through colleague scenarios, no regressions.

### Colleague Scenarios (6+)

1. **Meeting need**: "I need to get the team together Tuesday" → Offers meeting setup
2. **Project complexity**: "This project is getting complicated" → Offers project structure
3. **Deadline worry**: "I'm worried about the deadline" → Offers status check
4. **Casual chat (no offer)**: "What a nice day" → No offer (not a workflow need)
5. **Decline gracefully**: User declines offer → Piper acknowledges, moves on
6. **Throttled**: Second offer in 5 exchanges suppressed

### Regression
- Existing intent classification: all passing
- Existing multi-intent (#764): all passing
- Existing slot filling (#765): all passing
- Existing process registry: all passing
- Single-intent flow: unchanged

### Files
- `tests/unit/services/intent_service/test_soft_invocation_colleague.py` (NEW)

---

## Phase Z: Commit + Close

- Stage all new/modified files
- Run pre-commit hooks (isort, black, flake8)
- Commit with descriptive message
- Push to branch
- Update issue description (all checkboxes [x])
- Add closing comment with evidence
- Close issue

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| False positive offers (annoying) | Conservative patterns, high confidence threshold |
| ProactivityGate not yet wired to real trust data | Accept mock trust_stage; real wiring is separate issue |
| Offer acceptance detection too crude | Simple pattern matching sufficient for M0; LLM-based in future |
| Over-engineering the offer flow | M0 scope: append to response string, no complex UI |

## Test Count Estimate

| Phase | Tests |
|-------|-------|
| 1: Detector + data model | 20-25 |
| 2: Offer service + throttling | 15-20 |
| 3: IntentService integration | 10-15 |
| 4: Colleague + regression | 6+ |
| **Total** | **51-66** |

## Success Criteria

1. 10+ natural expressions correctly detected and offered
2. ProactivityGate respected at all trust stages
3. Exchange window throttling works (max 2 per 5)
4. Acceptance starts relevant workflow naturally
5. Decline is graceful and conversation continues
6. Zero regressions in existing tests
7. Passes colleague test: "Would a colleague offer help this way?"
