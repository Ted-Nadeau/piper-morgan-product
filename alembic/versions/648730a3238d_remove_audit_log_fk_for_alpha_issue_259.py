"""remove_audit_log_fk_for_alpha_issue_259

Revision ID: 648730a3238d
Revises: 68166c68224b
Create Date: 2025-10-30 07:51:10.213005

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "648730a3238d"
down_revision: Union[str, Sequence[str], None] = "68166c68224b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Remove FK constraint from audit_logs.user_id to support alpha_users (UUID) during alpha phase.

    Issue #259 - Alpha/production data separation

    The audit_logs.user_id column will remain nullable and indexed, but the foreign key
    constraint to users.id is removed to allow alpha_users (UUID primary keys) to be
    logged without FK violations.

    This will be re-added post-alpha when alpha users migrate to production users table.
    """
    # Drop FK constraint (keep column, keep index)
    op.drop_constraint("audit_logs_user_id_fkey", "audit_logs", type_="foreignkey")


def downgrade() -> None:
    """Re-add FK constraint from audit_logs.user_id to users.id"""
    # Re-add FK constraint
    op.create_foreign_key("audit_logs_user_id_fkey", "audit_logs", "users", ["user_id"], ["id"])
