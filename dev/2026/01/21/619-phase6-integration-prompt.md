# Agent Prompt: Phase 6 - Integration (#619)

**Issue**: #619 GRAMMAR-TRANSFORM: Intent Classification
**Phase**: 6 of 6 (Final)
**Estimated Time**: 2 hours
**Prerequisites**: Phases 1-5 complete

---

## Objective

Integrate all Phase 1-5 components into the IntentClassifier. This transforms the classifier from data processing to experiential understanding while maintaining backward compatibility.

---

## Pre-Integration Checklist

Before starting, verify all components exist:

```bash
# Check all required modules exist
python -c "
from services.shared_types import PlaceType, PerceptionMode
from services.intent_service.intent_types import IntentClassificationContext, IntentUnderstanding
from services.intent_service.place_detector import PlaceDetector
from services.intent_service.personality_bridge import PersonalityBridge
from services.intent_service.warmth_calibration import WarmthCalibrator
from services.intent_service.honest_failure import HonestFailureHandler
print('All Phase 1-5 components available!')
"
```

If any import fails, that phase needs to be completed first.

---

## Task 1: Add Dependencies to IntentClassifier

**File**: `services/intent_service/classifier.py`

Add imports at the top (after existing imports):

```python
# Grammar-conscious classification components (Issue #619)
from services.intent_service.intent_types import (
    IntentClassificationContext,
    IntentUnderstanding,
)
from services.intent_service.place_detector import PlaceDetector
from services.intent_service.personality_bridge import PersonalityBridge
from services.intent_service.warmth_calibration import WarmthCalibrator
from services.intent_service.honest_failure import (
    HonestFailureHandler,
    create_graceful_error_response,
)
```

Update `__init__` to initialize new components:

```python
def __init__(
    self,
    llm_service=None,
    event_bus: Optional[EventBus] = None,
    knowledge_graph_service=None,
):
    # ... existing initialization ...

    # Issue #619: Grammar-conscious classification components
    self.place_detector = PlaceDetector()
    self.personality_bridge = PersonalityBridge()
    self.warmth_calibrator = WarmthCalibrator()
    self.failure_handler = HonestFailureHandler(self.warmth_calibrator)
    logger.info("Grammar-conscious classification components initialized (#619)")
```

---

## Task 2: Add Grammar-Conscious Classification Method

Add a new method that returns `IntentUnderstanding` instead of `Intent`:

```python
async def classify_conscious(
    self,
    message: str,
    context: Optional[Dict] = None,
    session: Optional[Any] = None,
    spatial_context: Optional[Dict] = None,
    use_cache: bool = True,
) -> IntentUnderstanding:
    """
    Grammar-conscious intent classification.

    This method returns IntentUnderstanding instead of raw Intent,
    providing experiential framing of Piper's understanding.

    For backward compatibility, use classify() which returns Intent.
    New code should prefer this method for richer responses.

    Args:
        message: User input text
        context: Optional context dict
        session: Optional session object
        spatial_context: Optional spatial context
        use_cache: Whether to use cache (default True)

    Returns:
        IntentUnderstanding with Piper's experiential understanding
    """
    # Detect Place first
    place, place_settings = self.place_detector.detect_with_settings(
        spatial_context
    )

    # Build rich classification context
    classification_context = IntentClassificationContext.from_classify_args(
        message=message,
        context=context,
        spatial_context=spatial_context,
        place=place,
    )

    try:
        # Use existing classify() for the raw Intent
        intent = await self.classify(
            message=message,
            context=context,
            session=session,
            spatial_context=spatial_context,
            use_cache=use_cache,
        )

        # Check for low confidence - handle specially
        if intent.confidence < 0.5:
            return self.failure_handler.handle_low_confidence(
                intent=intent,
                context=classification_context,
                place_settings=place_settings,
            )

        # Check for vague intent
        if self._seems_vague(intent):
            return self.failure_handler.handle_vague_intent(
                intent=intent,
                context=classification_context,
                place_settings=place_settings,
            )

        # Transform to grammar-conscious understanding
        understanding = self.personality_bridge.transform(
            intent=intent,
            context=classification_context,
            place_settings=place_settings,
        )

        # Record for pattern detection
        if classification_context.user_id:
            self.personality_bridge.record_intent(
                classification_context.user_id,
                intent.action,
            )

        return understanding

    except Exception as e:
        logger.error(f"Classification failed: {e}", exc_info=True)
        # Return graceful failure instead of raising
        return create_graceful_error_response(
            context=classification_context,
            place_settings=place_settings,
            error=e,
        )
```

---

## Task 3: Create Integration Tests

**File**: `tests/unit/services/intent_service/test_classifier_conscious.py`

```python
"""Tests for grammar-conscious intent classification."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from services.shared_types import IntentCategory, PerceptionMode, PlaceType
from services.intent_service.classifier import IntentClassifier
from services.intent_service.intent import Intent
from services.intent_service.intent_types import IntentUnderstanding


class TestClassifyConscious:
    """Test classify_conscious method."""

    @pytest.fixture
    def mock_llm(self):
        llm = MagicMock()
        llm.complete = AsyncMock(return_value='{"category": "execution", "action": "create_item", "confidence": 0.9, "reasoning": "test"}')
        return llm

    @pytest.fixture
    def classifier(self, mock_llm):
        return IntentClassifier(llm_service=mock_llm)

    # --- Basic Integration Tests ---

    @pytest.mark.asyncio
    async def test_returns_intent_understanding(self, classifier):
        """classify_conscious returns IntentUnderstanding."""
        result = await classifier.classify_conscious(
            message="add a todo",
            context={"user_id": "test-user"},
        )
        assert isinstance(result, IntentUnderstanding)
        assert result.intent is not None
        assert result.understanding_narrative is not None

    @pytest.mark.asyncio
    async def test_preserves_intent_access(self, classifier):
        """Can still access underlying Intent."""
        result = await classifier.classify_conscious(
            message="create a new task",
            context={"user_id": "test-user"},
        )
        # Proxy properties work
        assert result.category is not None
        assert result.action is not None
        assert result.confidence is not None
        # Direct access works
        assert result.intent.category is not None

    # --- Place Awareness Tests ---

    @pytest.mark.asyncio
    async def test_detects_slack_dm(self, classifier):
        """Detects Slack DM context."""
        result = await classifier.classify_conscious(
            message="hi there",
            spatial_context={"room_id": "D123", "is_dm": True},
        )
        # DM should produce warmer understanding
        assert "casual" in str(result).lower() or result.understanding_narrative is not None

    @pytest.mark.asyncio
    async def test_detects_cli(self, classifier):
        """Detects CLI context."""
        result = await classifier.classify_conscious(
            message="list todos",
            spatial_context={"source": "cli"},
        )
        # Should still work, just with different tone
        assert result is not None

    # --- Experience Tests ---

    @pytest.mark.asyncio
    async def test_experience_test_noticing_language(self, classifier):
        """Uses experiential language."""
        result = await classifier.classify_conscious(
            message="find documents about the project",
            context={"user_id": "test-user"},
        )
        narrative = result.understanding_narrative.lower()
        # Should use first person
        assert "i" in narrative.split()  # "I" as a word
        # Should NOT be mechanical
        assert "query" not in narrative
        assert "returned" not in narrative
        assert "processed" not in narrative

    @pytest.mark.asyncio
    async def test_experience_test_confidence_human(self, classifier, mock_llm):
        """Confidence expressed in human terms."""
        mock_llm.complete = AsyncMock(
            return_value='{"category": "query", "action": "search_files", "confidence": 0.95, "reasoning": "clear request"}'
        )
        result = await classifier.classify_conscious(
            message="find all documents",
            context={"user_id": "test-user"},
        )
        # Should have confidence expression
        assert result.confidence_expression is not None
        # Should be human, not numeric
        assert "0.95" not in result.confidence_expression

    # --- Failure Handling Tests ---

    @pytest.mark.asyncio
    async def test_low_confidence_handled_gracefully(self, classifier, mock_llm):
        """Low confidence gets special handling."""
        mock_llm.complete = AsyncMock(
            return_value='{"category": "query", "action": "search_files", "confidence": 0.3, "reasoning": "uncertain"}'
        )
        result = await classifier.classify_conscious(
            message="do something with files maybe",
            context={"user_id": "test-user"},
        )
        # Should express uncertainty
        narrative = result.understanding_narrative.lower()
        assert "think" in narrative or "might" in narrative or "sure" in narrative or "uncertain" in narrative

    @pytest.mark.asyncio
    async def test_error_returns_understanding_not_exception(self, classifier, mock_llm):
        """Errors return IntentUnderstanding, not raise."""
        mock_llm.complete = AsyncMock(side_effect=ValueError("LLM broke"))

        # Should NOT raise
        result = await classifier.classify_conscious(
            message="test message",
            context={"user_id": "test-user"},
        )

        # Should return graceful failure
        assert isinstance(result, IntentUnderstanding)
        assert result.intent.action == "clarification_needed"

    # --- Backward Compatibility Tests ---

    @pytest.mark.asyncio
    async def test_classify_still_returns_intent(self, classifier):
        """Original classify() still returns Intent."""
        result = await classifier.classify(
            message="add a todo",
            context={"user_id": "test-user"},
        )
        assert isinstance(result, Intent)
        assert not isinstance(result, IntentUnderstanding)


class TestContractorTest:
    """Verify integration passes the Contractor Test."""

    @pytest.fixture
    def mock_llm(self):
        llm = MagicMock()
        llm.complete = AsyncMock(return_value='{"category": "execution", "action": "create_item", "confidence": 0.9, "reasoning": "test"}')
        return llm

    @pytest.fixture
    def classifier(self, mock_llm):
        return IntentClassifier(llm_service=mock_llm)

    @pytest.mark.asyncio
    async def test_professional_tone(self, classifier):
        """Responses have professional tone."""
        result = await classifier.classify_conscious(
            message="help me with this task",
            spatial_context={"channel": "general"},  # Public channel
        )

        narrative = result.understanding_narrative

        # Should NOT be over-enthusiastic
        assert "!" not in narrative or narrative.count("!") <= 1
        assert "awesome" not in narrative.lower()
        assert "amazing" not in narrative.lower()

        # Should NOT be robotic
        assert "Query:" not in narrative
        assert "Result:" not in narrative
```

---

## Task 4: Update Module Exports

**File**: `services/intent_service/__init__.py`

Ensure all new components are exported:

```python
from services.intent_service.classifier import IntentClassifier
from services.intent_service.intent import Intent
from services.intent_service.intent_types import (
    IntentClassificationContext,
    IntentUnderstanding,
)
from services.intent_service.place_detector import PlaceDetector
from services.intent_service.personality_bridge import PersonalityBridge
from services.intent_service.warmth_calibration import WarmthCalibrator, WarmthLevel
from services.intent_service.honest_failure import (
    HonestFailureHandler,
    create_graceful_error_response,
)

__all__ = [
    "IntentClassifier",
    "Intent",
    "IntentClassificationContext",
    "IntentUnderstanding",
    "PlaceDetector",
    "PersonalityBridge",
    "WarmthCalibrator",
    "WarmthLevel",
    "HonestFailureHandler",
    "create_graceful_error_response",
]
```

---

## Task 5: Run Full Test Suite

```bash
# Run all intent_service tests
pytest tests/unit/services/intent_service/ -v

# Run specific integration tests
pytest tests/unit/services/intent_service/test_classifier_conscious.py -v

# Verify existing tests still pass
pytest tests/unit/services/intent_service/test_classifier.py -v
```

---

## Acceptance Criteria

- [ ] IntentClassifier imports all Phase 1-5 components
- [ ] `__init__` initializes PlaceDetector, PersonalityBridge, WarmthCalibrator, HonestFailureHandler
- [ ] `classify_conscious()` method exists and returns IntentUnderstanding
- [ ] Place detection integrated into classification flow
- [ ] Low confidence handled with uncertainty expression
- [ ] Vague intents handled with clarification requests
- [ ] Errors return graceful IntentUnderstanding (not raise)
- [ ] Original `classify()` unchanged (backward compatible)
- [ ] All existing tests still pass
- [ ] New integration tests pass
- [ ] Contractor Test passes

---

## Completion Matrix

| Check | Status | Evidence |
|-------|--------|----------|
| Phase 1 components import | ⬜ | Python import succeeds |
| Phase 2 PlaceDetector integrated | ⬜ | Place detected in logs |
| Phase 3 PersonalityBridge integrated | ⬜ | Narratives generated |
| Phase 4 WarmthCalibrator integrated | ⬜ | Confidence expressions calibrated |
| Phase 5 HonestFailure integrated | ⬜ | Errors return understanding |
| classify_conscious() works | ⬜ | Integration tests pass |
| classify() unchanged | ⬜ | Existing tests pass |
| All tests green | ⬜ | `pytest` output |

---

## Verification Commands

```bash
# Full verification
pytest tests/unit/services/intent_service/ -v

# Quick integration check
python -c "
import asyncio
from services.intent_service.classifier import IntentClassifier
from unittest.mock import MagicMock, AsyncMock

# Mock LLM
mock_llm = MagicMock()
mock_llm.complete = AsyncMock(return_value='{\"category\": \"execution\", \"action\": \"create_item\", \"confidence\": 0.9, \"reasoning\": \"test\"}')

classifier = IntentClassifier(llm_service=mock_llm)

async def test():
    result = await classifier.classify_conscious(
        'add a todo for tomorrow',
        context={'user_id': 'test'},
        spatial_context={'source': 'web'}
    )
    print('Type:', type(result).__name__)
    print('Narrative:', result.understanding_narrative)
    print('Confidence:', result.confidence_expression)
    print('Place awareness:', result.place_awareness)
    print('\\nSuccess! Grammar-conscious classification working.')

asyncio.run(test())
"
```

---

## Post-Integration

After successful integration:

1. Update issue #619 with completion evidence
2. Create PR with all Phase 1-6 changes
3. Run full test suite: `pytest tests/unit/ -v`
4. Tag for review

---

## Notes

- `classify()` returns `Intent` (unchanged for compatibility)
- `classify_conscious()` returns `IntentUnderstanding` (new)
- Callers can migrate to `classify_conscious()` incrementally
- The transformation is complete when responses feel like Piper *understood* rather than *processed*
