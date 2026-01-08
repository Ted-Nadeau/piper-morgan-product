"""
Issue #552: Tests for standup conversation state management.

Epic #242: CONV-MCP-STANDUP-INTERACTIVE

Tests verify:
- StandupConversationState enum has all required states
- StandupConversation dataclass initializes and serializes correctly
- StandupConversationManager state machine validation
- Conversation lifecycle (create, get, transition, complete)
- Turn management and history
- Preferences and content management
"""

import pytest

from services.domain.models import ConversationTurn, StandupConversation
from services.shared_types import StandupConversationState
from services.standup.conversation_manager import (
    InvalidStateTransitionError,
    StandupConversationManager,
)


class TestStandupConversationState:
    """Tests for StandupConversationState enum."""

    def test_enum_has_all_states(self):
        """All required states exist."""
        states = [s.value for s in StandupConversationState]

        assert "initiated" in states
        assert "gathering_preferences" in states
        assert "generating" in states
        assert "refining" in states
        assert "finalizing" in states
        assert "complete" in states
        assert "abandoned" in states

    def test_enum_count(self):
        """Exactly 7 states defined."""
        assert len(StandupConversationState) == 7

    def test_enum_values_are_strings(self):
        """All enum values are lowercase strings."""
        for state in StandupConversationState:
            assert isinstance(state.value, str)
            assert state.value == state.value.lower()


class TestStandupConversation:
    """Tests for StandupConversation dataclass."""

    def test_default_state_is_initiated(self):
        """New conversation starts in INITIATED state."""
        conv = StandupConversation(session_id="test", user_id="user1")

        assert conv.state == StandupConversationState.INITIATED
        assert conv.previous_state is None

    def test_generates_unique_id(self):
        """Each conversation gets a unique ID."""
        conv1 = StandupConversation(session_id="test", user_id="user1")
        conv2 = StandupConversation(session_id="test", user_id="user1")

        assert conv1.id != conv2.id

    def test_default_collections_are_empty(self):
        """Default collections are initialized empty."""
        conv = StandupConversation(session_id="test", user_id="user1")

        assert conv.preferences == {}
        assert conv.turns == []
        assert conv.standup_versions == []
        assert conv.context == {}

    def test_to_dict_serialization(self):
        """to_dict() produces valid dictionary."""
        conv = StandupConversation(
            session_id="test",
            user_id="user1",
            preferences={"focus": "github"},
        )

        result = conv.to_dict()

        assert result["session_id"] == "test"
        assert result["user_id"] == "user1"
        assert result["state"] == "initiated"
        assert result["preferences"] == {"focus": "github"}
        assert "id" in result
        assert "created_at" in result
        assert "updated_at" in result

    def test_to_dict_includes_previous_state(self):
        """to_dict() includes previous_state when set."""
        conv = StandupConversation(session_id="test", user_id="user1")
        conv.previous_state = StandupConversationState.INITIATED
        conv.state = StandupConversationState.GENERATING

        result = conv.to_dict()

        assert result["state"] == "generating"
        assert result["previous_state"] == "initiated"

    def test_to_dict_with_none_previous_state(self):
        """to_dict() handles None previous_state."""
        conv = StandupConversation(session_id="test", user_id="user1")

        result = conv.to_dict()

        assert result["previous_state"] is None


class TestStandupConversationManager:
    """Tests for StandupConversationManager service."""

    @pytest.fixture
    def manager(self):
        """Fresh manager for each test."""
        return StandupConversationManager()

    def test_create_conversation(self, manager):
        """Create conversation initializes correctly."""
        conv = manager.create_conversation(
            session_id="session1",
            user_id="user1",
            initial_context={"source": "test"},
        )

        assert conv.session_id == "session1"
        assert conv.user_id == "user1"
        assert conv.state == StandupConversationState.INITIATED
        assert conv.context == {"source": "test"}

    def test_create_conversation_without_context(self, manager):
        """Create conversation works without initial context."""
        conv = manager.create_conversation(
            session_id="session1",
            user_id="user1",
        )

        assert conv.context == {}

    def test_get_conversation(self, manager):
        """Retrieve conversation by ID."""
        conv = manager.create_conversation("s1", "u1")

        retrieved = manager.get_conversation(conv.id)

        assert retrieved is not None
        assert retrieved.id == conv.id

    def test_get_conversation_not_found(self, manager):
        """Non-existent conversation returns None."""
        result = manager.get_conversation("nonexistent")

        assert result is None

    def test_get_conversation_by_session(self, manager):
        """Find active conversation for session."""
        conv = manager.create_conversation("session1", "user1")

        found = manager.get_conversation_by_session("session1")

        assert found is not None
        assert found.id == conv.id

    def test_get_conversation_by_session_not_found(self, manager):
        """Non-existent session returns None."""
        result = manager.get_conversation_by_session("nonexistent")

        assert result is None

    def test_get_conversation_by_session_ignores_complete(self, manager):
        """Completed conversations are not returned by session lookup."""
        conv = manager.create_conversation("session1", "user1")
        manager.transition_state(conv.id, StandupConversationState.GENERATING)
        manager.transition_state(conv.id, StandupConversationState.FINALIZING)
        manager.transition_state(conv.id, StandupConversationState.COMPLETE)

        found = manager.get_conversation_by_session("session1")

        assert found is None

    def test_get_conversation_by_session_ignores_abandoned(self, manager):
        """Abandoned conversations are not returned by session lookup."""
        conv = manager.create_conversation("session1", "user1")
        manager.transition_state(conv.id, StandupConversationState.ABANDONED)

        found = manager.get_conversation_by_session("session1")

        assert found is None


class TestStateTransitions:
    """Tests for state transition validation."""

    @pytest.fixture
    def manager(self):
        return StandupConversationManager()

    @pytest.fixture
    def conversation(self, manager):
        return manager.create_conversation("s1", "u1")

    def test_valid_transition_initiated_to_gathering(self, manager, conversation):
        """INITIATED -> GATHERING_PREFERENCES is valid."""
        result = manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_PREFERENCES
        )

        assert result.state == StandupConversationState.GATHERING_PREFERENCES
        assert result.previous_state == StandupConversationState.INITIATED

    def test_valid_transition_initiated_to_generating(self, manager, conversation):
        """INITIATED -> GENERATING is valid (skip preferences)."""
        result = manager.transition_state(conversation.id, StandupConversationState.GENERATING)

        assert result.state == StandupConversationState.GENERATING

    def test_valid_transition_initiated_to_abandoned(self, manager, conversation):
        """INITIATED -> ABANDONED is valid."""
        result = manager.transition_state(conversation.id, StandupConversationState.ABANDONED)

        assert result.state == StandupConversationState.ABANDONED

    def test_valid_transition_gathering_to_generating(self, manager, conversation):
        """GATHERING_PREFERENCES -> GENERATING is valid."""
        manager.transition_state(conversation.id, StandupConversationState.GATHERING_PREFERENCES)

        result = manager.transition_state(conversation.id, StandupConversationState.GENERATING)

        assert result.state == StandupConversationState.GENERATING

    def test_valid_transition_generating_to_refining(self, manager, conversation):
        """GENERATING -> REFINING is valid."""
        manager.transition_state(conversation.id, StandupConversationState.GENERATING)

        result = manager.transition_state(conversation.id, StandupConversationState.REFINING)

        assert result.state == StandupConversationState.REFINING

    def test_valid_transition_generating_to_finalizing(self, manager, conversation):
        """GENERATING -> FINALIZING is valid (skip refinement)."""
        manager.transition_state(conversation.id, StandupConversationState.GENERATING)

        result = manager.transition_state(conversation.id, StandupConversationState.FINALIZING)

        assert result.state == StandupConversationState.FINALIZING

    def test_valid_transition_refining_to_generating(self, manager, conversation):
        """REFINING -> GENERATING is valid (re-generate)."""
        manager.transition_state(conversation.id, StandupConversationState.GENERATING)
        manager.transition_state(conversation.id, StandupConversationState.REFINING)

        result = manager.transition_state(conversation.id, StandupConversationState.GENERATING)

        assert result.state == StandupConversationState.GENERATING

    def test_valid_transition_to_complete(self, manager, conversation):
        """Full path to COMPLETE."""
        manager.transition_state(conversation.id, StandupConversationState.GENERATING)
        manager.transition_state(conversation.id, StandupConversationState.FINALIZING)

        result = manager.transition_state(conversation.id, StandupConversationState.COMPLETE)

        assert result.state == StandupConversationState.COMPLETE
        assert result.completed_at is not None

    def test_invalid_transition_raises_error(self, manager, conversation):
        """Invalid transition raises InvalidStateTransitionError."""
        with pytest.raises(InvalidStateTransitionError) as exc_info:
            manager.transition_state(
                conversation.id,
                StandupConversationState.COMPLETE,  # Can't go directly to COMPLETE
            )

        assert "Cannot transition" in str(exc_info.value)
        assert "initiated" in str(exc_info.value).lower()

    def test_transition_from_complete_raises_error(self, manager, conversation):
        """Cannot transition out of COMPLETE (terminal state)."""
        manager.transition_state(conversation.id, StandupConversationState.GENERATING)
        manager.transition_state(conversation.id, StandupConversationState.FINALIZING)
        manager.transition_state(conversation.id, StandupConversationState.COMPLETE)

        with pytest.raises(InvalidStateTransitionError):
            manager.transition_state(conversation.id, StandupConversationState.REFINING)

    def test_transition_from_abandoned_raises_error(self, manager, conversation):
        """Cannot transition out of ABANDONED (terminal state)."""
        manager.transition_state(conversation.id, StandupConversationState.ABANDONED)

        with pytest.raises(InvalidStateTransitionError):
            manager.transition_state(conversation.id, StandupConversationState.GENERATING)

    def test_transition_nonexistent_conversation_raises_keyerror(self, manager):
        """Transitioning nonexistent conversation raises KeyError."""
        with pytest.raises(KeyError):
            manager.transition_state("nonexistent", StandupConversationState.GENERATING)

    def test_transition_updates_timestamp(self, manager, conversation):
        """State transition updates updated_at timestamp."""
        original_updated = conversation.updated_at

        result = manager.transition_state(conversation.id, StandupConversationState.GENERATING)

        assert result.updated_at >= original_updated


class TestConversationTurns:
    """Tests for turn management."""

    @pytest.fixture
    def manager(self):
        return StandupConversationManager()

    @pytest.fixture
    def conversation(self, manager):
        return manager.create_conversation("s1", "u1")

    def test_add_turn(self, manager, conversation):
        """Add turn records correctly."""
        turn = manager.add_turn(
            conversation.id,
            user_message="standup",
            assistant_response="Ready for your standup?",
            intent="standup_request",
        )

        assert turn.turn_number == 1
        assert turn.user_message == "standup"
        assert turn.assistant_response == "Ready for your standup?"
        assert turn.intent == "standup_request"

    def test_turn_numbers_increment(self, manager, conversation):
        """Turn numbers increment correctly."""
        turn1 = manager.add_turn(conversation.id, "msg1", "resp1")
        turn2 = manager.add_turn(conversation.id, "msg2", "resp2")
        turn3 = manager.add_turn(conversation.id, "msg3", "resp3")

        assert turn1.turn_number == 1
        assert turn2.turn_number == 2
        assert turn3.turn_number == 3

        conv = manager.get_conversation(conversation.id)
        assert len(conv.turns) == 3

    def test_add_turn_with_metadata(self, manager, conversation):
        """Turn metadata is preserved."""
        turn = manager.add_turn(
            conversation.id,
            "msg",
            "resp",
            metadata={"source": "chat", "confidence": 0.95},
        )

        assert turn.metadata["source"] == "chat"
        assert turn.metadata["confidence"] == 0.95

    def test_add_turn_nonexistent_conversation_raises_keyerror(self, manager):
        """Adding turn to nonexistent conversation raises KeyError."""
        with pytest.raises(KeyError):
            manager.add_turn("nonexistent", "msg", "resp")

    def test_add_turn_updates_timestamp(self, manager, conversation):
        """Adding turn updates conversation updated_at."""
        original_updated = conversation.updated_at

        manager.add_turn(conversation.id, "msg", "resp")

        conv = manager.get_conversation(conversation.id)
        assert conv.updated_at >= original_updated


class TestPreferencesAndContent:
    """Tests for preferences and standup content management."""

    @pytest.fixture
    def manager(self):
        return StandupConversationManager()

    @pytest.fixture
    def conversation(self, manager):
        return manager.create_conversation("s1", "u1")

    def test_update_preferences(self, manager, conversation):
        """Preferences merge correctly."""
        manager.update_preferences(conversation.id, {"focus": "github"})
        manager.update_preferences(conversation.id, {"exclude": ["docs"]})

        conv = manager.get_conversation(conversation.id)

        assert conv.preferences["focus"] == "github"
        assert conv.preferences["exclude"] == ["docs"]

    def test_update_preferences_overwrites_existing(self, manager, conversation):
        """Updating same key overwrites previous value."""
        manager.update_preferences(conversation.id, {"focus": "github"})
        manager.update_preferences(conversation.id, {"focus": "calendar"})

        conv = manager.get_conversation(conversation.id)

        assert conv.preferences["focus"] == "calendar"

    def test_update_preferences_nonexistent_raises_keyerror(self, manager):
        """Updating preferences on nonexistent conversation raises KeyError."""
        with pytest.raises(KeyError):
            manager.update_preferences("nonexistent", {"focus": "test"})

    def test_set_standup_content(self, manager, conversation):
        """Setting content works correctly."""
        manager.set_standup_content(conversation.id, "First standup content")

        conv = manager.get_conversation(conversation.id)

        assert conv.current_standup == "First standup content"

    def test_set_standup_content_tracks_versions(self, manager, conversation):
        """Content changes are versioned."""
        manager.set_standup_content(conversation.id, "Version 1")
        manager.set_standup_content(conversation.id, "Version 2")
        manager.set_standup_content(conversation.id, "Version 3")

        conv = manager.get_conversation(conversation.id)

        assert conv.current_standup == "Version 3"
        assert conv.standup_versions == ["Version 1", "Version 2"]

    def test_set_standup_content_nonexistent_raises_keyerror(self, manager):
        """Setting content on nonexistent conversation raises KeyError."""
        with pytest.raises(KeyError):
            manager.set_standup_content("nonexistent", "content")

    def test_set_standup_content_updates_timestamp(self, manager, conversation):
        """Setting content updates updated_at timestamp."""
        original_updated = conversation.updated_at

        manager.set_standup_content(conversation.id, "content")

        conv = manager.get_conversation(conversation.id)
        assert conv.updated_at >= original_updated


class TestCleanup:
    """Tests for conversation cleanup."""

    @pytest.fixture
    def manager(self):
        return StandupConversationManager()

    def test_cleanup_removes_expired(self, manager):
        """Cleanup removes expired conversations."""
        from datetime import timedelta

        conv = manager.create_conversation("s1", "u1")
        # Manually set updated_at to past
        conv.updated_at = conv.updated_at - timedelta(minutes=120)

        removed = manager.cleanup_expired(max_age_minutes=60)

        assert removed == 1
        assert manager.get_conversation(conv.id) is None

    def test_cleanup_preserves_complete(self, manager):
        """Cleanup does not remove completed conversations."""
        from datetime import timedelta

        conv = manager.create_conversation("s1", "u1")
        manager.transition_state(conv.id, StandupConversationState.GENERATING)
        manager.transition_state(conv.id, StandupConversationState.FINALIZING)
        manager.transition_state(conv.id, StandupConversationState.COMPLETE)
        # Manually set updated_at to past
        conv.updated_at = conv.updated_at - timedelta(minutes=120)

        removed = manager.cleanup_expired(max_age_minutes=60)

        assert removed == 0
        assert manager.get_conversation(conv.id) is not None

    def test_cleanup_preserves_recent(self, manager):
        """Cleanup preserves recent conversations."""
        conv = manager.create_conversation("s1", "u1")

        removed = manager.cleanup_expired(max_age_minutes=60)

        assert removed == 0
        assert manager.get_conversation(conv.id) is not None
