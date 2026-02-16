"""
Unit tests for Portfolio Onboarding Manager and Handler.

Issue #490: FTUX-PORTFOLIO
Phase 2: Conversational Onboarding State Machine

Tests:
- State transitions (manager)
- Turn handling (handler)
- Project extraction
- Decline flow
- Graceful fallback
"""

import pytest

from services.onboarding.portfolio_handler import OnboardingResponse, PortfolioOnboardingHandler
from services.onboarding.portfolio_manager import (
    InvalidStateTransitionError,
    PortfolioOnboardingManager,
)
from services.shared_types import PortfolioOnboardingState


class TestPortfolioOnboardingManager:
    """Tests for PortfolioOnboardingManager state machine."""

    @pytest.fixture
    def manager(self):
        """Create a fresh manager for each test."""
        return PortfolioOnboardingManager()

    def test_create_session(self, manager):
        """Creating a session should initialize with INITIATED state."""
        session = manager.create_session("session-123", "user-456")

        assert session.session_id == "session-123"
        assert session.user_id == "user-456"
        assert session.state == PortfolioOnboardingState.INITIATED
        assert session.captured_projects == []
        assert session.id is not None

    def test_get_session(self, manager):
        """Should retrieve session by ID."""
        session = manager.create_session("session-123", "user-456")
        retrieved = manager.get_session(session.id)

        assert retrieved is not None
        assert retrieved.id == session.id

    def test_get_session_by_user(self, manager):
        """Should retrieve active session for user."""
        session = manager.create_session("session-123", "user-456")
        retrieved = manager.get_session_by_user("user-456")

        assert retrieved is not None
        assert retrieved.id == session.id

    def test_state_transition_initiated_to_gathering(self, manager):
        """INITIATED → GATHERING_PROJECTS is valid."""
        session = manager.create_session("session-123", "user-456")

        updated = manager.transition_state(session.id, PortfolioOnboardingState.GATHERING_PROJECTS)

        assert updated.state == PortfolioOnboardingState.GATHERING_PROJECTS
        assert updated.previous_state == PortfolioOnboardingState.INITIATED

    def test_state_transition_initiated_to_declined(self, manager):
        """INITIATED → DECLINED is valid (user says no thanks)."""
        session = manager.create_session("session-123", "user-456")

        updated = manager.transition_state(session.id, PortfolioOnboardingState.DECLINED)

        assert updated.state == PortfolioOnboardingState.DECLINED

    def test_state_transition_gathering_to_confirming(self, manager):
        """GATHERING_PROJECTS → CONFIRMING is valid."""
        session = manager.create_session("session-123", "user-456")
        manager.transition_state(session.id, PortfolioOnboardingState.GATHERING_PROJECTS)

        updated = manager.transition_state(session.id, PortfolioOnboardingState.CONFIRMING)

        assert updated.state == PortfolioOnboardingState.CONFIRMING

    def test_state_transition_confirming_to_complete(self, manager):
        """CONFIRMING → COMPLETE is valid."""
        session = manager.create_session("session-123", "user-456")
        manager.transition_state(session.id, PortfolioOnboardingState.GATHERING_PROJECTS)
        manager.transition_state(session.id, PortfolioOnboardingState.CONFIRMING)

        updated = manager.transition_state(session.id, PortfolioOnboardingState.COMPLETE)

        assert updated.state == PortfolioOnboardingState.COMPLETE
        assert updated.completed_at is not None

    def test_invalid_state_transition_raises_error(self, manager):
        """Invalid transitions should raise InvalidStateTransitionError."""
        session = manager.create_session("session-123", "user-456")

        # INITIATED → COMPLETE is not valid (must go through GATHERING and CONFIRMING)
        with pytest.raises(InvalidStateTransitionError):
            manager.transition_state(session.id, PortfolioOnboardingState.COMPLETE)

    def test_add_project(self, manager):
        """Should add project to session."""
        session = manager.create_session("session-123", "user-456")
        manager.transition_state(session.id, PortfolioOnboardingState.GATHERING_PROJECTS)

        project_data = {"name": "HealthTrack", "description": "Fitness app"}
        updated = manager.add_project(session.id, project_data)

        assert len(updated.captured_projects) == 1
        assert updated.captured_projects[0]["name"] == "HealthTrack"

    def test_add_multiple_projects(self, manager):
        """Should accumulate multiple projects."""
        session = manager.create_session("session-123", "user-456")
        manager.transition_state(session.id, PortfolioOnboardingState.GATHERING_PROJECTS)

        manager.add_project(session.id, {"name": "Project A"})
        manager.add_project(session.id, {"name": "Project B"})
        updated = manager.add_project(session.id, {"name": "Project C"})

        assert len(updated.captured_projects) == 3

    def test_add_turn(self, manager):
        """Should record conversation turns."""
        session = manager.create_session("session-123", "user-456")

        turn = manager.add_turn(
            session.id,
            user_message="Hello",
            assistant_response="Hi there!",
        )

        assert turn.turn_number == 1
        assert turn.user_message == "Hello"
        assert turn.assistant_response == "Hi there!"

        updated = manager.get_session(session.id)
        assert len(updated.turns) == 1


class TestPortfolioOnboardingHandler:
    """Tests for PortfolioOnboardingHandler turn handling."""

    @pytest.fixture
    def handler(self):
        """Create handler with fresh manager."""
        manager = PortfolioOnboardingManager()
        return PortfolioOnboardingHandler(manager)

    def test_start_onboarding(self, handler):
        """Starting onboarding should return initial prompt."""
        response = handler.start_onboarding("session-123", "user-456")

        assert isinstance(response, OnboardingResponse)
        assert "project portfolio" in response.message.lower()
        assert response.state == PortfolioOnboardingState.INITIATED
        assert response.is_complete is False
        assert response.metadata["onboarding_id"] is not None

    def test_decline_flow(self, handler):
        """User declining should end session gracefully."""
        start_response = handler.start_onboarding("session-123", "user-456")
        onboarding_id = start_response.metadata["onboarding_id"]

        # User declines
        response = handler.handle_turn(onboarding_id, "No thanks")

        assert response.state == PortfolioOnboardingState.DECLINED
        assert response.is_complete is True
        assert "no problem" in response.message.lower() or "whenever" in response.message.lower()

    def test_accept_and_provide_project(self, handler):
        """User accepting and providing project info."""
        start_response = handler.start_onboarding("session-123", "user-456")
        onboarding_id = start_response.metadata["onboarding_id"]

        # User accepts
        response = handler.handle_turn(onboarding_id, "Sure!")
        assert response.state == PortfolioOnboardingState.GATHERING_PROJECTS

        # User provides project info
        response = handler.handle_turn(
            onboarding_id, "I'm building a mobile app called HealthTrack"
        )
        assert response.state == PortfolioOnboardingState.GATHERING_PROJECTS
        assert "healthtrack" in response.message.lower()

    def test_complete_flow(self, handler):
        """Full flow from start to complete."""
        start_response = handler.start_onboarding("session-123", "user-456")
        onboarding_id = start_response.metadata["onboarding_id"]

        # Accept
        handler.handle_turn(onboarding_id, "Yes")

        # Provide project
        handler.handle_turn(onboarding_id, "I'm working on HealthTrack")

        # Say done
        response = handler.handle_turn(onboarding_id, "That's all")
        assert response.state == PortfolioOnboardingState.CONFIRMING

        # Confirm
        response = handler.handle_turn(onboarding_id, "Yes, save it")
        assert response.state == PortfolioOnboardingState.COMPLETE
        assert response.is_complete is True
        assert response.captured_projects is not None
        assert len(response.captured_projects) >= 1

    def test_graceful_fallback_on_malformed_input(self, handler):
        """Should handle unclear input gracefully."""
        start_response = handler.start_onboarding("session-123", "user-456")
        onboarding_id = start_response.metadata["onboarding_id"]

        # Accept
        handler.handle_turn(onboarding_id, "Sure")

        # Provide project
        handler.handle_turn(onboarding_id, "HealthTrack app")

        # Done
        handler.handle_turn(onboarding_id, "done")

        # Unclear confirmation response
        response = handler.handle_turn(onboarding_id, "hmm maybe")

        # Should re-prompt rather than crash
        assert response.state == PortfolioOnboardingState.CONFIRMING
        assert "portfolio" in response.message.lower()

    def test_yes_in_gathering_prompts_for_project_name(self, handler):
        """Should recognize 'yes, I have another project' as wanting to add more, not as project name."""
        start_response = handler.start_onboarding("session-123", "user-456")
        onboarding_id = start_response.metadata["onboarding_id"]

        # Accept onboarding
        handler.handle_turn(onboarding_id, "Sure")

        # Provide first project
        handler.handle_turn(onboarding_id, "Piper Morgan")

        # Now say we want to add another - this was previously captured as project name
        response = handler.handle_turn(
            onboarding_id, "Yes, I have another project to tell you about"
        )

        # Should stay in GATHERING and ask for the project name
        assert response.state == PortfolioOnboardingState.GATHERING_PROJECTS
        assert "name" in response.message.lower() or "project" in response.message.lower()

        # The phrase should NOT be captured as a project name
        session = handler.manager.get_session(onboarding_id)
        project_names = [p.get("name", "") for p in session.captured_projects]
        assert "Yes, I have another project to tell you about" not in project_names
        assert len(project_names) == 1  # Only Piper Morgan


class TestProjectExtraction:
    """Tests for project info extraction from natural language."""

    @pytest.fixture
    def handler(self):
        manager = PortfolioOnboardingManager()
        return PortfolioOnboardingHandler(manager)

    def test_extract_called_pattern(self, handler):
        """Should extract project name from 'called X' pattern."""
        info = handler._extract_project_info("I'm building an app called HealthTrack")

        assert info["name"] == "HealthTrack"
        assert "description" in info

    def test_extract_named_pattern(self, handler):
        """Should extract project name from 'named X' pattern."""
        info = handler._extract_project_info("Working on a project named TaskMaster")

        assert info["name"] == "TaskMaster"

    def test_extract_project_pattern(self, handler):
        """Should extract from 'X project' pattern."""
        info = handler._extract_project_info("I'm focused on the billing system project")

        assert "billing" in info["name"].lower()

    def test_extract_building_pattern(self, handler):
        """Should extract from 'building X' pattern."""
        info = handler._extract_project_info("I'm building a todo app")

        assert "todo" in info["name"].lower()

    def test_fallback_extraction(self, handler):
        """Should use message as name when no pattern matches."""
        info = handler._extract_project_info("HealthTrack")

        assert info["name"] == "HealthTrack"


class TestStateTransitionEdgeCases:
    """Edge case tests for state transitions."""

    @pytest.fixture
    def manager(self):
        return PortfolioOnboardingManager()

    def test_cannot_transition_from_complete(self, manager):
        """COMPLETE is terminal - no transitions allowed."""
        session = manager.create_session("session-123", "user-456")
        manager.transition_state(session.id, PortfolioOnboardingState.GATHERING_PROJECTS)
        manager.transition_state(session.id, PortfolioOnboardingState.CONFIRMING)
        manager.transition_state(session.id, PortfolioOnboardingState.COMPLETE)

        # Cannot transition from COMPLETE
        with pytest.raises(InvalidStateTransitionError):
            manager.transition_state(session.id, PortfolioOnboardingState.GATHERING_PROJECTS)

    def test_cannot_transition_from_declined(self, manager):
        """DECLINED is terminal - no transitions allowed."""
        session = manager.create_session("session-123", "user-456")
        manager.transition_state(session.id, PortfolioOnboardingState.DECLINED)

        # Cannot transition from DECLINED
        with pytest.raises(InvalidStateTransitionError):
            manager.transition_state(session.id, PortfolioOnboardingState.GATHERING_PROJECTS)

    def test_gathering_can_loop(self, manager):
        """GATHERING_PROJECTS → GATHERING_PROJECTS is valid (more projects)."""
        session = manager.create_session("session-123", "user-456")
        manager.transition_state(session.id, PortfolioOnboardingState.GATHERING_PROJECTS)

        # Should not raise - looping in gathering is allowed
        updated = manager.transition_state(session.id, PortfolioOnboardingState.GATHERING_PROJECTS)
        assert updated.state == PortfolioOnboardingState.GATHERING_PROJECTS

    def test_confirming_can_go_back_to_gathering(self, manager):
        """CONFIRMING → GATHERING_PROJECTS is valid (add more)."""
        session = manager.create_session("session-123", "user-456")
        manager.transition_state(session.id, PortfolioOnboardingState.GATHERING_PROJECTS)
        manager.transition_state(session.id, PortfolioOnboardingState.CONFIRMING)

        updated = manager.transition_state(session.id, PortfolioOnboardingState.GATHERING_PROJECTS)
        assert updated.state == PortfolioOnboardingState.GATHERING_PROJECTS


class TestGlueMainProj:
    """Issue #766: GLUE-MAINPROJ — Fix repeated 'main project' question.

    Acceptance criteria:
    - "Main project" question asked maximum once per session
    - Question timing is contextually appropriate
    - User can designate/change main project at any time
    - No repeated templated questions in any workflow
    - Passes Colleague Test
    """

    @pytest.fixture
    def handler(self):
        manager = PortfolioOnboardingManager()
        return PortfolioOnboardingHandler(manager)

    def _start_and_accept(self, handler):
        """Helper: start onboarding and accept the offer."""
        start = handler.start_onboarding("session-766", "user-766")
        oid = start.metadata["onboarding_id"]
        handler.handle_turn(oid, "Sure, let's do it")
        return oid

    # --- Core fix: no repeated "main" question ---

    def test_initiated_response_does_not_say_main(self, handler):
        """_handle_initiated should not frame the first project as 'main'."""
        start = handler.start_onboarding("session-766", "user-766")
        oid = start.metadata["onboarding_id"]
        response = handler.handle_turn(oid, "Sure")
        assert "main" not in response.message.lower()

    def test_gathering_response_does_not_say_main_focus(self, handler):
        """After adding a project, response should not ask 'is that your main focus?'"""
        oid = self._start_and_accept(handler)
        response = handler.handle_turn(oid, "Project Alpha")
        assert "main focus" not in response.message.lower()

    def test_gathering_no_repeated_question_text(self, handler):
        """Adding multiple projects should produce varied responses, not identical ones."""
        oid = self._start_and_accept(handler)
        r1 = handler.handle_turn(oid, "Project Alpha")
        r2 = handler.handle_turn(oid, "Project Beta")
        # Responses should not be identical (varied acknowledgments)
        assert r1.message != r2.message

    def test_main_focus_asked_once_for_multi_project(self, handler):
        """'Main focus' should be asked exactly once, at the transition to confirming."""
        oid = self._start_and_accept(handler)
        r1 = handler.handle_turn(oid, "Project Alpha")
        r2 = handler.handle_turn(oid, "Project Beta")
        # Neither gathering response should mention "main"
        assert "main" not in r1.message.lower()
        assert "main" not in r2.message.lower()

        # Transition to confirming
        r3 = handler.handle_turn(oid, "that's all")
        # NOW it should ask about main focus (once)
        assert "main focus" in r3.message.lower()
        assert r3.state == PortfolioOnboardingState.CONFIRMING

    def test_single_project_does_not_ask_main(self, handler):
        """Single project flow should not ask about main focus at all."""
        oid = self._start_and_accept(handler)
        handler.handle_turn(oid, "Project Alpha")
        response = handler.handle_turn(oid, "that's all")
        # Single project — just confirm, don't ask about main
        assert "main focus" not in response.message.lower()
        assert response.state == PortfolioOnboardingState.CONFIRMING

    # --- is_default designation ---

    def test_single_project_auto_default(self, handler):
        """Single project should automatically become is_default=True."""
        oid = self._start_and_accept(handler)
        handler.handle_turn(oid, "Project Alpha")
        handler.handle_turn(oid, "that's all")
        response = handler.handle_turn(oid, "yes")
        assert response.is_complete
        assert response.captured_projects[0].get("is_default") is True

    def test_multi_project_designate_main(self, handler):
        """User can designate a main project from multiple captured projects."""
        oid = self._start_and_accept(handler)
        handler.handle_turn(oid, "Project Alpha")
        handler.handle_turn(oid, "Project Beta")
        handler.handle_turn(oid, "done")
        # User designates Alpha as main
        response = handler.handle_turn(oid, "Alpha")
        assert response.is_complete
        # Find which project is marked as default
        defaults = [p for p in response.captured_projects if p.get("is_default")]
        assert len(defaults) == 1
        assert "Alpha" in defaults[0]["name"]

    def test_multi_project_decline_designation(self, handler):
        """User can decline to designate a main project."""
        oid = self._start_and_accept(handler)
        handler.handle_turn(oid, "Project Alpha")
        handler.handle_turn(oid, "Project Beta")
        handler.handle_turn(oid, "done")
        # User declines to pick a primary
        response = handler.handle_turn(oid, "just save them")
        assert response.is_complete
        defaults = [p for p in response.captured_projects if p.get("is_default")]
        assert len(defaults) == 0

    # --- Narrative system integration ---

    def test_uses_varied_acknowledgments(self, handler):
        """Handler should use narrative system for varied responses."""
        oid = self._start_and_accept(handler)
        r1 = handler.handle_turn(oid, "Project Alpha")
        # First project should get a warm/enthusiastic acknowledgment
        assert "Alpha" in r1.message or "alpha" in r1.message.lower()

    # --- Full flow integration ---

    def test_full_three_project_flow(self, handler):
        """Complete flow: 3 projects, designate one as main, no repeated questions."""
        oid = self._start_and_accept(handler)

        # Add three projects — none should mention "main"
        r1 = handler.handle_turn(oid, "Project Alpha")
        assert "main" not in r1.message.lower()
        r2 = handler.handle_turn(oid, "Project Beta")
        assert "main" not in r2.message.lower()
        r3 = handler.handle_turn(oid, "Project Gamma")
        assert "main" not in r3.message.lower()

        # Signal done — should ask about main focus ONCE
        r4 = handler.handle_turn(oid, "that's all")
        assert "main focus" in r4.message.lower()
        assert r4.state == PortfolioOnboardingState.CONFIRMING

        # Designate Beta as main
        r5 = handler.handle_turn(oid, "Beta")
        assert r5.is_complete
        assert r5.state == PortfolioOnboardingState.COMPLETE
        defaults = [p for p in r5.captured_projects if p.get("is_default")]
        assert len(defaults) == 1
        assert "Beta" in defaults[0]["name"]

    def test_full_single_project_flow(self, handler):
        """Complete flow: 1 project, auto-default, no main question asked."""
        oid = self._start_and_accept(handler)

        r1 = handler.handle_turn(oid, "My solo project")
        assert "main" not in r1.message.lower()

        r2 = handler.handle_turn(oid, "that's it")
        assert "main focus" not in r2.message.lower()
        assert r2.state == PortfolioOnboardingState.CONFIRMING

        r3 = handler.handle_turn(oid, "yes")
        assert r3.is_complete
        assert r3.captured_projects[0].get("is_default") is True
