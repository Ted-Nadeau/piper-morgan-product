"""Add Todo Management System tables for PM-081

Revision ID: ffns5hckf96d
Revises: 8e4f2a3b9c5d
Create Date: 2025-08-05 12:15:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ffns5hckf96d"
down_revision: Union[str, Sequence[str], None] = "8e4f2a3b9c5d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Create enums with idempotent checks (handle diamond dependencies)
    op.execute(
        """
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'todostatus') THEN
                CREATE TYPE todostatus AS ENUM (
                    'pending', 'in_progress', 'completed', 'cancelled', 'blocked'
                );
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'todopriority') THEN
                CREATE TYPE todopriority AS ENUM (
                    'low', 'medium', 'high', 'urgent'
                );
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'listtype') THEN
                CREATE TYPE listtype AS ENUM (
                    'personal', 'project', 'team', 'template', 'archive'
                );
            END IF;
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'orderingstrategy') THEN
                CREATE TYPE orderingstrategy AS ENUM (
                    'manual', 'priority', 'due_date', 'created_date', 'alphabetical', 'status'
                );
            END IF;
        END
        $$;
    """
    )

    # Create todo_lists table
    op.create_table(
        "todo_lists",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("list_type", sa.String(), nullable=False),
        sa.Column("ordering_strategy", sa.String(), nullable=False),
        sa.Column("color", sa.String(7), nullable=True),  # Hex color codes
        sa.Column("emoji", sa.String(4), nullable=True),  # Unicode emoji
        sa.Column("is_archived", sa.Boolean(), nullable=False, default=False),
        sa.Column("is_default", sa.Boolean(), nullable=False, default=False),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("tags", sa.JSON(), nullable=True),  # Array of tag strings
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("owner_id", sa.String(), nullable=False),
        sa.Column("shared_with", sa.JSON(), nullable=True),  # Array of user IDs
        sa.Column("todo_count", sa.Integer(), nullable=False, default=0),
        sa.Column("completed_count", sa.Integer(), nullable=False, default=0),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create todos table
    op.create_table(
        "todos",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("priority", sa.String(), nullable=False),
        sa.Column("parent_id", sa.String(), nullable=True),
        sa.Column("position", sa.Integer(), nullable=False, default=0),
        sa.Column("due_date", sa.DateTime(), nullable=True),
        sa.Column("reminder_date", sa.DateTime(), nullable=True),
        sa.Column("scheduled_date", sa.DateTime(), nullable=True),
        sa.Column("tags", sa.JSON(), nullable=True),
        sa.Column("project_id", sa.String(), nullable=True),
        sa.Column("context", sa.String(), nullable=True),
        sa.Column("estimated_minutes", sa.Integer(), nullable=True),
        sa.Column("actual_minutes", sa.Integer(), nullable=True),
        sa.Column("completion_notes", sa.Text(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("knowledge_node_id", sa.String(), nullable=True),
        sa.Column("related_todos", sa.JSON(), nullable=True),  # Array of todo IDs
        sa.Column("creation_intent", sa.String(), nullable=True),
        sa.Column("intent_confidence", sa.Float(), nullable=True),
        sa.Column("external_refs", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("owner_id", sa.String(), nullable=False),
        sa.Column("assigned_to", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["parent_id"], ["todos.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create list_memberships table
    op.create_table(
        "list_memberships",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("list_id", sa.String(), nullable=False),
        sa.Column("todo_id", sa.String(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False, default=0),
        sa.Column("added_at", sa.DateTime(), nullable=False),
        sa.Column("added_by", sa.String(), nullable=False),
        sa.Column("list_priority", sa.String(), nullable=True),
        sa.Column("list_due_date", sa.DateTime(), nullable=True),
        sa.Column("list_notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["list_id"], ["todo_lists.id"]),
        sa.ForeignKeyConstraint(["todo_id"], ["todos.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create strategic indexes for TodoList table
    op.create_index(
        "idx_todo_lists_owner_type", "todo_lists", ["owner_id", "list_type"], unique=False
    )
    op.create_index(
        "idx_todo_lists_owner_archived", "todo_lists", ["owner_id", "is_archived"], unique=False
    )
    op.create_index("idx_todo_lists_shared", "todo_lists", ["shared_with"], unique=False)
    op.create_index(
        "idx_todo_lists_default", "todo_lists", ["owner_id", "is_default"], unique=False
    )
    op.create_index("idx_todo_lists_tags", "todo_lists", ["tags"], unique=False)

    # Create comprehensive indexes for Todo table
    # Core query patterns
    op.create_index("idx_todos_owner_status", "todos", ["owner_id", "status"], unique=False)
    op.create_index("idx_todos_owner_priority", "todos", ["owner_id", "priority"], unique=False)
    op.create_index("idx_todos_assigned_status", "todos", ["assigned_to", "status"], unique=False)

    # Date-based queries
    op.create_index("idx_todos_due_date", "todos", ["due_date"], unique=False)
    op.create_index("idx_todos_owner_due", "todos", ["owner_id", "due_date"], unique=False)
    op.create_index("idx_todos_scheduled", "todos", ["scheduled_date"], unique=False)
    op.create_index("idx_todos_reminder", "todos", ["reminder_date"], unique=False)

    # Hierarchical queries
    op.create_index("idx_todos_parent", "todos", ["parent_id"], unique=False)
    op.create_index("idx_todos_parent_position", "todos", ["parent_id", "position"], unique=False)

    # Context and categorization
    op.create_index("idx_todos_context", "todos", ["context"], unique=False)
    op.create_index("idx_todos_project", "todos", ["project_id"], unique=False)
    op.create_index("idx_todos_tags", "todos", ["tags"], unique=False)

    # PM-040/PM-034 integration
    op.create_index("idx_todos_knowledge_node", "todos", ["knowledge_node_id"], unique=False)
    op.create_index("idx_todos_creation_intent", "todos", ["creation_intent"], unique=False)

    # External references
    op.create_index("idx_todos_external_refs", "todos", ["external_refs"], unique=False)

    # Performance queries
    op.create_index("idx_todos_owner_created", "todos", ["owner_id", "created_at"], unique=False)
    op.create_index("idx_todos_owner_updated", "todos", ["owner_id", "updated_at"], unique=False)

    # Create strategic indexes for ListMembership table
    # Ensure unique membership per list-todo pair
    op.create_index("idx_unique_list_todo", "list_memberships", ["list_id", "todo_id"], unique=True)

    # Position-based ordering within lists
    op.create_index(
        "idx_membership_list_position", "list_memberships", ["list_id", "position"], unique=False
    )

    # Todo-centric queries
    op.create_index("idx_membership_todo", "list_memberships", ["todo_id"], unique=False)

    # List-centric queries
    op.create_index("idx_membership_list", "list_memberships", ["list_id"], unique=False)

    # User-added tracking
    op.create_index("idx_membership_added_by", "list_memberships", ["added_by"], unique=False)
    op.create_index("idx_membership_added_at", "list_memberships", ["added_at"], unique=False)

    # List-specific overrides
    op.create_index(
        "idx_membership_list_priority",
        "list_memberships",
        ["list_id", "list_priority"],
        unique=False,
    )
    op.create_index(
        "idx_membership_list_due", "list_memberships", ["list_id", "list_due_date"], unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""

    # Drop indexes for list_memberships
    op.drop_index("idx_membership_list_due", table_name="list_memberships")
    op.drop_index("idx_membership_list_priority", table_name="list_memberships")
    op.drop_index("idx_membership_added_at", table_name="list_memberships")
    op.drop_index("idx_membership_added_by", table_name="list_memberships")
    op.drop_index("idx_membership_list", table_name="list_memberships")
    op.drop_index("idx_membership_todo", table_name="list_memberships")
    op.drop_index("idx_membership_list_position", table_name="list_memberships")
    op.drop_index("idx_unique_list_todo", table_name="list_memberships")

    # Drop indexes for todos
    op.drop_index("idx_todos_owner_updated", table_name="todos")
    op.drop_index("idx_todos_owner_created", table_name="todos")
    op.drop_index("idx_todos_external_refs", table_name="todos")
    op.drop_index("idx_todos_creation_intent", table_name="todos")
    op.drop_index("idx_todos_knowledge_node", table_name="todos")
    op.drop_index("idx_todos_tags", table_name="todos")
    op.drop_index("idx_todos_project", table_name="todos")
    op.drop_index("idx_todos_context", table_name="todos")
    op.drop_index("idx_todos_parent_position", table_name="todos")
    op.drop_index("idx_todos_parent", table_name="todos")
    op.drop_index("idx_todos_reminder", table_name="todos")
    op.drop_index("idx_todos_scheduled", table_name="todos")
    op.drop_index("idx_todos_owner_due", table_name="todos")
    op.drop_index("idx_todos_due_date", table_name="todos")
    op.drop_index("idx_todos_assigned_status", table_name="todos")
    op.drop_index("idx_todos_owner_priority", table_name="todos")
    op.drop_index("idx_todos_owner_status", table_name="todos")

    # Drop indexes for todo_lists
    op.drop_index("idx_todo_lists_tags", table_name="todo_lists")
    op.drop_index("idx_todo_lists_default", table_name="todo_lists")
    op.drop_index("idx_todo_lists_shared", table_name="todo_lists")
    op.drop_index("idx_todo_lists_owner_archived", table_name="todo_lists")
    op.drop_index("idx_todo_lists_owner_type", table_name="todo_lists")

    # Drop tables
    op.drop_table("list_memberships")
    op.drop_table("todos")
    op.drop_table("todo_lists")

    # Drop enums
    op.execute("DROP TYPE IF EXISTS orderingstrategy")
    op.execute("DROP TYPE IF EXISTS listtype")
    op.execute("DROP TYPE IF EXISTS todopriority")
    op.execute("DROP TYPE IF EXISTS todostatus")
