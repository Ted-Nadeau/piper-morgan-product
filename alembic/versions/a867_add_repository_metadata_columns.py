"""add metadata columns to repositories table issue 867

Revision ID: a867_repo_metadata
Revises: a866_repo_entity
Create Date: 2026-02-28

Issue #867: GitHub API repo validation — add metadata columns
for description, language, visibility, and default_branch.
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "a867_repo_metadata"
down_revision: Union[str, Sequence[str], None] = "a866_repo_entity"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add metadata columns to repositories table."""
    op.add_column("repositories", sa.Column("description", sa.String(), nullable=True))
    op.add_column("repositories", sa.Column("language", sa.String(100), nullable=True))
    op.add_column("repositories", sa.Column("visibility", sa.String(20), nullable=True))
    op.add_column("repositories", sa.Column("default_branch", sa.String(255), nullable=True))


def downgrade() -> None:
    """Remove metadata columns from repositories table."""
    op.drop_column("repositories", "default_branch")
    op.drop_column("repositories", "visibility")
    op.drop_column("repositories", "language")
    op.drop_column("repositories", "description")
