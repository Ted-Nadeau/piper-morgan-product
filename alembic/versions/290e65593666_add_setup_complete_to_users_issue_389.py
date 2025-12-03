"""add_setup_complete_to_users_issue_389

Revision ID: 290e65593666
Revises: cd320b81e4c6
Create Date: 2025-12-01 20:39:10.817624

Issue #389: Add explicit setup_complete flag for state tracking
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "290e65593666"
down_revision: Union[str, Sequence[str], None] = "cd320b81e4c6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add setup_complete and setup_completed_at columns to users table."""
    # Add setup_complete boolean flag (default False for existing users)
    op.add_column(
        "users", sa.Column("setup_complete", sa.Boolean(), nullable=False, server_default="false")
    )
    # Add setup_completed_at timestamp (when setup was completed)
    op.add_column("users", sa.Column("setup_completed_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    """Remove setup_complete and setup_completed_at columns from users table."""
    op.drop_column("users", "setup_completed_at")
    op.drop_column("users", "setup_complete")
