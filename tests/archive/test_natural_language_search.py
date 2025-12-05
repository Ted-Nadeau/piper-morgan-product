#!/usr/bin/env python3
"""
Quick test for natural language search integration
Tests: 'find documents about project timeline' → real results
"""

import asyncio
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath("."))

from services.database.repositories import ProjectRepository
from services.database.session_factory import AsyncSessionFactory
from services.intent_service.classifier import IntentClassifier
from services.queries.conversation_queries import ConversationQueryService
from services.queries.file_queries import FileQueryService
from services.queries.project_queries import ProjectQueryService
from services.queries.query_router import QueryRouter
from services.repositories.file_repository import FileRepository


async def test_natural_language_search():
    """Test the full pipeline: natural language → intent → search results"""

    print("🧪 Testing Natural Language Search Integration")
    print("=" * 50)

    # Test query
    test_query = "find documents about project timeline"
    print(f"Test Query: '{test_query}'")
    print()

    # Step 1: Test Intent Classification
    print("📝 Step 1: Intent Classification")
    classifier = IntentClassifier()
    intent = await classifier.classify(test_query)

    print(f"  Category: {intent.category}")
    print(f"  Action: {intent.action}")
    print(f"  Confidence: {intent.confidence}")
    print(f"  Context: {intent.context}")
    print()

    # Step 2: Test Query Routing (if it's a search intent)
    if intent.action in ["search_files", "find_documents", "search_content", "search_documents"]:
        print("🔄 Step 2: Query Routing")

        # Add session_id to context for testing
        intent.context["session_id"] = "test_session"

        async with AsyncSessionFactory.session_scope_fresh() as session:
            # Set up query services
            project_repo = ProjectRepository(session)
            file_repo = FileRepository(session)

            project_query_service = ProjectQueryService(project_repo)
            conversation_query_service = ConversationQueryService()
            file_query_service = FileQueryService(file_repo)

            query_router = QueryRouter(
                project_query_service,
                conversation_query_service,
                file_query_service,
            )

            # Route the query
            print("  Routing query to appropriate service...")
            query_result = await query_router.route_query(intent)

            print(f"  Query Result Type: {type(query_result)}")
            if isinstance(query_result, dict):
                print(f"  Success: {query_result.get('success', 'unknown')}")
                print(f"  Total Files Found: {query_result.get('total_count', 0)}")
                print(f"  Search Type: {query_result.get('search_type', 'unknown')}")

                if query_result.get("files"):
                    print(f"  Found Files:")
                    for i, file in enumerate(query_result["files"][:5]):  # Show first 5
                        print(f"    {i+1}. {file.get('filename', 'unknown')}")
                        if "score" in file:
                            print(f"       Score: {file['score']}")
            else:
                print(f"  Raw Result: {query_result}")
    else:
        print(f"❌ Intent action '{intent.action}' is not a search action")
        print("   Expected: search_files, find_documents, search_content, or search_documents")
        return False

    print()
    print("✅ Test Complete!")
    return True


async def test_api_endpoint():
    """Test the API endpoint directly"""
    print("\n🌐 Testing API Endpoint Directly")
    print("=" * 30)

    try:
        async with AsyncSessionFactory.session_scope_fresh() as session:
            file_repo = FileRepository(session)
            file_query_service = FileQueryService(file_repo)

            # Test the search method directly
            result = await file_query_service.search_files_by_query("project timeline")

            print(f"API Test Result:")
            print(f"  Success: {result.get('success', False)}")
            print(f"  Total Count: {result.get('total_count', 0)}")
            print(f"  Search Type: {result.get('search_type', 'unknown')}")

            if result.get("files"):
                print(f"  Sample Files:")
                for file in result["files"][:3]:
                    print(f"    - {file.get('filename', 'unknown')}")

            return result.get("success", False)

    except Exception as e:
        print(f"❌ API Test Failed: {e}")
        return False


async def main():
    """Run all tests"""
    print("🚀 Natural Language Search Integration Test")
    print("Testing PM-038 MCP search with intent classification")
    print("=" * 60)
    print()

    # Test 1: Full pipeline
    success1 = await test_natural_language_search()

    # Test 2: API endpoint
    success2 = await test_api_endpoint()

    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS:")
    print(f"  Intent Classification + Routing: {'✅ PASS' if success1 else '❌ FAIL'}")
    print(f"  Direct API Test: {'✅ PASS' if success2 else '❌ FAIL'}")

    if success1 and success2:
        print("\n🎉 SUCCESS: Natural language search integration is working!")
        print("Users can now search with: 'find documents about project timeline'")
    else:
        print("\n⚠️  Some tests failed - check the output above for details")


if __name__ == "__main__":
    asyncio.run(main())
