#!/usr/bin/env python3
"""
Simple test for PM-007 Knowledge Hierarchy Enhancement
"""
import asyncio
import os
import sys

sys.path.append(".")


async def test_relationship_analysis():
    """Test if relationship analysis is working"""

    print("🧪 Testing PM-007 Relationship Analysis")
    print("=" * 50)

    try:
        from services.knowledge_graph.ingestion import get_ingester

        ingester = get_ingester()
        print("✅ DocumentIngester loaded successfully")

        # Check if the new method exists
        if hasattr(ingester, "_analyze_document_relationships"):
            print("✅ Relationship analysis method found")
        else:
            print("❌ Relationship analysis method missing")
            return

        # Test basic search
        results = await ingester.search("test", n_results=1)
        print(f"✅ Search working - returned {len(results)} results")

        if results:
            metadata = results[0].get("metadata", {})
            if "relationship_analysis_version" in metadata:
                print("✅ Documents have relationship analysis!")
                print(f"   Document type: {metadata.get('document_type')}")
                print(f"   Hierarchy level: {metadata.get('hierarchy_level')}")
            else:
                print("⚠️  Documents need re-ingestion for relationship analysis")

        print("\n🎯 Basic test complete!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_relationship_analysis())
