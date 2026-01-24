"""add_conversational_memory_entries

Revision ID: 80ce53cc1267
Revises: cf1c67547f87
Create Date: 2026-01-23 22:54:16.497369

Part of #657 MEM-ADR054-P1.
Creates table for ADR-054 Layer 1 (24-hour conversational memory).
"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "80ce53cc1267"
down_revision: Union[str, Sequence[str], None] = "cf1c67547f87"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create conversational_memory_entries table for ADR-054 Layer 1."""
    op.create_table(
        "conversational_memory_entries",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("conversation_id", sa.String(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("topic_summary", sa.String(500), nullable=False),
        sa.Column("entities_mentioned", postgresql.JSONB(), server_default="[]"),
        sa.Column("outcome", sa.String(500), nullable=True),
        sa.Column("user_sentiment", sa.String(20), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["conversation_id"], ["conversations.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_cme_user_id", "conversational_memory_entries", ["user_id"])
    op.create_index(
        "idx_cme_user_timestamp", "conversational_memory_entries", ["user_id", "timestamp"]
    )


def downgrade() -> None:
    """Drop conversational_memory_entries table."""
    op.drop_index("idx_cme_user_timestamp", table_name="conversational_memory_entries")
    op.drop_index("idx_cme_user_id", table_name="conversational_memory_entries")
    op.drop_table("conversational_memory_entries")
