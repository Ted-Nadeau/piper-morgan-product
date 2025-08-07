"""Universal List Architecture for PM-081

Revision ID: 6m5s5d1t6500
Revises: ffns5hckf96d
Create Date: 2025-08-05 15:45:00.000000

Chief Architect's universal composition over specialization principle.
Migrates from specialized TodoList to Universal List pattern.

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6m5s5d1t6500"
down_revision: Union[str, Sequence[str], None] = "ffns5hckf96d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade to Universal List architecture."""

    # Create universal lists table
    op.create_table(
        "lists",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("item_type", sa.String(), nullable=False, server_default="todo"),
        sa.Column("list_type", sa.String(), nullable=False, server_default="personal"),
        sa.Column("ordering_strategy", sa.String(), nullable=False, server_default="manual"),
        sa.Column("color", sa.String(7), nullable=True),
        sa.Column("emoji", sa.String(4), nullable=True),
        sa.Column("is_archived", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("is_default", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("tags", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("owner_id", sa.String(), nullable=False),
        sa.Column("shared_with", sa.JSON(), nullable=True),
        sa.Column("item_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("completed_count", sa.Integer(), nullable=False, server_default="0"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create universal list_items table
    op.create_table(
        "list_items",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("list_id", sa.String(), nullable=False),
        sa.Column("item_id", sa.String(), nullable=False),
        sa.Column("item_type", sa.String(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("added_at", sa.DateTime(), nullable=False),
        sa.Column("added_by", sa.String(), nullable=False),
        sa.Column("list_priority", sa.String(), nullable=True),
        sa.Column("list_due_date", sa.DateTime(), nullable=True),
        sa.Column("list_notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["list_id"], ["lists.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create strategic indexes for lists table
    op.create_index("idx_lists_owner_type", "lists", ["owner_id", "item_type"], unique=False)
    op.create_index("idx_lists_owner_list_type", "lists", ["owner_id", "list_type"], unique=False)
    op.create_index("idx_lists_owner_archived", "lists", ["owner_id", "is_archived"], unique=False)
    op.create_index("idx_lists_shared", "lists", ["shared_with"], unique=False)
    op.create_index(
        "idx_lists_default", "lists", ["owner_id", "item_type", "is_default"], unique=False
    )
    op.create_index("idx_lists_tags", "lists", ["tags"], unique=False)

    # Create strategic indexes for list_items table
    op.create_index("idx_unique_list_item", "list_items", ["list_id", "item_id"], unique=True)
    op.create_index("idx_list_item_position", "list_items", ["list_id", "position"], unique=False)
    op.create_index("idx_list_item_by_item", "list_items", ["item_id", "item_type"], unique=False)
    op.create_index("idx_list_item_by_list", "list_items", ["list_id"], unique=False)
    op.create_index("idx_list_item_added_by", "list_items", ["added_by"], unique=False)
    op.create_index("idx_list_item_added_at", "list_items", ["added_at"], unique=False)
    op.create_index(
        "idx_list_item_priority", "list_items", ["list_id", "list_priority"], unique=False
    )
    op.create_index("idx_list_item_due", "list_items", ["list_id", "list_due_date"], unique=False)

    # Migrate data from todo_lists to lists table
    op.execute(
        """
        INSERT INTO lists (
            id, name, description, item_type, list_type, ordering_strategy,
            color, emoji, is_archived, is_default, metadata, tags,
            created_at, updated_at, owner_id, shared_with,
            item_count, completed_count
        )
        SELECT
            id, name, description, 'todo',
            LOWER(list_type::text),
            LOWER(ordering_strategy::text),
            color, emoji, is_archived, is_default, metadata, tags,
            created_at, updated_at, owner_id, shared_with,
            todo_count, completed_count
        FROM todo_lists
    """
    )

    # Migrate data from list_memberships to list_items table
    op.execute(
        """
        INSERT INTO list_items (
            id, list_id, item_id, item_type, position,
            added_at, added_by, list_priority, list_due_date, list_notes
        )
        SELECT
            id, list_id, todo_id, 'todo', position,
            added_at, added_by,
            CASE WHEN list_priority IS NOT NULL THEN LOWER(list_priority::text) ELSE NULL END,
            list_due_date, list_notes
        FROM list_memberships
    """
    )

    # Update todos table to remove enum constraints and use simple strings
    # Remove foreign key constraint to parent_id temporarily
    op.drop_constraint("todos_parent_id_fkey", "todos", type_="foreignkey")

    # Create new todos table with string fields
    op.create_table(
        "todos_new",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default="pending"),
        sa.Column("priority", sa.String(), nullable=False, server_default="medium"),
        sa.Column("parent_id", sa.String(), nullable=True),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
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
        sa.Column("related_todos", sa.JSON(), nullable=True),
        sa.Column("creation_intent", sa.String(), nullable=True),
        sa.Column("intent_confidence", sa.Float(), nullable=True),
        sa.Column("external_refs", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("owner_id", sa.String(), nullable=False),
        sa.Column("assigned_to", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["parent_id"], ["todos_new.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Copy data from old todos table to new
    op.execute(
        """
        INSERT INTO todos_new
        SELECT
            id, title, description,
            LOWER(status::text),
            LOWER(priority::text),
            parent_id, position, due_date, reminder_date, scheduled_date,
            tags, project_id, context, estimated_minutes, actual_minutes,
            completion_notes, metadata, knowledge_node_id, related_todos,
            creation_intent, intent_confidence, external_refs,
            created_at, updated_at, completed_at, owner_id, assigned_to
        FROM todos
    """
    )

    # Drop old tables
    op.drop_table("list_memberships")
    op.drop_table("todo_lists")
    op.drop_table("todos")

    # Rename new todos table
    op.rename_table("todos_new", "todos")

    # Recreate all indexes for todos table
    op.create_index("idx_todos_owner_status", "todos", ["owner_id", "status"], unique=False)
    op.create_index("idx_todos_owner_priority", "todos", ["owner_id", "priority"], unique=False)
    op.create_index("idx_todos_assigned_status", "todos", ["assigned_to", "status"], unique=False)
    op.create_index("idx_todos_due_date", "todos", ["due_date"], unique=False)
    op.create_index("idx_todos_owner_due", "todos", ["owner_id", "due_date"], unique=False)
    op.create_index("idx_todos_scheduled", "todos", ["scheduled_date"], unique=False)
    op.create_index("idx_todos_reminder", "todos", ["reminder_date"], unique=False)
    op.create_index("idx_todos_parent", "todos", ["parent_id"], unique=False)
    op.create_index("idx_todos_parent_position", "todos", ["parent_id", "position"], unique=False)
    op.create_index("idx_todos_context", "todos", ["context"], unique=False)
    op.create_index("idx_todos_project", "todos", ["project_id"], unique=False)
    op.create_index("idx_todos_tags", "todos", ["tags"], unique=False)
    op.create_index("idx_todos_knowledge_node", "todos", ["knowledge_node_id"], unique=False)
    op.create_index("idx_todos_creation_intent", "todos", ["creation_intent"], unique=False)
    op.create_index("idx_todos_external_refs", "todos", ["external_refs"], unique=False)
    op.create_index("idx_todos_owner_created", "todos", ["owner_id", "created_at"], unique=False)
    op.create_index("idx_todos_owner_updated", "todos", ["owner_id", "updated_at"], unique=False)


def downgrade() -> None:
    """Downgrade back to specialized TodoList architecture."""

    # This is a complex migration - downgrade would need careful consideration
    # For now, we'll just drop the new tables and note that data would be lost

    # Drop indexes
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

    # Drop list_items indexes
    op.drop_index("idx_list_item_due", table_name="list_items")
    op.drop_index("idx_list_item_priority", table_name="list_items")
    op.drop_index("idx_list_item_added_at", table_name="list_items")
    op.drop_index("idx_list_item_added_by", table_name="list_items")
    op.drop_index("idx_list_item_by_list", table_name="list_items")
    op.drop_index("idx_list_item_by_item", table_name="list_items")
    op.drop_index("idx_list_item_position", table_name="list_items")
    op.drop_index("idx_unique_list_item", table_name="list_items")

    # Drop lists indexes
    op.drop_index("idx_lists_tags", table_name="lists")
    op.drop_index("idx_lists_default", table_name="lists")
    op.drop_index("idx_lists_shared", table_name="lists")
    op.drop_index("idx_lists_owner_archived", table_name="lists")
    op.drop_index("idx_lists_owner_list_type", table_name="lists")
    op.drop_index("idx_lists_owner_type", table_name="lists")

    # Drop tables
    op.drop_table("todos")
    op.drop_table("list_items")
    op.drop_table("lists")

    # Note: Full downgrade would require recreating the original schema
    # and enum types, which is complex and potentially lossy
