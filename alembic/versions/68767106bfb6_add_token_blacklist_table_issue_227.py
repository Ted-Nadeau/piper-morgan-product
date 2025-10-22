"""add_token_blacklist_table_issue_227

Revision ID: 68767106bfb6
Revises: f3a951d71200
Create Date: 2025-10-21 16:48:59.539338

Creates the token_blacklist table for JWT token revocation (Issue #227 CORE-USERS-JWT).
This table serves as database fallback when Redis is unavailable. Redis is primary storage
with TTL auto-expiration; this table requires periodic cleanup via background job.
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "68767106bfb6"
down_revision: Union[str, Sequence[str], None] = "f3a951d71200"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: Create token_blacklist table with strategic indexes."""

    # Create token_blacklist table
    op.create_table(
        "token_blacklist",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("token_id", sa.String(length=255), nullable=False),
        sa.Column("user_id", sa.String(length=255), nullable=True),
        sa.Column("reason", sa.String(length=50), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create strategic indexes for performance
    # 1. Unique index on token_id for fast blacklist lookups (most critical)
    op.create_index("idx_token_blacklist_token_id", "token_blacklist", ["token_id"], unique=True)

    # 2. Index on expires_at for cleanup job efficiency
    op.create_index("idx_token_blacklist_expires", "token_blacklist", ["expires_at"], unique=False)

    # 3. Index on user_id for user-specific queries
    op.create_index("idx_token_blacklist_user_id", "token_blacklist", ["user_id"], unique=False)

    # 4. Composite index on user_id + expires_at for user token cleanup
    op.create_index(
        "idx_token_blacklist_user_expires",
        "token_blacklist",
        ["user_id", "expires_at"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema: Drop token_blacklist table and indexes."""

    # Drop indexes first
    op.drop_index("idx_token_blacklist_user_expires", table_name="token_blacklist")
    op.drop_index("idx_token_blacklist_user_id", table_name="token_blacklist")
    op.drop_index("idx_token_blacklist_expires", table_name="token_blacklist")
    op.drop_index("idx_token_blacklist_token_id", table_name="token_blacklist")

    # Drop table
    op.drop_table("token_blacklist")
