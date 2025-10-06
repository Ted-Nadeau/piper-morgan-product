"""Test spatial intelligence in handlers - GREAT-4C Phase 1."""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.domain.models import Intent
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.shared_types import IntentCategory


async def test_spatial_patterns():
    """Test different spatial patterns produce different detail levels."""

    print("=" * 80)
    print("SPATIAL INTELLIGENCE TEST - GREAT-4C Phase 1")
    print("=" * 80)
    print()

    handlers = CanonicalHandlers()

    # Test STATUS query with different patterns
    print("Testing STATUS handler with spatial patterns...\n")

    # Test GRANULAR (detailed)
    print("1. GRANULAR Pattern (detailed):")
    print("-" * 80)
    granular_intent = Intent(
        category=IntentCategory.STATUS,
        action="provide_status",
        confidence=1.0,
        context={},
    )
    granular_intent.spatial_context = {"pattern": "GRANULAR"}  # Set as attribute
    granular_response = await handlers._handle_status_query(granular_intent, "test_session")
    print(granular_response["message"])
    print(f"\nLength: {len(granular_response['message'])} chars")
    print(f"Spatial pattern recognized: {granular_response.get('spatial_pattern')}")
    print()

    # Test EMBEDDED (brief)
    print("2. EMBEDDED Pattern (brief):")
    print("-" * 80)
    embedded_intent = Intent(
        category=IntentCategory.STATUS,
        action="provide_status",
        confidence=1.0,
        context={},
    )
    embedded_intent.spatial_context = {"pattern": "EMBEDDED"}  # Set as attribute
    embedded_response = await handlers._handle_status_query(embedded_intent, "test_session")
    print(embedded_response["message"])
    print(f"\nLength: {len(embedded_response['message'])} chars")
    print(f"Spatial pattern recognized: {embedded_response.get('spatial_pattern')}")
    print()

    # Test DEFAULT (standard)
    print("3. DEFAULT Pattern (standard - no spatial context):")
    print("-" * 80)
    default_intent = Intent(
        category=IntentCategory.STATUS,
        action="provide_status",
        confidence=1.0,
        context={},
    )
    # No spatial_context attribute set - should use DEFAULT
    default_response = await handlers._handle_status_query(default_intent, "test_session")
    print(default_response["message"])
    print(f"\nLength: {len(default_response['message'])} chars")
    print(f"Spatial pattern recognized: {default_response.get('spatial_pattern')}")
    print()

    # Validate different detail levels
    granular_len = len(granular_response["message"])
    embedded_len = len(embedded_response["message"])
    default_len = len(default_response["message"])

    print("=" * 80)
    print("VALIDATION")
    print("=" * 80)

    checks = []

    # Check 1: GRANULAR should be more detailed than DEFAULT
    if granular_len > default_len:
        print("✅ GRANULAR is more detailed than DEFAULT")
        checks.append(True)
    else:
        print(f"❌ GRANULAR ({granular_len}) should be > DEFAULT ({default_len})")
        checks.append(False)

    # Check 2: EMBEDDED should be briefer than DEFAULT
    if embedded_len < default_len:
        print("✅ EMBEDDED is briefer than DEFAULT")
        checks.append(True)
    else:
        print(f"❌ EMBEDDED ({embedded_len}) should be < DEFAULT ({default_len})")
        checks.append(False)

    # Check 3: Spatial pattern tracked in response
    if granular_response.get("spatial_pattern") == "GRANULAR":
        print("✅ Spatial pattern tracked in response")
        checks.append(True)
    else:
        print("❌ Spatial pattern not tracked properly")
        checks.append(False)

    print()
    if all(checks):
        print("✅ All spatial intelligence tests passed")
        print()
        print("Spatial intelligence is working correctly:")
        print(f"  - GRANULAR: {granular_len} chars (detailed)")
        print(f"  - DEFAULT:  {default_len} chars (moderate)")
        print(f"  - EMBEDDED: {embedded_len} chars (brief)")
        return 0
    else:
        print(f"❌ {len([c for c in checks if not c])} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(test_spatial_patterns())
    sys.exit(exit_code)
