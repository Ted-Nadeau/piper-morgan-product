#!/usr/bin/env python3
"""
Simple Knowledge Graph Schema Verification
Issue #99 - CORE-KNOW Phase 1

Tests tables exist and can accept data directly.
"""

import asyncio
import sys
import uuid
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import text

from services.database.connection import db


async def verify_schema_simple():
    """Simple verification that tables exist and work"""
    print("=" * 70)
    print("Knowledge Graph Schema Verification (Simple)")
    print("Issue #99 - CORE-KNOW Phase 1")
    print("=" * 70)
    print()

    try:
        await db.initialize()
        print("✅ Database connected")
        print()

        async with db.engine.connect() as conn:
            # Test 1: Verify tables exist
            print("📋 Test 1: Verify Tables Exist")
            result = await conn.execute(
                text(
                    """
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_name IN ('knowledge_nodes', 'knowledge_edges')
                    ORDER BY table_name
                """
                )
            )
            rows = result.fetchall()
            tables = [row[0] for row in rows]
            assert len(tables) == 2, f"Expected 2 tables, found {len(tables)}"
            print(f"   ✅ Found tables: {', '.join(tables)}")
            print()

            # Test 2: Check node columns
            print("📊 Test 2: Verify knowledge_nodes Schema")
            result = await conn.execute(
                text(
                    """
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = 'knowledge_nodes'
                    ORDER BY ordinal_position
                """
                )
            )
            rows = result.fetchall()
            columns = [f"{row[0]} ({row[1]})" for row in rows]
            print(f"   ✅ Columns ({len(columns)}):")
            for col in columns:
                print(f"      - {col}")
            assert len(columns) == 10, f"Expected 10 columns, found {len(columns)}"
            print()

            # Test 3: Check edge columns
            print("📊 Test 3: Verify knowledge_edges Schema")
            result = await conn.execute(
                text(
                    """
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = 'knowledge_edges'
                    ORDER BY ordinal_position
                """
                )
            )
            rows = result.fetchall()
            columns = [f"{row[0]} ({row[1]})" for row in rows]
            print(f"   ✅ Columns ({len(columns)}):")
            for col in columns:
                print(f"      - {col}")
            assert len(columns) == 10, f"Expected 10 columns, found {len(columns)}"
            print()

            # Test 4: Check indexes
            print("🔍 Test 4: Verify Indexes")
            result = await conn.execute(
                text(
                    """
                    SELECT tablename, indexname
                    FROM pg_indexes
                    WHERE tablename IN ('knowledge_nodes', 'knowledge_edges')
                    ORDER BY tablename, indexname
                """
                )
            )
            rows = result.fetchall()
            indexes = [(row[0], row[1]) for row in rows]
            print(f"   ✅ Indexes ({len(indexes)}):")
            for table, index in indexes:
                print(f"      - {table}: {index}")
            assert len(indexes) >= 8, f"Expected at least 8 indexes, found {len(indexes)}"
            print()

            # Test 5: Check foreign keys
            print("🔗 Test 5: Verify Foreign Keys")
            result = await conn.execute(
                text(
                    """
                    SELECT
                        tc.table_name,
                        kcu.column_name,
                        ccu.table_name AS foreign_table_name,
                        ccu.column_name AS foreign_column_name
                    FROM information_schema.table_constraints AS tc
                    JOIN information_schema.key_column_usage AS kcu
                      ON tc.constraint_name = kcu.constraint_name
                      AND tc.table_schema = kcu.table_schema
                    JOIN information_schema.constraint_column_usage AS ccu
                      ON ccu.constraint_name = tc.constraint_name
                      AND ccu.table_schema = tc.table_schema
                    WHERE tc.constraint_type = 'FOREIGN KEY'
                      AND tc.table_name = 'knowledge_edges'
                """
                )
            )
            rows = result.fetchall()
            fks = [(row[0], row[1], row[2], row[3]) for row in rows]
            print(f"   ✅ Foreign Keys ({len(fks)}):")
            for table, col, ref_table, ref_col in fks:
                print(f"      - {table}.{col} → {ref_table}.{ref_col}")
            assert len(fks) == 2, f"Expected 2 foreign keys, found {len(fks)}"
            print()

            # Test 6: Insert and query test data (raw SQL)
            print("✍️  Test 6: Test CRUD Operations (Raw SQL)")

            # Create test node
            node_id = str(uuid.uuid4())
            node_id_2 = str(uuid.uuid4())

            await conn.execute(
                text(
                    """
                    INSERT INTO knowledge_nodes
                    (id, name, node_type, description, session_id, created_at, updated_at)
                    VALUES (:id, :name, 'CONCEPT', :desc, :session, NOW(), NOW())
                """
                ),
                {"id": node_id, "name": "Test Node", "desc": "A test node", "session": "test"},
            )

            await conn.execute(
                text(
                    """
                    INSERT INTO knowledge_nodes
                    (id, name, node_type, description, session_id, created_at, updated_at)
                    VALUES (:id, :name, 'TECHNOLOGY', :desc, :session, NOW(), NOW())
                """
                ),
                {
                    "id": node_id_2,
                    "name": "Test Tech",
                    "desc": "A test technology",
                    "session": "test",
                },
            )

            print(f"   ✅ Created 2 test nodes")

            # Create test edge
            edge_id = str(uuid.uuid4())
            await conn.execute(
                text(
                    """
                    INSERT INTO knowledge_edges
                    (id, source_node_id, target_node_id, edge_type, weight, session_id, created_at, updated_at)
                    VALUES (:id, :source, :target, 'DEPENDS_ON', 0.8, :session, NOW(), NOW())
                """
                ),
                {"id": edge_id, "source": node_id, "target": node_id_2, "session": "test"},
            )

            print(f"   ✅ Created 1 test edge")

            # Query back
            result = await conn.execute(
                text("SELECT name FROM knowledge_nodes WHERE id = :id"), {"id": node_id}
            )
            row = result.fetchone()
            assert row[0] == "Test Node", "Failed to retrieve node"
            print(f"   ✅ Retrieved node: {row[0]}")

            # Cleanup
            await conn.execute(text("DELETE FROM knowledge_edges WHERE id = :id"), {"id": edge_id})
            await conn.execute(text("DELETE FROM knowledge_nodes WHERE id = :id"), {"id": node_id})
            await conn.execute(
                text("DELETE FROM knowledge_nodes WHERE id = :id"), {"id": node_id_2}
            )
            await conn.commit()

            print(f"   ✅ Cleanup completed")
            print()

        print("=" * 70)
        print("✅ All Tests Passed!")
        print("=" * 70)
        print()
        print("🎉 Knowledge Graph schema is fully operational!")
        print()
        print("📋 Summary:")
        print("   ✅ Tables exist (knowledge_nodes, knowledge_edges)")
        print("   ✅ Columns correct (10 each)")
        print("   ✅ Indexes created (8+ total)")
        print("   ✅ Foreign keys working (2 constraints)")
        print("   ✅ CRUD operations functional")
        print()
        print("🚀 Ready for Phase 2: IntentService Integration")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return False
    finally:
        await db.close()


if __name__ == "__main__":
    success = asyncio.run(verify_schema_simple())
    sys.exit(0 if success else 1)
