"""add_user_api_keys_table_issue_228

Revision ID: 8d46e93aabc3
Revises: 6d503d8783d2
Create Date: 2025-10-22 07:28:20.676253

Create user_api_keys table for multi-user API key isolation.

Issue #228 CORE-USERS-API Phase 1B
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8d46e93aabc3"
down_revision: Union[str, Sequence[str], None] = "6d503d8783d2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Create user_api_keys table for per-user API key storage.

    Table stores metadata; actual keys stored in OS keychain.
    """

    # Create user_api_keys table
    op.create_table(
        "user_api_keys",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.String(255), nullable=False),
        sa.Column("provider", sa.String(50), nullable=False),
        sa.Column("key_reference", sa.String(500), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("is_validated", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("last_validated_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("created_by", sa.String(255), nullable=True),
        sa.Column("previous_key_reference", sa.String(500), nullable=True),
        sa.Column("rotated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )

    # Create unique constraint on (user_id, provider)
    op.create_unique_constraint("uq_user_provider", "user_api_keys", ["user_id", "provider"])

    # Create indexes
    op.create_index("idx_user_api_keys_user_id", "user_api_keys", ["user_id"], unique=False)
    op.create_index("idx_user_api_keys_provider", "user_api_keys", ["provider"], unique=False)
    op.create_index("idx_user_api_keys_active", "user_api_keys", ["is_active"], unique=False)


def downgrade() -> None:
    """
    Remove user_api_keys table.
    """

    # Drop indexes
    op.drop_index("idx_user_api_keys_active", table_name="user_api_keys")
    op.drop_index("idx_user_api_keys_provider", table_name="user_api_keys")
    op.drop_index("idx_user_api_keys_user_id", table_name="user_api_keys")

    # Drop unique constraint
    op.drop_constraint("uq_user_provider", "user_api_keys", type_="unique")

    # Drop table
    op.drop_table("user_api_keys")
