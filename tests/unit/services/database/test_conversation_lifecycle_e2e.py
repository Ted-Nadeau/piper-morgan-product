"""
Integration test T14: Full lifecycle — create, converse, archive, search, continue, delete

Spec #858: Conversation Lifecycle Specification v1.1
Issue #715: MUX-HOME-CONVERSATIONS-LIFECYCLE

This test exercises the complete happy-path lifecycle through the API layer:
  Step 1: Create a conversation (POST)
  Step 2: Verify it appears in left sidebar (GET ?state=active)
  Step 3: Archive it (PATCH /state)
  Step 4: Verify it's gone from left sidebar, present in right sidebar
  Step 5: Search finds archived conversation
  Step 6: Reactivate it (PATCH /state)
  Step 7: Delete it (DELETE)

This uses mocked repos to exercise the route handlers end-to-end
without requiring a database.
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from services.domain import models as domain
from services.shared_types import ConversationLifecycleState
from web.api.routes.conversations import (
    CreateConversationRequest,
    UpdateStateRequest,
    create_conversation,
    delete_conversation,
    list_conversations,
    update_conversation_state,
)


def _mock_user():
    user = MagicMock()
    user.sub = str(uuid4())
    user.username = "testuser"
    return user


class TestT14FullLifecycle:
    """
    T14: Full lifecycle — create, converse, archive, search, continue, delete

    This is the critical end-to-end happy path integration test.
    """

    @pytest.mark.asyncio
    async def test_full_lifecycle_happy_path(self):
        """
        T14: End-to-end lifecycle through all states.

        Create → ACTIVE in sidebar → Archive → NOT in sidebar →
        Search finds it → Reactivate → Back in sidebar → Delete → Gone
        """
        user = _mock_user()
        conversation_id = str(uuid4())
        now = datetime.now(timezone.utc)

        # ── State tracking: simulate repository state ──
        # We'll track the conversation's state across transitions

        active_conv = domain.Conversation(
            id=conversation_id,
            user_id=user.sub,
            session_id=conversation_id,
            title="Q4 Planning Discussion",
            context={},
            is_active=True,
            lifecycle_state=ConversationLifecycleState.ACTIVE,
            created_at=now,
            updated_at=now,
            last_activity_at=now,
        )

        archived_conv = domain.Conversation(
            id=conversation_id,
            user_id=user.sub,
            session_id=conversation_id,
            title="Q4 Planning Discussion",
            context={},
            is_active=True,
            lifecycle_state=ConversationLifecycleState.ARCHIVED,
            archived_at=now,
            created_at=now,
            updated_at=now,
            last_activity_at=now,
        )

        deleted_conv = domain.Conversation(
            id=conversation_id,
            user_id=user.sub,
            session_id=conversation_id,
            title="Q4 Planning Discussion",
            context={},
            is_active=False,
            lifecycle_state=ConversationLifecycleState.DELETED,
            deleted_at=now,
            created_at=now,
            updated_at=now,
            last_activity_at=now,
        )

        repo = MagicMock()
        repo.get_turn_count = AsyncMock(return_value=3)

        # ── Step 1: Create ──
        repo.create = AsyncMock(return_value=active_conv)

        result = await create_conversation(
            request=CreateConversationRequest(title="Q4 Planning Discussion"),
            current_user=user,
            conv_repo=repo,
        )

        assert result.id == conversation_id
        assert result.lifecycle_state == "active"

        # ── Step 2: Verify ACTIVE appears in left sidebar ──
        repo.list_for_user = AsyncMock(return_value=[active_conv])

        sidebar = await list_conversations(
            state="active",
            current_user=user,
            conv_repo=repo,
        )

        assert len(sidebar.conversations) == 1
        assert sidebar.conversations[0].id == conversation_id
        assert sidebar.conversations[0].lifecycle_state == "active"

        # ── Step 3: Archive ──
        repo.get_by_id = AsyncMock(return_value=active_conv)
        repo.archive_conversation = AsyncMock(return_value=archived_conv)

        archive_result = await update_conversation_state(
            conversation_id=conversation_id,
            request=UpdateStateRequest(state="archived"),
            current_user=user,
            conv_repo=repo,
        )

        assert archive_result.lifecycle_state == "archived"
        assert archive_result.message == "Conversation archived"

        # ── Step 4: Verify NOT in left sidebar, but IS in right sidebar ──
        # Left sidebar (ACTIVE only) — empty
        repo.list_for_user = AsyncMock(return_value=[])

        left_sidebar = await list_conversations(
            state="active",
            current_user=user,
            conv_repo=repo,
        )
        assert len(left_sidebar.conversations) == 0

        # Right sidebar (ARCHIVED) — has it
        repo.list_for_user = AsyncMock(return_value=[archived_conv])

        right_sidebar = await list_conversations(
            state="archived",
            current_user=user,
            conv_repo=repo,
        )
        assert len(right_sidebar.conversations) == 1
        assert right_sidebar.conversations[0].lifecycle_state == "archived"

        # ── Step 5: Search finds archived conversation ──
        repo.search_for_user = AsyncMock(return_value=[archived_conv])

        search_result = await list_conversations(
            search="Q4 Planning",
            current_user=user,
            conv_repo=repo,
        )
        assert len(search_result.conversations) == 1
        assert search_result.conversations[0].title == "Q4 Planning Discussion"

        # ── Step 6: Reactivate ──
        repo.get_by_id = AsyncMock(return_value=archived_conv)
        repo.reactivate_conversation = AsyncMock(return_value=active_conv)

        reactivate_result = await update_conversation_state(
            conversation_id=conversation_id,
            request=UpdateStateRequest(state="active"),
            current_user=user,
            conv_repo=repo,
        )

        assert reactivate_result.lifecycle_state == "active"
        assert reactivate_result.message == "Conversation reactivated"

        # Verify back in left sidebar
        repo.list_for_user = AsyncMock(return_value=[active_conv])

        left_sidebar_after = await list_conversations(
            state="active",
            current_user=user,
            conv_repo=repo,
        )
        assert len(left_sidebar_after.conversations) == 1

        # ── Step 7: Delete ──
        repo.get_by_id = AsyncMock(return_value=active_conv)
        repo.delete_conversation = AsyncMock(return_value=deleted_conv)

        delete_result = await delete_conversation(
            conversation_id=conversation_id,
            current_user=user,
            conv_repo=repo,
        )

        assert delete_result.lifecycle_state == "deleted"
        assert delete_result.message == "Conversation deleted"

        # Verify gone from both sidebars
        repo.list_for_user = AsyncMock(return_value=[])

        final_left = await list_conversations(
            state="active",
            current_user=user,
            conv_repo=repo,
        )
        assert len(final_left.conversations) == 0

        final_right = await list_conversations(
            state="archived",
            current_user=user,
            conv_repo=repo,
        )
        assert len(final_right.conversations) == 0
