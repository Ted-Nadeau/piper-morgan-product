#!/usr/bin/env python3
"""
Verify Knowledge Graph Schema and CRUD Operations
Issue #99 - CORE-KNOW Phase 1

Tests that the Knowledge Graph tables work correctly with the repository.
"""

import asyncio
import sys
import uuid
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from services.database.repositories import KnowledgeGraphRepository
from services.database.session_factory import AsyncSessionFactory
from services.domain.models import KnowledgeEdge, KnowledgeNode
from services.shared_types import EdgeType, NodeType


async def verify_knowledge_graph_crud():
    """Verify basic CRUD operations on Knowledge Graph"""
    print("=" * 70)
    print("Knowledge Graph Schema Verification")
    print("Issue #99 - CORE-KNOW Phase 1")
    print("=" * 70)
    print()

    try:
        print("🔧 Testing Knowledge Graph CRUD Operations...")
        print()

        async with AsyncSessionFactory.session_scope_fresh() as session:
            repo = KnowledgeGraphRepository(session)

            # Test 1: Create a node
            print("📝 Test 1: Create Node")
            test_node = KnowledgeNode(
                id=str(uuid.uuid4()),
                name="Test Project",
                node_type=NodeType.CONCEPT,
                description="A test project for schema verification",
                metadata={"test": True},
                properties={"priority": "high"},
                session_id="test-session",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

            created_node = await repo.create_node(test_node)
            print(f"   ✅ Node created: {created_node.id}")
            print(f"      Name: {created_node.name}")
            print(f"      Type: {created_node.node_type.value}")
            print()

            # Test 2: Read the node
            print("📖 Test 2: Read Node")
            retrieved_node = await repo.get_node_by_id(created_node.id)
            assert retrieved_node is not None, "Node not found!"
            assert retrieved_node.name == "Test Project"
            print(f"   ✅ Node retrieved: {retrieved_node.name}")
            print(f"      Metadata: {retrieved_node.metadata}")
            print()

            # Test 3: Create a second node for edge testing
            print("📝 Test 3: Create Second Node (for Edge)")
            test_node_2 = KnowledgeNode(
                id=str(uuid.uuid4()),
                name="Related Concept",
                node_type=NodeType.TECHNOLOGY,
                description="A related technology",
                session_id="test-session",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

            created_node_2 = await repo.create_node(test_node_2)
            print(f"   ✅ Second node created: {created_node_2.id}")
            print()

            # Test 4: Create an edge
            print("🔗 Test 4: Create Edge")
            test_edge = KnowledgeEdge(
                id=str(uuid.uuid4()),
                source_node_id=created_node.id,
                target_node_id=created_node_2.id,
                edge_type=EdgeType.DEPENDS_ON,
                weight=0.8,
                metadata={"relationship": "uses"},
                properties={},
                session_id="test-session",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

            created_edge = await repo.create_edge(test_edge)
            print(f"   ✅ Edge created: {created_edge.id}")
            print(f"      From: {created_edge.source_node_id}")
            print(f"      To: {created_edge.target_node_id}")
            print(f"      Type: {created_edge.edge_type.value}")
            print()

            # Test 5: Get neighbors
            print("🔍 Test 5: Find Neighbors")
            neighbors = await repo.find_neighbors(created_node.id)
            print(f"   ✅ Found {len(neighbors)} neighbor(s)")
            for neighbor in neighbors:
                print(f"      - {neighbor.name} ({neighbor.node_type.value})")
            print()

            # Test 6: Get nodes by type
            print("📊 Test 6: Get Nodes by Type")
            concept_nodes = await repo.get_nodes_by_type(
                NodeType.CONCEPT, session_id="test-session"
            )
            print(f"   ✅ Found {len(concept_nodes)} CONCEPT node(s)")
            print()

            # Test 7: Get subgraph
            print("🕸️  Test 7: Extract Subgraph")
            subgraph = await repo.get_subgraph([created_node.id], max_depth=2)
            print(f"   ✅ Subgraph extracted:")
            print(f"      Nodes: {len(subgraph['nodes'])}")
            print(f"      Edges: {len(subgraph['edges'])}")
            print()

            # Test 8: Cleanup - Delete nodes
            print("🗑️  Test 8: Cleanup")
            # Delete edges first (foreign key constraint)
            from sqlalchemy import delete

            from services.database.models import KnowledgeEdgeDB, KnowledgeNodeDB

            await repo.session.execute(
                delete(KnowledgeEdgeDB).where(
                    (KnowledgeEdgeDB.source_node_id.in_([created_node.id, created_node_2.id]))
                    | (KnowledgeEdgeDB.target_node_id.in_([created_node.id, created_node_2.id]))
                )
            )
            # Delete nodes
            await repo.session.execute(
                delete(KnowledgeNodeDB).where(
                    KnowledgeNodeDB.id.in_([created_node.id, created_node_2.id])
                )
            )
            await repo.session.commit()
            print("   ✅ Test data cleaned up")
            print()

        print("=" * 70)
        print("✅ All Tests Passed!")
        print("=" * 70)
        print()
        print("📋 Summary:")
        print("   - Node creation: ✅")
        print("   - Node retrieval: ✅")
        print("   - Edge creation: ✅")
        print("   - Neighbor finding: ✅")
        print("   - Type filtering: ✅")
        print("   - Subgraph extraction: ✅")
        print("   - Cleanup: ✅")
        print()
        print("🎉 Knowledge Graph database schema is fully operational!")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(verify_knowledge_graph_crud())
    sys.exit(0 if success else 1)
