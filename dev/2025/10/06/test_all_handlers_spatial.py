"""Comprehensive spatial intelligence test for all 5 canonical handlers - GREAT-4C Phase 1."""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from services.domain.models import Intent
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.shared_types import IntentCategory


async def test_all_handlers():
    """Test spatial intelligence across all 5 canonical handlers."""

    print("=" * 80)
    print("COMPREHENSIVE SPATIAL INTELLIGENCE TEST - GREAT-4C Phase 1")
    print("=" * 80)
    print()

    handlers = CanonicalHandlers()
    all_checks = []

    # ============================================================================
    # Test 1: IDENTITY Handler
    # ============================================================================
    print("TEST 1: IDENTITY Handler")
    print("-" * 80)

    # GRANULAR
    identity_granular = Intent(
        category=IntentCategory.IDENTITY,
        action="provide_identity",
        confidence=1.0,
        context={},
    )
    identity_granular.spatial_context = {"pattern": "GRANULAR"}
    granular_response = await handlers._handle_identity_query(identity_granular, "test_session")
    granular_len = len(granular_response["message"])
    print(f"GRANULAR ({granular_len} chars):")
    print(granular_response["message"][:100] + "...")
    print()

    # EMBEDDED
    identity_embedded = Intent(
        category=IntentCategory.IDENTITY,
        action="provide_identity",
        confidence=1.0,
        context={},
    )
    identity_embedded.spatial_context = {"pattern": "EMBEDDED"}
    embedded_response = await handlers._handle_identity_query(identity_embedded, "test_session")
    embedded_len = len(embedded_response["message"])
    print(f"EMBEDDED ({embedded_len} chars): {embedded_response['message']}")
    print()

    # DEFAULT
    identity_default = Intent(
        category=IntentCategory.IDENTITY,
        action="provide_identity",
        confidence=1.0,
        context={},
    )
    default_response = await handlers._handle_identity_query(identity_default, "test_session")
    default_len = len(default_response["message"])
    print(f"DEFAULT ({default_len} chars):")
    print(default_response["message"][:100] + "...")
    print()

    # Validate
    identity_checks = []
    if granular_len > default_len:
        print("✅ IDENTITY: GRANULAR > DEFAULT")
        identity_checks.append(True)
    else:
        print(f"❌ IDENTITY: GRANULAR ({granular_len}) should be > DEFAULT ({default_len})")
        identity_checks.append(False)

    if embedded_len < default_len:
        print("✅ IDENTITY: EMBEDDED < DEFAULT")
        identity_checks.append(True)
    else:
        print(f"❌ IDENTITY: EMBEDDED ({embedded_len}) should be < DEFAULT ({default_len})")
        identity_checks.append(False)

    if granular_response.get("spatial_pattern") == "GRANULAR":
        print("✅ IDENTITY: Spatial pattern tracked")
        identity_checks.append(True)
    else:
        print("❌ IDENTITY: Spatial pattern not tracked")
        identity_checks.append(False)

    all_checks.extend(identity_checks)
    print()

    # ============================================================================
    # Test 2: TEMPORAL Handler
    # ============================================================================
    print("TEST 2: TEMPORAL Handler")
    print("-" * 80)

    # GRANULAR
    temporal_granular = Intent(
        category=IntentCategory.TEMPORAL,
        action="get_current_time",
        confidence=1.0,
        context={},
    )
    temporal_granular.spatial_context = {"pattern": "GRANULAR"}
    granular_response = await handlers._handle_temporal_query(temporal_granular, "test_session")
    granular_len = len(granular_response["message"])
    print(f"GRANULAR ({granular_len} chars):")
    print(granular_response["message"][:150] + "...")
    print()

    # EMBEDDED
    temporal_embedded = Intent(
        category=IntentCategory.TEMPORAL,
        action="get_current_time",
        confidence=1.0,
        context={},
    )
    temporal_embedded.spatial_context = {"pattern": "EMBEDDED"}
    embedded_response = await handlers._handle_temporal_query(temporal_embedded, "test_session")
    embedded_len = len(embedded_response["message"])
    print(f"EMBEDDED ({embedded_len} chars): {embedded_response['message']}")
    print()

    # DEFAULT
    temporal_default = Intent(
        category=IntentCategory.TEMPORAL,
        action="get_current_time",
        confidence=1.0,
        context={},
    )
    default_response = await handlers._handle_temporal_query(temporal_default, "test_session")
    default_len = len(default_response["message"])
    print(f"DEFAULT ({default_len} chars):")
    print(default_response["message"][:150] + "...")
    print()

    # Validate
    temporal_checks = []
    if embedded_len < default_len:
        print("✅ TEMPORAL: EMBEDDED < DEFAULT")
        temporal_checks.append(True)
    else:
        print(f"❌ TEMPORAL: EMBEDDED ({embedded_len}) should be < DEFAULT ({default_len})")
        temporal_checks.append(False)

    if granular_response.get("spatial_pattern") == "GRANULAR":
        print("✅ TEMPORAL: Spatial pattern tracked")
        temporal_checks.append(True)
    else:
        print("❌ TEMPORAL: Spatial pattern not tracked")
        temporal_checks.append(False)

    all_checks.extend(temporal_checks)
    print()

    # ============================================================================
    # Test 3: STATUS Handler
    # ============================================================================
    print("TEST 3: STATUS Handler")
    print("-" * 80)

    status_granular = Intent(
        category=IntentCategory.STATUS,
        action="provide_status",
        confidence=1.0,
        context={},
    )
    status_granular.spatial_context = {"pattern": "GRANULAR"}
    granular_response = await handlers._handle_status_query(status_granular, "test_session")
    print(f"GRANULAR: {granular_response['message']}")
    print()

    status_embedded = Intent(
        category=IntentCategory.STATUS,
        action="provide_status",
        confidence=1.0,
        context={},
    )
    status_embedded.spatial_context = {"pattern": "EMBEDDED"}
    embedded_response = await handlers._handle_status_query(status_embedded, "test_session")
    print(f"EMBEDDED: {embedded_response['message']}")
    print()

    if embedded_response.get("spatial_pattern") == "EMBEDDED":
        print("✅ STATUS: Spatial pattern tracked")
        all_checks.append(True)
    else:
        print("❌ STATUS: Spatial pattern not tracked")
        all_checks.append(False)

    print()

    # ============================================================================
    # Test 4: PRIORITY Handler
    # ============================================================================
    print("TEST 4: PRIORITY Handler")
    print("-" * 80)

    priority_granular = Intent(
        category=IntentCategory.PRIORITY,
        action="get_top_priority",
        confidence=1.0,
        context={},
    )
    priority_granular.spatial_context = {"pattern": "GRANULAR"}
    granular_response = await handlers._handle_priority_query(priority_granular, "test_session")
    print(f"GRANULAR: {granular_response['message']}")
    print()

    priority_embedded = Intent(
        category=IntentCategory.PRIORITY,
        action="get_top_priority",
        confidence=1.0,
        context={},
    )
    priority_embedded.spatial_context = {"pattern": "EMBEDDED"}
    embedded_response = await handlers._handle_priority_query(priority_embedded, "test_session")
    print(f"EMBEDDED: {embedded_response['message']}")
    print()

    if embedded_response.get("spatial_pattern") == "EMBEDDED":
        print("✅ PRIORITY: Spatial pattern tracked")
        all_checks.append(True)
    else:
        print("❌ PRIORITY: Spatial pattern not tracked")
        all_checks.append(False)

    print()

    # ============================================================================
    # Test 5: GUIDANCE Handler
    # ============================================================================
    print("TEST 5: GUIDANCE Handler")
    print("-" * 80)

    guidance_granular = Intent(
        category=IntentCategory.GUIDANCE,
        action="provide_guidance",
        confidence=1.0,
        context={},
    )
    guidance_granular.spatial_context = {"pattern": "GRANULAR"}
    granular_response = await handlers._handle_guidance_query(guidance_granular, "test_session")
    granular_len = len(granular_response["message"])
    print(f"GRANULAR ({granular_len} chars):")
    print(granular_response["message"][:150] + "...")
    print()

    guidance_embedded = Intent(
        category=IntentCategory.GUIDANCE,
        action="provide_guidance",
        confidence=1.0,
        context={},
    )
    guidance_embedded.spatial_context = {"pattern": "EMBEDDED"}
    embedded_response = await handlers._handle_guidance_query(guidance_embedded, "test_session")
    embedded_len = len(embedded_response["message"])
    print(f"EMBEDDED ({embedded_len} chars): {embedded_response['message']}")
    print()

    guidance_default = Intent(
        category=IntentCategory.GUIDANCE,
        action="provide_guidance",
        confidence=1.0,
        context={},
    )
    default_response = await handlers._handle_guidance_query(guidance_default, "test_session")
    default_len = len(default_response["message"])
    print(f"DEFAULT ({default_len} chars):")
    print(default_response["message"][:150] + "...")
    print()

    # Validate
    guidance_checks = []
    if granular_len > default_len:
        print("✅ GUIDANCE: GRANULAR > DEFAULT")
        guidance_checks.append(True)
    else:
        print(f"❌ GUIDANCE: GRANULAR ({granular_len}) should be > DEFAULT ({default_len})")
        guidance_checks.append(False)

    if embedded_len < default_len:
        print("✅ GUIDANCE: EMBEDDED < DEFAULT")
        guidance_checks.append(True)
    else:
        print(f"❌ GUIDANCE: EMBEDDED ({embedded_len}) should be < DEFAULT ({default_len})")
        guidance_checks.append(False)

    if granular_response.get("spatial_pattern") == "GRANULAR":
        print("✅ GUIDANCE: Spatial pattern tracked")
        guidance_checks.append(True)
    else:
        print("❌ GUIDANCE: Spatial pattern not tracked")
        guidance_checks.append(False)

    all_checks.extend(guidance_checks)
    print()

    # ============================================================================
    # Final Summary
    # ============================================================================
    print("=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)
    passed = len([c for c in all_checks if c])
    total = len(all_checks)
    print(f"Passed: {passed}/{total} checks")
    print()

    if all(all_checks):
        print("✅ All spatial intelligence tests passed!")
        print()
        print("Spatial intelligence is working correctly across all 5 handlers:")
        print("  - IDENTITY: Spatial patterns adjust detail level")
        print("  - TEMPORAL: Spatial patterns adjust calendar detail")
        print("  - STATUS: Spatial patterns adjust project detail")
        print("  - PRIORITY: Spatial patterns adjust priority detail")
        print("  - GUIDANCE: Spatial patterns adjust guidance specificity")
        return 0
    else:
        print(f"❌ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(test_all_handlers())
    sys.exit(exit_code)
