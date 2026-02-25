"""create features table issue 796

Revision ID: 4bd02594d62d
Revises: f5b173cbab46
Create Date: 2026-02-11 13:31:00.000000

Creates the features table which was missing from the migration chain.
The Feature model existed in services/database/models.py but was never
migrated - it was created via Base.metadata.create_all() during early
development.

This migration is inserted before 70847a6596f3 which tries to ALTER
the features table to add lifecycle_state column.

Note: lifecycle_state column is NOT included here - it will be added
by migration 70847a6596f3 which follows this one.
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4bd02594d62d"
down_revision: Union[str, Sequence[str], None] = "f5b173cbab46"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create features table."""
    op.create_table(
        "features",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("product_id", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("hypothesis", sa.Text(), nullable=True),
        sa.Column("acceptance_criteria", sa.JSON(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Drop features table."""
    op.drop_table("features")
