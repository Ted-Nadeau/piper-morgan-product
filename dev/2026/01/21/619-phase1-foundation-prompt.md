# Agent Prompt: Phase 1 - Foundation Dataclasses (#619)

**Issue**: #619 GRAMMAR-TRANSFORM: Intent Classification
**Phase**: 1 of 6
**Estimated Time**: 1-2 hours
**Pattern**: Pattern-050 (Context Dataclass Pair)

---

## Objective

Create the foundational dataclasses and enums needed for grammar-conscious intent classification. This enables Phases 2-4 to run in parallel.

---

## Task 1: Add Enums to shared_types.py

**File**: `services/shared_types.py`

Add these enums (check if they already exist first):

```python
class PlaceType(str, Enum):
    """Where the interaction is happening - the Place in MUX grammar."""
    SLACK_DM = "slack_dm"
    SLACK_CHANNEL = "slack_channel"
    WEB_CHAT = "web_chat"
    CLI = "cli"
    API = "api"
    UNKNOWN = "unknown"


class PerceptionMode(str, Enum):
    """How Piper perceives the intent - temporal framing."""
    NOTICING = "noticing"       # Present: "I notice you want..."
    REMEMBERING = "remembering"  # Past: "I remember you asked..."
    ANTICIPATING = "anticipating"  # Future: "You might also want..."
```

---

## Task 2: Create/Extend intent_types.py

**File**: `services/intent_service/intent_types.py`

If file exists, extend it. If not, create it.

```python
"""
Grammar-conscious intent classification types.

These dataclasses support the MUX grammar transformation of intent
classification from data processing to experiential understanding.

See: #619 GRAMMAR-TRANSFORM: Intent Classification
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from services.shared_types import PerceptionMode, PlaceType

# Import existing Intent class for wrapping
from services.intent_service.intent import Intent


@dataclass
class IntentClassificationContext:
    """
    Rich context for intent classification - the Situation.

    This captures everything Piper knows when trying to understand
    what someone wants. It's not just the message, but the full
    context of who, where, when, and what came before.
    """
    message: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    place: PlaceType = PlaceType.UNKNOWN
    spatial_context: Optional[Dict[str, Any]] = None
    conversation_history: Optional[List[str]] = None
    user_preferences: Optional[Dict[str, Any]] = None
    timestamp: datetime = field(default_factory=datetime.now)

    @classmethod
    def from_classify_args(
        cls,
        message: str,
        context: Optional[Dict] = None,
        spatial_context: Optional[Dict] = None,
        place: PlaceType = PlaceType.UNKNOWN,
    ) -> "IntentClassificationContext":
        """Build context from existing classify() arguments."""
        return cls(
            message=message,
            user_id=context.get("user_id") if context else None,
            session_id=context.get("session_id") if context else None,
            place=place,
            spatial_context=spatial_context,
            conversation_history=context.get("conversation_history") if context else None,
            user_preferences=context.get("user_preferences") if context else None,
        )


@dataclass
class IntentUnderstanding:
    """
    Grammar-conscious classification result - Piper's understanding.

    This wraps the raw Intent with experiential framing. Instead of
    "classification result", this represents "what Piper understood
    and how she's expressing that understanding."

    The `intent` field preserves backward compatibility - existing
    code can access the raw Intent via understanding.intent.
    """
    intent: Intent
    understanding_narrative: str  # "I understand you want to..."
    confidence_expression: str    # "I'm fairly certain" / "I think"
    place_awareness: str          # "Since we're in Slack..." (often empty)
    perception_mode: PerceptionMode
    follow_up_suggestion: Optional[str] = None  # What Piper might ask next

    @property
    def category(self):
        """Proxy to intent.category for compatibility."""
        return self.intent.category

    @property
    def action(self):
        """Proxy to intent.action for compatibility."""
        return self.intent.action

    @property
    def confidence(self):
        """Proxy to intent.confidence for compatibility."""
        return self.intent.confidence
```

---

## Task 3: Create Unit Tests

**File**: `tests/unit/services/intent_service/test_intent_types.py`

```python
"""Tests for grammar-conscious intent types."""

import pytest
from datetime import datetime

from services.shared_types import PerceptionMode, PlaceType, IntentCategory
from services.intent_service.intent_types import (
    IntentClassificationContext,
    IntentUnderstanding,
)
from services.intent_service.intent import Intent


class TestPlaceType:
    """Test PlaceType enum."""

    def test_all_places_defined(self):
        """All expected Place types exist."""
        assert PlaceType.SLACK_DM == "slack_dm"
        assert PlaceType.SLACK_CHANNEL == "slack_channel"
        assert PlaceType.WEB_CHAT == "web_chat"
        assert PlaceType.CLI == "cli"
        assert PlaceType.API == "api"
        assert PlaceType.UNKNOWN == "unknown"


class TestPerceptionMode:
    """Test PerceptionMode enum."""

    def test_all_modes_defined(self):
        """All perception modes exist."""
        assert PerceptionMode.NOTICING == "noticing"
        assert PerceptionMode.REMEMBERING == "remembering"
        assert PerceptionMode.ANTICIPATING == "anticipating"


class TestIntentClassificationContext:
    """Test IntentClassificationContext dataclass."""

    def test_basic_creation(self):
        """Can create with just a message."""
        ctx = IntentClassificationContext(message="add a todo")
        assert ctx.message == "add a todo"
        assert ctx.place == PlaceType.UNKNOWN
        assert ctx.user_id is None

    def test_full_creation(self):
        """Can create with all fields."""
        ctx = IntentClassificationContext(
            message="add a todo",
            user_id="user-123",
            session_id="session-456",
            place=PlaceType.SLACK_DM,
            spatial_context={"channel": "D123"},
            conversation_history=["hello", "hi there"],
        )
        assert ctx.user_id == "user-123"
        assert ctx.place == PlaceType.SLACK_DM
        assert len(ctx.conversation_history) == 2

    def test_from_classify_args(self):
        """Factory method builds from existing args."""
        ctx = IntentClassificationContext.from_classify_args(
            message="find documents",
            context={"user_id": "u1", "session_id": "s1"},
            spatial_context={"channel": "C123"},
            place=PlaceType.SLACK_CHANNEL,
        )
        assert ctx.message == "find documents"
        assert ctx.user_id == "u1"
        assert ctx.place == PlaceType.SLACK_CHANNEL


class TestIntentUnderstanding:
    """Test IntentUnderstanding dataclass."""

    def test_wraps_intent(self):
        """IntentUnderstanding wraps raw Intent."""
        raw_intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_item",
            confidence=0.9,
        )
        understanding = IntentUnderstanding(
            intent=raw_intent,
            understanding_narrative="I understand you want to create something",
            confidence_expression="Got it!",
            place_awareness="",
            perception_mode=PerceptionMode.NOTICING,
        )
        assert understanding.intent == raw_intent
        assert understanding.category == IntentCategory.EXECUTION
        assert understanding.action == "create_item"

    def test_proxy_properties(self):
        """Proxy properties allow compatible access."""
        raw_intent = Intent(
            category=IntentCategory.QUERY,
            action="search_files",
            confidence=0.75,
        )
        understanding = IntentUnderstanding(
            intent=raw_intent,
            understanding_narrative="I think you want to search",
            confidence_expression="I believe I understand",
            place_awareness="",
            perception_mode=PerceptionMode.NOTICING,
        )
        # These should work like accessing intent directly
        assert understanding.category == raw_intent.category
        assert understanding.action == raw_intent.action
        assert understanding.confidence == raw_intent.confidence

    def test_experience_not_mechanical(self):
        """Understanding uses experiential language."""
        understanding = IntentUnderstanding(
            intent=Intent(
                category=IntentCategory.EXECUTION,
                action="create_item",
                confidence=0.9,
            ),
            understanding_narrative="I understand you want to create something",
            confidence_expression="Got it!",
            place_awareness="",
            perception_mode=PerceptionMode.NOTICING,
        )
        # Experience test: no mechanical language
        assert "Query returned" not in understanding.understanding_narrative
        assert "Classification" not in understanding.understanding_narrative
        assert "I understand" in understanding.understanding_narrative
```

---

## Acceptance Criteria

- [ ] PlaceType enum added to shared_types.py
- [ ] PerceptionMode enum added to shared_types.py
- [ ] IntentClassificationContext dataclass created
- [ ] IntentUnderstanding dataclass created
- [ ] Proxy properties work for backward compatibility
- [ ] All unit tests pass: `pytest tests/unit/services/intent_service/test_intent_types.py -v`

---

## Verification Commands

```bash
# Run the new tests
pytest tests/unit/services/intent_service/test_intent_types.py -v

# Verify imports work
python -c "from services.shared_types import PlaceType, PerceptionMode; print('Enums OK')"
python -c "from services.intent_service.intent_types import IntentClassificationContext, IntentUnderstanding; print('Types OK')"
```

---

## Notes

- Do NOT modify classifier.py in this phase
- These types enable Phases 2-4 to work independently
- Keep dataclasses simple; logic goes in later phases
