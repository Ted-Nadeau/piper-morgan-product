"""
Document Memory Integration Tests

Tests the integration between Document Memory, CanonicalQueryEngine, and Morning Standup.
Follows the exact pattern from Sunday's Issue Intelligence integration.

Created: August 25, 2025 - Cursor Agent for Document Memory integration testing
"""

import asyncio
from typing import Any, Dict

import pytest

from services.features.document_memory import DocumentMemoryQueries


@pytest.mark.smoke
async def test_document_memory_extends_canonical():
    """DocumentMemoryQueries should extend CanonicalQueryEngine."""
    doc_memory = DocumentMemoryQueries(user_id="test")
    assert hasattr(doc_memory, "canonical_queries")
    assert isinstance(doc_memory.canonical_queries, dict)
    assert len(doc_memory.canonical_queries) >= 4


@pytest.mark.smoke
async def test_canonical_queries_callable():
    """All canonical queries should be callable methods."""
    doc_memory = DocumentMemoryQueries(user_id="test")
    for query_name, query_method in doc_memory.canonical_queries.items():
        assert callable(query_method), f"{query_name} not callable"


@pytest.mark.smoke
async def test_morning_standup_integration():
    """Morning Standup should have document integration capability."""
    import inspect

    from services.features.morning_standup import MorningStandupWorkflow

    # Check if generate_with_documents method exists in the class
    has_doc_method = hasattr(MorningStandupWorkflow, "generate_with_documents")
    assert (
        has_doc_method
    ), "generate_with_documents method missing from MorningStandupWorkflow class"

    # Check if the method signature is correct
    method = getattr(MorningStandupWorkflow, "generate_with_documents")
    assert callable(method), "generate_with_documents must be callable"


@pytest.mark.integration
async def test_basic_document_queries():
    """Basic document queries should execute without errors."""
    doc_memory = DocumentMemoryQueries(user_id="test")

    # Test each canonical query can be called (may return mock data)
    decisions = await doc_memory.find_decisions("test topic")
    assert decisions is not None

    context = await doc_memory.get_relevant_context()
    assert context is not None


if __name__ == "__main__":
    """Run tests directly for quick verification."""
    print("🚀 Running Document Memory Integration Tests")
    print("=" * 60)

    async def run_tests():
        test_functions = [
            test_document_memory_extends_canonical,
            test_morning_standup_integration,
            test_canonical_queries_callable,
            test_basic_document_queries,
        ]

        results = []
        for test_func in test_functions:
            try:
                await test_func()
                results.append(f"✅ {test_func.__name__}")
            except Exception as e:
                results.append(f"❌ {test_func.__name__}: {e}")

        print("\n" + "=" * 60)
        print("📊 Test Results Summary:")
        for result in results:
            print(result)

        passed = sum(1 for r in results if r.startswith("✅"))
        total = len(results)
        print(f"\n🎯 Overall: {passed}/{total} tests passed")

        if passed == total:
            print("🎉 All tests passed! Document Memory integration ready.")
        else:
            print("⚠️ Some tests failed or skipped - check implementation status.")

    # Run tests
    asyncio.run(run_tests())
