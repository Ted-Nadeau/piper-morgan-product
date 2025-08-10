"""Add feedback table for PM-005 feedback tracking implementation

Revision ID: 9ff35c63fe33
Revises: a9ee08bbdf8c
Create Date: 2025-08-09 12:28:49.582005

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9ff35c63fe33"
down_revision: Union[str, Sequence[str], None] = "a9ee08bbdf8c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Create feedback table
    op.create_table(
        "feedback",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("session_id", sa.String(), nullable=False),
        sa.Column("feedback_type", sa.String(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=True),
        sa.Column("comment", sa.Text(), nullable=False),
        sa.Column("context", postgresql.JSONB(), nullable=True),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.Column("conversation_context", postgresql.JSONB(), nullable=True),
        sa.Column("source", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("priority", sa.String(), nullable=True),
        sa.Column("sentiment_score", sa.Float(), nullable=True),
        sa.Column("categories", postgresql.JSONB(), nullable=True),
        sa.Column("tags", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create indexes for performance
    op.create_index("idx_feedback_session_id", "feedback", ["session_id"])
    op.create_index("idx_feedback_type", "feedback", ["feedback_type"])
    op.create_index("idx_feedback_rating", "feedback", ["rating"])
    op.create_index("idx_feedback_status", "feedback", ["status"])
    op.create_index("idx_feedback_created_at", "feedback", ["created_at"])
    op.create_index("idx_feedback_user_id", "feedback", ["user_id"])
    op.create_index("idx_feedback_source", "feedback", ["source"])


def downgrade() -> None:
    """Downgrade schema."""

    # Drop indexes
    op.drop_index("idx_feedback_source", "feedback")
    op.drop_index("idx_feedback_user_id", "feedback")
    op.drop_index("idx_feedback_created_at", "feedback")
    op.drop_index("idx_feedback_status", "feedback")
    op.drop_index("idx_feedback_rating", "feedback")
    op.drop_index("idx_feedback_type", "feedback")
    op.drop_index("idx_feedback_session_id", "feedback")

    # Drop table
    op.drop_table("feedback")
