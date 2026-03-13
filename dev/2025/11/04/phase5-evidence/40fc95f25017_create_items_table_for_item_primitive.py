"""create_items_table_for_item_primitive

Revision ID: 40fc95f25017
Revises: f95913b7e3fd
Create Date: 2025-11-03 17:04:03.142998

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "40fc95f25017"
down_revision: Union[str, Sequence[str], None] = "f95913b7e3fd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Create items table as base for polymorphic inheritance.

    Phase 1: Create empty items table with base fields
    Phase 2: (Future) Migrate todos to items + todo_items structure

    NOTE: This migration creates the table structure but does NOT migrate
    existing todo data. That happens in Phase 2 when Todo extends Item.
    """

    # Create items base table
    op.create_table(
        "items",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("text", sa.String(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("list_id", sa.String(), nullable=True),
        sa.Column("item_type", sa.String(50), nullable=False, server_default="item"),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")
        ),
        sa.Column(
            "updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")
        ),
        sa.PrimaryKeyConstraint("id", name="pk_items"),
    )

    # Create performance indexes (matching ItemDB.__table_args__)
    op.create_index("idx_items_list_id", "items", ["list_id"])
    op.create_index("idx_items_item_type", "items", ["item_type"])
    op.create_index("idx_items_list_position", "items", ["list_id", "position"])
    op.create_index("idx_items_created", "items", ["created_at"])


def downgrade() -> None:
    """Remove items table (safe rollback)."""
    # Drop indexes first
    op.drop_index("idx_items_created", table_name="items")
    op.drop_index("idx_items_list_position", table_name="items")
    op.drop_index("idx_items_item_type", table_name="items")
    op.drop_index("idx_items_list_id", table_name="items")

    # Drop table
    op.drop_table("items")
