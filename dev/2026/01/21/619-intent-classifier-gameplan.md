# Gameplan: Intent Classification Grammar Transformation (#619)

**Issue**: #619 GRAMMAR-TRANSFORM: Intent Classification
**Priority**: Critical (High Priority)
**Estimated Total**: 9-11 hours
**Approach**: Phased implementation with grammar pattern application

---

## Phase 1: Foundation (Context/Result Dataclasses)

**Duration**: 1-2 hours
**Pattern**: Pattern-050 (Context Dataclass Pair)

### Deliverables

1. **Create `services/intent_service/intent_types.py`** (if not exists, else extend)

```python
@dataclass
class IntentClassificationContext:
    """Rich context for intent classification - the Situation."""
    message: str
    user_id: Optional[str]
    session_id: Optional[str]
    place: PlaceType  # NEW: Where is this happening?
    spatial_context: Optional[Dict]
    conversation_history: Optional[List[str]]  # Recent messages
    user_preferences: Optional[Dict]  # Known preferences
    timestamp: datetime

@dataclass
class IntentUnderstanding:
    """Grammar-conscious classification result - Piper's understanding."""
    intent: Intent  # Original for compatibility
    understanding_narrative: str  # "I understand you want to..."
    confidence_expression: str  # "I'm fairly certain" / "I think"
    place_awareness: str  # "Since we're in Slack..."
    perception_mode: PerceptionMode  # NOTICING, REMEMBERING, ANTICIPATING
    follow_up_suggestion: Optional[str]  # What Piper might ask next
```

2. **Add to `services/shared_types.py`**:

```python
class PlaceType(str, Enum):
    """Where the interaction is happening."""
    SLACK_DM = "slack_dm"
    SLACK_CHANNEL = "slack_channel"
    WEB_CHAT = "web_chat"
    CLI = "cli"
    API = "api"
    UNKNOWN = "unknown"

class PerceptionMode(str, Enum):
    """How Piper is perceiving the intent."""
    NOTICING = "noticing"      # Present - "I notice you want..."
    REMEMBERING = "remembering"  # Past - "I remember you asked..."
    ANTICIPATING = "anticipating"  # Future - "You might also want..."
```

### Acceptance Criteria
- [ ] IntentClassificationContext dataclass created
- [ ] IntentUnderstanding dataclass created
- [ ] PlaceType enum in shared_types.py
- [ ] PerceptionMode enum in shared_types.py
- [ ] Unit tests for new types

---

## Phase 2: Place Detection

**Duration**: 2 hours
**Pattern**: Pattern-051 (Parallel Place Gathering)

### Deliverables

1. **Create `services/intent_service/place_detector.py`**:

```python
class PlaceDetector:
    """Detects where the conversation is happening."""

    def detect(self, spatial_context: Optional[Dict]) -> PlaceType:
        """Determine PlaceType from spatial context."""
        if not spatial_context:
            return PlaceType.UNKNOWN

        # Check for Slack indicators
        if spatial_context.get("room_id") or spatial_context.get("channel"):
            if spatial_context.get("is_dm", False):
                return PlaceType.SLACK_DM
            return PlaceType.SLACK_CHANNEL

        # Check for web indicators
        if spatial_context.get("source") == "web":
            return PlaceType.WEB_CHAT

        # Check for CLI
        if spatial_context.get("source") == "cli":
            return PlaceType.CLI

        return PlaceType.UNKNOWN

    def get_place_settings(self, place: PlaceType) -> Dict:
        """Return Place-appropriate settings."""
        return {
            PlaceType.SLACK_DM: {
                "formality": "casual",
                "verbosity": "medium",
                "can_use_emoji": True,
            },
            PlaceType.SLACK_CHANNEL: {
                "formality": "professional",
                "verbosity": "concise",
                "can_use_emoji": False,
            },
            PlaceType.WEB_CHAT: {
                "formality": "warm",
                "verbosity": "full",
                "can_use_emoji": True,
            },
            PlaceType.CLI: {
                "formality": "terse",
                "verbosity": "minimal",
                "can_use_emoji": False,
            },
        }.get(place, {
            "formality": "professional",
            "verbosity": "medium",
            "can_use_emoji": False,
        })
```

2. **Integrate into IntentClassifier**:
   - Add `PlaceDetector` as dependency
   - Detect Place at start of `classify()`
   - Store in classification context

### Acceptance Criteria
- [ ] PlaceDetector class created
- [ ] Detection logic handles all known Place types
- [ ] Place settings return appropriate values
- [ ] Integration point identified in classifier
- [ ] Unit tests for detection

---

## Phase 3: Personality Bridge

**Duration**: 2 hours
**Pattern**: Pattern-052 (Personality Bridge)

### Deliverables

1. **Add to IntentClassifier**:

```python
def _make_understanding_personal(
    self,
    intent: Intent,
    context: IntentClassificationContext,
    place_settings: Dict,
) -> IntentUnderstanding:
    """Transform raw Intent into Piper's understanding."""

    # Determine perception mode
    perception = self._determine_perception_mode(intent, context)

    # Build understanding narrative
    narrative = self._build_narrative(intent, perception, context)

    # Express confidence appropriately
    confidence_expr = self._express_confidence(intent.confidence, place_settings)

    # Note Place awareness if relevant
    place_note = self._note_place_awareness(context.place, place_settings)

    return IntentUnderstanding(
        intent=intent,
        understanding_narrative=narrative,
        confidence_expression=confidence_expr,
        place_awareness=place_note,
        perception_mode=perception,
        follow_up_suggestion=self._suggest_follow_up(intent, context),
    )

def _determine_perception_mode(
    self,
    intent: Intent,
    context: IntentClassificationContext
) -> PerceptionMode:
    """Determine how Piper is perceiving this intent."""
    # If we've seen similar from this user recently
    if self._is_repeated_pattern(context):
        return PerceptionMode.REMEMBERING
    # If this seems like a follow-up
    if self._seems_like_follow_up(context):
        return PerceptionMode.ANTICIPATING
    # Default: fresh observation
    return PerceptionMode.NOTICING

def _build_narrative(
    self,
    intent: Intent,
    perception: PerceptionMode,
    context: IntentClassificationContext,
) -> str:
    """Build the understanding narrative."""
    templates = {
        PerceptionMode.NOTICING: "I understand you want to {action}",
        PerceptionMode.REMEMBERING: "I remember you often ask about {action}",
        PerceptionMode.ANTICIPATING: "You might be wanting to {action}",
    }
    return templates[perception].format(action=self._humanize_action(intent.action))
```

2. **Action humanization map**:

```python
ACTION_NARRATIVES = {
    "create_item": "create something new",
    "search_files": "find some files",
    "search_documents": "search through documents",
    "list_items": "see a list",
    "analyze_data": "analyze some data",
    "clarification_needed": "help me understand better",
    # ... more mappings
}
```

### Acceptance Criteria
- [ ] `_make_understanding_personal()` method created
- [ ] Perception mode determination logic
- [ ] Narrative templates for each perception mode
- [ ] Action humanization map populated
- [ ] Unit tests for personality bridge

---

## Phase 4: Warmth Calibration

**Duration**: 1 hour
**Pattern**: Pattern-053 (Warmth Calibration)

### Deliverables

1. **Confidence expression calibration**:

```python
def _express_confidence(self, confidence: float, place_settings: Dict) -> str:
    """Express confidence in human terms."""
    formality = place_settings.get("formality", "professional")

    if confidence >= 0.9:
        expressions = {
            "casual": "Got it!",
            "professional": "I understand.",
            "warm": "I understand what you're looking for.",
            "terse": "Understood.",
        }
    elif confidence >= 0.7:
        expressions = {
            "casual": "I think I've got it",
            "professional": "I believe I understand.",
            "warm": "I think I understand what you mean.",
            "terse": "Likely understood.",
        }
    elif confidence >= 0.5:
        expressions = {
            "casual": "I'm not 100% sure, but",
            "professional": "I'm not entirely certain, but",
            "warm": "I want to make sure I understand—",
            "terse": "Uncertain.",
        }
    else:
        expressions = {
            "casual": "Hmm, I'm not quite sure what you mean",
            "professional": "I'm having difficulty understanding.",
            "warm": "I want to help, but I'm not sure I understood.",
            "terse": "Unclear.",
        }

    return expressions.get(formality, expressions["professional"])
```

2. **Place awareness notes**:

```python
def _note_place_awareness(self, place: PlaceType, settings: Dict) -> str:
    """Note relevant Place context."""
    if place == PlaceType.SLACK_CHANNEL:
        return "Since we're in a channel, I'll keep this brief."
    if place == PlaceType.SLACK_DM:
        return ""  # DMs don't need explanation
    if place == PlaceType.CLI:
        return ""  # CLI expects terseness
    return ""
```

### Acceptance Criteria
- [ ] Confidence expression varies by formality level
- [ ] Four confidence tiers (high/medium-high/medium/low)
- [ ] Place-aware verbosity adjustment
- [ ] Unit tests for warmth calibration

---

## Phase 5: Honest Failure

**Duration**: 1 hour
**Pattern**: Pattern-054 (Honest Failure)

### Deliverables

1. **Transform error handling in classify()**:

Replace:
```python
except Exception as e:
    logger.error(f"Classification failed: {e}", exc_info=True)
    raise IntentClassificationFailedError(details={"original_error": str(e)})
```

With:
```python
except Exception as e:
    logger.error(f"Classification failed: {e}", exc_info=True)
    return self._admit_confusion(context, str(e))

def _admit_confusion(
    self,
    context: IntentClassificationContext,
    error_detail: str
) -> IntentUnderstanding:
    """Gracefully admit when Piper can't understand."""
    place_settings = self.place_detector.get_place_settings(context.place)

    # Build honest confusion response
    confusion_narratives = {
        "casual": "I'm having trouble understanding that one.",
        "professional": "I'm having difficulty interpreting your request.",
        "warm": "I want to help, but I'm not quite following.",
        "terse": "Unable to interpret.",
    }

    formality = place_settings.get("formality", "professional")

    # Create a clarification-seeking intent
    clarification_intent = Intent(
        category=IntentCategory.CONVERSATION,
        action="clarification_needed",
        confidence=0.0,
        context={"error_detail": error_detail, "needs_human_help": True},
    )

    return IntentUnderstanding(
        intent=clarification_intent,
        understanding_narrative=confusion_narratives[formality],
        confidence_expression="",
        place_awareness="",
        perception_mode=PerceptionMode.NOTICING,
        follow_up_suggestion="Could you rephrase that for me?",
    )
```

2. **Update vague intent handling**:

```python
if intent.confidence < 0.3 or self._seems_vague(intent):
    return self._express_uncertainty(intent, context)
```

### Acceptance Criteria
- [ ] Errors don't raise technical exceptions to UI layer
- [ ] Confusion is expressed warmly
- [ ] Low-confidence intents get gentle follow-up suggestions
- [ ] Unit tests for failure paths

---

## Phase 6: Integration & Testing

**Duration**: 2 hours

### Deliverables

1. **Modify `classify()` return type**:
   - Return `IntentUnderstanding` instead of `Intent`
   - OR: Keep `Intent` return but attach understanding metadata

2. **Backward compatibility**:
   - `IntentUnderstanding.intent` provides original Intent
   - Existing callers can access `.intent` attribute

3. **Experience tests**:

```python
def test_experience_test_noticing():
    """Piper notices, doesn't process."""
    understanding = classifier.classify("add a todo for tomorrow")
    assert "I understand" in understanding.understanding_narrative
    assert "Query returned" not in str(understanding)

def test_place_affects_response():
    """Different Places get different tones."""
    understanding_dm = classifier.classify(
        "hey what's up",
        spatial_context={"is_dm": True}
    )
    understanding_channel = classifier.classify(
        "hey what's up",
        spatial_context={"is_dm": False, "channel": "general"}
    )
    assert understanding_dm.understanding_narrative != understanding_channel.understanding_narrative
```

### Acceptance Criteria
- [ ] All existing tests still pass
- [ ] Experience tests pass
- [ ] Place-awareness tests pass
- [ ] Warmth calibration tests pass
- [ ] No breaking changes to callers

---

## Completion Matrix

| Phase | Task | Status | Evidence Required |
|-------|------|--------|-------------------|
| 1 | IntentClassificationContext | ⬜ | Unit test passing |
| 1 | IntentUnderstanding | ⬜ | Unit test passing |
| 1 | PlaceType enum | ⬜ | Import works |
| 1 | PerceptionMode enum | ⬜ | Import works |
| 2 | PlaceDetector class | ⬜ | Unit test passing |
| 2 | Place settings | ⬜ | Unit test passing |
| 3 | Personality bridge method | ⬜ | Unit test passing |
| 3 | Perception mode logic | ⬜ | Unit test passing |
| 3 | Narrative templates | ⬜ | Manual review |
| 4 | Confidence expression | ⬜ | Unit test passing |
| 4 | Place awareness notes | ⬜ | Unit test passing |
| 5 | Honest failure handling | ⬜ | Unit test passing |
| 5 | Graceful confusion | ⬜ | Unit test passing |
| 6 | Backward compatibility | ⬜ | Existing tests pass |
| 6 | Experience tests | ⬜ | All pass |

---

## Implementation Order

Can be parallelized after Phase 1:

```
Phase 1 (Foundation)
    ↓
┌───────────┬───────────┬───────────┐
Phase 2     Phase 3     Phase 4
(Place)     (Bridge)    (Warmth)
└───────────┴───────────┴───────────┘
    ↓
Phase 5 (Failure)
    ↓
Phase 6 (Integration)
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Breaking API contract | IntentUnderstanding wraps Intent |
| Performance regression | Cache Place detection per session |
| Over-personalization | Follow Contractor Test; warmth is subtle |
| Scope creep into handlers | Scope limited to classification layer |

---

*Gameplan created: 2026-01-21 7:25 PM PT*
*Based on audit: 619-intent-classifier-grammar-audit.md*
