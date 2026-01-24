"""
Tests for composting domain models.

Part of #665 COMPOSTING-MODELS (child of #436 MUX-TECH-PHASE4-COMPOSTING).
"""

from datetime import datetime, timedelta

import pytest

from services.mux.composting_models import (
    CompostingTrigger,
    Correction,
    ExtractedLearning,
    Insight,
    Pattern,
    create_correction_learning,
    create_insight_learning,
    create_pattern_learning,
)

# =============================================================================
# CompostingTrigger Tests
# =============================================================================


class TestCompostingTrigger:
    """Tests for CompostingTrigger enum."""

    def test_has_all_expected_triggers(self):
        """Verify all trigger types exist."""
        triggers = [t.value for t in CompostingTrigger]
        assert "age" in triggers
        assert "irrelevance" in triggers
        assert "manual" in triggers
        assert "scheduled" in triggers
        assert "contradiction" in triggers

    def test_trigger_count(self):
        """Verify we have exactly 5 trigger types."""
        assert len(CompostingTrigger) == 5

    def test_trigger_values_are_strings(self):
        """Verify trigger values are lowercase strings."""
        for trigger in CompostingTrigger:
            assert isinstance(trigger.value, str)
            assert trigger.value == trigger.value.lower()


# =============================================================================
# Pattern Tests
# =============================================================================


class TestPattern:
    """Tests for Pattern dataclass."""

    def test_basic_creation(self):
        """Test basic pattern creation."""
        pattern = Pattern(description="User prefers morning meetings")
        assert pattern.description == "User prefers morning meetings"
        assert pattern.occurrences == []
        assert pattern.frequency == 0.0
        assert pattern.predictive_power == 0.0

    def test_full_creation(self):
        """Test pattern creation with all fields."""
        pattern = Pattern(
            description="Monday standup at 9am",
            occurrences=["meeting-1", "meeting-2", "meeting-3"],
            frequency=0.9,
            predictive_power=0.85,
        )
        assert pattern.description == "Monday standup at 9am"
        assert len(pattern.occurrences) == 3
        assert pattern.frequency == 0.9
        assert pattern.predictive_power == 0.85

    def test_to_dict(self):
        """Test serialization to dictionary."""
        pattern = Pattern(
            description="Test pattern",
            occurrences=["a", "b"],
            frequency=0.5,
            predictive_power=0.6,
        )
        d = pattern.to_dict()
        assert d["description"] == "Test pattern"
        assert d["occurrences"] == ["a", "b"]
        assert d["frequency"] == 0.5
        assert d["predictive_power"] == 0.6

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {
            "description": "From dict pattern",
            "occurrences": ["x", "y", "z"],
            "frequency": 0.75,
            "predictive_power": 0.8,
        }
        pattern = Pattern.from_dict(data)
        assert pattern.description == "From dict pattern"
        assert pattern.occurrences == ["x", "y", "z"]
        assert pattern.frequency == 0.75
        assert pattern.predictive_power == 0.8

    def test_from_dict_with_defaults(self):
        """Test deserialization handles missing fields."""
        data = {}
        pattern = Pattern.from_dict(data)
        assert pattern.description == ""
        assert pattern.occurrences == []
        assert pattern.frequency == 0.0
        assert pattern.predictive_power == 0.0

    def test_roundtrip_serialization(self):
        """Test to_dict -> from_dict preserves data."""
        original = Pattern(
            description="Roundtrip test",
            occurrences=["1", "2"],
            frequency=0.33,
            predictive_power=0.44,
        )
        restored = Pattern.from_dict(original.to_dict())
        assert restored.description == original.description
        assert restored.occurrences == original.occurrences
        assert restored.frequency == original.frequency
        assert restored.predictive_power == original.predictive_power


# =============================================================================
# Insight Tests
# =============================================================================


class TestInsight:
    """Tests for Insight dataclass."""

    def test_basic_creation(self):
        """Test basic insight creation."""
        insight = Insight(description="User prefers async communication")
        assert insight.description == "User prefers async communication"
        assert insight.derived_from == []
        assert insight.confidence == 0.5
        assert insight.surprisingness == 0.0

    def test_full_creation(self):
        """Test insight creation with all fields."""
        insight = Insight(
            description="Deep work in afternoons",
            derived_from=["pattern-1", "pattern-2"],
            confidence=0.8,
            surprisingness=0.3,
        )
        assert insight.description == "Deep work in afternoons"
        assert len(insight.derived_from) == 2
        assert insight.confidence == 0.8
        assert insight.surprisingness == 0.3

    def test_to_dict(self):
        """Test serialization to dictionary."""
        insight = Insight(
            description="Test insight",
            derived_from=["p1"],
            confidence=0.7,
            surprisingness=0.4,
        )
        d = insight.to_dict()
        assert d["description"] == "Test insight"
        assert d["derived_from"] == ["p1"]
        assert d["confidence"] == 0.7
        assert d["surprisingness"] == 0.4

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {
            "description": "From dict insight",
            "derived_from": ["p1", "p2"],
            "confidence": 0.9,
            "surprisingness": 0.6,
        }
        insight = Insight.from_dict(data)
        assert insight.description == "From dict insight"
        assert insight.derived_from == ["p1", "p2"]
        assert insight.confidence == 0.9
        assert insight.surprisingness == 0.6

    def test_from_dict_with_defaults(self):
        """Test deserialization handles missing fields."""
        data = {}
        insight = Insight.from_dict(data)
        assert insight.description == ""
        assert insight.derived_from == []
        assert insight.confidence == 0.5
        assert insight.surprisingness == 0.0


# =============================================================================
# Correction Tests
# =============================================================================


class TestCorrection:
    """Tests for Correction dataclass."""

    def test_basic_creation(self):
        """Test basic correction creation."""
        correction = Correction(
            previous_understanding="Email for clients",
            new_understanding="Slack for clients",
        )
        assert correction.previous_understanding == "Email for clients"
        assert correction.new_understanding == "Slack for clients"
        assert correction.evidence == []
        assert correction.confidence == 0.5

    def test_full_creation(self):
        """Test correction creation with all fields."""
        correction = Correction(
            previous_understanding="Morning meetings",
            new_understanding="Afternoon meetings",
            evidence=["conv-1", "conv-2"],
            confidence=0.9,
        )
        assert correction.previous_understanding == "Morning meetings"
        assert correction.new_understanding == "Afternoon meetings"
        assert len(correction.evidence) == 2
        assert correction.confidence == 0.9

    def test_to_dict(self):
        """Test serialization to dictionary."""
        correction = Correction(
            previous_understanding="Old",
            new_understanding="New",
            evidence=["e1"],
            confidence=0.8,
        )
        d = correction.to_dict()
        assert d["previous_understanding"] == "Old"
        assert d["new_understanding"] == "New"
        assert d["evidence"] == ["e1"]
        assert d["confidence"] == 0.8

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {
            "previous_understanding": "Was wrong",
            "new_understanding": "Now right",
            "evidence": ["proof1", "proof2"],
            "confidence": 0.95,
        }
        correction = Correction.from_dict(data)
        assert correction.previous_understanding == "Was wrong"
        assert correction.new_understanding == "Now right"
        assert correction.evidence == ["proof1", "proof2"]
        assert correction.confidence == 0.95

    def test_from_dict_with_defaults(self):
        """Test deserialization handles missing fields."""
        data = {}
        correction = Correction.from_dict(data)
        assert correction.previous_understanding == ""
        assert correction.new_understanding == ""
        assert correction.evidence == []
        assert correction.confidence == 0.5


# =============================================================================
# ExtractedLearning Tests
# =============================================================================


class TestExtractedLearning:
    """Tests for ExtractedLearning unified model."""

    def test_basic_creation_generates_id(self):
        """Test that creation generates a UUID."""
        learning = ExtractedLearning()
        assert learning.id is not None
        assert len(learning.id) == 36  # UUID format

    def test_creation_with_pattern(self):
        """Test creation with pattern learning."""
        pattern = Pattern(description="Test pattern")
        learning = ExtractedLearning(pattern=pattern)
        assert learning.pattern is not None
        assert learning.insight is None
        assert learning.correction is None

    def test_creation_with_insight(self):
        """Test creation with insight learning."""
        insight = Insight(description="Test insight")
        learning = ExtractedLearning(insight=insight)
        assert learning.pattern is None
        assert learning.insight is not None
        assert learning.correction is None

    def test_creation_with_correction(self):
        """Test creation with correction learning."""
        correction = Correction(previous_understanding="Old", new_understanding="New")
        learning = ExtractedLearning(correction=correction)
        assert learning.pattern is None
        assert learning.insight is None
        assert learning.correction is not None

    def test_learning_type_pattern(self):
        """Test learning_type property returns 'pattern'."""
        learning = ExtractedLearning(pattern=Pattern(description="Test"))
        assert learning.learning_type == "pattern"

    def test_learning_type_insight(self):
        """Test learning_type property returns 'insight'."""
        learning = ExtractedLearning(insight=Insight(description="Test"))
        assert learning.learning_type == "insight"

    def test_learning_type_correction(self):
        """Test learning_type property returns 'correction'."""
        learning = ExtractedLearning(
            correction=Correction(previous_understanding="Old", new_understanding="New")
        )
        assert learning.learning_type == "correction"

    def test_learning_type_unknown(self):
        """Test learning_type returns 'unknown' when nothing set."""
        learning = ExtractedLearning()
        assert learning.learning_type == "unknown"

    def test_description_from_pattern(self):
        """Test description property extracts from pattern."""
        learning = ExtractedLearning(pattern=Pattern(description="Pattern description"))
        assert learning.description == "Pattern description"

    def test_description_from_insight(self):
        """Test description property extracts from insight."""
        learning = ExtractedLearning(insight=Insight(description="Insight description"))
        assert learning.description == "Insight description"

    def test_description_from_correction(self):
        """Test description property extracts from correction (new_understanding)."""
        learning = ExtractedLearning(
            correction=Correction(
                previous_understanding="Old",
                new_understanding="New understanding",
            )
        )
        assert learning.description == "New understanding"

    def test_description_empty_when_nothing_set(self):
        """Test description returns empty string when nothing set."""
        learning = ExtractedLearning()
        assert learning.description == ""

    def test_is_high_confidence_true(self):
        """Test is_high_confidence returns True at 0.75+."""
        learning = ExtractedLearning(confidence=0.75)
        assert learning.is_high_confidence is True

        learning = ExtractedLearning(confidence=0.9)
        assert learning.is_high_confidence is True

    def test_is_high_confidence_false(self):
        """Test is_high_confidence returns False below 0.75."""
        learning = ExtractedLearning(confidence=0.74)
        assert learning.is_high_confidence is False

        learning = ExtractedLearning(confidence=0.5)
        assert learning.is_high_confidence is False

    def test_to_dict_with_pattern(self):
        """Test serialization includes pattern."""
        pattern = Pattern(description="Test", frequency=0.5)
        learning = ExtractedLearning(
            source_objects=["obj1"],
            pattern=pattern,
            confidence=0.8,
            topic_tags=["scheduling"],
        )
        d = learning.to_dict()
        assert "pattern" in d
        assert d["pattern"]["description"] == "Test"
        assert d["learning_type"] == "pattern"
        assert d["confidence"] == 0.8
        assert d["topic_tags"] == ["scheduling"]

    def test_to_dict_with_insight(self):
        """Test serialization includes insight."""
        insight = Insight(description="Test", confidence=0.7)
        learning = ExtractedLearning(insight=insight)
        d = learning.to_dict()
        assert "insight" in d
        assert d["insight"]["description"] == "Test"
        assert d["learning_type"] == "insight"

    def test_to_dict_with_correction(self):
        """Test serialization includes correction."""
        correction = Correction(previous_understanding="Old", new_understanding="New")
        learning = ExtractedLearning(correction=correction)
        d = learning.to_dict()
        assert "correction" in d
        assert d["correction"]["new_understanding"] == "New"
        assert d["learning_type"] == "correction"

    def test_from_dict_with_pattern(self):
        """Test deserialization with pattern."""
        data = {
            "id": "test-id",
            "source_objects": ["obj1", "obj2"],
            "created_at": "2026-01-24T08:00:00",
            "pattern": {
                "description": "From dict pattern",
                "frequency": 0.6,
            },
            "confidence": 0.7,
            "topic_tags": ["meetings"],
        }
        learning = ExtractedLearning.from_dict(data)
        assert learning.id == "test-id"
        assert learning.source_objects == ["obj1", "obj2"]
        assert learning.pattern is not None
        assert learning.pattern.description == "From dict pattern"
        assert learning.confidence == 0.7
        assert learning.topic_tags == ["meetings"]

    def test_from_dict_with_insight(self):
        """Test deserialization with insight."""
        data = {
            "insight": {
                "description": "From dict insight",
                "confidence": 0.8,
            }
        }
        learning = ExtractedLearning.from_dict(data)
        assert learning.insight is not None
        assert learning.insight.description == "From dict insight"

    def test_from_dict_with_correction(self):
        """Test deserialization with correction."""
        data = {
            "correction": {
                "previous_understanding": "Old",
                "new_understanding": "New",
            }
        }
        learning = ExtractedLearning.from_dict(data)
        assert learning.correction is not None
        assert learning.correction.new_understanding == "New"

    def test_from_dict_datetime_parsing(self):
        """Test datetime string is parsed correctly."""
        data = {"created_at": "2026-01-24T12:30:45"}
        learning = ExtractedLearning.from_dict(data)
        assert learning.created_at.year == 2026
        assert learning.created_at.month == 1
        assert learning.created_at.day == 24

    def test_from_dict_generates_id_if_missing(self):
        """Test that from_dict generates ID if not provided."""
        data = {}
        learning = ExtractedLearning.from_dict(data)
        assert learning.id is not None
        assert len(learning.id) == 36

    def test_requires_attention_default_false(self):
        """Test requires_attention defaults to False."""
        learning = ExtractedLearning()
        assert learning.requires_attention is False

    def test_requires_attention_can_be_set(self):
        """Test requires_attention can be set to True."""
        learning = ExtractedLearning(requires_attention=True)
        assert learning.requires_attention is True


# =============================================================================
# Factory Function Tests
# =============================================================================


class TestCreatePatternLearning:
    """Tests for create_pattern_learning factory."""

    def test_basic_creation(self):
        """Test basic pattern learning creation."""
        learning = create_pattern_learning(
            description="Monday meetings",
            occurrences=["m1", "m2", "m3"],
        )
        assert learning.learning_type == "pattern"
        assert learning.pattern.description == "Monday meetings"
        assert len(learning.pattern.occurrences) == 3

    def test_confidence_defaults_to_predictive_power(self):
        """Test confidence defaults to predictive_power if not specified."""
        learning = create_pattern_learning(
            description="Test",
            occurrences=[],
            predictive_power=0.8,
        )
        assert learning.confidence == 0.8

    def test_confidence_can_override(self):
        """Test confidence can be explicitly set."""
        learning = create_pattern_learning(
            description="Test",
            occurrences=[],
            predictive_power=0.8,
            confidence=0.6,
        )
        assert learning.confidence == 0.6

    def test_expression_is_generated(self):
        """Test expression is auto-generated."""
        learning = create_pattern_learning(
            description="User prefers mornings",
            occurrences=[],
        )
        assert "noticed a pattern" in learning.expression
        assert "User prefers mornings" in learning.expression

    def test_topic_tags_are_set(self):
        """Test topic tags are preserved."""
        learning = create_pattern_learning(
            description="Test",
            occurrences=[],
            topic_tags=["scheduling", "preferences"],
        )
        assert learning.topic_tags == ["scheduling", "preferences"]


class TestCreateInsightLearning:
    """Tests for create_insight_learning factory."""

    def test_basic_creation(self):
        """Test basic insight learning creation."""
        learning = create_insight_learning(
            description="Deep work preference",
            derived_from=["pattern-1", "pattern-2"],
        )
        assert learning.learning_type == "insight"
        assert learning.insight.description == "Deep work preference"
        assert len(learning.insight.derived_from) == 2

    def test_confidence_is_set(self):
        """Test confidence is properly set."""
        learning = create_insight_learning(
            description="Test",
            derived_from=[],
            confidence=0.85,
        )
        assert learning.confidence == 0.85
        assert learning.insight.confidence == 0.85

    def test_expression_is_generated(self):
        """Test expression is auto-generated."""
        learning = create_insight_learning(
            description="afternoons are for focus",
            derived_from=[],
        )
        assert "It occurs to me" in learning.expression
        assert "afternoons are for focus" in learning.expression


class TestCreateCorrectionLearning:
    """Tests for create_correction_learning factory."""

    def test_basic_creation(self):
        """Test basic correction learning creation."""
        learning = create_correction_learning(
            previous_understanding="Email for clients",
            new_understanding="Slack for clients",
            evidence=["conv-1", "conv-2"],
        )
        assert learning.learning_type == "correction"
        assert learning.correction.previous_understanding == "Email for clients"
        assert learning.correction.new_understanding == "Slack for clients"
        assert len(learning.correction.evidence) == 2

    def test_requires_attention_is_true(self):
        """Test corrections always require attention."""
        learning = create_correction_learning(
            previous_understanding="Old",
            new_understanding="New",
            evidence=[],
        )
        assert learning.requires_attention is True

    def test_expression_is_generated(self):
        """Test expression is auto-generated."""
        learning = create_correction_learning(
            previous_understanding="Old",
            new_understanding="user prefers async",
            evidence=[],
        )
        assert "had something wrong" in learning.expression
        assert "user prefers async" in learning.expression

    def test_confidence_is_set(self):
        """Test confidence is properly set."""
        learning = create_correction_learning(
            previous_understanding="Old",
            new_understanding="New",
            evidence=[],
            confidence=0.95,
        )
        assert learning.confidence == 0.95
        assert learning.correction.confidence == 0.95
