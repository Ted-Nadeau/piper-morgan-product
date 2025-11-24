"""UUID Migration Step 3: Re-add FK constraints and cleanup (Issue #262 + #291)

This is Part 3 of a 3-part decomposition of the original d8aeb665e878 migration.

Step 1 (d8aeb665e878a) dropped all FK constraints.
Step 2 (d8aeb665e878b) converted column types to UUID.
This step re-adds constraints with matching types and drops the alpha_users table.

Operations:
1. Re-add all FK constraints with CASCADE delete
2. Add new token_blacklist FK constraint (Issue #291)
3. Drop alpha_users table (data migrated to users in Step 2)

Revision ID: d8aeb665e878c
Revises: d8aeb665e878b
Create Date: 2025-11-22 16:50:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d8aeb665e878c"
down_revision: Union[str, Sequence[str], None] = "d8aeb665e878b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Re-add FK constraints with UUID types and drop alpha_users table.

    All constraints now have matching types (both sides are UUID).
    Safe to re-add after Step 2 (column types converted).
    """

    conn = op.get_bind()

    print("Step 3: Re-adding FK constraints with UUID types...")

    # Step 1: Re-add FK constraints with CASCADE delete
    print("Re-adding FK constraints...")

    # feedback.user_id -> users.id FK
    print("  - Adding feedback_user_id_fkey...")
    op.create_foreign_key(
        "feedback_user_id_fkey",
        "feedback",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # personality_profiles.user_id -> users.id FK
    print("  - Adding personality_profiles_user_id_fkey...")
    op.create_foreign_key(
        "personality_profiles_user_id_fkey",
        "personality_profiles",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Step 2: Add NEW FK constraint for token_blacklist (Issue #291)
    # This was missing entirely before UUID migration
    print("  - Adding token_blacklist_user_id_fkey (Issue #291)...")
    op.create_foreign_key(
        "token_blacklist_user_id_fkey",
        "token_blacklist",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # user_api_keys.user_id -> users.id FK (not dropped in Step 1, but re-add for consistency)
    print("  - Adding user_api_keys_user_id_fkey...")
    op.create_foreign_key(
        "user_api_keys_user_id_fkey",
        "user_api_keys",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # audit_logs.user_id -> users.id FK (if it still exists)
    print("  - Adding audit_logs_user_id_fkey (if table exists)...")
    conn.execute(
        sa.text(
            """
        DO $$
        BEGIN
            -- Only add constraint if table exists (may have been dropped elsewhere)
            IF EXISTS (SELECT 1 FROM information_schema.tables
                       WHERE table_name = 'audit_logs') THEN
                IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints
                              WHERE constraint_name = 'audit_logs_user_id_fkey'
                              AND table_name = 'audit_logs') THEN
                    ALTER TABLE audit_logs
                    ADD CONSTRAINT audit_logs_user_id_fkey
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
                    RAISE NOTICE 'Added audit_logs_user_id_fkey';
                ELSE
                    RAISE NOTICE 'audit_logs_user_id_fkey already exists';
                END IF;
            ELSE
                RAISE NOTICE 'audit_logs table not found (expected if dropped earlier)';
            END IF;
        END
        $$;
    """
        )
    )

    # Step 3: Drop alpha_users table (data migrated to users with is_alpha=true)
    print("Dropping alpha_users table (data migrated to users)...")
    conn.execute(
        sa.text(
            """
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM information_schema.tables
                       WHERE table_name = 'alpha_users') THEN
                DROP TABLE IF EXISTS alpha_users CASCADE;
                RAISE NOTICE 'Dropped alpha_users table';
            ELSE
                RAISE NOTICE 'alpha_users table not found (expected on fresh DB)';
            END IF;
        END
        $$;
    """
        )
    )

    print("✅ All FK constraints re-added with UUID types and alpha_users table dropped")


def downgrade() -> None:
    """Downgrade Step 3: Recreate alpha_users table and drop FK constraints.

    WARNING: This will lose the is_alpha flag values assigned in Step 2!
    For production, restore from backup instead.
    """

    print("Reverting Step 3 changes...")

    # Step 1: Recreate alpha_users table structure (basic version)
    print("Recreating alpha_users table...")
    op.create_table(
        "alpha_users",
        sa.Column("id", sa.String(), primary_key=True),
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

    # Step 2: Drop FK constraints
    print("Dropping FK constraints...")
    op.drop_constraint("audit_logs_user_id_fkey", "audit_logs", type_="foreignkey")
    op.drop_constraint("user_api_keys_user_id_fkey", "user_api_keys", type_="foreignkey")
    op.drop_constraint("token_blacklist_user_id_fkey", "token_blacklist", type_="foreignkey")
    op.drop_constraint(
        "personality_profiles_user_id_fkey", "personality_profiles", type_="foreignkey"
    )
    op.drop_constraint("feedback_user_id_fkey", "feedback", type_="foreignkey")

    print("ℹ️ Step 3 downgrade complete (FK constraints dropped, alpha_users recreated)")
