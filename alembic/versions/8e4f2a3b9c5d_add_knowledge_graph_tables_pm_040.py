"""Add knowledge graph tables for PM-040

Revision ID: 8e4f2a3b9c5d
Revises: d685380d5c5f
Create Date: 2025-08-04 16:21:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8e4f2a3b9c5d"
down_revision: Union[str, Sequence[str], None] = "d685380d5c5f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create NodeType enum
    nodetype_enum = postgresql.ENUM(
        "CONCEPT",
        "DOCUMENT",
        "PERSON",
        "ORGANIZATION",
        "TECHNOLOGY",
        "PROCESS",
        "METRIC",
        "EVENT",
        "RELATIONSHIP",
        "CUSTOM",
        name="nodetype",
    )
    nodetype_enum.create(op.get_bind())

    # Create EdgeType enum
    edgetype_enum = postgresql.ENUM(
        "REFERENCES",
        "DEPENDS_ON",
        "IMPLEMENTS",
        "MEASURES",
        "INVOLVES",
        "TRIGGERS",
        "ENHANCES",
        "REPLACES",
        "SUPPORTS",
        "CUSTOM",
        name="edgetype",
    )
    edgetype_enum.create(op.get_bind())

    # Create knowledge_nodes table
    op.create_table(
        "knowledge_nodes",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "node_type",
            sa.Enum(
                "CONCEPT",
                "DOCUMENT",
                "PERSON",
                "ORGANIZATION",
                "TECHNOLOGY",
                "PROCESS",
                "METRIC",
                "EVENT",
                "RELATIONSHIP",
                "CUSTOM",
                name="nodetype",
            ),
            nullable=False,
        ),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("node_metadata", sa.JSON(), nullable=True),
        sa.Column("properties", sa.JSON(), nullable=True),
        sa.Column("session_id", sa.String(), nullable=True),
        sa.Column(
            "embedding_vector", postgresql.ARRAY(sa.Float), nullable=True
        ),  # For future pgvector support
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create knowledge_edges table
    op.create_table(
        "knowledge_edges",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("source_node_id", sa.String(), nullable=False),
        sa.Column("target_node_id", sa.String(), nullable=False),
        sa.Column(
            "edge_type",
            sa.Enum(
                "REFERENCES",
                "DEPENDS_ON",
                "IMPLEMENTS",
                "MEASURES",
                "INVOLVES",
                "TRIGGERS",
                "ENHANCES",
                "REPLACES",
                "SUPPORTS",
                "CUSTOM",
                name="edgetype",
            ),
            nullable=False,
        ),
        sa.Column("weight", sa.Float(), nullable=True),
        sa.Column("node_metadata", sa.JSON(), nullable=True),
        sa.Column("properties", sa.JSON(), nullable=True),
        sa.Column("session_id", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["source_node_id"],
            ["knowledge_nodes.id"],
        ),
        sa.ForeignKeyConstraint(
            ["target_node_id"],
            ["knowledge_nodes.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create efficient indexes for graph traversal
    op.create_index("idx_nodes_session", "knowledge_nodes", ["session_id"], unique=False)
    op.create_index("idx_nodes_type", "knowledge_nodes", ["node_type"], unique=False)
    op.create_index("idx_nodes_name", "knowledge_nodes", ["name"], unique=False)

    op.create_index("idx_edges_source", "knowledge_edges", ["source_node_id"], unique=False)
    op.create_index("idx_edges_target", "knowledge_edges", ["target_node_id"], unique=False)
    op.create_index("idx_edges_type", "knowledge_edges", ["edge_type"], unique=False)
    op.create_index("idx_edges_session", "knowledge_edges", ["session_id"], unique=False)
    op.create_index(
        "idx_edges_source_target",
        "knowledge_edges",
        ["source_node_id", "target_node_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop indexes
    op.drop_index("idx_edges_source_target", table_name="knowledge_edges")
    op.drop_index("idx_edges_session", table_name="knowledge_edges")
    op.drop_index("idx_edges_type", table_name="knowledge_edges")
    op.drop_index("idx_edges_target", table_name="knowledge_edges")
    op.drop_index("idx_edges_source", table_name="knowledge_edges")

    op.drop_index("idx_nodes_name", table_name="knowledge_nodes")
    op.drop_index("idx_nodes_type", table_name="knowledge_nodes")
    op.drop_index("idx_nodes_session", table_name="knowledge_nodes")

    # Drop tables
    op.drop_table("knowledge_edges")
    op.drop_table("knowledge_nodes")

    # Drop enums
    op.execute("DROP TYPE IF EXISTS edgetype")
    op.execute("DROP TYPE IF EXISTS nodetype")
