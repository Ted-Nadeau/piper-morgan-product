"""create work_items table issue 796

Revision ID: 4ba89dbf5347
Revises: 4bd02594d62d
Create Date: 2026-02-11 13:45:00.000000

Creates the work_items table which was missing from the migration chain.
The WorkItem model existed in services/database/models.py but was never
migrated - it was created via Base.metadata.create_all() during early
development.

This migration is inserted before 70847a6596f3 which tries to ALTER
the work_items table to add lifecycle_state column.

Note: lifecycle_state column is NOT included here - it will be added
by migration 70847a6596f3 which follows this one.
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4ba89dbf5347"
down_revision: Union[str, Sequence[str], None] = "4bd02594d62d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create work_items table."""
    op.create_table(
        "work_items",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("product_id", sa.String(), nullable=True),
        sa.Column("feature_id", sa.String(), nullable=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("type", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("priority", sa.String(), nullable=True),
        sa.Column("labels", sa.JSON(), nullable=True),
        sa.Column("assignee", sa.String(), nullable=True),
        sa.Column("project_id", sa.String(), nullable=True),
        sa.Column("source_system", sa.String(), nullable=True),
        sa.Column("external_id", sa.String(), nullable=True),
        sa.Column("external_url", sa.String(), nullable=True),
        sa.Column("item_metadata", sa.JSON(), nullable=True),
        sa.Column("external_refs", sa.JSON(), nullable=True),
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
        sa.ForeignKeyConstraint(
            ["feature_id"],
            ["features.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Drop work_items table."""
    op.drop_table("work_items")
