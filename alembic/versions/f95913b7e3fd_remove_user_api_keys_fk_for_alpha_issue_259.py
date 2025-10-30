"""remove_user_api_keys_fk_for_alpha_issue_259

Revision ID: f95913b7e3fd
Revises: 648730a3238d
Create Date: 2025-10-30 11:35:01.318722

Issue #259: Alpha/Production Data Separation

Removes foreign key constraint from user_api_keys.user_id to users.id
to support alpha users (UUID) in addition to production users (String).

The column remains (nullable=False, indexed) for referential integrity,
but without DB-level FK constraint to allow both alpha_users and users tables.
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f95913b7e3fd"
down_revision: Union[str, Sequence[str], None] = "648730a3238d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Drop FK constraint from user_api_keys.user_id."""
    # Drop the foreign key constraint
    op.drop_constraint("user_api_keys_user_id_fkey", "user_api_keys", type_="foreignkey")


def downgrade() -> None:
    """Re-create FK constraint from user_api_keys.user_id."""
    # Re-create the foreign key constraint
    op.create_foreign_key(
        "user_api_keys_user_id_fkey", "user_api_keys", "users", ["user_id"], ["id"]
    )
