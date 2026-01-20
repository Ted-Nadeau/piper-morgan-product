"""
Tests for Situation Context Manager.

Phase 2 TDD: Situation is a frame (not a substrate) that holds sequences of Moments.
Used as async context manager to capture what happens during a bounded period.
"""

from datetime import datetime

import pytest


class TestSituationBasics:
    """Tests for basic Situation functionality."""

    def test_situation_has_description(self):
        """Situation carries a description of what's happening."""
        from services.mux.situation import Situation

        situation = Situation(
            description="Morning standup meeting", dramatic_tension="Deadline approaching"
        )

        assert situation.description == "Morning standup meeting"

    def test_situation_has_dramatic_tension(self):
        """Situation carries dramatic tension description."""
        from services.mux.situation import Situation

        situation = Situation(
            description="Sprint planning", dramatic_tension="Team capacity vs backlog size"
        )

        assert situation.dramatic_tension == "Team capacity vs backlog size"

    def test_situation_has_goals(self):
        """Situation can have goals set."""
        from services.mux.situation import Situation

        situation = Situation(
            description="Daily standup",
            dramatic_tension="Coordination needs",
            goals=["Share blockers", "Align on priorities"],
        )

        assert "Share blockers" in situation.goals
        assert len(situation.goals) == 2

    def test_situation_starts_with_no_moments(self):
        """New Situation has empty moments list."""
        from services.mux.situation import Situation

        situation = Situation(description="Test", dramatic_tension="None")

        assert situation.moments == []


class TestSituationAsContextManager:
    """Tests for Situation as async context manager."""

    @pytest.mark.asyncio
    async def test_situation_is_async_context_manager(self):
        """Situation can be used with async with."""
        from services.mux.situation import Situation

        situation = Situation(description="Test meeting", dramatic_tension="Test tension")

        async with situation as ctx:
            assert ctx is situation
            # Should be inside the situation now

    @pytest.mark.asyncio
    async def test_situation_sets_started_at_on_enter(self):
        """Entering situation records start time."""
        from services.mux.situation import Situation

        situation = Situation(description="Test", dramatic_tension="Test")

        before = datetime.now()
        async with situation:
            after_enter = datetime.now()
            assert situation.started_at is not None
            assert before <= situation.started_at <= after_enter

    @pytest.mark.asyncio
    async def test_situation_sets_ended_at_on_exit(self):
        """Exiting situation records end time."""
        from services.mux.situation import Situation

        situation = Situation(description="Test", dramatic_tension="Test")

        async with situation:
            pass

        assert situation.ended_at is not None
        assert situation.ended_at >= situation.started_at


class TestSituationMomentCapture:
    """Tests for capturing moments during a situation."""

    @pytest.mark.asyncio
    async def test_add_moment_captures_moment(self, mock_moment):
        """Moments added during situation are captured."""
        from services.mux.situation import Situation

        situation = Situation(description="Test", dramatic_tension="Test")

        async with situation:
            situation.add_moment(mock_moment)

        assert len(situation.moments) == 1
        assert situation.moments[0] is mock_moment

    @pytest.mark.asyncio
    async def test_add_multiple_moments(self, mock_moment):
        """Multiple moments can be captured."""
        from services.mux.situation import Situation
        from tests.unit.services.mux.conftest import MockMoment

        situation = Situation(description="Test", dramatic_tension="Test")

        moment2 = MockMoment(id="moment-002")

        async with situation:
            situation.add_moment(mock_moment)
            situation.add_moment(moment2)

        assert len(situation.moments) == 2


class TestSituationLearning:
    """Tests for extracting learning from a situation."""

    @pytest.mark.asyncio
    async def test_extract_learning_returns_learning_object(self):
        """Extracting learning returns SituationLearning."""
        from services.mux.situation import Situation, SituationLearning

        situation = Situation(
            description="Sprint planning",
            dramatic_tension="Too much work",
            goals=["Plan next sprint"],
            outcomes=["Committed to 5 stories"],
        )

        async with situation:
            pass

        learning = situation.extract_learning()

        assert isinstance(learning, SituationLearning)

    @pytest.mark.asyncio
    async def test_extract_learning_captures_goals(self):
        """Learning captures the original goals."""
        from services.mux.situation import Situation

        situation = Situation(
            description="Test", dramatic_tension="Test", goals=["Goal A", "Goal B"]
        )

        async with situation:
            pass

        learning = situation.extract_learning()

        assert learning.goals == ["Goal A", "Goal B"]

    @pytest.mark.asyncio
    async def test_extract_learning_captures_outcomes(self):
        """Learning captures the outcomes."""
        from services.mux.situation import Situation

        situation = Situation(description="Test", dramatic_tension="Test", outcomes=["Outcome X"])

        async with situation:
            pass

        learning = situation.extract_learning()

        assert learning.outcomes == ["Outcome X"]

    @pytest.mark.asyncio
    async def test_extract_learning_computes_delta(self):
        """Learning computes delta between goals and outcomes."""
        from services.mux.situation import Situation

        situation = Situation(
            description="Sprint planning",
            dramatic_tension="Capacity constraints",
            goals=["Plan 10 stories", "Identify risks"],
            outcomes=["Planned 5 stories"],
        )

        async with situation:
            pass

        learning = situation.extract_learning()

        # Delta should reflect what was achieved vs intended
        assert learning.delta is not None
        assert len(learning.delta) > 0

    @pytest.mark.asyncio
    async def test_add_outcome_during_situation(self):
        """Outcomes can be added during the situation."""
        from services.mux.situation import Situation

        situation = Situation(description="Meeting", dramatic_tension="Decision needed")

        async with situation:
            situation.add_outcome("Decision made: proceed with option A")

        assert "Decision made: proceed with option A" in situation.outcomes
