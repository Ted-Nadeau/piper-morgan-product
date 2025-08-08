"""PM-034 Phase 1: Conversation foundation

Revision ID: a9ee08bbdf8c
Revises: 7473b4231d5d
Create Date: 2025-08-07 08:46:04.826431

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a9ee08bbdf8c"
down_revision: Union[str, Sequence[str], None] = "7473b4231d5d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create conversations and conversation_turns tables for PM-034 Phase 1."""

    # Create conversations table
    op.create_table(
        "conversations",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("session_id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False, default=""),
        sa.Column("context", postgresql.JSONB(), nullable=False, default={}),
        sa.Column("is_active", sa.Boolean(), nullable=False, default=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("last_activity_at", sa.DateTime(), nullable=True),
    )

    # Create indexes for conversations table
    op.create_index("idx_conversations_user_id", "conversations", ["user_id"])
    op.create_index("idx_conversations_session_id", "conversations", ["session_id"])
    op.create_index("idx_conversations_is_active", "conversations", ["is_active"])
    op.create_index("idx_conversations_last_activity", "conversations", ["last_activity_at"])

    # Create conversation_turns table
    op.create_table(
        "conversation_turns",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("conversation_id", sa.String(), nullable=False),
        sa.Column("turn_number", sa.Integer(), nullable=False, default=0),
        sa.Column("user_message", sa.Text(), nullable=False, default=""),
        sa.Column("assistant_response", sa.Text(), nullable=False, default=""),
        sa.Column("intent", sa.String(), nullable=True),
        sa.Column("entities", postgresql.JSONB(), nullable=False, default=[]),
        sa.Column("references", postgresql.JSONB(), nullable=False, default={}),
        sa.Column("context_used", postgresql.JSONB(), nullable=False, default={}),
        sa.Column("metadata", postgresql.JSONB(), nullable=False, default={}),
        sa.Column("processing_time", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["conversation_id"], ["conversations.id"], ondelete="CASCADE"),
    )

    # Create indexes for conversation_turns table
    op.create_index(
        "idx_conversation_turns_conversation_id", "conversation_turns", ["conversation_id"]
    )
    op.create_index(
        "idx_conversation_turns_turn_number",
        "conversation_turns",
        ["conversation_id", "turn_number"],
    )
    op.create_index("idx_conversation_turns_created_at", "conversation_turns", ["created_at"])


def downgrade() -> None:
    """Drop conversations and conversation_turns tables."""
    op.drop_table("conversation_turns")
    op.drop_table("conversations")
