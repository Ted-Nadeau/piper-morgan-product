"""create repositories and project_repository_links tables issue 866

Revision ID: a866_repo_entity
Revises: d73b3722eb03
Create Date: 2026-02-26

Issue #866: Repository as first-class domain entity with M2M Project relationship.
Creates two new tables:
  - repositories: Independent, provider-agnostic code repository entities
  - project_repository_links: Many-to-many join table for Project <-> Repository
"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "a866_repo_entity"
down_revision: Union[str, Sequence[str], None] = "d73b3722eb03"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create repositories and project_repository_links tables."""
    # 1. Create repositories table
    op.create_table(
        "repositories",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("owner_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("provider", sa.String(50), nullable=False, server_default="github"),
        sa.Column("full_name", sa.String(), nullable=False),
        sa.Column("display_name", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.UniqueConstraint(
            "owner_id",
            "provider",
            "full_name",
            name="uq_repositories_owner_provider_fullname",
        ),
    )
    op.create_index("idx_repositories_owner_id", "repositories", ["owner_id"])
    op.create_index("idx_repositories_full_name", "repositories", ["full_name"])

    # 2. Create project_repository_links table
    op.create_table(
        "project_repository_links",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("project_id", sa.String(), nullable=False),
        sa.Column("repository_id", sa.String(), nullable=False),
        sa.Column("is_primary", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("linked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("linked_by", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"]),
        sa.UniqueConstraint(
            "project_id",
            "repository_id",
            name="uq_project_repo_link",
        ),
    )
    op.create_index("idx_project_repo_links_project_id", "project_repository_links", ["project_id"])
    op.create_index(
        "idx_project_repo_links_repository_id", "project_repository_links", ["repository_id"]
    )


def downgrade() -> None:
    """Drop project_repository_links and repositories tables."""
    op.drop_table("project_repository_links")
    op.drop_table("repositories")
