"""uuid_migration_issue_262_and_291

Complete UUID migration for users table and merge alpha_users.
Resolves Issue #262 (UUID migration) and Issue #291 (token blacklist FK).

Option 1B: Merge alpha_users into users with is_alpha flag.

Revision ID: d8aeb665e878
Revises: 234aa8ec628c
Create Date: 2025-11-09 13:07:57.730803

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d8aeb665e878"
down_revision: Union[str, Sequence[str], None] = "234aa8ec628c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    UUID Migration - Issue #262 + #291

    Steps:
    1. Drop existing FK constraints
    2. Convert users.id to UUID (table is empty)
    3. Add is_alpha flag to users
    4. Migrate alpha_users data into users
    5. Convert all FK columns to UUID
    6. Re-add FK constraints with CASCADE
    7. Add token_blacklist FK (Issue #291)
    8. Drop alpha_users table
    """

    # Step 1: Drop FK constraints that reference users
    # Use SQL-level conditional logic to handle fresh databases where constraints may not exist
    conn = op.get_bind()

    # Drop constraints only if they exist using PostgreSQL syntax
    conn.execute(
        sa.text(
            """
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM information_schema.table_constraints
                       WHERE constraint_name = 'alpha_users_prod_user_id_fkey'
                       AND table_name = 'alpha_users') THEN
                ALTER TABLE alpha_users DROP CONSTRAINT alpha_users_prod_user_id_fkey;
                RAISE NOTICE 'Dropped alpha_users_prod_user_id_fkey';
            ELSE
                RAISE NOTICE 'Constraint alpha_users_prod_user_id_fkey not found (expected on fresh DB)';
            END IF;
        END
        $$;
    """
        )
    )

    conn.execute(
        sa.text(
            """
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM information_schema.table_constraints
                       WHERE constraint_name = 'feedback_user_id_fkey'
                       AND table_name = 'feedback') THEN
                ALTER TABLE feedback DROP CONSTRAINT feedback_user_id_fkey;
                RAISE NOTICE 'Dropped feedback_user_id_fkey';
            ELSE
                RAISE NOTICE 'Constraint feedback_user_id_fkey not found (expected on fresh DB)';
            END IF;
        END
        $$;
    """
        )
    )

    conn.execute(
        sa.text(
            """
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM information_schema.table_constraints
                       WHERE constraint_name = 'personality_profiles_user_id_fkey'
                       AND table_name = 'personality_profiles') THEN
                ALTER TABLE personality_profiles DROP CONSTRAINT personality_profiles_user_id_fkey;
                RAISE NOTICE 'Dropped personality_profiles_user_id_fkey';
            ELSE
                RAISE NOTICE 'Constraint personality_profiles_user_id_fkey not found (expected on fresh DB)';
            END IF;
        END
        $$;
    """
        )
    )

    # Step 2: Convert users.id to UUID (table is empty, safe to alter)
    op.alter_column(
        "users",
        "id",
        type_=postgresql.UUID(as_uuid=True),
        postgresql_using="gen_random_uuid()",
        server_default=sa.text("gen_random_uuid()"),
    )

    # Step 3: Add is_alpha flag to users
    op.add_column(
        "users", sa.Column("is_alpha", sa.Boolean(), nullable=False, server_default="false")
    )

    # Step 4: Migrate alpha_users data into users
    # Copy the single alpha user (xian) from alpha_users to users
    op.execute(
        """
        INSERT INTO users (
            id, username, email, password_hash, role,
            is_active, is_verified, is_alpha,
            created_at, updated_at, last_login_at
        )
        SELECT
            id, username, email, password_hash, 'user' as role,
            is_active, is_verified, true as is_alpha,
            created_at, updated_at, last_login_at
        FROM alpha_users
        WHERE username = 'xian'
    """
    )

    # Step 5: Convert all FK columns to UUID
    # alpha_users.prod_user_id (will be dropped anyway, but convert for consistency)
    op.alter_column(
        "alpha_users",
        "prod_user_id",
        type_=postgresql.UUID(as_uuid=True),
        postgresql_using="prod_user_id::uuid",
        nullable=True,
    )

    # feedback.user_id
    op.alter_column(
        "feedback",
        "user_id",
        type_=postgresql.UUID(as_uuid=True),
        postgresql_using="user_id::uuid",
        nullable=True,
    )

    # personality_profiles.user_id
    op.alter_column(
        "personality_profiles",
        "user_id",
        type_=postgresql.UUID(as_uuid=True),
        postgresql_using="user_id::uuid",
        nullable=True,
    )

    # token_blacklist.user_id (Issue #291)
    op.alter_column(
        "token_blacklist",
        "user_id",
        type_=postgresql.UUID(as_uuid=True),
        postgresql_using="user_id::uuid",
        nullable=True,
    )

    # user_api_keys.user_id
    op.alter_column(
        "user_api_keys",
        "user_id",
        type_=postgresql.UUID(as_uuid=True),
        postgresql_using="user_id::uuid",
        nullable=True,
    )

    # Handle tables with existing data
    # audit_logs has 7 records but no valid user references - delete them
    op.execute("DELETE FROM audit_logs WHERE user_id IS NOT NULL")
    op.alter_column(
        "audit_logs",
        "user_id",
        type_=postgresql.UUID(as_uuid=True),
        postgresql_using="user_id::uuid",
        nullable=True,
    )

    # NOTE: todo_items, lists, and todo_lists use owner_id which contains
    # non-UUID values like "system", "test-user-integration", etc.
    # These are NOT user references and should remain VARCHAR.
    # DO NOT CONVERT these columns.

    # Step 6: Re-add FK constraints with CASCADE
    op.create_foreign_key(
        "feedback_user_id_fkey", "feedback", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )

    op.create_foreign_key(
        "personality_profiles_user_id_fkey",
        "personality_profiles",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Step 7: Add NEW FK constraint for token_blacklist (Issue #291)
    op.create_foreign_key(
        "token_blacklist_user_id_fkey",
        "token_blacklist",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Step 8: Drop alpha_users table (data migrated)
    op.drop_table("alpha_users")


def downgrade() -> None:
    """
    Rollback UUID migration

    NOTE: This will lose the merged alpha_users data!
    For production, restore from backup instead.
    """

    # Recreate alpha_users table structure (basic version)
    op.create_table(
        "alpha_users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("username", sa.String(50), unique=True, nullable=False),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("password_hash", sa.String(500)),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("NOW()")),
        sa.Column("last_login_at", sa.DateTime()),
        sa.Column("prod_user_id", sa.String(255)),
    )

    # Drop new FK constraints
    op.drop_constraint("token_blacklist_user_id_fkey", "token_blacklist", type_="foreignkey")
    op.drop_constraint(
        "personality_profiles_user_id_fkey", "personality_profiles", type_="foreignkey"
    )
    op.drop_constraint("feedback_user_id_fkey", "feedback", type_="foreignkey")

    # Revert FK columns to VARCHAR
    # NOTE: todo_items, lists, todo_lists owner_id columns were NOT converted
    # (they are not user references), so no need to revert them
    op.alter_column("audit_logs", "user_id", type_=sa.String(255))
    op.alter_column("user_api_keys", "user_id", type_=sa.String(255))
    op.alter_column("token_blacklist", "user_id", type_=sa.String(255))
    op.alter_column("personality_profiles", "user_id", type_=sa.String(255))
    op.alter_column("feedback", "user_id", type_=sa.String(255))
    op.alter_column("alpha_users", "prod_user_id", type_=sa.String(255))

    # Remove is_alpha flag
    op.drop_column("users", "is_alpha")

    # Revert users.id to VARCHAR
    op.alter_column("users", "id", type_=sa.String(255))

    # Re-add original FK constraints
    op.create_foreign_key(
        "alpha_users_prod_user_id_fkey", "alpha_users", "users", ["prod_user_id"], ["id"]
    )
    op.create_foreign_key("feedback_user_id_fkey", "feedback", "users", ["user_id"], ["id"])
    op.create_foreign_key(
        "personality_profiles_user_id_fkey", "personality_profiles", "users", ["user_id"], ["id"]
    )
