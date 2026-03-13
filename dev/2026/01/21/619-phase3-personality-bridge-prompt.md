# Agent Prompt: Phase 3 - Personality Bridge (#619)

**Issue**: #619 GRAMMAR-TRANSFORM: Intent Classification
**Phase**: 3 of 6 (can run parallel with 2, 4 after Phase 1)
**Estimated Time**: 2 hours
**Pattern**: Pattern-052 (Personality Bridge)
**Prerequisite**: Phase 1 complete (IntentUnderstanding, PerceptionMode exist)

---

## Objective

Create the personality bridge that transforms raw Intent data into Piper's experiential understanding. This is the core grammar transformation - making "classification result" into "what Piper understood."

---

## Task 1: Create Personality Bridge Module

**File**: `services/intent_service/personality_bridge.py`

```python
"""
Personality bridge for grammar-conscious intent classification.

This module transforms raw Intent objects into IntentUnderstanding,
adding the experiential framing that makes Piper feel like a colleague
who understood you, not a system that processed your query.

The bridge applies:
- Perception mode (noticing, remembering, anticipating)
- Understanding narratives ("I understand you want to...")
- Action humanization (technical → natural language)

See: #619 GRAMMAR-TRANSFORM: Intent Classification
Pattern: Pattern-052 (Personality Bridge)
"""

from typing import Any, Dict, Optional

from services.shared_types import IntentCategory, PerceptionMode, PlaceType
from services.intent_service.intent import Intent
from services.intent_service.intent_types import (
    IntentClassificationContext,
    IntentUnderstanding,
)


# Maps technical action names to human-readable descriptions
ACTION_NARRATIVES: Dict[str, str] = {
    # Execution actions
    "create_item": "create something new",
    "create_todo": "add a new todo",
    "update_item": "update something",
    "delete_item": "remove something",
    "complete_todo": "mark something as done",

    # Query actions
    "search_files": "find some files",
    "search_documents": "search through documents",
    "find_documents": "locate some documents",
    "list_items": "see a list of things",
    "list_todos": "see your todos",
    "count_projects": "know how many projects you have",
    "get_project": "get project details",

    # Analysis actions
    "analyze_data": "analyze some data",
    "analyze_document": "analyze a document",
    "summarize_document": "get a summary",
    "compare_documents": "compare documents",

    # Conversation actions
    "clarification_needed": "help me understand what you need",
    "greeting": "say hello",
    "get_help": "get some help",

    # Strategy actions
    "strategic_planning": "think through a plan",
    "prioritize": "figure out priorities",

    # Learning actions
    "learn_pattern": "learn something new",
}

# Narrative templates by perception mode
PERCEPTION_TEMPLATES: Dict[PerceptionMode, str] = {
    PerceptionMode.NOTICING: "I understand you want to {action}",
    PerceptionMode.REMEMBERING: "I remember you often ask about {action}",
    PerceptionMode.ANTICIPATING: "You might be wanting to {action}",
}


class PersonalityBridge:
    """
    Transforms raw Intent into grammar-conscious IntentUnderstanding.

    The personality bridge is where technical classification becomes
    experiential understanding. It's the difference between
    "Query: search_files, confidence: 0.85" and
    "I understand you want to find some files."
    """

    def __init__(self, recent_intents: Optional[Dict[str, list]] = None):
        """
        Initialize the personality bridge.

        Args:
            recent_intents: Optional dict mapping user_id to list of recent
                           action strings, for pattern detection.
        """
        self.recent_intents = recent_intents or {}

    def transform(
        self,
        intent: Intent,
        context: IntentClassificationContext,
        place_settings: Dict[str, Any],
    ) -> IntentUnderstanding:
        """
        Transform raw Intent into IntentUnderstanding.

        This is the main bridge method that takes classification output
        and makes it feel like Piper's understanding.

        Args:
            intent: Raw Intent from classification
            context: Rich classification context
            place_settings: Settings from PlaceDetector

        Returns:
            IntentUnderstanding with experiential framing
        """
        # Determine how Piper is perceiving this
        perception = self._determine_perception_mode(intent, context)

        # Build the understanding narrative
        narrative = self._build_narrative(intent, perception)

        # Express confidence in human terms
        confidence_expr = self._express_confidence(
            intent.confidence, place_settings
        )

        # Note Place awareness if relevant
        place_note = self._note_place_awareness(context.place, place_settings)

        # Suggest follow-up if appropriate
        follow_up = self._suggest_follow_up(intent, context)

        return IntentUnderstanding(
            intent=intent,
            understanding_narrative=narrative,
            confidence_expression=confidence_expr,
            place_awareness=place_note,
            perception_mode=perception,
            follow_up_suggestion=follow_up,
        )

    def _determine_perception_mode(
        self,
        intent: Intent,
        context: IntentClassificationContext,
    ) -> PerceptionMode:
        """
        Determine how Piper is perceiving this intent.

        - REMEMBERING: If user has asked similar things recently
        - ANTICIPATING: If this seems like a follow-up
        - NOTICING: Default - fresh observation
        """
        # Check for repeated pattern
        if context.user_id and self._is_repeated_pattern(
            context.user_id, intent.action
        ):
            return PerceptionMode.REMEMBERING

        # Check if this follows from conversation history
        if context.conversation_history and self._seems_like_follow_up(
            intent, context.conversation_history
        ):
            return PerceptionMode.ANTICIPATING

        # Default: noticing something new
        return PerceptionMode.NOTICING

    def _is_repeated_pattern(self, user_id: str, action: str) -> bool:
        """Check if this user frequently requests this action."""
        user_history = self.recent_intents.get(user_id, [])
        if len(user_history) < 3:
            return False
        # If more than half of recent intents are this action
        return user_history.count(action) >= len(user_history) // 2

    def _seems_like_follow_up(
        self, intent: Intent, history: list[str]
    ) -> bool:
        """Check if intent seems to follow from conversation history."""
        if not history:
            return False
        # Simple heuristic: if last message was a question and this is related
        last_message = history[-1].lower() if history else ""
        follow_up_indicators = ["yes", "no", "that one", "the first", "okay"]
        return any(indicator in last_message for indicator in follow_up_indicators)

    def _build_narrative(
        self,
        intent: Intent,
        perception: PerceptionMode,
    ) -> str:
        """
        Build the understanding narrative.

        This is the core of making classification feel experiential.
        """
        template = PERCEPTION_TEMPLATES[perception]
        humanized_action = self._humanize_action(intent.action)
        return template.format(action=humanized_action)

    def _humanize_action(self, action: str) -> str:
        """Convert technical action name to natural language."""
        # Check our mapping first
        if action in ACTION_NARRATIVES:
            return ACTION_NARRATIVES[action]

        # Fallback: convert snake_case to readable form
        readable = action.replace("_", " ")
        return readable

    def _express_confidence(
        self,
        confidence: float,
        place_settings: Dict[str, Any],
    ) -> str:
        """Express confidence level in human terms."""
        formality = place_settings.get("formality", "professional")

        # High confidence (>= 0.9)
        if confidence >= 0.9:
            return {
                "casual": "Got it!",
                "professional": "I understand.",
                "warm": "I understand what you're looking for.",
                "terse": "Understood.",
                "neutral": "Understood.",
            }.get(formality, "I understand.")

        # Medium-high confidence (>= 0.7)
        if confidence >= 0.7:
            return {
                "casual": "I think I've got it",
                "professional": "I believe I understand.",
                "warm": "I think I understand what you mean.",
                "terse": "Likely.",
                "neutral": "I believe I understand.",
            }.get(formality, "I believe I understand.")

        # Medium confidence (>= 0.5)
        if confidence >= 0.5:
            return {
                "casual": "I'm not 100% sure, but",
                "professional": "I'm not entirely certain, but",
                "warm": "I want to make sure I understand—",
                "terse": "Uncertain.",
                "neutral": "I'm not entirely certain, but",
            }.get(formality, "I'm not entirely certain, but")

        # Low confidence (< 0.5)
        return {
            "casual": "Hmm, I'm not quite sure what you mean",
            "professional": "I'm having difficulty understanding.",
            "warm": "I want to help, but I'm not sure I understood.",
            "terse": "Unclear.",
            "neutral": "I'm having difficulty understanding.",
        }.get(formality, "I'm having difficulty understanding.")

    def _note_place_awareness(
        self,
        place: PlaceType,
        place_settings: Dict[str, Any],
    ) -> str:
        """
        Generate Place awareness note if relevant.

        Most Places don't need explicit acknowledgment - it would feel
        weird for Piper to say "Since we're in a DM..." every time.
        Only note Place when it affects the response meaningfully.
        """
        if place == PlaceType.SLACK_CHANNEL:
            return "Since we're in a channel, I'll keep this brief."
        # Most cases: no explicit Place mention
        return ""

    def _suggest_follow_up(
        self,
        intent: Intent,
        context: IntentClassificationContext,
    ) -> Optional[str]:
        """Suggest what Piper might ask next, if appropriate."""
        # Low confidence: offer to clarify
        if intent.confidence < 0.5:
            return "Could you tell me more about what you're looking for?"

        # Vague action: ask for specifics
        if intent.action in ("clarification_needed", "learn_pattern"):
            return "What specifically would you like me to help with?"

        # Search without query: ask what to search for
        if intent.action in ("search_files", "search_documents"):
            if not intent.context or not intent.context.get("search_query"):
                return "What would you like me to search for?"

        # Most cases: no follow-up needed
        return None

    def record_intent(self, user_id: str, action: str) -> None:
        """
        Record an intent for pattern detection.

        Call this after classification to build history for
        REMEMBERING perception mode.
        """
        if user_id not in self.recent_intents:
            self.recent_intents[user_id] = []
        self.recent_intents[user_id].append(action)
        # Keep only last 10
        self.recent_intents[user_id] = self.recent_intents[user_id][-10:]
```

---

## Task 2: Create Unit Tests

**File**: `tests/unit/services/intent_service/test_personality_bridge.py`

```python
"""Tests for PersonalityBridge."""

import pytest

from services.shared_types import IntentCategory, PerceptionMode, PlaceType
from services.intent_service.intent import Intent
from services.intent_service.intent_types import IntentClassificationContext
from services.intent_service.personality_bridge import (
    PersonalityBridge,
    ACTION_NARRATIVES,
)


class TestPersonalityBridge:
    """Test PersonalityBridge transformation."""

    @pytest.fixture
    def bridge(self):
        return PersonalityBridge()

    @pytest.fixture
    def basic_intent(self):
        return Intent(
            category=IntentCategory.EXECUTION,
            action="create_item",
            confidence=0.9,
        )

    @pytest.fixture
    def basic_context(self):
        return IntentClassificationContext(
            message="add a todo",
            place=PlaceType.WEB_CHAT,
        )

    @pytest.fixture
    def casual_settings(self):
        return {"formality": "casual", "verbosity": "medium"}

    @pytest.fixture
    def professional_settings(self):
        return {"formality": "professional", "verbosity": "concise"}

    # --- Transform Tests ---

    def test_transform_creates_understanding(
        self, bridge, basic_intent, basic_context, casual_settings
    ):
        """Transform creates IntentUnderstanding."""
        understanding = bridge.transform(
            basic_intent, basic_context, casual_settings
        )
        assert understanding.intent == basic_intent
        assert understanding.perception_mode == PerceptionMode.NOTICING
        assert "understand" in understanding.understanding_narrative.lower()

    def test_experience_test_no_mechanical_language(
        self, bridge, basic_intent, basic_context, casual_settings
    ):
        """Understanding uses experiential, not mechanical language."""
        understanding = bridge.transform(
            basic_intent, basic_context, casual_settings
        )
        # These should NOT appear
        assert "Query" not in understanding.understanding_narrative
        assert "Classification" not in understanding.understanding_narrative
        assert "returned" not in understanding.understanding_narrative
        # These SHOULD appear
        assert "I" in understanding.understanding_narrative

    # --- Perception Mode Tests ---

    def test_noticing_is_default(
        self, bridge, basic_intent, basic_context, casual_settings
    ):
        """Default perception mode is NOTICING."""
        understanding = bridge.transform(
            basic_intent, basic_context, casual_settings
        )
        assert understanding.perception_mode == PerceptionMode.NOTICING

    def test_remembering_for_repeated_patterns(self, basic_context, casual_settings):
        """Repeated patterns trigger REMEMBERING mode."""
        # Set up history showing repeated pattern
        bridge = PersonalityBridge(
            recent_intents={"user-1": ["create_item"] * 5}
        )
        context = IntentClassificationContext(
            message="add another",
            user_id="user-1",
            place=PlaceType.WEB_CHAT,
        )
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_item",
            confidence=0.9,
        )
        understanding = bridge.transform(intent, context, casual_settings)
        assert understanding.perception_mode == PerceptionMode.REMEMBERING

    # --- Confidence Expression Tests ---

    def test_high_confidence_expression_casual(
        self, bridge, basic_context, casual_settings
    ):
        """High confidence expressed casually."""
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_item",
            confidence=0.95,
        )
        understanding = bridge.transform(intent, basic_context, casual_settings)
        assert understanding.confidence_expression == "Got it!"

    def test_high_confidence_expression_professional(
        self, bridge, basic_context, professional_settings
    ):
        """High confidence expressed professionally."""
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_item",
            confidence=0.95,
        )
        understanding = bridge.transform(intent, basic_context, professional_settings)
        assert understanding.confidence_expression == "I understand."

    def test_low_confidence_expresses_uncertainty(
        self, bridge, basic_context, casual_settings
    ):
        """Low confidence expressed as uncertainty."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="search_files",
            confidence=0.3,
        )
        understanding = bridge.transform(intent, basic_context, casual_settings)
        assert "not" in understanding.confidence_expression.lower() or \
               "sure" in understanding.confidence_expression.lower()

    # --- Action Humanization Tests ---

    def test_action_humanization(self, bridge):
        """Technical actions become human-readable."""
        assert "new" in bridge._humanize_action("create_item")
        assert "find" in bridge._humanize_action("search_files")
        assert "list" in bridge._humanize_action("list_items")

    def test_unknown_action_readable(self, bridge):
        """Unknown actions still become readable."""
        result = bridge._humanize_action("weird_unknown_action")
        assert "_" not in result  # Underscores removed
        assert "weird unknown action" == result

    # --- Place Awareness Tests ---

    def test_slack_channel_notes_brevity(
        self, bridge, basic_intent, professional_settings
    ):
        """Slack channel gets brevity note."""
        context = IntentClassificationContext(
            message="add a todo",
            place=PlaceType.SLACK_CHANNEL,
        )
        understanding = bridge.transform(
            basic_intent, context, professional_settings
        )
        assert "brief" in understanding.place_awareness.lower()

    def test_other_places_no_note(
        self, bridge, basic_intent, basic_context, casual_settings
    ):
        """Other Places don't need explicit notes."""
        understanding = bridge.transform(
            basic_intent, basic_context, casual_settings
        )
        assert understanding.place_awareness == ""

    # --- Follow-up Suggestion Tests ---

    def test_low_confidence_suggests_clarification(
        self, bridge, basic_context, casual_settings
    ):
        """Low confidence suggests clarification."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="search_files",
            confidence=0.3,
        )
        understanding = bridge.transform(intent, basic_context, casual_settings)
        assert understanding.follow_up_suggestion is not None
        assert "more" in understanding.follow_up_suggestion.lower()

    def test_high_confidence_no_follow_up(
        self, bridge, basic_intent, basic_context, casual_settings
    ):
        """High confidence usually needs no follow-up."""
        understanding = bridge.transform(
            basic_intent, basic_context, casual_settings
        )
        assert understanding.follow_up_suggestion is None


class TestActionNarratives:
    """Test ACTION_NARRATIVES completeness."""

    def test_common_actions_have_narratives(self):
        """Common actions have human-readable narratives."""
        common_actions = [
            "create_item",
            "search_files",
            "list_items",
            "clarification_needed",
        ]
        for action in common_actions:
            assert action in ACTION_NARRATIVES
            # Narrative should be human-readable
            narrative = ACTION_NARRATIVES[action]
            assert "_" not in narrative
            assert len(narrative) > 5
```

---

## Acceptance Criteria

- [ ] PersonalityBridge class created
- [ ] transform() converts Intent to IntentUnderstanding
- [ ] Perception mode detection (NOTICING, REMEMBERING, ANTICIPATING)
- [ ] Action humanization (technical → natural language)
- [ ] Confidence expression varies by formality
- [ ] Place awareness notes generated appropriately
- [ ] Follow-up suggestions for low confidence
- [ ] All unit tests pass: `pytest tests/unit/services/intent_service/test_personality_bridge.py -v`

---

## Verification Commands

```bash
# Run the new tests
pytest tests/unit/services/intent_service/test_personality_bridge.py -v

# Verify import works
python -c "from services.intent_service.personality_bridge import PersonalityBridge; print('PersonalityBridge OK')"

# Quick manual test
python -c "
from services.intent_service.personality_bridge import PersonalityBridge
from services.intent_service.intent import Intent
from services.intent_service.intent_types import IntentClassificationContext
from services.shared_types import IntentCategory, PlaceType

bridge = PersonalityBridge()
intent = Intent(category=IntentCategory.EXECUTION, action='create_item', confidence=0.9)
ctx = IntentClassificationContext(message='add a todo', place=PlaceType.WEB_CHAT)
settings = {'formality': 'warm', 'verbosity': 'full'}

understanding = bridge.transform(intent, ctx, settings)
print('Narrative:', understanding.understanding_narrative)
print('Confidence:', understanding.confidence_expression)
print('Mode:', understanding.perception_mode)
"
```

---

## Notes

- This phase does NOT modify classifier.py
- The bridge is the heart of the grammar transformation
- ACTION_NARRATIVES can be extended as new actions are added
- Perception mode detection is simple now; can be enhanced later
