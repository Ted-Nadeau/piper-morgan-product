"""Add composite indexes for performance improvement - Issue #356

Revision ID: a7c3f9e2b1d4
Revises: 4d1e2c3b5f7a
Create Date: 2025-11-21 23:05:00.000000

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "a7c3f9e2b1d4"
down_revision = "4d1e2c3b5f7a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add composite indexes for common query patterns - Issue #356 PERF-INDEX"""

    # =================================================================
    # CONVERSATION SYSTEM INDEXES (High Priority)
    # =================================================================

    # Index 1: conversations - User conversation history listing
    # Query pattern: "Get user's conversations ordered by most recent"
    # SELECT * FROM conversations WHERE user_id = ? ORDER BY created_at DESC LIMIT 10
    # Performance impact: O(n) → O(log n) for user conversation history
    # Use case: Conversation listing page, user dashboard
    op.create_index(
        "idx_conversations_user_created",
        "conversations",
        ["user_id", sa.text("created_at DESC")],
        postgresql_using="btree",
    )

    # Index 2: conversation_turns - Recent turns in conversation (context window)
    # Query pattern: "Get last N turns from a conversation ordered chronologically"
    # SELECT * FROM conversation_turns WHERE conversation_id = ? ORDER BY created_at DESC LIMIT 10
    # Performance impact: O(n) → O(log n) for context window retrieval
    # Use case: ConversationManager context window, conversation display, anaphoric resolution
    op.create_index(
        "idx_conversation_turns_conv_created",
        "conversation_turns",
        ["conversation_id", sa.text("created_at DESC")],
        postgresql_using="btree",
    )

    # Index 3: conversation_turns - Entity-based search (JSONB array)
    # Query pattern: "Find turns mentioning specific entity"
    # SELECT * FROM conversation_turns WHERE entities @> ?
    # Performance impact: GIN index for JSONB array containment queries
    # Use case: Entity tracking across conversations, conversation search
    op.create_index(
        "idx_conversation_turns_entities",
        "conversation_turns",
        ["entities"],
        postgresql_using="gin",
    )

    # Index 4: conversation_turns - Reference resolution tracking (JSONB object)
    # Query pattern: "Find turns with specific anaphoric reference"
    # SELECT * FROM conversation_turns WHERE references @> ?
    # Performance impact: GIN index for JSONB object key searches
    # Use case: Reference resolver, pronoun/reference tracking
    op.create_index(
        "idx_conversation_turns_references",
        "conversation_turns",
        ["references"],
        postgresql_using="gin",
    )

    # =================================================================
    # GENERAL SYSTEM INDEXES (Medium Priority)
    # =================================================================

    # Index 5: audit_logs - User activity timeline queries
    # Query pattern: SELECT * FROM audit_logs WHERE user_id = ? ORDER BY created_at DESC
    # Performance impact: O(n) → O(log n) for user audit trails
    # Use case: User activity audit, compliance reporting
    op.create_index(
        "idx_audit_logs_user_timeline",
        "audit_logs",
        ["user_id", sa.text("created_at DESC")],
        postgresql_using="btree",
    )

    # Index 6: feedback - User feedback review with status filter
    # Query pattern: SELECT * FROM feedback WHERE user_id = ? AND status = ? ORDER BY created_at DESC
    # Performance impact: Multi-column filter + sort optimization
    # Use case: Feedback review page, user feedback analytics
    op.create_index(
        "idx_feedback_user_status_date",
        "feedback",
        ["user_id", "status", sa.text("created_at DESC")],
        postgresql_using="btree",
    )


def downgrade() -> None:
    """Remove composite indexes"""
    op.drop_index("idx_feedback_user_status_date", table_name="feedback")
    op.drop_index("idx_audit_logs_user_timeline", table_name="audit_logs")
    op.drop_index("idx_conversation_turns_references", table_name="conversation_turns")
    op.drop_index("idx_conversation_turns_entities", table_name="conversation_turns")
    op.drop_index("idx_conversation_turns_conv_created", table_name="conversation_turns")
    op.drop_index("idx_conversations_user_created", table_name="conversations")
