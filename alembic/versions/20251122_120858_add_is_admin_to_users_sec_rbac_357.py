"""Add is_admin column to users table (SEC-RBAC Phase 3)

Revision ID: 20251122_120858
Revises: 20251122_upgrade_shared_with_to_roles
Create Date: 2025-11-22 12:08:58.000000

SEC-RBAC Phase 3: System-Wide Admin Role
Issue: #357 (SEC-RBAC: Implement RBAC)
ADR: ADR-044 (Lightweight RBAC)

Purpose:
- Add is_admin column to users table to support system-wide admin bypass
- Set PM user (xian) as admin
- Create index for admin queries
- Allow admins to access any resource (support team needs this)

Implementation:
- Adds is_admin boolean column with default False
- Creates index ix_users_is_admin for efficient admin queries
- Sets user with email xian@example.com as admin (conservative: single PM is admin)
- Includes rollback capability
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic
revision = "20251122_120858"
down_revision = "20251122_upgrade_shared_with"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add is_admin column to users table"""

    # Add is_admin column to users table
    op.add_column(
        "users", sa.Column("is_admin", sa.Boolean(), server_default="false", nullable=False)
    )

    # Create index for efficient admin filtering
    op.create_index("ix_users_is_admin", "users", ["is_admin"])

    # Set PM user (xian) as admin - conservative approach, only one admin initially
    # This allows the PM to access any user's resources for support/debugging
    op.execute(
        """
        UPDATE users
        SET is_admin = true
        WHERE email = 'xian@example.com'
        LIMIT 1
    """
    )


def downgrade() -> None:
    """Remove is_admin column from users table"""

    # Drop index
    op.drop_index("ix_users_is_admin", table_name="users")

    # Drop column
    op.drop_column("users", "is_admin")
