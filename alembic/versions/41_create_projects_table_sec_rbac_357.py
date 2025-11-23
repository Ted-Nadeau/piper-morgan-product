"""Create projects table for PM-034 project management

Revision ID: 41000fc95f25017
Revises: 40fc95f25017
Create Date: 2025-11-22 16:30:00.000000

This migration creates the projects table that should have existed before
todo_items references it via foreign key constraint in migration 234aa8ec628c.

ProjectDB model defines the schema with owner_id, name, description, shared_with, etc.
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "41000fc95f25017"
down_revision: Union[str, Sequence[str], None] = "40fc95f25017"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create projects table with schema matching ProjectDB model."""

    # Create projects table
    op.create_table(
        "projects",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("owner_id", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=False, unique=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("shared_with", sa.JSON(), nullable=True, server_default="[]"),
        sa.Column("is_default", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_archived", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.PrimaryKeyConstraint("id", name="pk_projects"),
    )

    # Create indexes for common queries
    op.create_index("idx_projects_owner_id", "projects", ["owner_id"])
    op.create_index("idx_projects_name", "projects", ["name"])
    op.create_index("idx_projects_is_archived", "projects", ["is_archived"])
    op.create_index(
        "idx_projects_owner_archived",
        "projects",
        ["owner_id", "is_archived"],
        postgresql_where=sa.text("is_archived = false"),
    )

    print("✅ Projects table created successfully")


def downgrade() -> None:
    """Drop projects table and indexes."""

    # Drop indexes
    op.drop_index("idx_projects_owner_archived", "projects")
    op.drop_index("idx_projects_is_archived", "projects")
    op.drop_index("idx_projects_name", "projects")
    op.drop_index("idx_projects_owner_id", "projects")

    # Drop table
    op.drop_table("projects")

    print("✅ Projects table dropped")
