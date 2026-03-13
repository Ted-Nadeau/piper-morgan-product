# Agent Prompt: Phase 5 - Honest Failure (#619)

**Issue**: #619 GRAMMAR-TRANSFORM: Intent Classification
**Phase**: 5 of 6
**Estimated Time**: 1 hour
**Pattern**: Pattern-054 (Honest Failure)
**Prerequisite**: Phases 1-4 complete

---

## Objective

Create graceful failure handling that expresses Piper's confusion honestly rather than throwing technical errors. When Piper doesn't understand, she should admit it warmly.

---

## Task 1: Create Honest Failure Module

**File**: `services/intent_service/honest_failure.py`

```python
"""
Honest failure handling for grammar-conscious intent classification.

When Piper can't understand something, she should admit it gracefully
rather than throwing technical errors. This transforms:
  "IntentClassificationFailedError: LLM response malformed"
into:
  "I'm having trouble understanding that. Could you rephrase it?"

The principle: Piper is a colleague who admits when she's confused,
not a system that "fails."

See: #619 GRAMMAR-TRANSFORM: Intent Classification
Pattern: Pattern-054 (Honest Failure)
"""

from typing import Any, Dict, Optional

from services.shared_types import IntentCategory, PerceptionMode, PlaceType
from services.intent_service.intent import Intent
from services.intent_service.intent_types import (
    IntentClassificationContext,
    IntentUnderstanding,
)
from services.intent_service.warmth_calibration import WarmthCalibrator


class HonestFailureHandler:
    """
    Handles classification failures with grace and warmth.

    Instead of raising exceptions that surface as technical errors,
    this handler creates IntentUnderstanding responses that express
    Piper's confusion appropriately for the context.
    """

    # Confusion narratives by formality
    CONFUSION_NARRATIVES = {
        "casual": "I'm having trouble understanding that one.",
        "professional": "I'm having difficulty interpreting your request.",
        "warm": "I want to help, but I'm not quite following.",
        "terse": "Unable to interpret.",
        "neutral": "I'm not sure I understand.",
    }

    # Follow-up suggestions by formality
    FOLLOW_UP_SUGGESTIONS = {
        "casual": "Could you say that differently?",
        "professional": "Could you please rephrase your request?",
        "warm": "Could you tell me more about what you're looking for?",
        "terse": "Please clarify.",
        "neutral": "Could you rephrase that?",
    }

    def __init__(self, warmth_calibrator: Optional[WarmthCalibrator] = None):
        """
        Initialize the failure handler.

        Args:
            warmth_calibrator: Optional calibrator for error gentleness.
                              If not provided, creates a default one.
        """
        self.warmth_calibrator = warmth_calibrator or WarmthCalibrator()

    def handle_classification_failure(
        self,
        context: IntentClassificationContext,
        place_settings: Dict[str, Any],
        error_detail: Optional[str] = None,
    ) -> IntentUnderstanding:
        """
        Handle a classification failure gracefully.

        Instead of raising an exception, create a warm response that
        asks for clarification.

        Args:
            context: The classification context that failed
            place_settings: Settings from PlaceDetector
            error_detail: Optional technical error detail (for logging)

        Returns:
            IntentUnderstanding that asks for clarification
        """
        formality = place_settings.get("formality", "professional")

        # Create clarification-seeking intent
        clarification_intent = Intent(
            category=IntentCategory.CONVERSATION,
            action="clarification_needed",
            confidence=0.0,
            context={
                "original_message": context.message,
                "failure_type": "classification",
                "needs_human_help": True,
            },
        )

        # Add error detail for debugging (not shown to user)
        if error_detail:
            clarification_intent.context["_error_detail"] = error_detail

        # Get appropriate confusion narrative
        narrative = self.CONFUSION_NARRATIVES.get(
            formality, self.CONFUSION_NARRATIVES["neutral"]
        )

        # Get appropriate follow-up
        follow_up = self.FOLLOW_UP_SUGGESTIONS.get(
            formality, self.FOLLOW_UP_SUGGESTIONS["neutral"]
        )

        return IntentUnderstanding(
            intent=clarification_intent,
            understanding_narrative=narrative,
            confidence_expression="",  # No confidence to express
            place_awareness="",  # Don't call out Place during confusion
            perception_mode=PerceptionMode.NOTICING,
            follow_up_suggestion=follow_up,
        )

    def handle_low_confidence(
        self,
        intent: Intent,
        context: IntentClassificationContext,
        place_settings: Dict[str, Any],
    ) -> IntentUnderstanding:
        """
        Handle low-confidence classification by expressing uncertainty.

        When Piper has a guess but isn't confident, she should express
        that uncertainty rather than acting confident.

        Args:
            intent: The low-confidence Intent
            context: Classification context
            place_settings: Settings from PlaceDetector

        Returns:
            IntentUnderstanding that expresses uncertainty
        """
        formality = place_settings.get("formality", "professional")

        # Build uncertain narrative
        uncertain_narratives = {
            "casual": f"I think you might want to {self._humanize_action(intent.action)}, but I'm not sure.",
            "professional": f"I believe you may be asking to {self._humanize_action(intent.action)}, though I'm uncertain.",
            "warm": f"It seems like you might want to {self._humanize_action(intent.action)}—is that right?",
            "terse": f"Uncertain: {intent.action}?",
            "neutral": f"I think you want to {self._humanize_action(intent.action)}, but please confirm.",
        }

        narrative = uncertain_narratives.get(
            formality, uncertain_narratives["neutral"]
        )

        # Confidence expression for uncertainty
        confidence_expressions = {
            "casual": "I'm not totally sure though",
            "professional": "However, I'm not entirely certain.",
            "warm": "I want to make sure I got that right.",
            "terse": "Unconfirmed.",
            "neutral": "Please confirm.",
        }

        confidence_expr = confidence_expressions.get(
            formality, confidence_expressions["neutral"]
        )

        return IntentUnderstanding(
            intent=intent,
            understanding_narrative=narrative,
            confidence_expression=confidence_expr,
            place_awareness="",
            perception_mode=PerceptionMode.NOTICING,
            follow_up_suggestion="Is that what you meant?",
        )

    def handle_vague_intent(
        self,
        intent: Intent,
        context: IntentClassificationContext,
        place_settings: Dict[str, Any],
    ) -> IntentUnderstanding:
        """
        Handle vague/underspecified intents by asking for details.

        When the user's request is too vague to act on (e.g., "help me
        with something"), Piper should ask for specifics.

        Args:
            intent: The vague Intent
            context: Classification context
            place_settings: Settings from PlaceDetector

        Returns:
            IntentUnderstanding that asks for specifics
        """
        formality = place_settings.get("formality", "professional")

        # Vague request narratives
        vague_narratives = {
            "casual": "I'd love to help! What specifically are you looking for?",
            "professional": "I'm ready to assist. Could you provide more details?",
            "warm": "I'm here to help! What would you like me to do?",
            "terse": "Please specify.",
            "neutral": "Could you be more specific about what you need?",
        }

        narrative = vague_narratives.get(formality, vague_narratives["neutral"])

        return IntentUnderstanding(
            intent=intent,
            understanding_narrative=narrative,
            confidence_expression="",
            place_awareness="",
            perception_mode=PerceptionMode.NOTICING,
            follow_up_suggestion=None,  # Narrative already asks
        )

    def _humanize_action(self, action: str) -> str:
        """Convert technical action to human-readable form."""
        # Simple conversion: replace underscores with spaces
        return action.replace("_", " ")


def create_graceful_error_response(
    context: IntentClassificationContext,
    place_settings: Dict[str, Any],
    error: Exception,
) -> IntentUnderstanding:
    """
    Factory function to create graceful error response.

    Use this in try/except blocks instead of re-raising:

    try:
        result = await classify(...)
    except Exception as e:
        return create_graceful_error_response(context, settings, e)

    Args:
        context: Classification context
        place_settings: Place settings
        error: The caught exception

    Returns:
        IntentUnderstanding expressing confusion
    """
    handler = HonestFailureHandler()
    return handler.handle_classification_failure(
        context=context,
        place_settings=place_settings,
        error_detail=str(error),
    )
```

---

## Task 2: Create Unit Tests

**File**: `tests/unit/services/intent_service/test_honest_failure.py`

```python
"""Tests for HonestFailureHandler."""

import pytest

from services.shared_types import IntentCategory, PerceptionMode, PlaceType
from services.intent_service.intent import Intent
from services.intent_service.intent_types import IntentClassificationContext
from services.intent_service.honest_failure import (
    HonestFailureHandler,
    create_graceful_error_response,
)


class TestHonestFailureHandler:
    """Test HonestFailureHandler."""

    @pytest.fixture
    def handler(self):
        return HonestFailureHandler()

    @pytest.fixture
    def basic_context(self):
        return IntentClassificationContext(
            message="do the thing with the stuff",
            user_id="user-1",
            place=PlaceType.WEB_CHAT,
        )

    @pytest.fixture
    def casual_settings(self):
        return {"formality": "casual", "verbosity": "medium"}

    @pytest.fixture
    def professional_settings(self):
        return {"formality": "professional", "verbosity": "concise"}

    @pytest.fixture
    def terse_settings(self):
        return {"formality": "terse", "verbosity": "minimal"}

    # --- Classification Failure Tests ---

    def test_failure_creates_understanding(
        self, handler, basic_context, casual_settings
    ):
        """Failure creates IntentUnderstanding, not exception."""
        result = handler.handle_classification_failure(
            context=basic_context,
            place_settings=casual_settings,
        )
        # Returns understanding, not raises exception
        assert result is not None
        assert result.intent.category == IntentCategory.CONVERSATION
        assert result.intent.action == "clarification_needed"

    def test_failure_narrative_is_warm(
        self, handler, basic_context, casual_settings
    ):
        """Failure narrative uses warm language."""
        result = handler.handle_classification_failure(
            context=basic_context,
            place_settings=casual_settings,
        )
        narrative = result.understanding_narrative.lower()
        # Should express difficulty, not failure
        assert "having trouble" in narrative or "not quite" in narrative
        # Should NOT be technical
        assert "error" not in narrative
        assert "failed" not in narrative
        assert "exception" not in narrative

    def test_failure_suggests_followup(
        self, handler, basic_context, casual_settings
    ):
        """Failure suggests how to proceed."""
        result = handler.handle_classification_failure(
            context=basic_context,
            place_settings=casual_settings,
        )
        assert result.follow_up_suggestion is not None
        # Should ask for clarification
        assert "?" in result.follow_up_suggestion

    def test_terse_failure_is_brief(
        self, handler, basic_context, terse_settings
    ):
        """Terse context gets brief failure message."""
        result = handler.handle_classification_failure(
            context=basic_context,
            place_settings=terse_settings,
        )
        assert len(result.understanding_narrative) < 30
        assert result.follow_up_suggestion == "Please clarify."

    # --- Low Confidence Tests ---

    def test_low_confidence_expresses_uncertainty(
        self, handler, basic_context, casual_settings
    ):
        """Low confidence expressed as uncertainty."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="search_files",
            confidence=0.3,
        )
        result = handler.handle_low_confidence(
            intent=intent,
            context=basic_context,
            place_settings=casual_settings,
        )
        narrative = result.understanding_narrative.lower()
        # Should express uncertainty
        assert "think" in narrative or "might" in narrative or "not sure" in narrative

    def test_low_confidence_asks_confirmation(
        self, handler, basic_context, professional_settings
    ):
        """Low confidence asks for confirmation."""
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_item",
            confidence=0.4,
        )
        result = handler.handle_low_confidence(
            intent=intent,
            context=basic_context,
            place_settings=professional_settings,
        )
        # Should ask if understanding is correct
        assert result.follow_up_suggestion is not None
        assert "?" in result.follow_up_suggestion

    # --- Vague Intent Tests ---

    def test_vague_intent_asks_for_specifics(
        self, handler, basic_context, casual_settings
    ):
        """Vague intent asks for more details."""
        intent = Intent(
            category=IntentCategory.LEARNING,
            action="learn_pattern",
            confidence=0.5,
        )
        result = handler.handle_vague_intent(
            intent=intent,
            context=basic_context,
            place_settings=casual_settings,
        )
        narrative = result.understanding_narrative.lower()
        # Should ask what they want
        assert "what" in narrative or "specific" in narrative

    def test_vague_intent_offers_help(
        self, handler, basic_context, casual_settings
    ):
        """Vague intent offers willingness to help."""
        intent = Intent(
            category=IntentCategory.CONVERSATION,
            action="get_help",
            confidence=0.6,
        )
        result = handler.handle_vague_intent(
            intent=intent,
            context=basic_context,
            place_settings=casual_settings,
        )
        narrative = result.understanding_narrative.lower()
        # Should offer help
        assert "help" in narrative

    # --- Experience Tests ---

    def test_no_technical_jargon(self, handler, basic_context, casual_settings):
        """Responses should avoid technical jargon."""
        result = handler.handle_classification_failure(
            context=basic_context,
            place_settings=casual_settings,
            error_detail="JSONDecodeError: Invalid JSON",
        )
        narrative = result.understanding_narrative.lower()
        follow_up = (result.follow_up_suggestion or "").lower()

        # Technical terms should NOT appear in user-facing text
        assert "json" not in narrative
        assert "decode" not in narrative
        assert "exception" not in narrative
        assert "json" not in follow_up


class TestCreateGracefulErrorResponse:
    """Test the factory function."""

    def test_factory_creates_response(self):
        """Factory function creates graceful response."""
        context = IntentClassificationContext(
            message="broken request",
            place=PlaceType.WEB_CHAT,
        )
        settings = {"formality": "warm"}

        result = create_graceful_error_response(
            context=context,
            place_settings=settings,
            error=ValueError("something broke"),
        )

        assert result is not None
        assert result.intent.action == "clarification_needed"
        # Error detail stored for debugging but not shown
        assert "_error_detail" in result.intent.context


class TestContractorTest:
    """Verify responses pass the 'Contractor Test'."""

    def test_failure_sounds_professional(self):
        """Failure responses should sound professional."""
        handler = HonestFailureHandler()
        context = IntentClassificationContext(
            message="test",
            place=PlaceType.SLACK_CHANNEL,
        )
        settings = {"formality": "professional"}

        result = handler.handle_classification_failure(
            context=context,
            place_settings=settings,
        )

        narrative = result.understanding_narrative

        # Should NOT sound like a children's app
        assert "Oops" not in narrative
        assert "Uh oh" not in narrative
        assert "!" not in narrative  # No exclamation in errors

        # SHOULD sound like a professional colleague
        assert "I'm" in narrative  # First person
```

---

## Task 3: Update Exports

**File**: `services/intent_service/__init__.py`

Add to exports:

```python
from services.intent_service.honest_failure import (
    HonestFailureHandler,
    create_graceful_error_response,
)

__all__ = [
    # ... existing exports ...
    "HonestFailureHandler",
    "create_graceful_error_response",
]
```

---

## Acceptance Criteria

- [ ] HonestFailureHandler class created
- [ ] handle_classification_failure() returns IntentUnderstanding
- [ ] handle_low_confidence() expresses uncertainty
- [ ] handle_vague_intent() asks for specifics
- [ ] No technical jargon in user-facing text
- [ ] create_graceful_error_response() factory works
- [ ] Contractor Test passes
- [ ] All unit tests pass: `pytest tests/unit/services/intent_service/test_honest_failure.py -v`

---

## Verification Commands

```bash
# Run the new tests
pytest tests/unit/services/intent_service/test_honest_failure.py -v

# Verify import works
python -c "from services.intent_service.honest_failure import HonestFailureHandler; print('HonestFailureHandler OK')"

# Quick manual test
python -c "
from services.intent_service.honest_failure import HonestFailureHandler
from services.intent_service.intent_types import IntentClassificationContext
from services.shared_types import PlaceType

handler = HonestFailureHandler()
ctx = IntentClassificationContext(message='do the thing', place=PlaceType.WEB_CHAT)

result = handler.handle_classification_failure(ctx, {'formality': 'warm'})
print('Narrative:', result.understanding_narrative)
print('Follow-up:', result.follow_up_suggestion)
"
```

---

## Notes

- This phase does NOT modify classifier.py yet
- Error details stored in context for logging, not shown to user
- The principle: Piper admits confusion, doesn't "fail"
- Integration into classifier happens in Phase 6
