#!/usr/bin/env python3
"""
Manual test script for Phase 2.1 Pattern Management Endpoints
Issue #300 - CORE-ALPHA-LEARNING-BASIC

Tests all 5 pattern management endpoints:
- GET /patterns (list)
- GET /patterns/{id} (details)
- DELETE /patterns/{id}
- POST /patterns/{id}/enable
- POST /patterns/{id}/disable
"""

import asyncio
from datetime import datetime
from uuid import UUID

from services.database.models import LearnedPattern, PatternType
from services.database.session_factory import AsyncSessionFactory

# Test user ID (same as used in endpoints)
TEST_USER_ID = UUID("3f4593ae-5bc9-468d-b08d-8c4c02a5b963")


async def create_test_patterns():
    """Create test patterns for testing endpoints"""
    print("Creating test patterns...")

    async with AsyncSessionFactory.session_scope() as session:
        # Pattern 1: User workflow
        pattern1 = LearnedPattern(
            user_id=TEST_USER_ID,
            pattern_type=PatternType.USER_WORKFLOW,
            pattern_data={
                "intent": "query_github",
                "context": {"query": "recent PRs"},
                "frequency": "daily",
            },
            confidence=0.85,
            usage_count=10,
            success_count=9,
            failure_count=1,
            enabled=True,
            last_used_at=datetime.utcnow(),
        )

        # Pattern 2: Command sequence
        pattern2 = LearnedPattern(
            user_id=TEST_USER_ID,
            pattern_type=PatternType.COMMAND_SEQUENCE,
            pattern_data={
                "intent": "query_notion",
                "context": {"database": "tasks"},
                "sequence": ["list", "filter", "sort"],
            },
            confidence=0.72,
            usage_count=5,
            success_count=4,
            failure_count=1,
            enabled=True,
            last_used_at=datetime.utcnow(),
        )

        # Pattern 3: Time-based (disabled)
        pattern3 = LearnedPattern(
            user_id=TEST_USER_ID,
            pattern_type=PatternType.TIME_BASED,
            pattern_data={
                "intent": "standup",
                "context": {"time": "09:00"},
                "days": ["monday", "wednesday", "friday"],
            },
            confidence=0.65,
            usage_count=3,
            success_count=2,
            failure_count=1,
            enabled=False,  # Disabled for testing
            last_used_at=datetime.utcnow(),
        )

        session.add_all([pattern1, pattern2, pattern3])
        await session.commit()

        print(f"✅ Created 3 test patterns:")
        print(f"   - Pattern 1: {pattern1.id} (USER_WORKFLOW, enabled)")
        print(f"   - Pattern 2: {pattern2.id} (COMMAND_SEQUENCE, enabled)")
        print(f"   - Pattern 3: {pattern3.id} (TIME_BASED, disabled)")

        return [str(pattern1.id), str(pattern2.id), str(pattern3.id)]


async def test_list_patterns():
    """Test GET /patterns"""
    print("\n" + "=" * 80)
    print("TEST 1: GET /api/v1/learning/patterns")
    print("=" * 80)
    print("curl -s http://localhost:8001/api/v1/learning/patterns | python -m json.tool")
    print("\nExpected: List of 3 patterns with metadata")
    print("To run: curl -s http://localhost:8001/api/v1/learning/patterns | python -m json.tool")


async def test_get_pattern(pattern_id: str):
    """Test GET /patterns/{id}"""
    print("\n" + "=" * 80)
    print(f"TEST 2: GET /api/v1/learning/patterns/{pattern_id}")
    print("=" * 80)
    print(
        f"curl -s http://localhost:8001/api/v1/learning/patterns/{pattern_id} | python -m json.tool"
    )
    print("\nExpected: Single pattern with full details")
    print(
        f"To run: curl -s http://localhost:8001/api/v1/learning/patterns/{pattern_id} | python -m json.tool"
    )


async def test_enable_pattern(pattern_id: str):
    """Test POST /patterns/{id}/enable"""
    print("\n" + "=" * 80)
    print(f"TEST 3: POST /api/v1/learning/patterns/{pattern_id}/enable")
    print("=" * 80)
    print(
        f"curl -X POST -s http://localhost:8001/api/v1/learning/patterns/{pattern_id}/enable | python -m json.tool"
    )
    print("\nExpected: Success message with enabled=true")
    print(
        f"To run: curl -X POST -s http://localhost:8001/api/v1/learning/patterns/{pattern_id}/enable | python -m json.tool"
    )


async def test_disable_pattern(pattern_id: str):
    """Test POST /patterns/{id}/disable"""
    print("\n" + "=" * 80)
    print(f"TEST 4: POST /api/v1/learning/patterns/{pattern_id}/disable")
    print("=" * 80)
    print(
        f"curl -X POST -s http://localhost:8001/api/v1/learning/patterns/{pattern_id}/disable | python -m json.tool"
    )
    print("\nExpected: Success message with enabled=false")
    print(
        f"To run: curl -X POST -s http://localhost:8001/api/v1/learning/patterns/{pattern_id}/disable | python -m json.tool"
    )


async def test_delete_pattern(pattern_id: str):
    """Test DELETE /patterns/{id}"""
    print("\n" + "=" * 80)
    print(f"TEST 5: DELETE /api/v1/learning/patterns/{pattern_id}")
    print("=" * 80)
    print(
        f"curl -X DELETE -s http://localhost:8001/api/v1/learning/patterns/{pattern_id} | python -m json.tool"
    )
    print("\nExpected: Success message confirming deletion")
    print(
        f"To run: curl -X DELETE -s http://localhost:8001/api/v1/learning/patterns/{pattern_id} | python -m json.tool"
    )


async def test_invalid_pattern_id():
    """Test error handling for invalid pattern ID"""
    print("\n" + "=" * 80)
    print("TEST 6: GET /api/v1/learning/patterns/{invalid-id} (Error Handling)")
    print("=" * 80)
    print("curl -s http://localhost:8001/api/v1/learning/patterns/invalid-id | python -m json.tool")
    print("\nExpected: 400 error with INVALID_PATTERN_ID")
    print(
        "To run: curl -s http://localhost:8001/api/v1/learning/patterns/invalid-id | python -m json.tool"
    )


async def test_not_found():
    """Test error handling for non-existent pattern"""
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    print("\n" + "=" * 80)
    print(f"TEST 7: GET /api/v1/learning/patterns/{fake_uuid} (Not Found)")
    print("=" * 80)
    print(
        f"curl -s http://localhost:8001/api/v1/learning/patterns/{fake_uuid} | python -m json.tool"
    )
    print("\nExpected: 404 error with PATTERN_NOT_FOUND")
    print(
        f"To run: curl -s http://localhost:8001/api/v1/learning/patterns/{fake_uuid} | python -m json.tool"
    )


async def cleanup_test_patterns():
    """Clean up test patterns"""
    print("\n" + "=" * 80)
    print("CLEANUP: Removing test patterns")
    print("=" * 80)

    async with AsyncSessionFactory.session_scope() as session:
        from sqlalchemy import delete

        result = await session.execute(
            delete(LearnedPattern).where(LearnedPattern.user_id == TEST_USER_ID)
        )
        await session.commit()

        print(f"✅ Deleted {result.rowcount} test patterns")


async def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("PHASE 2.1 PATTERN MANAGEMENT ENDPOINTS - MANUAL TEST GUIDE")
    print("Issue #300 - CORE-ALPHA-LEARNING-BASIC")
    print("=" * 80)
    print("\nThis script creates test patterns and provides curl commands to test each endpoint.")
    print("Make sure the server is running on http://localhost:8001")
    print("\nStarting in 2 seconds...")
    await asyncio.sleep(2)

    # Create test patterns
    pattern_ids = await create_test_patterns()

    # Generate test commands
    await test_list_patterns()
    await test_get_pattern(pattern_ids[0])
    await test_enable_pattern(pattern_ids[2])  # Enable the disabled pattern
    await test_disable_pattern(pattern_ids[0])  # Disable an enabled pattern
    await test_delete_pattern(pattern_ids[1])  # Delete a pattern
    await test_invalid_pattern_id()
    await test_not_found()

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\nTest patterns created:")
    print(f"  - Pattern 1: {pattern_ids[0]} (workflow, enabled)")
    print(f"  - Pattern 2: {pattern_ids[1]} (command sequence, enabled)")
    print(f"  - Pattern 3: {pattern_ids[2]} (time-based, disabled)")
    print("\nRun the curl commands above to test each endpoint.")
    print("\nTo clean up test data, run:")
    print("  python tests/manual/test_phase2_patterns.py --cleanup")

    import sys

    if "--cleanup" in sys.argv:
        await cleanup_test_patterns()


if __name__ == "__main__":
    asyncio.run(main())
