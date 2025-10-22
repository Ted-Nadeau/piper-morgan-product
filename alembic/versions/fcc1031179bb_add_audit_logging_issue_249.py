"""add_audit_logging_issue_249

Revision ID: fcc1031179bb
Revises: 8d46e93aabc3
Create Date: 2025-10-22 09:41:13.172402

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "fcc1031179bb"
down_revision: Union[str, Sequence[str], None] = "8d46e93aabc3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create audit_logs table with comprehensive indexing for Issue #249"""

    # Create audit_logs table
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.String(length=255), nullable=False),
        sa.Column("user_id", sa.String(length=255), nullable=True),
        sa.Column("session_id", sa.String(length=255), nullable=True),
        sa.Column("event_type", sa.String(length=50), nullable=False),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("resource_type", sa.String(length=50), nullable=True),
        sa.Column("resource_id", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("details", sa.JSON(), nullable=True),
        sa.Column("ip_address", sa.String(length=45), nullable=True),
        sa.Column("user_agent", sa.String(length=500), nullable=True),
        sa.Column("request_id", sa.String(length=255), nullable=True),
        sa.Column("request_path", sa.String(length=500), nullable=True),
        sa.Column("old_value", sa.JSON(), nullable=True),
        sa.Column("new_value", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create strategic indexes for query performance
    op.create_index("idx_audit_user_date", "audit_logs", ["user_id", "created_at"])
    op.create_index("idx_audit_event_type", "audit_logs", ["event_type"])
    op.create_index("idx_audit_action", "audit_logs", ["action"])
    op.create_index("idx_audit_resource", "audit_logs", ["resource_type", "resource_id"])
    op.create_index("idx_audit_severity", "audit_logs", ["severity"])
    op.create_index("idx_audit_status", "audit_logs", ["status"])
    op.create_index("idx_audit_ip", "audit_logs", ["ip_address"])
    op.create_index("idx_audit_session", "audit_logs", ["session_id"])
    op.create_index("idx_audit_request", "audit_logs", ["request_id"])


def downgrade() -> None:
    """Drop audit_logs table and indexes"""

    # Drop indexes (must happen before dropping table)
    op.drop_index("idx_audit_request", table_name="audit_logs")
    op.drop_index("idx_audit_session", table_name="audit_logs")
    op.drop_index("idx_audit_ip", table_name="audit_logs")
    op.drop_index("idx_audit_status", table_name="audit_logs")
    op.drop_index("idx_audit_severity", table_name="audit_logs")
    op.drop_index("idx_audit_resource", table_name="audit_logs")
    op.drop_index("idx_audit_action", table_name="audit_logs")
    op.drop_index("idx_audit_event_type", table_name="audit_logs")
    op.drop_index("idx_audit_user_date", table_name="audit_logs")

    # Drop table
    op.drop_table("audit_logs")
