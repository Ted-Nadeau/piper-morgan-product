"""UUID Migration Step 2: Convert column types to UUID (Issue #262 + #291)

This is Part 2 of a 3-part decomposition of the original d8aeb665e878 migration.

Step 1 (d8aeb665e878a) dropped all FK constraints that reference users table.
This step converts the column types safely without FK constraint conflicts.

Operations:
1. Convert users.id from VARCHAR to UUID
2. Add is_alpha flag to users table
3. Migrate alpha_users data to users table (if it exists)
4. Convert all FK columns to UUID:
   - feedback.user_id
   - personality_profiles.user_id
   - token_blacklist.user_id
   - user_api_keys.user_id
   - audit_logs.user_id
   - alpha_users.prod_user_id

Revision ID: d8aeb665e878b
Revises: d8aeb665e878a
Create Date: 2025-11-22 16:50:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d8aeb665e878b"
down_revision: Union[str, Sequence[str], None] = "d8aeb665e878a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Convert column types from VARCHAR to UUID.

    Safe to run after Step 1 (FK constraints dropped).
    Enables Step 3 to re-add constraints with matching types.
    """

    conn = op.get_bind()

    print("Step 2: Converting column types to UUID...")

    # Step 1: Convert users.id to UUID (table may be empty on fresh DB)
    # First drop the old default, delete data that can't be converted, then convert type
    print("Converting users.id to UUID...")
    conn.execute(sa.text("ALTER TABLE users ALTER COLUMN id DROP DEFAULT;"))

    # Delete any rows that have non-UUID id values (like "system_default")
    # Keep only rows with valid UUID-like values or NULL
    # UUIDs are 36 chars: 8-4-4-4-12 hex digits with dashes
    uuid_pattern = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"

    # Clean up users table
    conn.execute(
        sa.text(
            f"""
        DELETE FROM users
        WHERE id IS NOT NULL
        AND id !~ '{uuid_pattern}';
    """
        )
    )

    conn.execute(
        sa.text(
            """
        ALTER TABLE users
        ALTER COLUMN id TYPE uuid USING COALESCE(id::uuid, gen_random_uuid());
    """
        )
    )
    conn.execute(sa.text("ALTER TABLE users ALTER COLUMN id SET DEFAULT gen_random_uuid();"))

    # Clean up FK columns before converting their types
    print("  - Cleaning non-UUID values from FK columns...")
    conn.execute(
        sa.text(
            f"""
        DELETE FROM feedback
        WHERE user_id IS NOT NULL
        AND user_id !~ '{uuid_pattern}';
    """
        )
    )
    conn.execute(
        sa.text(
            f"""
        DELETE FROM personality_profiles
        WHERE user_id IS NOT NULL
        AND user_id !~ '{uuid_pattern}';
    """
        )
    )
    conn.execute(
        sa.text(
            f"""
        DELETE FROM token_blacklist
        WHERE user_id IS NOT NULL
        AND user_id !~ '{uuid_pattern}';
    """
        )
    )
    conn.execute(
        sa.text(
            f"""
        DELETE FROM user_api_keys
        WHERE user_id IS NOT NULL
        AND user_id !~ '{uuid_pattern}';
    """
        )
    )

    # Step 2: Add is_alpha flag to users
    print("Adding is_alpha flag to users...")
    op.add_column(
        "users", sa.Column("is_alpha", sa.Boolean(), nullable=False, server_default="false")
    )

    # Step 3: Migrate alpha_users data into users (if alpha_users table still exists)
    # This conditional handles both fresh DB (no alpha_users) and existing DB
    print("Migrating alpha_users data to users (if table exists)...")
    conn.execute(
        sa.text(
            """
        DO $$
        BEGIN
            -- Check if alpha_users table exists before attempting migration
            IF EXISTS (SELECT 1 FROM information_schema.tables
                       WHERE table_name = 'alpha_users') THEN
                -- Migrate xian from alpha_users to users with is_alpha=true
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
                ON CONFLICT (id) DO NOTHING;  -- Skip if user already exists

                RAISE NOTICE 'Migrated xian alpha user to users table with is_alpha=true';
            ELSE
                RAISE NOTICE 'alpha_users table not found (expected on fresh DB)';
            END IF;
        END
        $$;
    """
        )
    )

    # Step 4: Convert all FK columns to UUID
    print("Converting FK columns to UUID...")

    # alpha_users.prod_user_id (will be dropped in Step 3, but convert for consistency)
    print("  - Converting alpha_users.prod_user_id...")
    conn.execute(
        sa.text(
            """
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM information_schema.tables
                       WHERE table_name = 'alpha_users'
                       AND EXISTS (SELECT 1 FROM information_schema.columns
                                   WHERE table_name = 'alpha_users'
                                   AND column_name = 'prod_user_id')) THEN
                ALTER TABLE alpha_users
                ALTER COLUMN prod_user_id TYPE uuid USING COALESCE(prod_user_id::uuid, gen_random_uuid());
                RAISE NOTICE 'Converted alpha_users.prod_user_id to UUID';
            ELSE
                RAISE NOTICE 'Skipping alpha_users.prod_user_id (table or column not found)';
            END IF;
        END
        $$;
    """
        )
    )

    # feedback.user_id - Use raw SQL
    print("  - Converting feedback.user_id...")
    conn.execute(
        sa.text(
            """
        ALTER TABLE feedback
        ALTER COLUMN user_id TYPE uuid USING COALESCE(user_id::uuid, NULL);
    """
        )
    )

    # personality_profiles.user_id - Use raw SQL
    print("  - Converting personality_profiles.user_id...")
    conn.execute(
        sa.text(
            """
        ALTER TABLE personality_profiles
        ALTER COLUMN user_id TYPE uuid USING COALESCE(user_id::uuid, NULL);
    """
        )
    )

    # token_blacklist.user_id - Use raw SQL
    print("  - Converting token_blacklist.user_id...")
    conn.execute(
        sa.text(
            """
        ALTER TABLE token_blacklist
        ALTER COLUMN user_id TYPE uuid USING COALESCE(user_id::uuid, NULL);
    """
        )
    )

    # user_api_keys.user_id - Use raw SQL
    print("  - Converting user_api_keys.user_id...")
    conn.execute(
        sa.text(
            """
        ALTER TABLE user_api_keys
        ALTER COLUMN user_id TYPE uuid USING COALESCE(user_id::uuid, NULL);
    """
        )
    )

    # audit_logs.user_id (has existing data but no valid user references) - Use raw SQL
    print("  - Converting audit_logs.user_id...")
    conn.execute(sa.text("DELETE FROM audit_logs WHERE user_id IS NOT NULL"))
    conn.execute(
        sa.text(
            """
        ALTER TABLE audit_logs
        ALTER COLUMN user_id TYPE uuid USING COALESCE(user_id::uuid, NULL);
    """
        )
    )

    # NOTE: todo_items, lists, and todo_lists use owner_id which contains
    # non-UUID values like "system", "test-user-integration", etc.
    # These are NOT user references and should remain VARCHAR.
    # DO NOT CONVERT these columns.

    # However, projects.owner_id IS a user reference and should be converted to UUID
    # (if projects table exists)
    print("  - Converting projects.owner_id (user reference)...")
    conn.execute(
        sa.text(
            """
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM information_schema.tables
                       WHERE table_name = 'projects') THEN
                IF EXISTS (SELECT 1 FROM information_schema.columns
                          WHERE table_name = 'projects'
                          AND column_name = 'owner_id') THEN
                    ALTER TABLE projects
                    ALTER COLUMN owner_id TYPE uuid USING COALESCE(owner_id::uuid, NULL);
                    RAISE NOTICE 'Converted projects.owner_id to UUID';
                ELSE
                    RAISE NOTICE 'Column owner_id not found in projects table';
                END IF;
            ELSE
                RAISE NOTICE 'Projects table not found (expected on fresh DB)';
            END IF;
        END
        $$;
    """
        )
    )

    print(
        "✅ All column type conversions complete (users.id, all FK columns, and projects.owner_id now UUID)"
    )


def downgrade() -> None:
    """Downgrade Step 2: Revert column type conversions.

    WARNING: This will lose the migrated alpha_users data in users table!
    For production, restore from backup instead.
    """

    print("Reverting column type conversions to VARCHAR...")

    conn = op.get_bind()

    # Revert FK columns back to VARCHAR using raw SQL
    print("  - Reverting audit_logs.user_id...")
    conn.execute(sa.text("ALTER TABLE audit_logs ALTER COLUMN user_id TYPE varchar(255)"))

    print("  - Reverting user_api_keys.user_id...")
    conn.execute(sa.text("ALTER TABLE user_api_keys ALTER COLUMN user_id TYPE varchar(255)"))

    print("  - Reverting token_blacklist.user_id...")
    conn.execute(sa.text("ALTER TABLE token_blacklist ALTER COLUMN user_id TYPE varchar(255)"))

    print("  - Reverting personality_profiles.user_id...")
    conn.execute(sa.text("ALTER TABLE personality_profiles ALTER COLUMN user_id TYPE varchar(255)"))

    print("  - Reverting feedback.user_id...")
    conn.execute(sa.text("ALTER TABLE feedback ALTER COLUMN user_id TYPE varchar(255)"))

    # Revert alpha_users.prod_user_id if table exists
    print("  - Reverting alpha_users.prod_user_id...")
    conn.execute(
        sa.text(
            """
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM information_schema.tables
                       WHERE table_name = 'alpha_users'
                       AND EXISTS (SELECT 1 FROM information_schema.columns
                                   WHERE table_name = 'alpha_users'
                                   AND column_name = 'prod_user_id')) THEN
                ALTER TABLE alpha_users
                ALTER COLUMN prod_user_id TYPE varchar(255);
                RAISE NOTICE 'Reverted alpha_users.prod_user_id to VARCHAR';
            END IF;
        END
        $$;
    """
        )
    )

    # Revert projects.owner_id if table exists
    print("  - Reverting projects.owner_id...")
    conn.execute(
        sa.text(
            """
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM information_schema.tables
                       WHERE table_name = 'projects'
                       AND EXISTS (SELECT 1 FROM information_schema.columns
                                   WHERE table_name = 'projects'
                                   AND column_name = 'owner_id')) THEN
                ALTER TABLE projects
                ALTER COLUMN owner_id TYPE varchar(255);
                RAISE NOTICE 'Reverted projects.owner_id to VARCHAR';
            END IF;
        END
        $$;
    """
        )
    )

    # Remove is_alpha flag
    print("  - Dropping is_alpha flag...")
    op.drop_column("users", "is_alpha")

    # Revert users.id to VARCHAR
    print("  - Reverting users.id to VARCHAR...")
    conn.execute(sa.text("ALTER TABLE users ALTER COLUMN id TYPE varchar(255)"))

    print("ℹ️ Step 2 downgrade complete (column types reverted to VARCHAR)")
