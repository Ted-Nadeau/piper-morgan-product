"""Add personality_profiles table for PM-155

Revision ID: f3a951d71200
Revises: 9ff35c63fe33
Create Date: 2025-09-11 13:49:37.570055

Creates the personality_profiles table for user personality preferences.
Includes proper indexes for performance and populates default profiles.
"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f3a951d71200"
down_revision: Union[str, Sequence[str], None] = "9ff35c63fe33"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Create personality_profiles table
    op.create_table(
        "personality_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", sa.String(255), nullable=False),
        sa.Column("warmth_level", sa.Float(), nullable=False, server_default="0.6"),
        sa.Column("confidence_style", sa.String(50), nullable=False, server_default="contextual"),
        sa.Column("action_orientation", sa.String(50), nullable=False, server_default="medium"),
        sa.Column("technical_depth", sa.String(50), nullable=False, server_default="balanced"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create strategic indexes for performance
    op.create_index(
        "idx_personality_profiles_user_id", "personality_profiles", ["user_id"], unique=True
    )
    op.create_index(
        "idx_personality_profiles_active", "personality_profiles", ["is_active"], unique=False
    )
    op.create_index(
        "idx_personality_profiles_user_active",
        "personality_profiles",
        ["user_id", "is_active"],
        unique=False,
    )
    op.create_index(
        "idx_personality_profiles_warmth", "personality_profiles", ["warmth_level"], unique=False
    )
    op.create_index(
        "idx_personality_profiles_confidence",
        "personality_profiles",
        ["confidence_style"],
        unique=False,
    )
    op.create_index(
        "idx_personality_profiles_action",
        "personality_profiles",
        ["action_orientation"],
        unique=False,
    )
    op.create_index(
        "idx_personality_profiles_technical",
        "personality_profiles",
        ["technical_depth"],
        unique=False,
    )

    # Populate default profiles for existing users
    # Note: Since this project uses string user_ids without a users table,
    # we'll create a mechanism to populate defaults when users are first encountered
    # The repository layer will handle creating default profiles on first access

    # Create a default system profile for fallback scenarios
    op.execute(
        """
        INSERT INTO personality_profiles (
            id, user_id, warmth_level, confidence_style, action_orientation,
            technical_depth, created_at, updated_at, is_active
        ) VALUES (
            gen_random_uuid(),
            'system_default',
            0.6,
            'contextual',
            'medium',
            'balanced',
            NOW(),
            NOW(),
            true
        )
        """
    )


def downgrade() -> None:
    """Downgrade schema."""

    # Drop indexes
    op.drop_index("idx_personality_profiles_technical", table_name="personality_profiles")
    op.drop_index("idx_personality_profiles_action", table_name="personality_profiles")
    op.drop_index("idx_personality_profiles_confidence", table_name="personality_profiles")
    op.drop_index("idx_personality_profiles_warmth", table_name="personality_profiles")
    op.drop_index("idx_personality_profiles_user_active", table_name="personality_profiles")
    op.drop_index("idx_personality_profiles_active", table_name="personality_profiles")
    op.drop_index("idx_personality_profiles_user_id", table_name="personality_profiles")

    # Drop table
    op.drop_table("personality_profiles")
