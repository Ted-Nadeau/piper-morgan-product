"""Add project_ids to lists table for many-to-many List-Project association

Revision ID: e90b452fe6ff
Revises: 601_phase0_graph
Create Date: 2026-01-22

L1 Sprint #477: List ↔ Project many-to-many association
"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e90b452fe6ff"
down_revision: Union[str, None] = "601_phase0_graph"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add project_ids column to lists table
    op.add_column(
        "lists",
        sa.Column("project_ids", postgresql.JSONB(), nullable=True, server_default="[]"),
    )

    # Add GIN index for efficient project_ids queries
    op.create_index(
        "idx_lists_projects",
        "lists",
        ["project_ids"],
        unique=False,
        postgresql_using="gin",
    )


def downgrade() -> None:
    # Remove index first
    op.drop_index("idx_lists_projects", table_name="lists", postgresql_using="gin")

    # Remove column
    op.drop_column("lists", "project_ids")
