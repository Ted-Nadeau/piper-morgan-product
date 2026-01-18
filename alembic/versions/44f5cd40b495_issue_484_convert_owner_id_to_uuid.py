"""Issue #484: Convert owner_id columns to UUID with FK to users

This migration ensures type consistency across the codebase by converting
owner_id columns in lists and todo_items tables from VARCHAR to UUID,
with foreign key constraints to the users table.

NOTE: todo_lists was removed from this migration (2026-01-17) because the
todo_lists table was dropped and replaced by 'lists' in migration
6m5s5d1t6500 (Universal List Architecture, Aug 2025). Fresh database installs
would fail because todo_lists doesn't exist.

Background (Pattern-045 "Green Tests, Red User"):
- On Dec 7, 2025, 705 unit tests passed while all CRUD operations failed
- Root cause: Domain models used owner_id: UUID while some DB models used String
- This migration fixes the remaining 2 tables that still use VARCHAR

Operations:
1. Clean up orphaned data (non-UUID owner_ids and missing user references)
2. Convert VARCHAR columns to UUID type
3. Add foreign key constraints to users(id)

Tables affected:
- lists.owner_id: VARCHAR -> UUID with FK to users(id)
- todo_items.owner_id: VARCHAR -> UUID with FK to users(id)

Revision ID: 44f5cd40b495
Revises: 290e65593666
Create Date: 2026-01-03 19:16:20.872123

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "44f5cd40b495"
down_revision: Union[str, Sequence[str], None] = "290e65593666"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# UUID regex pattern for PostgreSQL
UUID_PATTERN = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"


def upgrade() -> None:
    """Convert owner_id columns from VARCHAR to UUID with FK constraints.

    Strategy:
    1. Delete rows with non-UUID owner_id values (test data like "system", "test_user")
    2. Delete rows with UUID owner_id that don't exist in users table (orphaned data)
    3. Convert column type from VARCHAR to UUID
    4. Add foreign key constraint to users(id)
    """
    conn = op.get_bind()

    print("Issue #484: Converting owner_id columns to UUID...")

    # ============================================================
    # Table 1: todo_items (inherits from items, so also affects items table)
    # ============================================================
    print("  Processing todo_items...")

    # Step 1a: Delete non-UUID values
    result = conn.execute(
        sa.text(
            f"""
            DELETE FROM todo_items
            WHERE owner_id IS NOT NULL
            AND owner_id !~ '{UUID_PATTERN}';
        """
        )
    )
    print(f"    - Deleted {result.rowcount} rows with non-UUID owner_id")

    # Step 1b: Delete orphaned references (UUID doesn't exist in users)
    result = conn.execute(
        sa.text(
            """
            DELETE FROM todo_items
            WHERE owner_id IS NOT NULL
            AND owner_id::uuid NOT IN (SELECT id FROM users);
        """
        )
    )
    print(f"    - Deleted {result.rowcount} rows with orphaned owner_id")

    # Step 1c: Convert VARCHAR to UUID
    conn.execute(
        sa.text(
            """
            ALTER TABLE todo_items
            ALTER COLUMN owner_id TYPE uuid USING owner_id::uuid;
        """
        )
    )
    print("    - Converted owner_id to UUID type")

    # Step 1d: Add FK constraint
    conn.execute(
        sa.text(
            """
            ALTER TABLE todo_items
            ADD CONSTRAINT fk_todo_items_owner_id
            FOREIGN KEY (owner_id) REFERENCES users(id);
        """
        )
    )
    print("    - Added FK constraint to users(id)")

    # ============================================================
    # Table 2: lists
    # ============================================================
    print("  Processing lists...")

    # Step 2a: Delete non-UUID values
    result = conn.execute(
        sa.text(
            f"""
            DELETE FROM lists
            WHERE owner_id IS NOT NULL
            AND owner_id !~ '{UUID_PATTERN}';
        """
        )
    )
    print(f"    - Deleted {result.rowcount} rows with non-UUID owner_id")

    # Step 2b: Delete orphaned references
    result = conn.execute(
        sa.text(
            """
            DELETE FROM lists
            WHERE owner_id IS NOT NULL
            AND owner_id::uuid NOT IN (SELECT id FROM users);
        """
        )
    )
    print(f"    - Deleted {result.rowcount} rows with orphaned owner_id")

    # Step 2c: Convert VARCHAR to UUID
    conn.execute(
        sa.text(
            """
            ALTER TABLE lists
            ALTER COLUMN owner_id TYPE uuid USING owner_id::uuid;
        """
        )
    )
    print("    - Converted owner_id to UUID type")

    # Step 2d: Add FK constraint
    conn.execute(
        sa.text(
            """
            ALTER TABLE lists
            ADD CONSTRAINT fk_lists_owner_id
            FOREIGN KEY (owner_id) REFERENCES users(id);
        """
        )
    )
    print("    - Added FK constraint to users(id)")

    # NOTE: todo_lists section removed - table was dropped in migration
    # 6m5s5d1t6500 and replaced by 'lists' (already handled above)

    print("Issue #484: Migration complete!")


def downgrade() -> None:
    """Revert owner_id columns back to VARCHAR.

    Note: This will drop FK constraints and convert types back,
    but CANNOT restore deleted orphaned data.
    """
    conn = op.get_bind()

    print("Issue #484: Reverting owner_id columns to VARCHAR...")

    # todo_items
    conn.execute(
        sa.text(
            """
            ALTER TABLE todo_items
            DROP CONSTRAINT IF EXISTS fk_todo_items_owner_id;
        """
        )
    )
    conn.execute(
        sa.text(
            """
            ALTER TABLE todo_items
            ALTER COLUMN owner_id TYPE varchar USING owner_id::text;
        """
        )
    )

    # lists
    conn.execute(
        sa.text(
            """
            ALTER TABLE lists
            DROP CONSTRAINT IF EXISTS fk_lists_owner_id;
        """
        )
    )
    conn.execute(
        sa.text(
            """
            ALTER TABLE lists
            ALTER COLUMN owner_id TYPE varchar USING owner_id::text;
        """
        )
    )

    # NOTE: todo_lists section removed - table doesn't exist
    # (was dropped in migration 6m5s5d1t6500)

    print("Issue #484: Downgrade complete (orphaned data not restored)")
