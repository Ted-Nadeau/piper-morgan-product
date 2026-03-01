"""add lifecycle columns to conversations table issue 715

Revision ID: a715_conv_lifecycle
Revises: a867_repo_metadata
Create Date: 2026-03-01

Issue #715: MUX-HOME-CONVERSATIONS-LIFECYCLE
Spec #858: Conversation Lifecycle Specification v1.1

Adds lifecycle_state, archived_at, deleted_at to conversations.
Backfills existing rows to lifecycle_state='active'.
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "a715_conv_lifecycle"
down_revision: Union[str, Sequence[str], None] = "a867_repo_metadata"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add lifecycle columns and backfill existing conversations."""
    # Add lifecycle_state with server_default so existing rows get 'active'
    op.add_column(
        "conversations",
        sa.Column(
            "lifecycle_state",
            sa.String(20),
            nullable=False,
            server_default="active",
        ),
    )
    op.add_column(
        "conversations",
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "conversations",
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # Index for filtering by lifecycle state (sidebar queries)
    op.create_index(
        "idx_conversations_lifecycle_state",
        "conversations",
        ["lifecycle_state"],
    )


def downgrade() -> None:
    """Remove lifecycle columns from conversations table."""
    op.drop_index("idx_conversations_lifecycle_state", table_name="conversations")
    op.drop_column("conversations", "deleted_at")
    op.drop_column("conversations", "archived_at")
    op.drop_column("conversations", "lifecycle_state")
