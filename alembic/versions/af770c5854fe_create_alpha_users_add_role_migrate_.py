"""create_alpha_users_add_role_migrate_xian_alpha_issue_259

Revision ID: af770c5854fe
Revises: fcc1031179bb
Create Date: 2025-10-23 11:09:35.209794

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "af770c5854fe"
down_revision: Union[str, Sequence[str], None] = "fcc1031179bb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema.

    Issue #259: CORE-USER-ALPHA-TABLE

    Part 1: Add role column to users table (for Issue #261 superuser support)
    Part 2: Create alpha_users table for alpha testers
    Part 3: Migrate xian-alpha from users → alpha_users
    """

    # Part 1: Add role column to users table
    op.add_column("users", sa.Column("role", sa.String(50), nullable=False, server_default="user"))
    op.create_index("idx_users_role", "users", ["role"])

    # Part 2: Create alpha_users table
    op.create_table(
        "alpha_users",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("username", sa.String(50), unique=True, nullable=False),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("display_name", sa.String(100)),
        # Auth fields (preserved from users table)
        sa.Column("password_hash", sa.String(500)),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("is_verified", sa.Boolean, nullable=False, server_default="false"),
        # Timestamps (preserved from users table)
        sa.Column(
            "created_at", sa.TIMESTAMP, nullable=False, server_default=sa.func.current_timestamp()
        ),
        sa.Column(
            "updated_at", sa.TIMESTAMP, nullable=False, server_default=sa.func.current_timestamp()
        ),
        sa.Column("last_login_at", sa.TIMESTAMP),
        # Alpha-specific fields
        sa.Column("alpha_wave", sa.Integer, server_default="2"),
        sa.Column("test_start_date", sa.TIMESTAMP, server_default=sa.func.current_timestamp()),
        sa.Column("test_end_date", sa.TIMESTAMP),
        sa.Column("migrated_to_prod", sa.Boolean, server_default="false"),
        sa.Column("migration_date", sa.TIMESTAMP),
        sa.Column("prod_user_id", sa.String(255), sa.ForeignKey("users.id")),
        # Preferences (JSONB for flexibility)
        sa.Column(
            "preferences", sa.dialects.postgresql.JSONB, server_default=sa.text("'{}'::jsonb")
        ),
        sa.Column(
            "learning_data", sa.dialects.postgresql.JSONB, server_default=sa.text("'{}'::jsonb")
        ),
        # Metadata
        sa.Column("notes", sa.Text),
        sa.Column("feedback_count", sa.Integer, server_default="0"),
        sa.Column("last_active", sa.TIMESTAMP),
    )

    # Create indexes for alpha_users
    op.create_index("idx_alpha_users_username", "alpha_users", ["username"])
    op.create_index("idx_alpha_users_email", "alpha_users", ["email"])
    op.create_index("idx_alpha_users_alpha_wave", "alpha_users", ["alpha_wave"])
    op.create_index("idx_alpha_users_migrated", "alpha_users", ["migrated_to_prod"])
    op.create_index(
        "idx_alpha_users_prod_user",
        "alpha_users",
        ["prod_user_id"],
        postgresql_where=sa.text("prod_user_id IS NOT NULL"),
    )
    op.create_index(
        "idx_alpha_users_last_active",
        "alpha_users",
        ["last_active"],
        postgresql_where=sa.text("last_active IS NOT NULL"),
    )

    # Part 3: Migrate xian-alpha from users → alpha_users
    # This is a data migration, executed via SQL
    conn = op.get_bind()

    # Copy xian-alpha to alpha_users
    conn.execute(
        sa.text(
            """
        INSERT INTO alpha_users (
            id,
            username,
            email,
            display_name,
            password_hash,
            is_active,
            is_verified,
            created_at,
            updated_at,
            last_login_at,
            alpha_wave,
            test_start_date,
            notes
        )
        SELECT
            id::uuid,
            username,
            email,
            username as display_name,
            password_hash,
            is_active,
            is_verified,
            created_at,
            updated_at,
            last_login_at,
            2 as alpha_wave,
            created_at as test_start_date,
            'Migrated from users table during Sprint A7 Issue #259' as notes
        FROM users
        WHERE username = 'xian-alpha'
    """
        )
    )

    # Verify migration succeeded
    result = conn.execute(sa.text("SELECT COUNT(*) FROM alpha_users WHERE username = 'xian-alpha'"))
    count = result.scalar()

    if count == 0:
        raise Exception("Migration failed: xian-alpha not found in alpha_users")

    print(f"✅ Migration successful: xian-alpha found in alpha_users (count={count})")

    # Rename xian-alpha in users table to prevent username conflicts
    # We can't DELETE due to FK constraints (audit_logs, user_api_keys reference users.id)
    # Instead, we rename and mark inactive so authentication will check alpha_users first
    # The alpha_users.xian-alpha is now the canonical active account
    conn.execute(
        sa.text(
            """
        UPDATE users
        SET username = 'xian-alpha.migrated',
            is_active = false
        WHERE username = 'xian-alpha'
    """
        )
    )


def downgrade() -> None:
    """Downgrade schema.

    Reverse Issue #259 changes:
    - Migrate xian-alpha back to users table
    - Drop alpha_users table
    - Remove role column from users
    """

    conn = op.get_bind()

    # Part 1: Migrate xian-alpha back to users table (if exists)
    result = conn.execute(sa.text("SELECT COUNT(*) FROM alpha_users WHERE username = 'xian-alpha'"))
    if result.scalar() > 0:
        conn.execute(
            sa.text(
                """
            INSERT INTO users (
                id,
                username,
                email,
                password_hash,
                is_active,
                is_verified,
                created_at,
                updated_at,
                last_login_at
            )
            SELECT
                id::varchar,
                username,
                email,
                password_hash,
                is_active,
                is_verified,
                created_at,
                updated_at,
                last_login_at
            FROM alpha_users
            WHERE username = 'xian-alpha'
        """
            )
        )

    # Part 2: Drop alpha_users table and indexes
    op.drop_index("idx_alpha_users_last_active", "alpha_users")
    op.drop_index("idx_alpha_users_prod_user", "alpha_users")
    op.drop_index("idx_alpha_users_migrated", "alpha_users")
    op.drop_index("idx_alpha_users_alpha_wave", "alpha_users")
    op.drop_index("idx_alpha_users_email", "alpha_users")
    op.drop_index("idx_alpha_users_username", "alpha_users")
    op.drop_table("alpha_users")

    # Part 3: Remove role column from users
    op.drop_index("idx_users_role", "users")
    op.drop_column("users", "role")
