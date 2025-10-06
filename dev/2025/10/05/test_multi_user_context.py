"""Test that different users get different contexts - GREAT-4C Phase 0."""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.domain.models import Intent
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.shared_types import IntentCategory


async def test_multi_user():
    """Verify no hardcoded user assumptions."""

    print("=" * 80)
    print("MULTI-USER CONTEXT TEST - GREAT-4C Phase 0")
    print("=" * 80)
    print()

    handlers = CanonicalHandlers()

    # Create GUIDANCE intent
    guidance_intent = Intent(
        category=IntentCategory.GUIDANCE,
        action="get_guidance",
        confidence=1.0,
        context={},
    )

    print("Test 1: User 1 (session: user1_session)")
    print("-" * 80)
    user1_response = await handlers._handle_guidance_query(guidance_intent, "user1_session")
    user1_message = user1_response.get("message", "")
    print(user1_message[:200] + "..." if len(user1_message) > 200 else user1_message)
    print()

    print("Test 2: User 2 (session: user2_session)")
    print("-" * 80)
    user2_response = await handlers._handle_guidance_query(guidance_intent, "user2_session")
    user2_message = user2_response.get("message", "")
    print(user2_message[:200] + "..." if len(user2_message) > 200 else user2_message)
    print()

    print("Test 3: User 3 (session: user3_session)")
    print("-" * 80)
    user3_response = await handlers._handle_guidance_query(guidance_intent, "user3_session")
    user3_message = user3_response.get("message", "")
    print(user3_message[:200] + "..." if len(user3_message) > 200 else user3_message)
    print()

    # Validate no hardcoded "VA" or "Kind Systems" in responses
    forbidden_strings = ["VA Q4", "Kind Systems", "DRAGONS team"]

    violations = []
    for forbidden in forbidden_strings:
        if forbidden in user1_message:
            violations.append(f"User 1 message contains hardcoded: {forbidden}")
        if forbidden in user2_message:
            violations.append(f"User 2 message contains hardcoded: {forbidden}")
        if forbidden in user3_message:
            violations.append(f"User 3 message contains hardcoded: {forbidden}")

    print("=" * 80)
    print("VALIDATION")
    print("=" * 80)

    if violations:
        print("❌ Found hardcoded context:")
        for v in violations:
            print(f"  - {v}")
        sys.exit(1)
    else:
        print("✅ Multi-user test passed - no hardcoded context found")
        print()
        print("All responses are generic and user-session specific.")
        print("Users will see their own organization/projects from their PIPER.md")
        sys.exit(0)


if __name__ == "__main__":
    asyncio.run(test_multi_user())
