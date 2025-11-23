"""UUID Migration Step 1: Drop FK constraints (Issue #262 + #291)

This is Part 1 of a 3-part decomposition of the original d8aeb665e878 migration.

Original migration tried to do too much in one transaction, causing type mismatch
errors when converting column types with FK constraints present.

This step ONLY drops the FK constraints, making subsequent steps safe.

Uses direct SQL to drop all known FK constraints that reference users.id.

Revision ID: d8aeb665e878a
Revises: 234aa8ec628c
Create Date: 2025-11-22 16:50:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d8aeb665e878a"
down_revision: Union[str, Sequence[str], None] = "234aa8ec628c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Drop all FK constraints that reference users table.

    These constraints block column type changes in the next steps.
    Drops all FK constraints where a column references users.id.
    """

    conn = op.get_bind()

    print("Step 1: Dropping all FK constraints that reference users table...")

    # List of known tables that have FK constraints to users.id
    tables_with_fk = [
        "feedback",
        "personality_profiles",
        "token_blacklist",
        "user_api_keys",
        "audit_logs",
        "alpha_users",  # prod_user_id FK
    ]

    constraints_dropped = 0

    # Drop all FK constraints from each table
    for table_name in tables_with_fk:
        # Get all FK constraints for this table
        sql_query = """
        SELECT constraint_name
        FROM information_schema.table_constraints
        WHERE constraint_type = 'FOREIGN KEY'
        AND table_schema = 'public'
        AND table_name = :table_name;
        """

        result = conn.execute(sa.text(sql_query), {"table_name": table_name})
        constraints = result.fetchall()

        # Drop each constraint
        for (constraint_name,) in constraints:
            try:
                drop_sql = f'ALTER TABLE "{table_name}" DROP CONSTRAINT "{constraint_name}";'
                conn.execute(sa.text(drop_sql))
                print(f"  ✓ Dropped FK: {table_name}.{constraint_name}")
                constraints_dropped += 1
            except Exception as e:
                # Constraint might not exist on fresh database, which is fine
                pass

    print(f"✅ Dropped {constraints_dropped} FK constraints")


def downgrade() -> None:
    """Downgrade Step 1: No action needed.

    FK constraints will be re-added by Step 3 if we downgrade past it.
    Since Step 1 only drops constraints, downgrading it means they stay dropped
    until someone explicitly runs Step 3 upward again.
    """
    print("ℹ️ Step 1 downgrade: FK constraints remain dropped (will be re-added by Step 3 upgrade)")
