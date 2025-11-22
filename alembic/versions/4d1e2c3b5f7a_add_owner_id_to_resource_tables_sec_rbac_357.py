"""add_owner_id_to_resource_tables_sec_rbac_357

Adds owner_id field (UUID FK to users.id) to all user-owned resource tables
for Phase 1 of SEC-RBAC implementation.

Resource ownership is fundamental to authorization - every resource must have
an owner_id that matches the authenticated user accessing it.

Tables Modified:
1. uploaded_files - Change session_id (String) to owner_id (UUID) FK
2. projects - Add owner_id UUID FK
3. project_integrations - Add owner_id UUID FK
4. knowledge_nodes - Add owner_id UUID FK
5. knowledge_edges - Add owner_id UUID FK
6. list_memberships - Add owner_id UUID FK
7. list_items - Add owner_id UUID FK
8. feedback - Add owner_id UUID FK
9. personality_profiles - Add owner_id UUID FK

Note: TodoDB, ListDB, TodoListDB already have owner_id from previous migrations.

Revision ID: 4d1e2c3b5f7a
Revises: 3242bdd246f1
Create Date: 2025-11-21 18:30:00.000000

Issue: #357 SEC-RBAC Phase 1
"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4d1e2c3b5f7a"
down_revision: Union[str, Sequence[str], None] = "3242bdd246f1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: Add owner_id fields for resource ownership."""

    # 1. uploaded_files: Change session_id to owner_id
    # First, add the new owner_id column
    op.add_column(
        "uploaded_files",
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
    )

    # Migrate data from session_id to owner_id
    # For alpha: Assign all test files to the alpha owner (xian)
    # In alpha, all data is test data belonging to the lead developer
    op.execute(
        """
        UPDATE uploaded_files
        SET owner_id = '3f4593ae-5bc9-468d-b08d-8c4c02a5b963'
        WHERE session_id IS NOT NULL
    """
    )

    # Make owner_id NOT NULL after backfill
    op.alter_column("uploaded_files", "owner_id", nullable=False)

    # Add FK constraint
    op.create_foreign_key(
        "fk_uploaded_files_owner_id",
        "uploaded_files",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Drop old session_id column
    op.drop_column("uploaded_files", "session_id")

    # 2. projects: Add owner_id
    op.add_column(
        "projects",
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
    )

    # Backfill with system user or NULL for now
    op.execute("UPDATE projects SET owner_id = NULL WHERE owner_id IS NULL")

    # Make owner_id NOT NULL after review/backfill
    # Note: This may need manual backfill first
    # For now, allow NULL to avoid breaking existing data
    op.create_foreign_key(
        "fk_projects_owner_id",
        "projects",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # 3. project_integrations: Add owner_id
    op.add_column(
        "project_integrations",
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
    )

    op.create_foreign_key(
        "fk_project_integrations_owner_id",
        "project_integrations",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # 4. knowledge_nodes: Add owner_id
    op.add_column(
        "knowledge_nodes",
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
    )

    op.create_foreign_key(
        "fk_knowledge_nodes_owner_id",
        "knowledge_nodes",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # 5. knowledge_edges: Add owner_id
    op.add_column(
        "knowledge_edges",
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
    )

    op.create_foreign_key(
        "fk_knowledge_edges_owner_id",
        "knowledge_edges",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # 6. list_memberships: Add owner_id
    op.add_column(
        "list_memberships",
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
    )

    op.create_foreign_key(
        "fk_list_memberships_owner_id",
        "list_memberships",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # 7. list_items: Add owner_id
    op.add_column("list_items", sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True))

    op.create_foreign_key(
        "fk_list_items_owner_id",
        "list_items",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # 8. feedback: Add owner_id
    op.add_column("feedback", sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True))

    op.create_foreign_key(
        "fk_feedback_owner_id",
        "feedback",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # 9. personality_profiles: Add owner_id
    op.add_column(
        "personality_profiles",
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
    )

    op.create_foreign_key(
        "fk_personality_profiles_owner_id",
        "personality_profiles",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Create indexes on owner_id for query performance
    op.create_index("idx_uploaded_files_owner", "uploaded_files", ["owner_id"])
    op.create_index("idx_projects_owner", "projects", ["owner_id"])
    op.create_index("idx_project_integrations_owner", "project_integrations", ["owner_id"])
    op.create_index("idx_knowledge_nodes_owner", "knowledge_nodes", ["owner_id"])
    op.create_index("idx_knowledge_edges_owner", "knowledge_edges", ["owner_id"])
    op.create_index("idx_list_memberships_owner", "list_memberships", ["owner_id"])
    op.create_index("idx_list_items_owner", "list_items", ["owner_id"])
    op.create_index("idx_feedback_owner", "feedback", ["owner_id"])
    op.create_index("idx_personality_profiles_owner", "personality_profiles", ["owner_id"])


def downgrade() -> None:
    """Downgrade schema: Remove owner_id fields and restore previous schema."""

    # Drop all indexes
    op.drop_index("idx_uploaded_files_owner", "uploaded_files")
    op.drop_index("idx_projects_owner", "projects")
    op.drop_index("idx_project_integrations_owner", "project_integrations")
    op.drop_index("idx_knowledge_nodes_owner", "knowledge_nodes")
    op.drop_index("idx_knowledge_edges_owner", "knowledge_edges")
    op.drop_index("idx_list_memberships_owner", "list_memberships")
    op.drop_index("idx_list_items_owner", "list_items")
    op.drop_index("idx_feedback_owner", "feedback")
    op.drop_index("idx_personality_profiles_owner", "personality_profiles")

    # Drop all foreign keys
    op.drop_constraint("fk_uploaded_files_owner_id", "uploaded_files", type_="foreignkey")
    op.drop_constraint("fk_projects_owner_id", "projects", type_="foreignkey")
    op.drop_constraint(
        "fk_project_integrations_owner_id", "project_integrations", type_="foreignkey"
    )
    op.drop_constraint("fk_knowledge_nodes_owner_id", "knowledge_nodes", type_="foreignkey")
    op.drop_constraint("fk_knowledge_edges_owner_id", "knowledge_edges", type_="foreignkey")
    op.drop_constraint("fk_list_memberships_owner_id", "list_memberships", type_="foreignkey")
    op.drop_constraint("fk_list_items_owner_id", "list_items", type_="foreignkey")
    op.drop_constraint("fk_feedback_owner_id", "feedback", type_="foreignkey")
    op.drop_constraint(
        "fk_personality_profiles_owner_id", "personality_profiles", type_="foreignkey"
    )

    # Drop all columns
    op.drop_column("uploaded_files", "owner_id")
    op.drop_column("projects", "owner_id")
    op.drop_column("project_integrations", "owner_id")
    op.drop_column("knowledge_nodes", "owner_id")
    op.drop_column("knowledge_edges", "owner_id")
    op.drop_column("list_memberships", "owner_id")
    op.drop_column("list_items", "owner_id")
    op.drop_column("feedback", "owner_id")
    op.drop_column("personality_profiles", "owner_id")

    # Restore session_id column to uploaded_files
    op.add_column("uploaded_files", sa.Column("session_id", sa.String(), nullable=True))
