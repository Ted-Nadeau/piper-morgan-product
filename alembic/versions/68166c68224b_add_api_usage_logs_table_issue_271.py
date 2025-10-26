"""add_api_usage_logs_table_issue_271

Revision ID: 68166c68224b
Revises: af770c5854fe
Create Date: 2025-10-25 17:48:51.512348

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "68166c68224b"
down_revision: Union[str, Sequence[str], None] = "af770c5854fe"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema.

    Issue #271: CORE-KEYS-COST-TRACKING

    Create api_usage_logs table to track all API calls, token consumption,
    and estimated costs across LLM providers.
    """
    op.create_table(
        "api_usage_logs",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.String(255), nullable=False, index=True),
        sa.Column("provider", sa.String(50), nullable=False, index=True),
        sa.Column("model", sa.String(100), nullable=False, index=True),
        # Token usage
        sa.Column("prompt_tokens", sa.Integer, nullable=False, server_default="0"),
        sa.Column("completion_tokens", sa.Integer, nullable=False, server_default="0"),
        sa.Column("total_tokens", sa.Integer, nullable=False, server_default="0"),
        # Cost information
        sa.Column("estimated_cost", sa.DECIMAL(10, 6), nullable=False, server_default="0.0"),
        # Context
        sa.Column("conversation_id", sa.String(255), index=True),
        sa.Column("feature", sa.String(100), server_default="chat"),
        # Metadata
        sa.Column("request_id", sa.String(255), index=True),
        sa.Column("response_time_ms", sa.Integer),
        sa.Column(
            "created_at",
            sa.TIMESTAMP,
            nullable=False,
            server_default=sa.func.current_timestamp(),
            index=True,
        ),
    )

    # Composite indexes for efficient queries
    op.create_index("idx_api_usage_logs_user_created", "api_usage_logs", ["user_id", "created_at"])
    op.create_index(
        "idx_api_usage_logs_provider_created",
        "api_usage_logs",
        ["provider", "created_at"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("api_usage_logs")
