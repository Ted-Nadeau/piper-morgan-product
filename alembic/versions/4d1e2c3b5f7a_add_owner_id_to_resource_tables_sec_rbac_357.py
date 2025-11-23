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
    """Upgrade schema: Add owner_id fields for resource ownership.

    Note: This migration handles tables conditionally. Some tables may not exist
    in all databases (project_integrations, knowledge_nodes, knowledge_edges may
    be created by other features later).
    """

    conn = op.get_bind()

    # 1. uploaded_files: Change session_id to owner_id (if table exists)
    if _table_exists(conn, "uploaded_files"):
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
        op.create_index("idx_uploaded_files_owner", "uploaded_files", ["owner_id"])

    # 2. projects: owner_id already exists from migration 41000fc95f25017
    # Just add the FK constraint (column already exists as VARCHAR)
    if _table_exists(conn, "projects"):
        op.create_foreign_key(
            "fk_projects_owner_id",
            "projects",
            "users",
            ["owner_id"],
            ["id"],
            ondelete="CASCADE",
        )
        op.create_index("idx_projects_owner", "projects", ["owner_id"])

    # 3-5. Other tables are handled conditionally in PL/pgSQL
    # These tables may not exist in all databases
    conn.execute(
        sa.text(
            """
        DO $$
        BEGIN
            -- project_integrations
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'project_integrations') THEN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                              WHERE table_name = 'project_integrations' AND column_name = 'owner_id') THEN
                    ALTER TABLE project_integrations ADD COLUMN owner_id UUID;
                    ALTER TABLE project_integrations ADD CONSTRAINT fk_project_integrations_owner_id
                        FOREIGN KEY(owner_id) REFERENCES users(id) ON DELETE CASCADE;
                END IF;
            END IF;

            -- knowledge_nodes
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'knowledge_nodes') THEN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                              WHERE table_name = 'knowledge_nodes' AND column_name = 'owner_id') THEN
                    ALTER TABLE knowledge_nodes ADD COLUMN owner_id UUID;
                    ALTER TABLE knowledge_nodes ADD CONSTRAINT fk_knowledge_nodes_owner_id
                        FOREIGN KEY(owner_id) REFERENCES users(id) ON DELETE CASCADE;
                END IF;
            END IF;

            -- knowledge_edges
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'knowledge_edges') THEN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                              WHERE table_name = 'knowledge_edges' AND column_name = 'owner_id') THEN
                    ALTER TABLE knowledge_edges ADD COLUMN owner_id UUID;
                    ALTER TABLE knowledge_edges ADD CONSTRAINT fk_knowledge_edges_owner_id
                        FOREIGN KEY(owner_id) REFERENCES users(id) ON DELETE CASCADE;
                END IF;
            END IF;

            -- list_memberships
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'list_memberships') THEN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                              WHERE table_name = 'list_memberships' AND column_name = 'owner_id') THEN
                    ALTER TABLE list_memberships ADD COLUMN owner_id UUID;
                    ALTER TABLE list_memberships ADD CONSTRAINT fk_list_memberships_owner_id
                        FOREIGN KEY(owner_id) REFERENCES users(id) ON DELETE CASCADE;
                END IF;
            END IF;

            -- list_items
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'list_items') THEN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                              WHERE table_name = 'list_items' AND column_name = 'owner_id') THEN
                    ALTER TABLE list_items ADD COLUMN owner_id UUID;
                    ALTER TABLE list_items ADD CONSTRAINT fk_list_items_owner_id
                        FOREIGN KEY(owner_id) REFERENCES users(id) ON DELETE CASCADE;
                END IF;
            END IF;

            -- feedback
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'feedback') THEN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                              WHERE table_name = 'feedback' AND column_name = 'owner_id') THEN
                    ALTER TABLE feedback ADD COLUMN owner_id UUID;
                    ALTER TABLE feedback ADD CONSTRAINT fk_feedback_owner_id
                        FOREIGN KEY(owner_id) REFERENCES users(id) ON DELETE CASCADE;
                END IF;
            END IF;

            -- personality_profiles
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'personality_profiles') THEN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                              WHERE table_name = 'personality_profiles' AND column_name = 'owner_id') THEN
                    ALTER TABLE personality_profiles ADD COLUMN owner_id UUID;
                    ALTER TABLE personality_profiles ADD CONSTRAINT fk_personality_profiles_owner_id
                        FOREIGN KEY(owner_id) REFERENCES users(id) ON DELETE CASCADE;
                END IF;
            END IF;
        END
        $$;
    """
        )
    )


def _table_exists(conn, table_name: str) -> bool:
    """Check if a table exists in the public schema."""
    result = conn.execute(
        sa.text(
            f"""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = :name
        )
    """
        ),
        {"name": table_name},
    )
    return result.scalar() or False


def downgrade() -> None:
    """Downgrade schema: Remove owner_id fields and restore previous schema."""

    conn = op.get_bind()

    # Drop indexes conditionally (only if table exists)
    if _table_exists(conn, "uploaded_files"):
        op.drop_index("idx_uploaded_files_owner", "uploaded_files")
        op.drop_constraint("fk_uploaded_files_owner_id", "uploaded_files", type_="foreignkey")
        op.drop_column("uploaded_files", "owner_id")
        # Restore session_id column
        op.add_column("uploaded_files", sa.Column("session_id", sa.String(), nullable=True))

    if _table_exists(conn, "projects"):
        op.drop_index("idx_projects_owner", "projects")
        op.drop_constraint("fk_projects_owner_id", "projects", type_="foreignkey")
        # Note: Do NOT drop projects.owner_id - it was created in migration 41000fc95f25017

    # Drop conditional constraints for tables that may not exist
    conn.execute(
        sa.text(
            """
        DO $$
        BEGIN
            -- project_integrations
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'project_integrations') THEN
                IF EXISTS (SELECT 1 FROM information_schema.table_constraints
                          WHERE table_name = 'project_integrations' AND constraint_name = 'fk_project_integrations_owner_id') THEN
                    ALTER TABLE project_integrations DROP CONSTRAINT fk_project_integrations_owner_id;
                END IF;
                IF EXISTS (SELECT 1 FROM information_schema.columns
                          WHERE table_name = 'project_integrations' AND column_name = 'owner_id') THEN
                    ALTER TABLE project_integrations DROP COLUMN owner_id;
                END IF;
            END IF;

            -- knowledge_nodes
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'knowledge_nodes') THEN
                IF EXISTS (SELECT 1 FROM information_schema.table_constraints
                          WHERE table_name = 'knowledge_nodes' AND constraint_name = 'fk_knowledge_nodes_owner_id') THEN
                    ALTER TABLE knowledge_nodes DROP CONSTRAINT fk_knowledge_nodes_owner_id;
                END IF;
                IF EXISTS (SELECT 1 FROM information_schema.columns
                          WHERE table_name = 'knowledge_nodes' AND column_name = 'owner_id') THEN
                    ALTER TABLE knowledge_nodes DROP COLUMN owner_id;
                END IF;
            END IF;

            -- knowledge_edges
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'knowledge_edges') THEN
                IF EXISTS (SELECT 1 FROM information_schema.table_constraints
                          WHERE table_name = 'knowledge_edges' AND constraint_name = 'fk_knowledge_edges_owner_id') THEN
                    ALTER TABLE knowledge_edges DROP CONSTRAINT fk_knowledge_edges_owner_id;
                END IF;
                IF EXISTS (SELECT 1 FROM information_schema.columns
                          WHERE table_name = 'knowledge_edges' AND column_name = 'owner_id') THEN
                    ALTER TABLE knowledge_edges DROP COLUMN owner_id;
                END IF;
            END IF;

            -- list_memberships
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'list_memberships') THEN
                IF EXISTS (SELECT 1 FROM information_schema.table_constraints
                          WHERE table_name = 'list_memberships' AND constraint_name = 'fk_list_memberships_owner_id') THEN
                    ALTER TABLE list_memberships DROP CONSTRAINT fk_list_memberships_owner_id;
                END IF;
                IF EXISTS (SELECT 1 FROM information_schema.columns
                          WHERE table_name = 'list_memberships' AND column_name = 'owner_id') THEN
                    ALTER TABLE list_memberships DROP COLUMN owner_id;
                END IF;
            END IF;

            -- list_items
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'list_items') THEN
                IF EXISTS (SELECT 1 FROM information_schema.table_constraints
                          WHERE table_name = 'list_items' AND constraint_name = 'fk_list_items_owner_id') THEN
                    ALTER TABLE list_items DROP CONSTRAINT fk_list_items_owner_id;
                END IF;
                IF EXISTS (SELECT 1 FROM information_schema.columns
                          WHERE table_name = 'list_items' AND column_name = 'owner_id') THEN
                    ALTER TABLE list_items DROP COLUMN owner_id;
                END IF;
            END IF;

            -- feedback
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'feedback') THEN
                IF EXISTS (SELECT 1 FROM information_schema.table_constraints
                          WHERE table_name = 'feedback' AND constraint_name = 'fk_feedback_owner_id') THEN
                    ALTER TABLE feedback DROP CONSTRAINT fk_feedback_owner_id;
                END IF;
                IF EXISTS (SELECT 1 FROM information_schema.columns
                          WHERE table_name = 'feedback' AND column_name = 'owner_id') THEN
                    ALTER TABLE feedback DROP COLUMN owner_id;
                END IF;
            END IF;

            -- personality_profiles
            IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'personality_profiles') THEN
                IF EXISTS (SELECT 1 FROM information_schema.table_constraints
                          WHERE table_name = 'personality_profiles' AND constraint_name = 'fk_personality_profiles_owner_id') THEN
                    ALTER TABLE personality_profiles DROP CONSTRAINT fk_personality_profiles_owner_id;
                END IF;
                IF EXISTS (SELECT 1 FROM information_schema.columns
                          WHERE table_name = 'personality_profiles' AND column_name = 'owner_id') THEN
                    ALTER TABLE personality_profiles DROP COLUMN owner_id;
                END IF;
            END IF;
        END
        $$;
    """
        )
    )
