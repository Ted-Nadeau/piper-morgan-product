#!/usr/bin/env python3
"""
Create Knowledge Graph Database Tables
Issue #99 - CORE-KNOW Phase 1

Uses SQLAlchemy's Base.metadata.create_all() to create tables from existing models.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from services.database.connection import db
from services.database.models import KnowledgeEdgeDB, KnowledgeNodeDB


async def create_knowledge_graph_tables():
    """Create knowledge graph tables in PostgreSQL"""
    print("=" * 70)
    print("Knowledge Graph Database Tables Creation")
    print("Issue #99 - CORE-KNOW Phase 1")
    print("=" * 70)
    print()

    try:
        # Initialize database connection
        print("📡 Connecting to PostgreSQL...")
        await db.initialize()
        print(f"✅ Connected to: {db._build_database_url().split('@')[1]}")  # Hide password
        print()

        # Create all tables (will skip existing tables)
        print("🗄️  Creating Knowledge Graph tables...")
        print("   - knowledge_nodes (with indexes)")
        print("   - knowledge_edges (with indexes)")
        print()

        await db.create_tables()

        print("✅ Knowledge Graph tables created successfully!")
        print()

        # Verify tables exist
        print("🔍 Verifying tables...")
        async with db.engine.connect() as conn:
            # Check knowledge_nodes
            result = await conn.execute(
                """
                SELECT EXISTS (
                    SELECT FROM pg_tables
                    WHERE tablename = 'knowledge_nodes'
                )
                """
            )
            nodes_exists = result.scalar()

            # Check knowledge_edges
            result = await conn.execute(
                """
                SELECT EXISTS (
                    SELECT FROM pg_tables
                    WHERE tablename = 'knowledge_edges'
                )
                """
            )
            edges_exists = result.scalar()

            print(f"   - knowledge_nodes: {'✅ EXISTS' if nodes_exists else '❌ MISSING'}")
            print(f"   - knowledge_edges: {'✅ EXISTS' if edges_exists else '❌ MISSING'}")
            print()

            if nodes_exists and edges_exists:
                # Check indexes
                result = await conn.execute(
                    """
                    SELECT indexname FROM pg_indexes
                    WHERE tablename IN ('knowledge_nodes', 'knowledge_edges')
                    ORDER BY tablename, indexname
                    """
                )
                indexes = [row[0] for row in result]

                print(f"📊 Indexes created ({len(indexes)} total):")
                for idx in indexes:
                    print(f"   - {idx}")
                print()

                return True
            else:
                print("❌ Table creation failed!")
                return False

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return False
    finally:
        # Close connection
        await db.close()
        print("👋 Database connection closed")


if __name__ == "__main__":
    success = asyncio.run(create_knowledge_graph_tables())
    sys.exit(0 if success else 1)
