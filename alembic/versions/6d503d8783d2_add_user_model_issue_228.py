"""add_user_model_issue_228

Revision ID: 6d503d8783d2
Revises: 68767106bfb6
Create Date: 2025-10-22 07:20:22.573555

Create User model and integrate with existing models.

Steps:
1. Create users table with indexes
2. Populate users table from existing user_id values
3. Add FK constraints to personality_profiles
4. Add FK constraints to token_blacklist
5. Alter feedback.user_id column type and add FK constraint

Issue #228 CORE-USERS-API Phase 1A
"""

from datetime import datetime
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy import text

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6d503d8783d2"
down_revision: Union[str, Sequence[str], None] = "68767106bfb6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Create User model and integrate with existing models.

    Steps:
    1. Create users table with indexes
    2. Populate users table from existing user_id values
    3. Add FK constraints to personality_profiles
    4. Add FK constraints to token_blacklist
    5. Alter feedback.user_id column type and add FK constraint
    """

    # Step 1: Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.String(255), nullable=False),
        sa.Column("username", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(500), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.Column("last_login_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create indexes on users table
    op.create_index("idx_users_username", "users", ["username"], unique=True)
    op.create_index("idx_users_email", "users", ["email"], unique=True)
    op.create_index("idx_users_active", "users", ["is_active"], unique=False)

    # Step 2: Populate users table from existing user_id values
    # Get connection for raw SQL
    connection = op.get_bind()

    # Get unique user_ids from personality_profiles
    result = connection.execute(
        text("SELECT DISTINCT user_id FROM personality_profiles WHERE user_id IS NOT NULL")
    )
    personality_user_ids = [row[0] for row in result]

    # Get unique user_ids from feedback (if any)
    try:
        result = connection.execute(
            text(
                "SELECT DISTINCT user_id FROM feedback WHERE user_id IS NOT NULL AND user_id != ''"
            )
        )
        feedback_user_ids = [row[0] for row in result]
    except Exception:
        # Feedback table might not have data or column might not exist yet
        feedback_user_ids = []

    # Combine and deduplicate
    all_user_ids = list(set(personality_user_ids + feedback_user_ids))

    # Create User records for each unique user_id
    for user_id in all_user_ids:
        connection.execute(
            text(
                """
                INSERT INTO users (id, username, email, is_active, is_verified, created_at, updated_at)
                VALUES (:id, :username, :email, :is_active, :is_verified, :created_at, :updated_at)
                """
            ),
            {
                "id": user_id,
                "username": user_id,  # Use user_id as username initially
                "email": f"{user_id}@example.com",  # Placeholder email
                "is_active": True,
                "is_verified": False,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            },
        )

    # Step 3: Add FK constraint to personality_profiles
    op.create_foreign_key(
        "fk_personality_profiles_user_id",
        "personality_profiles",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",  # If user deleted, delete profiles
    )

    # Step 4: Add FK constraint to token_blacklist
    op.create_foreign_key(
        "fk_token_blacklist_user_id",
        "token_blacklist",
        "users",
        ["user_id"],
        ["id"],
        ondelete="SET NULL",  # If user deleted, set user_id to NULL
    )

    # Step 5: Alter feedback.user_id column type and add FK
    # First, alter column type from String to String(255)
    op.alter_column(
        "feedback",
        "user_id",
        type_=sa.String(255),
        existing_type=sa.String(),
        existing_nullable=True,
    )

    # Then add FK constraint
    op.create_foreign_key(
        "fk_feedback_user_id",
        "feedback",
        "users",
        ["user_id"],
        ["id"],
        ondelete="SET NULL",  # If user deleted, set user_id to NULL
    )


def downgrade() -> None:
    """
    Remove User model and FK constraints.

    Rollback steps in reverse order.
    """

    # Step 5 rollback: Drop FK from feedback and restore column type
    op.drop_constraint("fk_feedback_user_id", "feedback", type_="foreignkey")
    op.alter_column(
        "feedback",
        "user_id",
        type_=sa.String(),
        existing_type=sa.String(255),
        existing_nullable=True,
    )

    # Step 4 rollback: Drop FK from token_blacklist
    op.drop_constraint("fk_token_blacklist_user_id", "token_blacklist", type_="foreignkey")

    # Step 3 rollback: Drop FK from personality_profiles
    op.drop_constraint(
        "fk_personality_profiles_user_id", "personality_profiles", type_="foreignkey"
    )

    # Step 2 rollback: No action needed (users table will be dropped)

    # Step 1 rollback: Drop users table and indexes
    op.drop_index("idx_users_active", table_name="users")
    op.drop_index("idx_users_email", table_name="users")
    op.drop_index("idx_users_username", table_name="users")
    op.drop_table("users")
