#!/usr/bin/env python3
"""
Test natural language search with real content that we know exists
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


async def test_real_content_search():
    """Test with broader terms that are likely to find results"""

    test_queries = [
        "find documents about requirements",
        "search for MCP files",
        "find documents about technical specifications",
    ]

    for query in test_queries:
        print(f"\n🔍 Testing: '{query}'")
        print("-" * 50)

        # Intent classification
        classifier = IntentClassifier()
        intent = await classifier.classify(query)
        print(f"Action: {intent.action}, Confidence: {intent.confidence}")

        if intent.action in ["search_documents", "find_documents", "search_files"]:
            # Add context and route
            intent.context["session_id"] = None  # Search all sessions

            async with AsyncSessionFactory.session_scope_fresh() as session:
                file_repo = FileRepository(session)
                file_query_service = FileQueryService(file_repo)

                # Search across all sessions
                result = await file_query_service.search_files_all_sessions(query, limit=5)

                print(f"Success: {result.get('success', False)}")
                print(f"Found: {result.get('total_count', 0)} files")
                print(f"Search type: {result.get('search_type', 'unknown')}")

                if result.get("files"):
                    print("Files found:")
                    for i, file in enumerate(result["files"][:3]):
                        print(f"  {i+1}. {file.get('filename', 'unknown')}")

                return result.get("total_count", 0) > 0
        else:
            print(f"Not a search action: {intent.action}")
            return False


async def main():
    print("🧪 Testing Natural Language Search with Real Content")
    print("=" * 60)

    success = await test_real_content_search()

    print("\n" + "=" * 60)
    if success:
        print("✅ SUCCESS: Natural language search is finding real content!")
        print(
            "🎉 Users can now search with natural language and get results using PM-038 MCP infrastructure!"
        )
    else:
        print("❌ No results found - may need to check file content or search scope")


if __name__ == "__main__":
    asyncio.run(main())
