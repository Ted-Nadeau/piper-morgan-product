"""fix_projects_unique_constraint_736

Revision ID: 3c85fd899ece
Revises: 70847a6596f3
Create Date: 2026-01-29 08:38:27.884240

Fix: Change projects table unique constraint from `name` alone to composite
`(owner_id, name)` for proper multi-tenancy support.

This allows different users to have projects with the same name while still
preventing duplicate project names within a single user's project list.
"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3c85fd899ece"
down_revision: Union[str, Sequence[str], None] = "70847a6596f3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Change unique constraint from name-only to (owner_id, name) composite."""
    # Drop the existing unique constraint on name alone
    op.drop_constraint("projects_name_key", "projects", type_="unique")

    # Create new composite unique constraint on (owner_id, name)
    op.create_unique_constraint("uq_projects_owner_name", "projects", ["owner_id", "name"])

    print("Changed projects unique constraint from name-only to (owner_id, name)")


def downgrade() -> None:
    """Revert to name-only unique constraint."""
    # Drop the composite unique constraint
    op.drop_constraint("uq_projects_owner_name", "projects", type_="unique")

    # Restore the original name-only unique constraint
    op.create_unique_constraint("projects_name_key", "projects", ["name"])

    print("Reverted projects unique constraint to name-only")
