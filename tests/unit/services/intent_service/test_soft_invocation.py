"""
Tests for SoftInvocationDetector + WorkflowOfferService.

Issue #767: GLUE-SOFTINVOKE — Soft workflow invocation from natural language.
Phase 1: Pattern detection + data model
Phase 2: Offer service + throttling

Tests cover:
- Pattern matching for each workflow type (10+ expressions)
- No false positives on casual conversation
- WorkflowOffer properties
- OfferWindow exchange throttling
- ProactivityGate integration
- Offer formatting
- Accept/decline detection
"""

from unittest.mock import MagicMock

import pytest

from services.intent_service.soft_invocation import (
    EXCHANGE_WINDOW_SIZE,
    MAX_OFFERS_PER_WINDOW,
    OfferWindow,
    SoftInvocationDetector,
    WorkflowOffer,
    WorkflowOfferService,
    detect_offer_response,
)
from services.trust.proactivity_gate import ProactivityGate, TrustStage


@pytest.fixture
def detector():
    return SoftInvocationDetector()


@pytest.fixture
def offer_service():
    return WorkflowOfferService()


# --- Pattern Detection Tests ---


class TestMeetingPatterns:
    """Meeting/scheduling workflow detection."""

    def test_need_to_get_together(self, detector):
        result = detector.detect("I need to get the team together Tuesday")
        assert result.has_offer
        assert result.offer.workflow_type == "meeting"

    def test_should_sync_up(self, detector):
        result = detector.detect("We should sync up about the release")
        assert result.has_offer
        assert result.offer.workflow_type == "meeting"

    def test_lets_catch_up(self, detector):
        result = detector.detect("Let's catch up on the project this week")
        assert result.has_offer
        assert result.offer.workflow_type == "meeting"

    def test_need_to_schedule_meeting(self, detector):
        result = detector.detect("I need to schedule a meeting with the design team")
        assert result.has_offer
        assert result.offer.workflow_type == "meeting"

    def test_should_discuss(self, detector):
        result = detector.detect("We should talk about the roadmap")
        assert result.has_offer
        assert result.offer.workflow_type == "meeting"

    def test_can_we_meet(self, detector):
        result = detector.detect("Can we meet to go over the proposal?")
        assert result.has_offer
        assert result.offer.workflow_type == "meeting"


class TestProjectSetupPatterns:
    """Project organization workflow detection."""

    def test_project_getting_complicated(self, detector):
        result = detector.detect("This project is getting complicated")
        assert result.has_offer
        assert result.offer.workflow_type == "project_setup"

    def test_help_me_organize(self, detector):
        result = detector.detect("Help me organize this project")
        assert result.has_offer
        assert result.offer.workflow_type == "project_setup"

    def test_things_getting_messy(self, detector):
        result = detector.detect("Things are getting messy with all these tasks")
        assert result.has_offer
        assert result.offer.workflow_type == "project_setup"

    def test_dont_know_how_to_structure(self, detector):
        result = detector.detect("I don't know how to structure this")
        assert result.has_offer
        assert result.offer.workflow_type == "project_setup"


class TestStatusCheckPatterns:
    """Status/deadline concern detection."""

    def test_worried_about_deadline(self, detector):
        result = detector.detect("I'm worried about the deadline")
        assert result.has_offer
        assert result.offer.workflow_type == "status_check"

    def test_not_sure_where_things_stand(self, detector):
        result = detector.detect("I'm not sure where things stand on the release")
        assert result.has_offer
        assert result.offer.workflow_type == "status_check"

    def test_are_we_on_track(self, detector):
        result = detector.detect("Are we on track for Friday?")
        assert result.has_offer
        assert result.offer.workflow_type == "status_check"

    def test_how_are_things_going(self, detector):
        result = detector.detect("How are things going with the migration?")
        assert result.has_offer
        assert result.offer.workflow_type == "status_check"


class TestStandupPatterns:
    """Standup/alignment detection."""

    def test_team_needs_alignment(self, detector):
        result = detector.detect("The team needs alignment on the sprint goals")
        assert result.has_offer
        assert result.offer.workflow_type == "standup"

    def test_everyone_out_of_sync(self, detector):
        result = detector.detect("Everyone seems out of sync lately")
        assert result.has_offer
        assert result.offer.workflow_type == "standup"

    def test_should_do_standup(self, detector):
        result = detector.detect("We should do a standup today")
        assert result.has_offer
        assert result.offer.workflow_type == "standup"


class TestReviewPatterns:
    """Review/feedback detection."""

    def test_need_someone_to_review(self, detector):
        result = detector.detect("Can someone review this PR?")
        assert result.has_offer
        assert result.offer.workflow_type == "review"

    def test_need_feedback(self, detector):
        result = detector.detect("I need feedback on the design doc")
        assert result.has_offer
        assert result.offer.workflow_type == "review"


class TestPriorityPatterns:
    """Priority/focus detection."""

    def test_dont_know_what_to_focus_on(self, detector):
        result = detector.detect("I don't know what to focus on today")
        assert result.has_offer
        assert result.offer.workflow_type == "priority_check"

    def test_too_many_things(self, detector):
        result = detector.detect("Too many things to do, I'm overwhelmed")
        assert result.has_offer
        assert result.offer.workflow_type == "priority_check"

    def test_what_should_i_work_on(self, detector):
        result = detector.detect("What should I work on first?")
        assert result.has_offer
        assert result.offer.workflow_type == "priority_check"


class TestReminderPatterns:
    """Reminder/tracking detection."""

    def test_keep_forgetting(self, detector):
        result = detector.detect("I keep forgetting to update the changelog")
        assert result.has_offer
        assert result.offer.workflow_type == "reminder"

    def test_dont_let_me_forget(self, detector):
        result = detector.detect("I need to remember to follow up with Sarah")
        assert result.has_offer
        assert result.offer.workflow_type == "reminder"


# --- No False Positive Tests ---


class TestNoFalsePositives:
    """Ensure casual conversation doesn't trigger offers."""

    def test_simple_greeting(self, detector):
        result = detector.detect("Good morning!")
        assert not result.has_offer

    def test_casual_chat(self, detector):
        result = detector.detect("What a nice day outside")
        assert not result.has_offer

    def test_short_message(self, detector):
        result = detector.detect("Hey")
        assert not result.has_offer

    def test_empty_message(self, detector):
        result = detector.detect("")
        assert not result.has_offer

    def test_simple_question(self, detector):
        result = detector.detect("What time is it?")
        assert not result.has_offer

    def test_explicit_command(self, detector):
        # Explicit commands should use normal intent classification, not soft invocation
        result = detector.detect("Check my calendar")
        assert not result.has_offer

    def test_thank_you(self, detector):
        result = detector.detect("Thanks for the help!")
        assert not result.has_offer


# --- WorkflowOffer Data Model Tests ---


class TestWorkflowOffer:
    def test_creation(self):
        offer = WorkflowOffer(
            workflow_type="meeting",
            offer_message="Want me to set up a meeting?",
            decline_message="No worries.",
            confidence=0.7,
            trigger_pattern=r"test",
        )
        assert offer.workflow_type == "meeting"
        assert offer.confidence == 0.7

    def test_frozen(self):
        offer = WorkflowOffer(
            workflow_type="meeting",
            offer_message="test",
            decline_message="test",
            confidence=0.7,
        )
        with pytest.raises(AttributeError):
            offer.workflow_type = "standup"  # type: ignore


# --- OfferWindow Tests ---


class TestOfferWindow:
    def test_empty_window(self):
        window = OfferWindow()
        assert window.count_in_window(5) == 0

    def test_count_within_window(self):
        window = OfferWindow()
        window.record_offer(3)
        window.record_offer(5)
        # At turn 7, window covers turns 2-7: both offers are in window
        assert window.count_in_window(7) == 2

    def test_count_outside_window(self):
        window = OfferWindow()
        window.record_offer(1)
        window.record_offer(2)
        # At turn 10, window covers turns 5-10: neither offer is in window
        assert window.count_in_window(10) == 0

    def test_mixed_window(self):
        window = OfferWindow()
        window.record_offer(1)  # Outside window at turn 8
        window.record_offer(5)  # Inside window at turn 8
        assert window.count_in_window(8) == 1


# --- Accept/Decline Detection Tests ---


class TestAcceptDeclineDetection:
    def test_accept_yes(self):
        assert detect_offer_response("Yes") == "accept"

    def test_accept_sure(self):
        assert detect_offer_response("Sure!") == "accept"

    def test_accept_please(self):
        assert detect_offer_response("Please") == "accept"

    def test_accept_go_ahead(self):
        assert detect_offer_response("Go ahead") == "accept"

    def test_accept_sounds_good(self):
        assert detect_offer_response("Sounds good") == "accept"

    def test_accept_yes_please(self):
        assert detect_offer_response("Yes please") == "accept"

    def test_accept_lets_do_it(self):
        assert detect_offer_response("Let's do it") == "accept"

    def test_decline_no(self):
        assert detect_offer_response("No") == "decline"

    def test_decline_not_now(self):
        assert detect_offer_response("Not now") == "decline"

    def test_decline_just_venting(self):
        assert detect_offer_response("Just venting") == "decline"

    def test_decline_im_good(self):
        assert detect_offer_response("I'm good") == "decline"

    def test_decline_maybe_later(self):
        assert detect_offer_response("Maybe later") == "decline"

    def test_decline_no_thanks(self):
        assert detect_offer_response("No thanks") == "decline"

    def test_neither(self):
        assert detect_offer_response("Tell me more about the project") is None

    def test_empty(self):
        assert detect_offer_response("") is None


# --- WorkflowOfferService Tests ---


class TestOfferServiceThrottling:
    """ProactivityGate + exchange window throttling."""

    def test_new_user_blocked(self, offer_service):
        """NEW trust stage blocks all offers."""
        allowed, reason = offer_service.should_offer(
            trust_stage=TrustStage.NEW,
            session_id="sess1",
            current_turn=1,
            suggestions_this_session=0,
        )
        assert not allowed
        assert "doesn't allow" in reason

    def test_building_user_allowed(self, offer_service):
        """BUILDING trust stage allows hints."""
        allowed, reason = offer_service.should_offer(
            trust_stage=TrustStage.BUILDING,
            session_id="sess1",
            current_turn=1,
            suggestions_this_session=0,
        )
        assert allowed

    def test_established_user_allowed(self, offer_service):
        """ESTABLISHED trust stage allows suggestions."""
        allowed, reason = offer_service.should_offer(
            trust_stage=TrustStage.ESTABLISHED,
            session_id="sess1",
            current_turn=1,
            suggestions_this_session=0,
        )
        assert allowed

    def test_session_limit_reached(self, offer_service):
        """Session-level limit blocks offers."""
        allowed, reason = offer_service.should_offer(
            trust_stage=TrustStage.BUILDING,
            session_id="sess1",
            current_turn=1,
            suggestions_this_session=5,  # Over BUILDING limit of 2
        )
        assert not allowed
        assert "limit" in reason

    def test_exchange_window_saturated(self, offer_service):
        """Exchange window blocks after MAX_OFFERS_PER_WINDOW."""
        # Record 2 offers in recent turns
        offer_service.record_offer("sess1", 3)
        offer_service.record_offer("sess1", 4)

        allowed, reason = offer_service.should_offer(
            trust_stage=TrustStage.ESTABLISHED,
            session_id="sess1",
            current_turn=5,
            suggestions_this_session=2,
        )
        assert not allowed
        assert "window saturated" in reason

    def test_exchange_window_clears(self, offer_service):
        """Old offers fall out of window."""
        offer_service.record_offer("sess1", 1)
        offer_service.record_offer("sess1", 2)

        # At turn 10, both offers are outside the 5-turn window
        allowed, reason = offer_service.should_offer(
            trust_stage=TrustStage.ESTABLISHED,
            session_id="sess1",
            current_turn=10,
            suggestions_this_session=2,
        )
        assert allowed


class TestOfferServiceFormatting:
    """Offer message formatting."""

    def test_format_offer_appends(self, offer_service):
        offer = WorkflowOffer(
            workflow_type="meeting",
            offer_message="Want me to set up a meeting?",
            decline_message="No worries.",
            confidence=0.7,
        )
        result = offer_service.format_offer(offer, "That sounds like a busy day.")
        assert "busy day" in result
        assert "set up a meeting" in result

    def test_format_offer_strips_trailing_whitespace(self, offer_service):
        offer = WorkflowOffer(
            workflow_type="meeting",
            offer_message="Want me to help?",
            decline_message="No worries.",
            confidence=0.7,
        )
        result = offer_service.format_offer(offer, "Response here.  \n")
        assert result.startswith("Response here.")

    def test_format_acceptance_known_type(self, offer_service):
        msg = offer_service.format_acceptance("meeting")
        assert "set that up" in msg

    def test_format_acceptance_unknown_type(self, offer_service):
        msg = offer_service.format_acceptance("unknown_workflow")
        assert "help" in msg

    def test_format_decline(self, offer_service):
        offer = WorkflowOffer(
            workflow_type="meeting",
            offer_message="test",
            decline_message="No worries, just let me know.",
            confidence=0.7,
        )
        msg = offer_service.format_decline(offer)
        assert msg == "No worries, just let me know."


# --- SoftInvocationResult Tests ---


class TestSoftInvocationResult:
    def test_no_offer_result(self, detector):
        result = detector.detect("Good morning!")
        assert not result.has_offer
        assert result.offer is None
        assert result.reason

    def test_offer_result(self, detector):
        result = detector.detect("I need to get the team together")
        assert result.has_offer
        assert result.offer is not None
        assert result.offer.workflow_type == "meeting"
        assert result.offer.offer_message
        assert result.offer.decline_message
        assert result.offer.confidence > 0
