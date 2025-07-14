"""add_summarize_to_tasktype_enum

Revision ID: 96a50c4771aa
Revises: d685380d5c5f
Create Date: 2025-07-12 17:11:24.369405

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "96a50c4771aa"
down_revision: Union[str, Sequence[str], None] = "d685380d5c5f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add new value to the PostgreSQL enum type (uppercase, to match existing values)
    op.execute(
        """
        ALTER TYPE tasktype ADD VALUE IF NOT EXISTS 'SUMMARIZE';
    """
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Downgrade is tricky for enums in PostgreSQL; safest is to recreate the enum without the value
    # 1. Rename the old enum
    op.execute("ALTER TYPE tasktype RENAME TO tasktype_old;")
    # 2. Create the new enum without the SUMMARIZE value
    op.execute(
        """
        CREATE TYPE tasktype AS ENUM (
            'ANALYZE_REQUEST',
            'EXTRACT_REQUIREMENTS',
            'IDENTIFY_DEPENDENCIES',
            'CREATE_WORK_ITEM',
            'UPDATE_WORK_ITEM',
            'NOTIFY_STAKEHOLDERS',
            'GENERATE_DOCUMENT',
            'CREATE_SUMMARY',
            'GITHUB_CREATE_ISSUE',
            'ANALYZE_GITHUB_ISSUE',
            'ANALYZE_FILE',
            'EXTRACT_WORK_ITEM',
            'JIRA_CREATE_TICKET',
            'SLACK_SEND_MESSAGE',
            'PROCESS_USER_FEEDBACK'
        );
    """
    )
    # 3. Alter the column to use the new type
    op.execute("ALTER TABLE tasks ALTER COLUMN type TYPE tasktype USING type::text::tasktype;")
    # 4. Drop the old enum
    op.execute("DROP TYPE tasktype_old;")
