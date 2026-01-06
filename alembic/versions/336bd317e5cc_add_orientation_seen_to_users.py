"""Add orientation_seen to users

Revision ID: 336bd317e5cc
Revises: 44f5cd40b495
Create Date: 2026-01-06 12:33:04.041358

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "336bd317e5cc"
down_revision: Union[str, Sequence[str], None] = "44f5cd40b495"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema.

    Add orientation_seen column to users table for Issue #549.
    Tracks whether user has seen post-setup orientation modal.
    """
    op.add_column(
        "users", sa.Column("orientation_seen", sa.Boolean(), nullable=False, server_default="false")
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "orientation_seen")
