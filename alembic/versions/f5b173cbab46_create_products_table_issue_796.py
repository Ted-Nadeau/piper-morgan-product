"""create products table issue 796

Revision ID: f5b173cbab46
Revises: 80ce53cc1267
Create Date: 2026-02-11 13:30:00.000000

Creates the products table which was missing from the migration chain.
The Product model existed in services/database/models.py but was never
migrated - it was created via Base.metadata.create_all() during early
development.

This migration is inserted before 70847a6596f3 which tries to ALTER
the features table (which has a FK to products).
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f5b173cbab46"
down_revision: Union[str, Sequence[str], None] = "80ce53cc1267"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create products table."""
    op.create_table(
        "products",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("vision", sa.Text(), nullable=True),
        sa.Column("strategy", sa.Text(), nullable=True),
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
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Drop products table."""
    op.drop_table("products")
