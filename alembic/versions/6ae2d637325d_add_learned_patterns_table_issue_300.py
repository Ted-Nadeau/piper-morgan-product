"""add_learned_patterns_table_issue_300

Add learned_patterns table for Basic Auto-Learning system.

This table stores user-specific patterns discovered through real-time learning.
Confidence increases with successful applications, decreases with failures.

Issue #300: CORE-ALPHA-LEARNING-BASIC - Foundation Stone #1

Revision ID: 6ae2d637325d
Revises: d8aeb665e878
Create Date: 2025-11-12 21:40:20.609750

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6ae2d637325d"
down_revision: Union[str, Sequence[str], None] = "d8aeb665e878"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Create learned_patterns table."""
    # Create pattern_type enum
    pattern_type_enum = postgresql.ENUM(
        "USER_WORKFLOW",
        "COMMAND_SEQUENCE",
        "TIME_BASED",
        "CONTEXT_BASED",
        "PREFERENCE",
        "INTEGRATION",
        name="patterntype",
        create_type=False,  # Will be created by sa.Enum
    )

    # Create learned_patterns table
    op.create_table(
        "learned_patterns",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "pattern_type",
            sa.Enum(
                "USER_WORKFLOW",
                "COMMAND_SEQUENCE",
                "TIME_BASED",
                "CONTEXT_BASED",
                "PREFERENCE",
                "INTEGRATION",
                name="patterntype",
            ),
            nullable=False,
        ),
        sa.Column("pattern_data", sa.JSON(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0.5"),
        sa.Column("usage_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("success_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("failure_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("last_used_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create indexes for performance
    op.create_index(
        "ix_learned_patterns_user_confidence", "learned_patterns", ["user_id", "confidence"]
    )
    op.create_index("ix_learned_patterns_user_enabled", "learned_patterns", ["user_id", "enabled"])
    op.create_index("ix_learned_patterns_user_id", "learned_patterns", ["user_id"])


def downgrade() -> None:
    """Downgrade schema - Drop learned_patterns table."""
    op.drop_index("ix_learned_patterns_user_id", table_name="learned_patterns")
    op.drop_index("ix_learned_patterns_user_enabled", table_name="learned_patterns")
    op.drop_index("ix_learned_patterns_user_confidence", table_name="learned_patterns")
    op.drop_table("learned_patterns")

    # Drop the enum type
    sa.Enum(name="patterntype").drop(op.get_bind(), checkfirst=True)
