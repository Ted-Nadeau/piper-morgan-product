import asyncio
import sys

sys.path.append(".")


async def test():
    from services.knowledge_graph.ingestion import get_ingester

    print("🧪 Testing PM-007 Enhancement")
    print("=" * 50)

    ingester = get_ingester()
    print("✅ Ingester loaded")

    # Check method exists
    if hasattr(ingester, "_analyze_document_relationships"):
        print("✅ Relationship analysis method found")
    else:
        print("❌ Method missing")
        return

    # Test search
    results = await ingester.search("test", n_results=1)
    print(f"✅ Search returned {len(results)} results")

    if results:
        metadata = results[0].get("metadata", {})
        if "relationship_analysis_version" in metadata:
            print("✅ Documents have relationship analysis!")
            print(f"   Document type: {metadata.get('document_type')}")
            print(f"   Hierarchy level: {metadata.get('hierarchy_level')}")
        else:
            print("⚠️  Documents need re-ingestion for relationship analysis")

    print("\n🎯 Test complete!")


if __name__ == "__main__":
    asyncio.run(test())
