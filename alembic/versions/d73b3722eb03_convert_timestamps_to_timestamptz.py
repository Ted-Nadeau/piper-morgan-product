"""convert_timestamps_to_timestamptz

Revision ID: d73b3722eb03
Revises: 3c85fd899ece
Create Date: 2026-02-03 12:37:05.301179

Issue #771: Fix schema drift where SQLAlchemy models declare DateTime(timezone=True)
but actual PostgreSQL columns are 'timestamp without time zone'.

This migration converts all timestamp columns to timestamptz, interpreting
existing naive timestamps as UTC (which they are, since we use UTC everywhere).

After this migration, code can use timezone-aware datetimes consistently.
"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d73b3722eb03"
down_revision: Union[str, Sequence[str], None] = "3c85fd899ece"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# All columns that need conversion (from audit query)
# Format: (table_name, column_name)
COLUMNS_TO_CONVERT = [
    ("action_humanizations", "created_at"),
    ("action_humanizations", "last_used"),
    ("api_usage_logs", "created_at"),
    ("audit_logs", "created_at"),
    ("audit_logs", "updated_at"),
    ("conversation_links", "created_at"),
    ("conversation_turns", "completed_at"),
    ("conversation_turns", "created_at"),
    ("conversations", "created_at"),
    ("conversations", "last_activity_at"),
    ("conversations", "updated_at"),
    ("features", "created_at"),
    ("features", "updated_at"),
    ("feedback", "created_at"),
    ("feedback", "updated_at"),
    ("intents", "created_at"),
    ("items", "created_at"),
    ("items", "updated_at"),
    ("knowledge_edges", "created_at"),
    ("knowledge_edges", "updated_at"),
    ("knowledge_nodes", "created_at"),
    ("knowledge_nodes", "updated_at"),
    ("learned_patterns", "created_at"),
    ("learned_patterns", "last_used_at"),
    ("learned_patterns", "updated_at"),
    ("learning_settings", "created_at"),
    ("learning_settings", "updated_at"),
    ("list_items", "added_at"),
    ("list_items", "list_due_date"),
    ("list_memberships", "added_at"),
    ("list_memberships", "list_due_date"),
    ("lists", "created_at"),
    ("lists", "updated_at"),
    ("personality_profiles", "created_at"),
    ("personality_profiles", "updated_at"),
    ("products", "created_at"),
    ("products", "updated_at"),
    ("project_integrations", "created_at"),
    ("projects", "created_at"),
    ("projects", "updated_at"),
    ("stakeholders", "created_at"),
    ("tasks", "completed_at"),
    ("tasks", "created_at"),
    ("tasks", "started_at"),
    ("tasks", "updated_at"),
    ("todo_items", "completed_at"),
    ("todo_items", "due_date"),
    ("todo_items", "reminder_date"),
    ("todo_items", "scheduled_date"),
    ("todo_lists", "created_at"),
    ("todo_lists", "updated_at"),
    ("token_blacklist", "created_at"),
    ("token_blacklist", "expires_at"),
    ("uploaded_files", "last_referenced"),
    ("uploaded_files", "upload_time"),
    ("user_api_keys", "created_at"),
    ("user_api_keys", "last_validated_at"),
    ("user_api_keys", "rotated_at"),
    ("user_api_keys", "updated_at"),
    ("user_trust_profiles", "created_at"),
    ("user_trust_profiles", "last_interaction_at"),
    ("user_trust_profiles", "last_stage_change_at"),
    ("user_trust_profiles", "updated_at"),
    ("users", "created_at"),
    ("users", "last_login_at"),
    ("users", "setup_completed_at"),
    ("users", "updated_at"),
    ("work_items", "created_at"),
    ("work_items", "updated_at"),
    ("workflows", "completed_at"),
    ("workflows", "created_at"),
    ("workflows", "started_at"),
    ("workflows", "updated_at"),
]


def upgrade() -> None:
    """Convert all timestamp columns to timestamptz.

    Existing naive timestamps are interpreted as UTC, which is correct
    since all our code uses UTC for database operations.
    """
    for table_name, column_name in COLUMNS_TO_CONVERT:
        op.execute(
            f"""
            ALTER TABLE {table_name}
            ALTER COLUMN {column_name} TYPE TIMESTAMPTZ
            USING {column_name} AT TIME ZONE 'UTC'
        """
        )


def downgrade() -> None:
    """Convert timestamptz columns back to timestamp without time zone.

    This preserves the UTC values as naive timestamps.
    """
    for table_name, column_name in COLUMNS_TO_CONVERT:
        op.execute(
            f"""
            ALTER TABLE {table_name}
            ALTER COLUMN {column_name} TYPE TIMESTAMP
            USING {column_name} AT TIME ZONE 'UTC'
        """
        )
