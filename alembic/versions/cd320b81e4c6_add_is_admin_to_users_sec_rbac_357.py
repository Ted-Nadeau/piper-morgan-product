"""add_is_admin_to_users_sec_rbac_357

Revision ID: cd320b81e4c6
Revises: 056977b6ec4c
Create Date: 2025-11-23 20:58:22.769079

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd320b81e4c6'
down_revision: Union[str, Sequence[str], None] = '056977b6ec4c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add is_admin column to users table for SEC-RBAC admin bypass pattern (Issue #357)."""
    # Add is_admin column (default False for existing users)
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=False, server_default='false'))

    # Set xian@example.com as admin (if exists)
    op.execute(
        """
        UPDATE users
        SET is_admin = true
        WHERE email = 'xian@example.com'
        """
    )


def downgrade() -> None:
    """Remove is_admin column from users table."""
    op.drop_column('users', 'is_admin')
