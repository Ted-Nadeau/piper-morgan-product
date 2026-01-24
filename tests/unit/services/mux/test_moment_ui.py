"""
Tests for Moment UI rendering.

Part of #418 MUX-INTERACT-MOMENT-UI.

Tests cover:
- MomentType enum (10 types from ADR-046)
- MomentLifecycle state machine
- RenderedMoment structure and transitions
- All 10 type-specific renderers
- Theatrical framing (not transactional notifications)
- Urgency levels and visual weight
- Situation grouping
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

import pytest

from services.mux.moment_ui import (
    MOMENT_RENDERERS,
    AssertionMomentRenderer,
    CapabilityMomentRenderer,
    EpicMomentRenderer,
    EventMomentRenderer,
    FunctionMomentRenderer,
    IssueMomentRenderer,
    MomentAction,
    MomentLifecycle,
    MomentType,
    PermissionMomentRenderer,
    QuestionMomentRenderer,
    RenderedMoment,
    RenderedSituation,
    RuleMomentRenderer,
    SchemaMomentRenderer,
    Urgency,
    VisualWeight,
    render_moment,
)

# =============================================================================
# Test Fixtures
# =============================================================================


@dataclass
class MockMoment:
    """A simple Moment for testing renderers."""

    id: str
    timestamp: datetime
    _captures: Dict[str, Any]

    def captures(self) -> Dict[str, Any]:
        return self._captures


@pytest.fixture
def basic_moment():
    """A basic moment with minimal data."""
    return MockMoment(
        id="moment-001",
        timestamp=datetime.now(),
        _captures={"description": "Test moment"},
    )


@pytest.fixture
def issue_moment():
    """An issue moment with blocking flag."""
    return MockMoment(
        id="issue-001",
        timestamp=datetime.now(),
        _captures={
            "description": "Build is failing",
            "impact": "Can't deploy to production",
            "blocking": True,
        },
    )


@pytest.fixture
def question_moment():
    """A question moment."""
    return MockMoment(
        id="question-001",
        timestamp=datetime.now(),
        _captures={
            "question": "Which approach would you prefer?",
        },
    )


# =============================================================================
# MomentType Enum Tests
# =============================================================================


class TestMomentType:
    """Tests for MomentType enum."""

    def test_has_all_ten_types(self):
        """ADR-046 defines exactly 10 Moment types."""
        assert len(MomentType) == 10

    def test_type_values(self):
        """Each type has expected string value."""
        assert MomentType.CAPABILITY.value == "capability"
        assert MomentType.EPIC.value == "epic"
        assert MomentType.RULE.value == "rule"
        assert MomentType.ASSERTION.value == "assertion"
        assert MomentType.QUESTION.value == "question"
        assert MomentType.ISSUE.value == "issue"
        assert MomentType.PERMISSION.value == "permission"
        assert MomentType.SCHEMA.value == "schema"
        assert MomentType.EVENT.value == "event"
        assert MomentType.FUNCTION.value == "function"

    def test_is_string_enum(self):
        """MomentType inherits from str for easy serialization."""
        assert isinstance(MomentType.CAPABILITY, str)
        assert MomentType.QUESTION == "question"


# =============================================================================
# MomentLifecycle Tests
# =============================================================================


class TestMomentLifecycle:
    """Tests for MomentLifecycle state machine."""

    def test_has_five_states(self):
        """Lifecycle has all expected states."""
        assert len(MomentLifecycle) == 5
        assert MomentLifecycle.EMERGING.value == "emerging"
        assert MomentLifecycle.PRESENT.value == "present"
        assert MomentLifecycle.RESOLVED.value == "resolved"
        assert MomentLifecycle.DEFERRED.value == "deferred"
        assert MomentLifecycle.DISMISSED.value == "dismissed"


# =============================================================================
# Urgency Tests
# =============================================================================


class TestUrgency:
    """Tests for Urgency levels."""

    def test_urgency_levels(self):
        """Three urgency levels as specified."""
        assert len(Urgency) == 3
        assert Urgency.AMBIENT.value == "ambient"
        assert Urgency.NOTABLE.value == "notable"
        assert Urgency.URGENT.value == "urgent"


# =============================================================================
# VisualWeight Tests
# =============================================================================


class TestVisualWeight:
    """Tests for VisualWeight levels."""

    def test_visual_weight_levels(self):
        """Three visual weight levels."""
        assert len(VisualWeight) == 3
        assert VisualWeight.SUBTLE.value == "subtle"
        assert VisualWeight.NORMAL.value == "normal"
        assert VisualWeight.PROMINENT.value == "prominent"


# =============================================================================
# MomentAction Tests
# =============================================================================


class TestMomentAction:
    """Tests for MomentAction dataclass."""

    def test_basic_action(self):
        """Can create a basic action."""
        action = MomentAction(
            label="Click me",
            action_type="engage",
        )
        assert action.label == "Click me"
        assert action.action_type == "engage"
        assert action.payload == {}
        assert action.is_destructive is False
        assert action.requires_confirmation is False

    def test_destructive_action(self):
        """Destructive actions can be flagged."""
        action = MomentAction(
            label="Delete",
            action_type="delete",
            is_destructive=True,
            requires_confirmation=True,
        )
        assert action.is_destructive is True
        assert action.requires_confirmation is True

    def test_action_with_payload(self):
        """Actions can carry payload data."""
        action = MomentAction(
            label="Navigate",
            action_type="navigate",
            payload={"url": "/dashboard", "tab": "insights"},
        )
        assert action.payload["url"] == "/dashboard"
        assert action.payload["tab"] == "insights"


# =============================================================================
# RenderedMoment Tests
# =============================================================================


class TestRenderedMoment:
    """Tests for RenderedMoment dataclass."""

    def test_basic_rendered_moment(self):
        """Can create a basic rendered moment."""
        rendered = RenderedMoment(
            moment_id="test-001",
            moment_type=MomentType.QUESTION,
            headline="I need your input",
            context="Which approach?",
            significance="This affects our next steps",
        )
        assert rendered.moment_id == "test-001"
        assert rendered.moment_type == MomentType.QUESTION
        assert rendered.lifecycle == MomentLifecycle.EMERGING
        assert rendered.headline == "I need your input"

    def test_lifecycle_transitions(self):
        """Lifecycle transitions work correctly."""
        rendered = RenderedMoment(
            moment_id="test-001",
            moment_type=MomentType.QUESTION,
        )

        # EMERGING → PRESENT
        assert rendered.lifecycle == MomentLifecycle.EMERGING
        rendered.transition_to(MomentLifecycle.PRESENT)
        assert rendered.lifecycle == MomentLifecycle.PRESENT
        assert rendered.is_actionable is True

        # PRESENT → RESOLVED
        rendered.transition_to(MomentLifecycle.RESOLVED)
        assert rendered.lifecycle == MomentLifecycle.RESOLVED
        assert rendered.is_complete is True
        assert rendered.resolved_at is not None

    def test_invalid_transition_raises(self):
        """Invalid transitions raise ValueError."""
        rendered = RenderedMoment(
            moment_id="test-001",
            moment_type=MomentType.QUESTION,
        )

        # Can't go EMERGING → RESOLVED directly
        with pytest.raises(ValueError, match="Invalid transition"):
            rendered.transition_to(MomentLifecycle.RESOLVED)

    def test_deferred_transition(self):
        """PRESENT → DEFERRED transition works."""
        rendered = RenderedMoment(
            moment_id="test-001",
            moment_type=MomentType.QUESTION,
        )
        rendered.transition_to(MomentLifecycle.PRESENT)
        rendered.transition_to(MomentLifecycle.DEFERRED)

        assert rendered.lifecycle == MomentLifecycle.DEFERRED
        # Deferred is not "complete" - it will come back
        assert rendered.is_complete is False

    def test_dismissed_transition(self):
        """PRESENT → DISMISSED transition works."""
        rendered = RenderedMoment(
            moment_id="test-001",
            moment_type=MomentType.EVENT,
        )
        rendered.transition_to(MomentLifecycle.PRESENT)
        rendered.transition_to(MomentLifecycle.DISMISSED)

        assert rendered.lifecycle == MomentLifecycle.DISMISSED
        assert rendered.is_complete is True
        assert rendered.resolved_at is not None

    def test_is_actionable(self):
        """is_actionable only true in PRESENT state."""
        rendered = RenderedMoment(
            moment_id="test-001",
            moment_type=MomentType.QUESTION,
        )
        assert rendered.is_actionable is False  # EMERGING

        rendered.transition_to(MomentLifecycle.PRESENT)
        assert rendered.is_actionable is True  # PRESENT

        rendered.transition_to(MomentLifecycle.RESOLVED)
        assert rendered.is_actionable is False  # RESOLVED


# =============================================================================
# Renderer Registry Tests
# =============================================================================


class TestRendererRegistry:
    """Tests for the MOMENT_RENDERERS registry."""

    def test_all_types_have_renderers(self):
        """Every MomentType has a registered renderer."""
        for moment_type in MomentType:
            assert moment_type in MOMENT_RENDERERS, f"Missing renderer for {moment_type}"

    def test_registry_has_exactly_ten_renderers(self):
        """Registry has exactly 10 renderers (one per type)."""
        assert len(MOMENT_RENDERERS) == 10


# =============================================================================
# render_moment Function Tests
# =============================================================================


class TestRenderMoment:
    """Tests for the render_moment function."""

    def test_render_moment_uses_correct_renderer(self, basic_moment):
        """render_moment dispatches to type-specific renderer."""
        rendered = render_moment(basic_moment, MomentType.QUESTION)

        assert rendered.moment_id == "moment-001"
        assert rendered.moment_type == MomentType.QUESTION
        assert rendered.headline == "I need your input"

    def test_render_moment_invalid_type_raises(self, basic_moment):
        """render_moment raises for unknown type."""
        # Remove a renderer temporarily
        original = MOMENT_RENDERERS.pop(MomentType.CAPABILITY)
        try:
            with pytest.raises(ValueError, match="No renderer"):
                render_moment(basic_moment, MomentType.CAPABILITY)
        finally:
            MOMENT_RENDERERS[MomentType.CAPABILITY] = original


# =============================================================================
# Individual Renderer Tests
# =============================================================================


class TestCapabilityRenderer:
    """Tests for CapabilityMomentRenderer."""

    def test_capability_is_ambient(self, basic_moment):
        """Capabilities are ambient (subtle, not interrupting)."""
        renderer = CapabilityMomentRenderer()
        rendered = renderer.render(basic_moment)

        assert rendered.moment_type == MomentType.CAPABILITY
        assert rendered.urgency == Urgency.AMBIENT
        assert rendered.visual_weight == VisualWeight.SUBTLE

    def test_capability_has_no_resolution(self, basic_moment):
        """Capabilities don't 'complete' - they're informational."""
        renderer = CapabilityMomentRenderer()
        rendered = renderer.render(basic_moment)

        assert rendered.has_resolution is False

    def test_capability_headline_is_helpful(self, basic_moment):
        """Headline uses theatrical framing, not technical."""
        renderer = CapabilityMomentRenderer()
        rendered = renderer.render(basic_moment)

        assert "help" in rendered.headline.lower()
        assert "CAPABILITY" not in rendered.headline  # No technical identifiers


class TestEpicRenderer:
    """Tests for EpicMomentRenderer."""

    def test_epic_is_prominent(self, basic_moment):
        """Epics get prominent visual treatment."""
        renderer = EpicMomentRenderer()
        rendered = renderer.render(basic_moment)

        assert rendered.moment_type == MomentType.EPIC
        assert rendered.visual_weight == VisualWeight.PROMINENT

    def test_epic_has_multiple_actions(self, basic_moment):
        """Epics offer multiple ways to engage."""
        renderer = EpicMomentRenderer()
        rendered = renderer.render(basic_moment)

        assert rendered.primary_action is not None
        assert len(rendered.secondary_actions) >= 2


class TestRuleRenderer:
    """Tests for RuleMomentRenderer."""

    def test_rule_is_ambient(self, basic_moment):
        """Rules are ambient (guidelines, not interruptions)."""
        renderer = RuleMomentRenderer()
        rendered = renderer.render(basic_moment)

        assert rendered.urgency == Urgency.AMBIENT
        assert rendered.can_defer is False  # Rules are informational


class TestAssertionRenderer:
    """Tests for AssertionMomentRenderer."""

    def test_assertion_allows_correction(self, basic_moment):
        """Assertions can be confirmed or corrected by user."""
        renderer = AssertionMomentRenderer()
        rendered = renderer.render(basic_moment)

        assert rendered.primary_action.action_type == "confirm"

        # Has "correct" action in secondaries
        correct_actions = [a for a in rendered.secondary_actions if a.action_type == "correct"]
        assert len(correct_actions) == 1

    def test_assertion_headline_is_tentative(self, basic_moment):
        """Assertion headline expresses uncertainty appropriately."""
        renderer = AssertionMomentRenderer()
        rendered = renderer.render(basic_moment)

        # Not assertive language
        headline_lower = rendered.headline.lower()
        assert "think" in headline_lower or "noticed" in headline_lower


class TestQuestionRenderer:
    """Tests for QuestionMomentRenderer."""

    def test_question_primary_is_reply(self, question_moment):
        """Questions have reply as primary action."""
        renderer = QuestionMomentRenderer()
        rendered = renderer.render(question_moment)

        assert rendered.primary_action.action_type == "reply"

    def test_question_can_be_deferred(self, question_moment):
        """Questions can be saved for later."""
        renderer = QuestionMomentRenderer()
        rendered = renderer.render(question_moment)

        assert rendered.can_defer is True

        # Has defer action
        defer_actions = [a for a in rendered.secondary_actions if a.action_type == "defer"]
        assert len(defer_actions) == 1


class TestIssueRenderer:
    """Tests for IssueMomentRenderer."""

    def test_blocking_issue_is_urgent(self, issue_moment):
        """Blocking issues get urgent treatment."""
        renderer = IssueMomentRenderer()
        rendered = renderer.render(issue_moment)

        assert rendered.urgency == Urgency.URGENT
        assert rendered.visual_weight == VisualWeight.PROMINENT

    def test_blocking_issue_cannot_defer(self, issue_moment):
        """Blocking issues cannot be deferred."""
        renderer = IssueMomentRenderer()
        rendered = renderer.render(issue_moment)

        assert rendered.can_defer is False

    def test_non_blocking_issue_is_notable(self):
        """Non-blocking issues are notable, not urgent."""
        moment = MockMoment(
            id="issue-002",
            timestamp=datetime.now(),
            _captures={
                "description": "Minor UI glitch",
                "blocking": False,
            },
        )
        renderer = IssueMomentRenderer()
        rendered = renderer.render(moment)

        assert rendered.urgency == Urgency.NOTABLE
        assert rendered.can_defer is True


class TestPermissionRenderer:
    """Tests for PermissionMomentRenderer."""

    def test_permission_has_allow_deny(self, basic_moment):
        """Permissions have clear allow/deny actions."""
        renderer = PermissionMomentRenderer()
        rendered = renderer.render(basic_moment)

        assert rendered.primary_action.action_type == "authorize"

        deny_actions = [a for a in rendered.secondary_actions if a.action_type == "deny"]
        assert len(deny_actions) == 1


class TestSchemaRenderer:
    """Tests for SchemaMomentRenderer."""

    def test_schema_is_ambient(self, basic_moment):
        """Schemas are ambient (informational structures)."""
        renderer = SchemaMomentRenderer()
        rendered = renderer.render(basic_moment)

        assert rendered.urgency == Urgency.AMBIENT
        assert rendered.has_resolution is False


class TestEventRenderer:
    """Tests for EventMomentRenderer."""

    def test_event_requiring_action_is_notable(self):
        """Events requiring action are notable."""
        moment = MockMoment(
            id="event-001",
            timestamp=datetime.now(),
            _captures={
                "description": "PR review requested",
                "requires_action": True,
            },
        )
        renderer = EventMomentRenderer()
        rendered = renderer.render(moment)

        assert rendered.urgency == Urgency.NOTABLE
        assert rendered.has_resolution is True

    def test_informational_event_is_ambient(self):
        """Informational events are ambient."""
        moment = MockMoment(
            id="event-002",
            timestamp=datetime.now(),
            _captures={
                "description": "Build completed",
                "requires_action": False,
            },
        )
        renderer = EventMomentRenderer()
        rendered = renderer.render(moment)

        assert rendered.urgency == Urgency.AMBIENT
        assert rendered.has_resolution is False


class TestFunctionRenderer:
    """Tests for FunctionMomentRenderer."""

    def test_function_has_execute_action(self, basic_moment):
        """Functions have execute as primary action."""
        renderer = FunctionMomentRenderer()
        rendered = renderer.render(basic_moment)

        assert rendered.primary_action.action_type == "execute"

    def test_function_has_preview_option(self, basic_moment):
        """Functions can be previewed before execution."""
        renderer = FunctionMomentRenderer()
        rendered = renderer.render(basic_moment)

        preview_actions = [a for a in rendered.secondary_actions if a.action_type == "expand"]
        assert len(preview_actions) == 1


# =============================================================================
# Theatrical Framing Tests (Anti-Pattern Verification)
# =============================================================================


class TestTheatricalFraming:
    """
    Verify theatrical framing vs transactional notifications.

    Anti-patterns to avoid:
    1. Notification spam: Not every event is a Moment
    2. Flat presentation: All Moments look the same
    3. No agency: Moments that inform but don't offer action
    4. No resolution: Moments that never complete
    5. Context-free: Presenting without situational framing
    """

    def test_no_technical_identifiers_in_headlines(self, basic_moment):
        """Headlines don't expose technical type names in code-like format."""
        for moment_type in MomentType:
            rendered = render_moment(basic_moment, moment_type)
            headline = rendered.headline

            # No code-style identifiers like "Moment.type.X" or "TYPE:"
            assert f"Moment.type.{moment_type.value}" not in headline
            assert f"{moment_type.value.upper()}:" not in headline
            # Headlines should read naturally, not technically
            assert headline[0].isupper()  # Starts with capital (sentence)

    def test_all_moments_have_significance(self, basic_moment):
        """Every rendered Moment explains why it matters."""
        for moment_type in MomentType:
            rendered = render_moment(basic_moment, moment_type)

            # significance should be non-empty or in the context
            has_significance = rendered.significance != "" or rendered.context != ""
            assert has_significance, f"{moment_type} lacks significance"

    def test_actionable_moments_have_actions(self, basic_moment):
        """Moments that resolve must have actions."""
        for moment_type in MomentType:
            rendered = render_moment(basic_moment, moment_type)

            if rendered.has_resolution:
                # Must have at least a primary or secondary action
                has_action = (
                    rendered.primary_action is not None or len(rendered.secondary_actions) > 0
                )
                assert has_action, f"{moment_type} resolves but has no actions"


# =============================================================================
# RenderedSituation Tests
# =============================================================================


class TestRenderedSituation:
    """Tests for RenderedSituation (grouped Moments)."""

    def test_basic_situation(self):
        """Can create a basic situation with moments."""
        situation = RenderedSituation(
            situation_id="morning-001",
            title="Morning orientation",
            description="Starting your day",
            moments=[
                RenderedMoment(
                    moment_id="m1",
                    moment_type=MomentType.EVENT,
                    urgency=Urgency.AMBIENT,
                ),
                RenderedMoment(
                    moment_id="m2",
                    moment_type=MomentType.QUESTION,
                    urgency=Urgency.NOTABLE,
                ),
            ],
        )

        assert situation.title == "Morning orientation"
        assert len(situation.moments) == 2

    def test_urgency_is_highest_of_children(self):
        """Situation urgency is max of moment urgencies."""
        situation = RenderedSituation(
            situation_id="test-001",
            title="Test",
            moments=[
                RenderedMoment(
                    moment_id="m1",
                    moment_type=MomentType.EVENT,
                    urgency=Urgency.AMBIENT,
                ),
                RenderedMoment(
                    moment_id="m2",
                    moment_type=MomentType.ISSUE,
                    urgency=Urgency.URGENT,
                ),
                RenderedMoment(
                    moment_id="m3",
                    moment_type=MomentType.QUESTION,
                    urgency=Urgency.NOTABLE,
                ),
            ],
        )

        assert situation.urgency == Urgency.URGENT

    def test_empty_situation_is_ambient(self):
        """Empty situation has ambient urgency."""
        situation = RenderedSituation(
            situation_id="empty-001",
            title="Empty",
        )

        assert situation.urgency == Urgency.AMBIENT

    def test_pending_count(self):
        """pending_count tracks actionable moments."""
        m1 = RenderedMoment(
            moment_id="m1",
            moment_type=MomentType.QUESTION,
            lifecycle=MomentLifecycle.PRESENT,  # Actionable
        )
        m2 = RenderedMoment(
            moment_id="m2",
            moment_type=MomentType.EVENT,
            lifecycle=MomentLifecycle.EMERGING,  # Not yet actionable
        )
        m3 = RenderedMoment(
            moment_id="m3",
            moment_type=MomentType.ISSUE,
            lifecycle=MomentLifecycle.PRESENT,  # Actionable
        )

        situation = RenderedSituation(
            situation_id="test-001",
            title="Test",
            moments=[m1, m2, m3],
        )

        assert situation.pending_count == 2

    def test_has_urgent(self):
        """has_urgent detects urgent moments."""
        situation_no_urgent = RenderedSituation(
            situation_id="test-001",
            title="Calm",
            moments=[
                RenderedMoment(
                    moment_id="m1",
                    moment_type=MomentType.EVENT,
                    urgency=Urgency.AMBIENT,
                ),
            ],
        )
        assert situation_no_urgent.has_urgent is False

        situation_with_urgent = RenderedSituation(
            situation_id="test-002",
            title="Alert",
            moments=[
                RenderedMoment(
                    moment_id="m1",
                    moment_type=MomentType.ISSUE,
                    urgency=Urgency.URGENT,
                ),
            ],
        )
        assert situation_with_urgent.has_urgent is True

    def test_collapse_state(self):
        """Situations can be collapsed."""
        situation = RenderedSituation(
            situation_id="test-001",
            title="Test",
        )

        assert situation.is_collapsed is False
        situation.is_collapsed = True
        assert situation.is_collapsed is True
