"""
Add EXTRACT_WORK_ITEM to tasktype enum

Revision ID: 11b3e791dad1
Revises: 31937a4b9327
Create Date: 2025-07-09 19:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '11b3e791dad1'
down_revision = '31937a4b9327'
branch_labels = None
depends_on = None

def upgrade():
    # Add new value to the PostgreSQL enum type (uppercase, to match existing values)
    op.execute("""
        ALTER TYPE tasktype ADD VALUE IF NOT EXISTS 'EXTRACT_WORK_ITEM';
    """)

def downgrade():
    # Downgrade is tricky for enums in PostgreSQL; safest is to recreate the enum without the value
    # 1. Rename the old enum
    op.execute("ALTER TYPE tasktype RENAME TO tasktype_old;")
    # 2. Create the new enum without the value
    op.execute("""
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
            'JIRA_CREATE_TICKET',
            'SLACK_SEND_MESSAGE',
            'PROCESS_USER_FEEDBACK'
        );
    """)
    # 3. Alter the column to use the new type
    op.execute("ALTER TABLE tasks ALTER COLUMN type TYPE tasktype USING type::text::tasktype;")
    # 4. Drop the old enum
    op.execute("DROP TYPE tasktype_old;")
