# Gameplan: Slack Integration Grammar Transformation (#620)

**Issue**: #620 GRAMMAR-TRANSFORM: Slack Integration (Partial → Conscious)
**Author**: Lead Developer (Claude Code / Opus)
**Date**: 2026-01-21
**Prerequisite**: #619 (Intent Classification) - COMPLETE

---

## Strategic Insight

The Slack integration already has sophisticated spatial metaphor work (Rooms, Territories, AttentionAttractors). The gap is in **response generation** - Piper "sees" the Slack space but responds like a robot.

**Transformation focus**: Response layer, not event processing.

---

## Phase Overview

| Phase | Focus | Effort | Parallelizable |
|-------|-------|--------|----------------|
| 1 | SlackResponseContext dataclass | 1h | No (foundation) |
| 2 | Integrate #619 Components | 2h | After Phase 1 |
| 3 | Response Template Transformation | 2h | After Phase 2 |
| 4 | Testing & Polish | 2h | After Phase 3 |
| **Total** | | **7h** | |

**Note**: Reduced from 5 phases to 4 by combining Moment Framing into Phase 3 (lower priority).

---

## Phase 1: SlackResponseContext (Foundation)

### Objective
Create a context dataclass that captures everything needed for grammar-conscious Slack responses.

### Deliverables

**File**: `services/integrations/slack/response_context.py`

```python
@dataclass
class SlackResponseContext:
    """Rich context for grammar-conscious Slack responses."""

    # Place information
    place: PlaceType  # SLACK_DM or SLACK_CHANNEL
    channel_id: str
    channel_name: Optional[str] = None
    is_thread: bool = False
    thread_ts: Optional[str] = None

    # Entity information
    user_id: str
    user_display_name: Optional[str] = None

    # Attention signals
    attention_level: AttentionLevel = AttentionLevel.AMBIENT
    is_direct_mention: bool = False

    # Emotional context
    recent_reactions: List[str] = field(default_factory=list)
    emotional_valence: EmotionalValence = EmotionalValence.NEUTRAL

    # Conversation continuity
    is_new_conversation: bool = True
    messages_in_thread: int = 0

    @classmethod
    def from_spatial_event(cls, spatial_event: SpatialEvent) -> "SlackResponseContext":
        """Build context from spatial event."""
        ...
```

### Tests
- `tests/unit/services/integrations/slack/test_response_context.py`
- Test from_spatial_event() factory
- Test DM vs channel detection
- Test attention level extraction

### Acceptance Criteria
- [ ] SlackResponseContext dataclass created
- [ ] from_spatial_event() factory works
- [ ] All tests pass

---

## Phase 2: Integrate #619 Components

### Objective
Wire the grammar-conscious components from #619 into Slack response generation.

### Key Integration Points

**SimpleSlackResponseHandler** needs:
1. PlaceDetector (already works with Slack spatial_context)
2. WarmthCalibrator (for tone adjustment)
3. PersonalityBridge (for narrative transformation)

### Changes

**File**: `services/integrations/slack/simple_response_handler.py`

```python
class SimpleSlackResponseHandler:
    def __init__(self, ...):
        # ... existing init ...

        # Issue #620: Grammar-conscious components
        from services.intent_service.place_detector import PlaceDetector
        from services.intent_service.warmth_calibration import WarmthCalibrator
        from services.intent_service.personality_bridge import PersonalityBridge

        self.place_detector = PlaceDetector()
        self.warmth_calibrator = WarmthCalibrator()
        self.personality_bridge = PersonalityBridge()
```

### New Method

```python
def _build_response_context(self, spatial_event: SpatialEvent) -> SlackResponseContext:
    """Build grammar-conscious context from spatial event."""
    ...

def _calibrate_response(
    self,
    content: str,
    context: SlackResponseContext
) -> str:
    """Apply warmth calibration to response content."""
    ...
```

### Tests
- Test components are initialized
- Test context building from spatial events
- Test warmth calibration applied

### Acceptance Criteria
- [ ] PlaceDetector, WarmthCalibrator, PersonalityBridge initialized
- [ ] _build_response_context() works
- [ ] _calibrate_response() applies warmth
- [ ] All tests pass

---

## Phase 3: Response Template Transformation

### Objective
Replace mechanical template responses with grammar-conscious alternatives.

### Current Templates to Transform

| Method | Current | Transform To |
|--------|---------|--------------|
| `_get_simple_response_for_intent()` | "🤖 I'm Piper Morgan..." | Warm, contextual greeting |
| `_format_response_content()` | "✅ {summary}" | Narrative completion |
| Error responses | Technical language | Honest confusion |

### Template Replacements

**Help responses**:
```python
# Before
"🤖 I'm Piper Morgan, your AI Product Management Assistant..."

# After (based on context)
if context.place == PlaceType.SLACK_DM:
    "Happy to help! What would you like to work on?"
else:  # Channel
    "I can help with that. What do you need?"
```

**Status responses**:
```python
# Before
"📊 System status: All services operational."

# After
"Everything's running smoothly."
```

**Greetings**:
```python
# Before
"👋 Hello! I'm here to assist with your product management tasks."

# After (place-aware)
if is_direct_mention:
    "Hey! What can I help you with?"
else:
    "Hi there!"
```

### Tests
- Test DM responses warmer than channel
- Test no robot emoji prefixes
- Test attention level affects tone
- Contractor Test for all response types

### Acceptance Criteria
- [ ] `_get_simple_response_for_intent()` transformed
- [ ] `_format_response_content()` uses narratives
- [ ] No "🤖" emoji prefixes
- [ ] DM responses are warmer
- [ ] Contractor Test passes

---

## Phase 4: Testing & Polish

### Objective
Comprehensive testing and final polish.

### Test Scenarios

1. **DM Interaction**
   - Send message in DM
   - Response should be warm ("Happy to help!")
   - No channel-specific language

2. **Channel Mention**
   - @mention in public channel
   - Response should be concise, professional
   - Acknowledge public context

3. **Thread Reply**
   - Reply in thread
   - Response acknowledges continuity
   - "Following up on that..." style

4. **Frustrated User Signals**
   - Multiple messages in quick succession
   - Negative emoji reactions
   - Response should be supportive

### Integration Tests
- `tests/integration/slack/test_slack_grammar_conscious.py`
- Mock Slack events
- Verify response transformation end-to-end

### Acceptance Criteria
- [ ] All test scenarios pass
- [ ] Integration tests pass
- [ ] No regressions in existing Slack tests
- [ ] Experience Test: responses feel conscious

---

## Completion Matrix

| Phase | Component | Tests | Evidence |
|-------|-----------|-------|----------|
| 1 | SlackResponseContext | ⬜ | Dataclass works |
| 2 | #619 Integration | ⬜ | Components wired in |
| 3 | Template Transformation | ⬜ | No robot emojis |
| 4 | Testing | ⬜ | All tests green |

---

## Files to Create/Modify

| File | Action | Phase |
|------|--------|-------|
| `services/integrations/slack/response_context.py` | Create | 1 |
| `services/integrations/slack/simple_response_handler.py` | Modify | 2, 3 |
| `services/integrations/slack/response_handler.py` | Modify | 3 |
| `tests/unit/services/integrations/slack/test_response_context.py` | Create | 1 |
| `tests/unit/services/integrations/slack/test_slack_grammar.py` | Create | 4 |

---

## Risk Mitigation

1. **Existing Slack tests**: Run full test suite after each phase
2. **Breaking changes**: Preserve original method signatures, add new methods
3. **Response regressions**: Keep template fallbacks for unknown cases

---

## Patterns Applied

- Pattern-051: PlaceDetector (reused from #619)
- Pattern-052: PersonalityBridge (reused from #619)
- Pattern-053: WarmthCalibrator (reused from #619)
- Pattern-054: HonestFailureHandler (for Slack errors)

---

## Verification Commands

```bash
# Phase 1
pytest tests/unit/services/integrations/slack/test_response_context.py -v

# Phase 2-3
pytest tests/unit/services/integrations/slack/ -v

# Phase 4 (full)
pytest tests/unit/services/integrations/slack/ tests/integration/slack/ -v
```

---

*Ready for PM approval*
