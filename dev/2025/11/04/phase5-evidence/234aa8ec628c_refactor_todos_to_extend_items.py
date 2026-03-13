"""refactor_todos_to_extend_items

Phase 2: Refactor todos to use polymorphic inheritance from items.

This migration:
1. Migrates base todo data (id, title→text, position, etc.) to items table
2. Creates todo_items table for todo-specific data
3. Migrates todo-specific data to todo_items table
4. Drops old todos table

After this migration:
- items table contains base data for all todos (with item_type='todo')
- todo_items table contains todo-specific data
- TodoDB extends ItemDB using SQLAlchemy joined table inheritance

Revision ID: 234aa8ec628c
Revises: 40fc95f25017
Create Date: 2025-11-04 05:46:24.832870

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "234aa8ec628c"
down_revision: Union[str, Sequence[str], None] = "40fc95f25017"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Migrate existing todos to new polymorphic structure.

    Strategy:
    1. Copy base todo data to items table (id, title→text, position, etc.)
    2. Create todo_items table for todo-specific fields
    3. Copy todo-specific data to todo_items table
    4. Drop old todos table
    """

    # Step 1: Migrate base todo data to items table
    # Map: title → text, position (default 0), item_type = 'todo'
    print("Migrating base todo data to items table...")
    op.execute(
        """
        INSERT INTO items (id, text, position, list_id, item_type, created_at, updated_at)
        SELECT
            id,
            title,                    -- title → text
            COALESCE(position, 0),    -- position (default 0)
            NULL,                      -- list_id (todos don't use this yet)
            'todo'::VARCHAR(50),      -- item_type discriminator
            created_at,
            updated_at
        FROM todos
        ON CONFLICT (id) DO NOTHING   -- Skip if already exists
    """
    )

    # Step 2: Create todo_items table with all todo-specific fields
    print("Creating todo_items table...")
    op.create_table(
        "todo_items",
        # Primary key that's also FK to items
        sa.Column("id", sa.String(), nullable=False),
        # Core todo fields
        sa.Column("description", sa.Text(), server_default="", nullable=True),
        sa.Column("status", sa.String(length=11), nullable=False, server_default="pending"),
        sa.Column("priority", sa.String(length=6), nullable=False, server_default="medium"),
        sa.Column("completed", sa.Boolean(), nullable=False, server_default="false"),
        # Hierarchical structure
        sa.Column("parent_id", sa.String(), nullable=True),
        # Scheduling
        sa.Column("due_date", sa.DateTime(), nullable=True),
        sa.Column("reminder_date", sa.DateTime(), nullable=True),
        sa.Column("scheduled_date", sa.DateTime(), nullable=True),
        # Context and categorization
        sa.Column("tags", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("project_id", sa.String(), nullable=True),
        sa.Column("context", sa.String(), nullable=True),
        # Progress tracking
        sa.Column("estimated_minutes", sa.Integer(), nullable=True),
        sa.Column("actual_minutes", sa.Integer(), nullable=True),
        sa.Column("completion_notes", sa.Text(), server_default="", nullable=True),
        # PM-040 Knowledge Graph integration
        sa.Column("list_metadata", sa.JSON(), nullable=True),
        sa.Column("knowledge_node_id", sa.String(), nullable=True),
        sa.Column("related_todos", sa.JSON(), nullable=True),
        # PM-034 Intent Classification integration
        sa.Column("creation_intent", sa.String(), nullable=True),
        sa.Column("intent_confidence", sa.Float(), nullable=True),
        # External integrations
        sa.Column("external_refs", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        # Timestamps
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        # Ownership
        sa.Column("owner_id", sa.String(), nullable=False),
        sa.Column("assigned_to", sa.String(), nullable=True),
        # Constraints
        sa.ForeignKeyConstraint(
            ["id"], ["items.id"], name="fk_todo_items_items", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["parent_id"], ["todo_items.id"], name="fk_todo_items_parent"),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], name="fk_todo_items_project"),
        sa.PrimaryKeyConstraint("id", name="pk_todo_items"),
    )

    # Step 3: Migrate todo-specific data to todo_items table
    print("Migrating todo-specific data to todo_items...")
    op.execute(
        """
        INSERT INTO todo_items (
            id, description, status, priority, completed, parent_id,
            due_date, reminder_date, scheduled_date,
            tags, project_id, context,
            estimated_minutes, actual_minutes, completion_notes,
            list_metadata, knowledge_node_id, related_todos,
            creation_intent, intent_confidence, external_refs,
            completed_at, owner_id, assigned_to
        )
        SELECT
            id,
            COALESCE(description, ''),
            COALESCE(status::VARCHAR, 'pending'),  -- Cast ENUM to VARCHAR
            COALESCE(priority::VARCHAR, 'medium'),  -- Cast ENUM to VARCHAR
            COALESCE(status::VARCHAR = 'completed', false) as completed,  -- Derive completed from status
            parent_id,
            due_date,
            reminder_date,
            scheduled_date,
            tags,
            project_id,
            context,
            estimated_minutes,
            actual_minutes,
            COALESCE(completion_notes, ''),
            list_metadata,
            knowledge_node_id,
            related_todos,
            creation_intent,
            intent_confidence,
            external_refs,
            completed_at,
            owner_id,
            assigned_to
        FROM todos
        ON CONFLICT (id) DO NOTHING   -- Skip if already exists
    """
    )

    # Step 4: Drop old todos table (this also drops its indexes)
    # First drop dependent objects
    print("Dropping old todos table and dependencies...")
    op.execute("DROP TABLE IF EXISTS list_memberships CASCADE")
    op.drop_table("todos")

    # Step 4.5: Drop old ENUM types (no longer needed with VARCHAR columns)
    print("Dropping old ENUM types...")
    op.execute("DROP TYPE IF EXISTS todostatus CASCADE")
    op.execute("DROP TYPE IF EXISTS todopriority CASCADE")

    # Step 5: Create indexes on todo_items (after todos table is dropped to avoid name conflicts)
    print("Creating indexes on todo_items...")
    op.create_index("idx_todos_owner_status", "todo_items", ["owner_id", "status"])
    op.create_index("idx_todos_owner_priority", "todo_items", ["owner_id", "priority"])
    op.create_index("idx_todos_assigned_status", "todo_items", ["assigned_to", "status"])
    op.create_index("idx_todos_due_date", "todo_items", ["due_date"])
    op.create_index("idx_todos_owner_due", "todo_items", ["owner_id", "due_date"])
    op.create_index("idx_todos_scheduled", "todo_items", ["scheduled_date"])
    op.create_index("idx_todos_reminder", "todo_items", ["reminder_date"])
    op.create_index("idx_todos_parent", "todo_items", ["parent_id"])
    op.create_index("idx_todos_context", "todo_items", ["context"])
    op.create_index("idx_todos_project", "todo_items", ["project_id"])
    op.create_index("idx_todos_tags", "todo_items", ["tags"], postgresql_using="gin")
    op.create_index("idx_todos_knowledge_node", "todo_items", ["knowledge_node_id"])
    op.create_index("idx_todos_creation_intent", "todo_items", ["creation_intent"])
    op.create_index(
        "idx_todos_external_refs", "todo_items", ["external_refs"], postgresql_using="gin"
    )

    print("Migration complete! Todos now use polymorphic inheritance from items.")


def downgrade() -> None:
    """
    Reverse the migration: Restore original todos table structure.

    WARNING: This downgrade will lose any new todo data created after the upgrade.
    """

    # Step 1: Recreate original todos table
    print("Recreating original todos table...")
    op.create_table(
        "todos",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), server_default=""),
        sa.Column("status", sa.String(length=11), nullable=False),
        sa.Column("priority", sa.String(length=6), nullable=False),
        sa.Column("parent_id", sa.String(), nullable=True),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("due_date", sa.DateTime(), nullable=True),
        sa.Column("reminder_date", sa.DateTime(), nullable=True),
        sa.Column("scheduled_date", sa.DateTime(), nullable=True),
        sa.Column("tags", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("project_id", sa.String(), nullable=True),
        sa.Column("context", sa.String(), nullable=True),
        sa.Column("estimated_minutes", sa.Integer(), nullable=True),
        sa.Column("actual_minutes", sa.Integer(), nullable=True),
        sa.Column("completion_notes", sa.Text(), server_default=""),
        sa.Column("list_metadata", sa.JSON(), nullable=True),
        sa.Column("knowledge_node_id", sa.String(), nullable=True),
        sa.Column("related_todos", sa.JSON(), nullable=True),
        sa.Column("creation_intent", sa.String(), nullable=True),
        sa.Column("intent_confidence", sa.Float(), nullable=True),
        sa.Column("external_refs", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("owner_id", sa.String(), nullable=False),
        sa.Column("assigned_to", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["parent_id"], ["todos.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Step 2: Migrate data back from items + todo_items to todos
    print("Migrating data back to todos table...")
    op.execute(
        """
        INSERT INTO todos (
            id, title, description, status, priority, parent_id, position,
            due_date, reminder_date, scheduled_date,
            tags, project_id, context,
            estimated_minutes, actual_minutes, completion_notes,
            list_metadata, knowledge_node_id, related_todos,
            creation_intent, intent_confidence, external_refs,
            created_at, updated_at, completed_at,
            owner_id, assigned_to
        )
        SELECT
            i.id,
            i.text as title,          -- text → title
            t.description,
            t.status,
            t.priority,
            t.parent_id,
            i.position,
            t.due_date,
            t.reminder_date,
            t.scheduled_date,
            t.tags,
            t.project_id,
            t.context,
            t.estimated_minutes,
            t.actual_minutes,
            t.completion_notes,
            t.list_metadata,
            t.knowledge_node_id,
            t.related_todos,
            t.creation_intent,
            t.intent_confidence,
            t.external_refs,
            i.created_at,
            i.updated_at,
            t.completed_at,
            t.owner_id,
            t.assigned_to
        FROM items i
        INNER JOIN todo_items t ON i.id = t.id
        WHERE i.item_type = 'todo'
    """
    )

    # Step 3: Drop todo_items table
    print("Dropping todo_items table...")
    op.drop_table("todo_items")

    # Step 4: Remove todos from items table
    print("Removing todos from items table...")
    op.execute("DELETE FROM items WHERE item_type = 'todo'")

    print("Downgrade complete! Restored original todos table.")
