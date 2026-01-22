"""MUX-MULTICHAT-PHASE0: Add conversation graph primitives

Issue #601: Schema design for conversation graph per ADR-050.

This migration adds:
1. parent_id column to conversation_turns for threading
2. conversation_links table for explicit relationships

Phase 0: Schema design only - migration file created but NOT APPLIED.
Apply in Phase 1 when implementation begins.

Revision ID: 601_phase0_graph
Revises: 336bd317e5cc
Create Date: 2026-01-22

"""

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "601_phase0_graph"
down_revision = "336bd317e5cc"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add conversation graph primitives.

    1. Add parent_id to conversation_turns for simple threading
    2. Create conversation_links table for explicit relationships
    """
    # 1. Add parent_id column to conversation_turns
    op.add_column(
        "conversation_turns",
        sa.Column(
            "parent_id",
            sa.String(),
            sa.ForeignKey("conversation_turns.id", ondelete="SET NULL"),
            nullable=True,
            comment="Parent turn ID for threading (self-referential FK)",
        ),
    )

    # Index for thread traversal queries
    op.create_index(
        "idx_conversation_turns_parent",
        "conversation_turns",
        ["parent_id"],
        unique=False,
    )

    # 2. Create conversation_links table
    op.create_table(
        "conversation_links",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("conversation_id", sa.String(), nullable=False),
        sa.Column("source_id", sa.String(), nullable=False),
        sa.Column("target_id", sa.String(), nullable=False),
        sa.Column(
            "link_type",
            sa.String(),
            nullable=False,
            comment="ConversationLinkType enum value or custom type",
        ),
        sa.Column(
            "additional_types",
            postgresql.JSONB(),
            nullable=False,
            server_default="[]",
            comment="For multi-type links per ADR-050",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "created_by",
            sa.String(),
            nullable=True,
            comment="User or system that created the link",
        ),
        # Foreign key constraints
        sa.ForeignKeyConstraint(
            ["conversation_id"],
            ["conversations.id"],
            ondelete="CASCADE",
            name="fk_conversation_links_conversation",
        ),
        sa.ForeignKeyConstraint(
            ["source_id"],
            ["conversation_turns.id"],
            ondelete="CASCADE",
            name="fk_conversation_links_source",
        ),
        sa.ForeignKeyConstraint(
            ["target_id"],
            ["conversation_turns.id"],
            ondelete="CASCADE",
            name="fk_conversation_links_target",
        ),
        # Check constraint: no self-links
        sa.CheckConstraint(
            "source_id != target_id",
            name="chk_conversation_links_no_self_link",
        ),
    )

    # Indexes for common query patterns
    op.create_index(
        "idx_conversation_links_conversation",
        "conversation_links",
        ["conversation_id"],
        unique=False,
    )
    op.create_index(
        "idx_conversation_links_source",
        "conversation_links",
        ["source_id"],
        unique=False,
    )
    op.create_index(
        "idx_conversation_links_target",
        "conversation_links",
        ["target_id"],
        unique=False,
    )
    op.create_index(
        "idx_conversation_links_type",
        "conversation_links",
        ["link_type"],
        unique=False,
    )
    # Composite index for "find all links of type X in conversation Y"
    op.create_index(
        "idx_conversation_links_conv_type",
        "conversation_links",
        ["conversation_id", "link_type"],
        unique=False,
    )


def downgrade() -> None:
    """Remove conversation graph primitives."""
    # Drop conversation_links table and all its indexes
    op.drop_index("idx_conversation_links_conv_type", table_name="conversation_links")
    op.drop_index("idx_conversation_links_type", table_name="conversation_links")
    op.drop_index("idx_conversation_links_target", table_name="conversation_links")
    op.drop_index("idx_conversation_links_source", table_name="conversation_links")
    op.drop_index("idx_conversation_links_conversation", table_name="conversation_links")
    op.drop_table("conversation_links")

    # Drop parent_id from conversation_turns
    op.drop_index("idx_conversation_turns_parent", table_name="conversation_turns")
    op.drop_column("conversation_turns", "parent_id")
