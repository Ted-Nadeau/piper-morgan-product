"""
Tests for Issue #889: Standup suspend/resume bug fixes.

Category A fixes:
1. SUSPENDED state excluded from active conversation lookups
2. Resume acceptance wiring (SUSPENDED → INITIATED)
3. Resume decline wiring (SUSPENDED → ABANDONED)
4. Dead code cleanup (_check_active_standup deprecation)

These tests verify the standup suspend/resume path works correctly
for users, even without the Category B enhancements (3-part structural
collection, #900).
"""

from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.shared_types import StandupConversationState
from services.standup.conversation_manager import StandupConversationManager


class TestSuspendedExclusionInLookups:
    """Issue #889: SUSPENDED conversations should not be returned by default lookups."""

    def setup_method(self):
        self.manager = StandupConversationManager()

    def test_get_conversation_by_session_excludes_suspended(self):
        """SUSPENDED conversations are not 'active' and should not be found by default."""
        conv = self.manager.create_conversation("sess-1", "user-1")
        self.manager.transition_state(conv.id, StandupConversationState.GATHERING_PREFERENCES)
        self.manager.transition_state(conv.id, StandupConversationState.SUSPENDED)

        result = self.manager.get_conversation_by_session("sess-1")
        assert result is None

    def test_get_conversation_by_session_includes_suspended_when_requested(self):
        """With include_suspended=True, SUSPENDED conversations are returned."""
        conv = self.manager.create_conversation("sess-1", "user-1")
        self.manager.transition_state(conv.id, StandupConversationState.GATHERING_PREFERENCES)
        self.manager.transition_state(conv.id, StandupConversationState.SUSPENDED)

        result = self.manager.get_conversation_by_session("sess-1", include_suspended=True)
        assert result is not None
        assert result.id == conv.id
        assert result.state == StandupConversationState.SUSPENDED

    def test_get_conversation_by_user_excludes_suspended(self):
        """SUSPENDED conversations are not returned by user lookup by default."""
        conv = self.manager.create_conversation("sess-1", "user-1")
        self.manager.transition_state(conv.id, StandupConversationState.GENERATING)
        self.manager.transition_state(conv.id, StandupConversationState.SUSPENDED)

        result = self.manager.get_conversation_by_user("user-1")
        assert result is None

    def test_get_conversation_by_user_includes_suspended_when_requested(self):
        """With include_suspended=True, SUSPENDED conversations are returned."""
        conv = self.manager.create_conversation("sess-1", "user-1")
        self.manager.transition_state(conv.id, StandupConversationState.GENERATING)
        self.manager.transition_state(conv.id, StandupConversationState.SUSPENDED)

        result = self.manager.get_conversation_by_user("user-1", include_suspended=True)
        assert result is not None
        assert result.state == StandupConversationState.SUSPENDED

    def test_active_conversation_still_found(self):
        """Active (non-suspended, non-terminal) conversations are still found."""
        conv = self.manager.create_conversation("sess-1", "user-1")
        self.manager.transition_state(conv.id, StandupConversationState.GENERATING)

        result = self.manager.get_conversation_by_session("sess-1")
        assert result is not None
        assert result.state == StandupConversationState.GENERATING

    def test_complete_conversation_still_excluded(self):
        """COMPLETE conversations are still excluded (regression check)."""
        conv = self.manager.create_conversation("sess-1", "user-1")
        self.manager.transition_state(conv.id, StandupConversationState.GENERATING)
        self.manager.transition_state(conv.id, StandupConversationState.FINALIZING)
        self.manager.transition_state(conv.id, StandupConversationState.COMPLETE)

        result = self.manager.get_conversation_by_session("sess-1")
        assert result is None

    def test_abandoned_conversation_still_excluded(self):
        """ABANDONED conversations are still excluded (regression check)."""
        conv = self.manager.create_conversation("sess-1", "user-1")
        self.manager.transition_state(conv.id, StandupConversationState.ABANDONED)

        result = self.manager.get_conversation_by_session("sess-1")
        assert result is None


class TestResumeAcceptanceWiring:
    """Issue #889: When user says 'yes' to resume offer, standup resumes."""

    @pytest.mark.asyncio
    async def test_resume_transitions_suspended_to_initiated(self):
        """Accepting resume offer transitions SUSPENDED → INITIATED."""
        from services.intent.intent_service import IntentService

        service = IntentService()
        manager = StandupConversationManager()

        # Create a suspended standup for the user
        conv = manager.create_conversation("old-sess", "user-1")
        manager.transition_state(conv.id, StandupConversationState.GENERATING)
        manager.transition_state(conv.id, StandupConversationState.SUSPENDED)

        with patch(
            "services.conversation.conversation_handler._get_standup_components",
            return_value=(manager, MagicMock()),
        ):
            result = await service._resume_suspended_standup("user-1", "new-sess")

        assert result.success is True
        assert "pick up where we left off" in result.message
        assert result.intent_data["action"] == "standup_conversation_resumed"
        assert conv.state == StandupConversationState.INITIATED
        assert conv.session_id == "new-sess"  # Updated to current session

    @pytest.mark.asyncio
    async def test_resume_shows_existing_content(self):
        """Resume message includes previously captured standup content."""
        from services.intent.intent_service import IntentService

        service = IntentService()
        manager = StandupConversationManager()

        conv = manager.create_conversation("old-sess", "user-1")
        manager.transition_state(conv.id, StandupConversationState.GENERATING)
        manager.set_standup_content(conv.id, "**Yesterday**: Worked on auth\n**Today**: Continue auth")
        manager.transition_state(conv.id, StandupConversationState.SUSPENDED)

        with patch(
            "services.conversation.conversation_handler._get_standup_components",
            return_value=(manager, MagicMock()),
        ):
            result = await service._resume_suspended_standup("user-1", "new-sess")

        assert "Worked on auth" in result.message
        assert "Continue auth" in result.message

    @pytest.mark.asyncio
    async def test_resume_no_suspended_session_gives_fallback(self):
        """If no suspended session exists, a fallback message is returned."""
        from services.intent.intent_service import IntentService

        service = IntentService()
        manager = StandupConversationManager()

        with patch(
            "services.conversation.conversation_handler._get_standup_components",
            return_value=(manager, MagicMock()),
        ):
            result = await service._resume_suspended_standup("user-1", "new-sess")

        assert result.success is True
        assert "couldn't find" in result.message
        assert "/standup" in result.message


class TestResumeDeclineWiring:
    """Issue #889: When user says 'no' to resume offer, session is abandoned."""

    @pytest.mark.asyncio
    async def test_decline_transitions_suspended_to_abandoned(self):
        """Declining resume offer transitions SUSPENDED → ABANDONED."""
        from services.intent.intent_service import IntentService

        service = IntentService()
        manager = StandupConversationManager()

        conv = manager.create_conversation("old-sess", "user-1")
        manager.transition_state(conv.id, StandupConversationState.GENERATING)
        manager.transition_state(conv.id, StandupConversationState.SUSPENDED)

        with patch(
            "services.conversation.conversation_handler._get_standup_components",
            return_value=(manager, MagicMock()),
        ):
            result = await service._abandon_suspended_standup("user-1")

        assert result.success is True
        assert "No problem" in result.message
        assert conv.state == StandupConversationState.ABANDONED


class TestPendingResumeOfferDetection:
    """Issue #889: _check_pending_resume_offer correctly detects accept/decline."""

    @pytest.mark.asyncio
    async def test_accept_signals_trigger_resume(self):
        """Various 'yes' phrases trigger resume."""
        from services.intent.intent_service import IntentService
        from services.process.registry import ProcessType, SuspendedInfo

        service = IntentService()

        suspended_info = SuspendedInfo(
            process_type=ProcessType.STANDUP,
            suspended_at=datetime.now(),
            description="Your standup was paused.",
        )

        accept_phrases = ["yes", "continue", "resume", "sure", "ok", "yes please"]

        for phrase in accept_phrases:
            with (
                patch(
                    "services.intent.intent_service.get_process_registry",
                ) as mock_registry_fn,
                patch.object(
                    service,
                    "_resume_suspended_standup",
                    new_callable=AsyncMock,
                    return_value=MagicMock(success=True),
                ) as mock_resume,
            ):
                mock_registry = MagicMock()
                mock_registry.check_suspended_processes = AsyncMock(return_value=suspended_info)
                mock_registry_fn.return_value = mock_registry

                result = await service._check_pending_resume_offer("user-1", "sess-1", phrase)
                assert result is not None, f"'{phrase}' should trigger resume"
                mock_resume.assert_called_once()

    @pytest.mark.asyncio
    async def test_decline_signals_trigger_abandon(self):
        """Various 'no' phrases trigger abandon."""
        from services.intent.intent_service import IntentService
        from services.process.registry import ProcessType, SuspendedInfo

        service = IntentService()

        suspended_info = SuspendedInfo(
            process_type=ProcessType.STANDUP,
            suspended_at=datetime.now(),
            description="Your standup was paused.",
        )

        decline_phrases = ["no", "fresh", "start over", "nah", "no thanks"]

        for phrase in decline_phrases:
            with (
                patch(
                    "services.intent.intent_service.get_process_registry",
                ) as mock_registry_fn,
                patch.object(
                    service,
                    "_abandon_suspended_standup",
                    new_callable=AsyncMock,
                    return_value=MagicMock(success=True),
                ) as mock_abandon,
            ):
                mock_registry = MagicMock()
                mock_registry.check_suspended_processes = AsyncMock(return_value=suspended_info)
                mock_registry_fn.return_value = mock_registry

                result = await service._check_pending_resume_offer("user-1", "sess-1", phrase)
                assert result is not None, f"'{phrase}' should trigger abandon"
                mock_abandon.assert_called_once()

    @pytest.mark.asyncio
    async def test_unrelated_message_returns_none(self):
        """Messages that aren't accept/decline are ignored — normal classification proceeds."""
        from services.intent.intent_service import IntentService
        from services.process.registry import ProcessType, SuspendedInfo

        service = IntentService()

        suspended_info = SuspendedInfo(
            process_type=ProcessType.STANDUP,
            suspended_at=datetime.now(),
            description="Your standup was paused.",
        )

        with patch(
            "services.intent.intent_service.get_process_registry",
        ) as mock_registry_fn:
            mock_registry = MagicMock()
            mock_registry.check_suspended_processes = AsyncMock(return_value=suspended_info)
            mock_registry_fn.return_value = mock_registry

            result = await service._check_pending_resume_offer(
                "user-1", "sess-1", "show me my calendar"
            )
            assert result is None

    @pytest.mark.asyncio
    async def test_no_suspended_session_returns_none(self):
        """When there's no suspended session, returns None immediately."""
        from services.intent.intent_service import IntentService

        service = IntentService()

        with patch(
            "services.intent.intent_service.get_process_registry",
        ) as mock_registry_fn:
            mock_registry = MagicMock()
            mock_registry.check_suspended_processes = AsyncMock(return_value=None)
            mock_registry_fn.return_value = mock_registry

            result = await service._check_pending_resume_offer("user-1", "sess-1", "yes")
            assert result is None


class TestDeprecatedCheckActiveStandup:
    """Issue #889: _check_active_standup is deprecated but still functional."""

    def test_method_still_exists(self):
        """_check_active_standup exists for backward compatibility."""
        from services.intent.intent_service import IntentService

        assert hasattr(IntentService, "_check_active_standup")

    @pytest.mark.asyncio
    async def test_excludes_suspended_conversations(self):
        """_check_active_standup now skips SUSPENDED state (bug fix)."""
        from services.intent.intent_service import IntentService

        service = IntentService()
        manager = StandupConversationManager()

        conv = manager.create_conversation("sess-1", "user-1")
        manager.transition_state(conv.id, StandupConversationState.GENERATING)
        manager.transition_state(conv.id, StandupConversationState.SUSPENDED)

        with patch(
            "services.conversation.conversation_handler._get_standup_components",
            return_value=(manager, MagicMock()),
        ):
            result = await service._check_active_standup("user-1", "sess-1", "hello")

        # Should return None because SUSPENDED is not active
        assert result is None

    def test_deprecation_noted_in_docstring(self):
        """The method's docstring notes its deprecation."""
        import inspect

        from services.intent.intent_service import IntentService

        source = inspect.getsource(IntentService._check_active_standup)
        assert "DEPRECATED" in source or "deprecated" in source

    def test_no_debug_prints(self):
        """Issue #889 cleanup: debug print statements removed."""
        import inspect

        from services.intent.intent_service import IntentService

        source = inspect.getsource(IntentService._check_active_standup)
        assert "print(" not in source
