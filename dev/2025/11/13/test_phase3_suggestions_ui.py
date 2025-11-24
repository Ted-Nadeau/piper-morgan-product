#!/usr/bin/env python3
"""
Test Phase 3.2: Suggestions UI

Creates test patterns and verifies suggestions appear in UI.
"""
import asyncio
from uuid import UUID

import requests

from services.database.models import LearnedPattern, PatternType
from services.database.session_factory import AsyncSessionFactory


async def create_test_pattern():
    """Create a high-confidence test pattern"""
    async with AsyncSessionFactory.session_scope() as session:
        # Test user from Phase 2
        user_id = UUID("3f4593ae-5bc9-468d-b08d-8c4c02a5b963")

        # Create a high-confidence pattern (0.75 > 0.7 threshold)
        pattern = LearnedPattern(
            user_id=user_id,
            pattern_type=PatternType.USER_WORKFLOW,
            pattern_data={
                "intent": "status",
                "description": "Check project status in the morning",
                "reasoning": "You frequently check status at the start of the day",
            },
            confidence=0.85,
            usage_count=12,
            success_count=10,
            failure_count=2,
            enabled=True,
        )

        session.add(pattern)
        await session.commit()
        await session.refresh(pattern)

        print(f"✅ Created test pattern: {pattern.id}")
        print(f"   Type: {pattern.pattern_type.value}")
        print(f"   Confidence: {pattern.confidence}")
        print(f"   Reasoning: {pattern.pattern_data['reasoning']}")

        return pattern.id


def test_api_response():
    """Test that API returns suggestions"""
    print("\n🧪 Testing API response...")

    response = requests.post(
        "http://localhost:8001/api/v1/intent",
        json={"message": "what is my status", "session_id": "test-ui"},
        timeout=10,
    )

    if response.status_code == 200:
        data = response.json()
        suggestions = data.get("suggestions", [])

        print(f"✅ API returned {len(suggestions)} suggestions")

        if suggestions:
            print("\n📋 Suggestion details:")
            for s in suggestions:
                print(f"   Pattern ID: {s['pattern_id']}")
                print(f"   Confidence: {s['confidence']}")
                print(f"   Type: {s['pattern_type']}")
                print(f"   Usage: {s['usage_count']} times")
        else:
            print("⚠️  No suggestions returned (threshold may not be met)")
    else:
        print(f"❌ API error: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    print("=" * 60)
    print("PHASE 3.2 SUGGESTIONS UI TEST")
    print("=" * 60)

    # Create test pattern
    pattern_id = asyncio.run(create_test_pattern())

    # Test API
    test_api_response()

    print("\n✅ TEST COMPLETE")
    print("\n📌 Next Steps:")
    print("1. Open http://localhost:8001 in browser")
    print("2. Type: 'what is my status'")
    print("3. Verify suggestions badge appears")
    print("4. Click badge to expand panel")
    print("5. Test Accept/Reject/Dismiss buttons")
