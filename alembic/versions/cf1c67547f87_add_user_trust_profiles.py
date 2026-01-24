"""add_user_trust_profiles

Revision ID: cf1c67547f87
Revises: e90b452fe6ff
Create Date: 2026-01-23 09:58:13.629213

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "cf1c67547f87"
down_revision: Union[str, Sequence[str], None] = "e90b452fe6ff"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create user_trust_profiles table for #647 TRUST-LEVELS-1."""
    op.create_table(
        "user_trust_profiles",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("current_stage", sa.Integer(), nullable=False),
        sa.Column("highest_stage_achieved", sa.Integer(), nullable=False),
        sa.Column("successful_count", sa.Integer(), nullable=False),
        sa.Column("neutral_count", sa.Integer(), nullable=False),
        sa.Column("negative_count", sa.Integer(), nullable=False),
        sa.Column("consecutive_negative", sa.Integer(), nullable=False),
        sa.Column("recent_events", sa.JSON(), nullable=False),
        sa.Column("stage_history", sa.JSON(), nullable=False),
        sa.Column("last_interaction_at", sa.DateTime(), nullable=False),
        sa.Column("last_stage_change_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_user_trust_profiles_user_id"), "user_trust_profiles", ["user_id"], unique=True
    )


def downgrade() -> None:
    """Drop user_trust_profiles table."""
    op.drop_index(op.f("ix_user_trust_profiles_user_id"), table_name="user_trust_profiles")
    op.drop_table("user_trust_profiles")
