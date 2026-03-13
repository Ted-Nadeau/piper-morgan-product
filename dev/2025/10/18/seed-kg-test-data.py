#!/usr/bin/env python3
"""
Seed Knowledge Graph with test data for canonical query testing.
Issue #99 - CORE-KNOW Phase 3

Creates:
- Project nodes (SITE-001: pmorgan.tech Website MVP)
- Person nodes (PM, stakeholders)
- Document nodes (project docs)
- Edges (relationships between entities)

Uses raw SQL to avoid repository __dict__ issues.
"""

import asyncio
import json
import sys
import uuid
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import text

from services.database.connection import db


async def seed_test_data():
    """Seed Knowledge Graph with test data using raw SQL."""
    print("=" * 70)
    print("Seeding Knowledge Graph Test Data")
    print("Issue #99 - CORE-KNOW Phase 3")
    print("=" * 70)
    print()

    try:
        await db.initialize()
        print("✅ Database connected")
        print()

        async with db.engine.connect() as conn:
            # 1. Create project node (using CONCEPT type)
            print("Creating project node...")
            project_id = str(uuid.uuid4())
            await conn.execute(
                text(
                    """
                    INSERT INTO knowledge_nodes
                    (id, name, node_type, description, node_metadata, session_id, created_at, updated_at)
                    VALUES (:id, :name, 'CONCEPT', :desc, :metadata, :session, NOW(), NOW())
                """
                ),
                {
                    "id": project_id,
                    "name": "pmorgan.tech Website MVP",
                    "desc": "Website project for Paul Morgan Tech - Full stack web application with modern design system",
                    "metadata": json.dumps(
                        {
                            "project_id": "SITE-001",
                            "status": "in_progress",
                            "phases": {"total": 5, "complete": 3, "current": "Integration"},
                            "focus_areas": ["technical foundation", "design system"],
                            "blockers": ["ConvertKit integration", "Medium RSS feeds"],
                        }
                    ),
                    "session": "test-session-001",
                },
            )
            print(f"✓ Created project node: pmorgan.tech Website MVP")
            print(f"  ID: {project_id}")

            # 2. Create person node (PM)
            print("\nCreating person node...")
            pm_id = str(uuid.uuid4())
            await conn.execute(
                text(
                    """
                    INSERT INTO knowledge_nodes
                    (id, name, node_type, description, node_metadata, session_id, created_at, updated_at)
                    VALUES (:id, :name, 'PERSON', :desc, :metadata, :session, NOW(), NOW())
                """
                ),
                {
                    "id": pm_id,
                    "name": "Paul Morgan",
                    "desc": "Project Manager and Tech Lead for pmorgan.tech",
                    "metadata": json.dumps(
                        {"role": "PM", "interests": ["AI", "web development", "productivity"]}
                    ),
                    "session": "test-session-001",
                },
            )
            print(f"✓ Created person node: Paul Morgan")
            print(f"  ID: {pm_id}")

            # 3. Create document node
            print("\nCreating document node...")
            doc_id = str(uuid.uuid4())
            await conn.execute(
                text(
                    """
                    INSERT INTO knowledge_nodes
                    (id, name, node_type, description, node_metadata, session_id, created_at, updated_at)
                    VALUES (:id, :name, 'DOCUMENT', :desc, :metadata, :session, NOW(), NOW())
                """
                ),
                {
                    "id": doc_id,
                    "name": "Website Design System",
                    "desc": "Design system documentation for pmorgan.tech website including color palette, typography, and component library",
                    "metadata": json.dumps(
                        {"status": "complete", "last_updated": datetime.now().isoformat()}
                    ),
                    "session": "test-session-001",
                },
            )
            print(f"✓ Created document node: Website Design System")
            print(f"  ID: {doc_id}")

            # 4. Create edges (relationships)
            print("\nCreating relationships...")

            # PM → Website Project
            edge1_id = str(uuid.uuid4())
            await conn.execute(
                text(
                    """
                    INSERT INTO knowledge_edges
                    (id, source_node_id, target_node_id, edge_type, weight, node_metadata, session_id, created_at, updated_at)
                    VALUES (:id, :source, :target, 'SUPPORTS', 1.0, :metadata, :session, NOW(), NOW())
                """
                ),
                {
                    "id": edge1_id,
                    "source": pm_id,
                    "target": project_id,
                    "metadata": json.dumps({"role": "owner"}),
                    "session": "test-session-001",
                },
            )
            print(f"✓ Created edge: PM → Website Project (SUPPORTS)")

            # Project → Design Doc
            edge2_id = str(uuid.uuid4())
            await conn.execute(
                text(
                    """
                    INSERT INTO knowledge_edges
                    (id, source_node_id, target_node_id, edge_type, weight, node_metadata, session_id, created_at, updated_at)
                    VALUES (:id, :source, :target, 'REFERENCES', 1.0, :metadata, :session, NOW(), NOW())
                """
                ),
                {
                    "id": edge2_id,
                    "source": project_id,
                    "target": doc_id,
                    "metadata": json.dumps({"relationship": "has_document"}),
                    "session": "test-session-001",
                },
            )
            print(f"✓ Created edge: Website Project → Design Doc (REFERENCES)")

            # 5. Create interaction history
            print("\nCreating interaction history...")
            interactions = [
                "Discussed technical foundation setup",
                "Reviewed design system progress",
                "Identified ConvertKit blocker",
                "Planning Medium RSS integration",
            ]

            interaction_ids = []
            for i, interaction in enumerate(interactions):
                interaction_id = str(uuid.uuid4())
                interaction_ids.append(interaction_id)

                await conn.execute(
                    text(
                        """
                        INSERT INTO knowledge_nodes
                        (id, name, node_type, description, node_metadata, session_id, created_at, updated_at)
                        VALUES (:id, :name, 'CONCEPT', :desc, :metadata, :session, NOW(), NOW())
                    """
                    ),
                    {
                        "id": interaction_id,
                        "name": f"Interaction: {interaction[:30]}",
                        "desc": interaction,
                        "metadata": json.dumps(
                            {
                                "type": "interaction",
                                "timestamp": datetime.now().isoformat(),
                                "sequence": i + 1,
                            }
                        ),
                        "session": "test-session-001",
                    },
                )

                # Link to PM
                edge_id = str(uuid.uuid4())
                await conn.execute(
                    text(
                        """
                        INSERT INTO knowledge_edges
                        (id, source_node_id, target_node_id, edge_type, weight, node_metadata, session_id, created_at, updated_at)
                        VALUES (:id, :source, :target, 'REFERENCES', 1.0, :metadata, :session, NOW(), NOW())
                    """
                    ),
                    {
                        "id": edge_id,
                        "source": pm_id,
                        "target": interaction_id,
                        "metadata": json.dumps({"interaction_type": "discussion"}),
                        "session": "test-session-001",
                    },
                )

            print(f"✓ Created {len(interactions)} interaction nodes")

            # 6. Create technology nodes
            print("\nCreating technology nodes...")
            tech_stack = [
                ("FastAPI", "Modern Python web framework"),
                ("PostgreSQL", "Relational database"),
                ("React", "Frontend JavaScript library"),
            ]

            tech_ids = []
            for tech_name, tech_desc in tech_stack:
                tech_id = str(uuid.uuid4())
                tech_ids.append(tech_id)

                await conn.execute(
                    text(
                        """
                        INSERT INTO knowledge_nodes
                        (id, name, node_type, description, session_id, created_at, updated_at)
                        VALUES (:id, :name, 'TECHNOLOGY', :desc, :session, NOW(), NOW())
                    """
                    ),
                    {
                        "id": tech_id,
                        "name": tech_name,
                        "desc": tech_desc,
                        "session": "test-session-001",
                    },
                )

                # Link to project
                edge_id = str(uuid.uuid4())
                await conn.execute(
                    text(
                        """
                        INSERT INTO knowledge_edges
                        (id, source_node_id, target_node_id, edge_type, weight, session_id, created_at, updated_at)
                        VALUES (:id, :source, :target, 'DEPENDS_ON', 1.0, :session, NOW(), NOW())
                    """
                    ),
                    {
                        "id": edge_id,
                        "source": project_id,
                        "target": tech_id,
                        "session": "test-session-001",
                    },
                )

            print(f"✓ Created {len(tech_stack)} technology nodes")

            # Commit all changes
            await conn.commit()

            # Summary
            print("\n" + "=" * 70)
            print("✅ Test Data Seeding Complete!")
            print("=" * 70)
            print(f"\n📊 Summary:")
            print(f"   Projects: 1 (pmorgan.tech Website MVP)")
            print(f"   People: 1 (Paul Morgan)")
            print(f"   Documents: 1 (Website Design System)")
            print(f"   Technologies: {len(tech_stack)}")
            print(f"   Interactions: {len(interactions)}")
            print(f"   Total Nodes: {1 + 1 + 1 + len(tech_stack) + len(interactions)}")
            print(f"   Total Edges: {2 + len(interactions) + len(tech_stack)}")
            print(f"\n   Session ID: test-session-001")
            print()
            print("🎯 Ready for canonical query testing!")
            print()

            return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return False
    finally:
        await db.close()


if __name__ == "__main__":
    success = asyncio.run(seed_test_data())
    sys.exit(0 if success else 1)
