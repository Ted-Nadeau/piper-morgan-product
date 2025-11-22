"""Add analytics-focused indexes for conversation intent tracking - Issue #532

Revision ID: b8e4f3c9a2d7
Revises: a7c3f9e2b1d4
Create Date: 2025-11-21 23:35:00.000000

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "b8e4f3c9a2d7"
down_revision = "a7c3f9e2b1d4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add analytics indexes for conversation intent tracking - Issue #532"""

    # Index 1: conversation_turns - Intent classification analytics
    # Query pattern: "Get all turns of a specific intent type"
    # SELECT * FROM conversation_turns WHERE intent = 'question' LIMIT 100
    # Performance impact: Intent-based analytics queries
    # Use case: Conversation analytics, intent distribution analysis, learning system feedback
    op.create_index(
        "idx_conversation_turns_intent",
        "conversation_turns",
        ["intent"],
        postgresql_using="btree",
    )

    # Index 2: conversation_turns - Composite intent + conversation
    # Query pattern: "Get all turns of specific intent within conversation"
    # SELECT * FROM conversation_turns WHERE conversation_id = ? AND intent = ?
    # Performance impact: Intent-specific conversation analysis
    # Use case: Conversation threading by intent, intent trajectory within conversation
    op.create_index(
        "idx_conversation_turns_conv_intent",
        "conversation_turns",
        ["conversation_id", "intent"],
        postgresql_using="btree",
    )


def downgrade() -> None:
    """Remove analytics indexes"""
    op.drop_index("idx_conversation_turns_conv_intent", table_name="conversation_turns")
    op.drop_index("idx_conversation_turns_intent", table_name="conversation_turns")
