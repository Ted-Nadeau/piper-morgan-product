#!/usr/bin/env python3
"""
Test and validate StructuralAnalyzer against known breakthrough moments.

Validates Nov 1, 2025 detection:
- Expected: ADR-040 creation (Local Database Per Environment)
- Expected: ADR_CREATION breakthrough signal
- Expected: Refactoring event detection (P0 blockers breakthrough)
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pattern_analyzers.base import BreakthroughSignal
from pattern_analyzers.structural_analyzer import StructuralAnalyzer


async def test_nov_1_structural_detection():
    """Test StructuralAnalyzer against Nov 1, 2025 known breakthrough"""

    print("🔍 Testing StructuralAnalyzer against Nov 1, 2025 data...")
    print("=" * 70)

    # Initialize analyzer
    project_root = Path(__file__).parent.parent
    analyzer = StructuralAnalyzer(project_root)

    # Analyze period including Nov 1
    start_date = datetime(2025, 10, 31)
    end_date = datetime(2025, 11, 2)

    print(f"\n📅 Analysis Period: {start_date.date()} to {end_date.date()}")

    results = await analyzer.analyze(start_date, end_date)

    # Test 1: ADR Activity Detection
    print("\n" + "=" * 70)
    print("TEST 1: ADR Activity Detection")
    print("=" * 70)

    adr_activity = results.get("adr_activity", {})
    adr_events = adr_activity.get("events", [])
    print(f"✓ Detected {len(adr_events)} ADR creation(s)")

    for event in adr_events:
        print(f"\n  ADR-{event['adr_number']}: {event['title']}")
        print(f"  Created: {event['created']}")
        print(f"  File: {event['file']}")
        print(f"  Commit: {event['commit']}")
        print(f"  Author: {event['author']}")

    # Test 2: Refactoring Events
    print("\n" + "=" * 70)
    print("TEST 2: Refactoring Event Detection")
    print("=" * 70)

    refactoring_events = results.get("refactoring_events", [])
    print(f"✓ Detected {len(refactoring_events)} refactoring event(s)")

    for event in refactoring_events[:5]:  # Show top 5
        print(f"\n  Date: {event['date']}")
        print(f"  Commit: {event['commit']}")
        print(f"  Message: {event['message']}")
        print(f"  Files Changed: {event['files_changed']}")
        print(f"  Lines +{event['lines_added']} -{event['lines_deleted']}")
        print(f"  Type: {event['type']}")

    # Test 3: Class Evolution
    print("\n" + "=" * 70)
    print("TEST 3: Class Evolution Tracking")
    print("=" * 70)

    class_evolution = results.get("class_evolution", {})
    new_classes = class_evolution.get("new_classes", [])
    total_classes = class_evolution.get("total_classes_created", 0)

    print(f"✓ Detected {total_classes} new class(es)")
    print(f"✓ Classes per day: {class_evolution.get('classes_per_day', 0):.2f}")

    if new_classes:
        print("\n  Sample new classes:")
        for cls in new_classes[:5]:  # Show first 5
            print(f"    {cls['class_name']} ({cls['base_classes'] or 'no base'})")
            print(f"      File: {cls['file']}")
            print(f"      Date: {cls['date']}")

    # Test 4: Import Changes
    print("\n" + "=" * 70)
    print("TEST 4: Import Graph Analysis")
    print("=" * 70)

    import_changes = results.get("import_changes", {})
    unique_modules = import_changes.get("unique_modules_imported", 0)
    total_imports = import_changes.get("total_import_uses", 0)

    print(f"✓ Unique modules: {unique_modules}")
    print(f"✓ Total import uses: {total_imports}")

    top_imports = import_changes.get("top_imported_modules", [])
    if top_imports:
        print("\n  Top imported modules:")
        for imp in top_imports[:5]:
            print(f"    {imp['module']}: {imp['usage_count']} uses")

    # Test 5: Architectural Patterns
    print("\n" + "=" * 70)
    print("TEST 5: Architectural Pattern Detection")
    print("=" * 70)

    architectural_patterns = results.get("architectural_patterns", {})
    patterns_detected = architectural_patterns.get("patterns_detected", [])
    pattern_usage = architectural_patterns.get("pattern_usage", {})

    print(f"✓ Detected {len(patterns_detected)} architectural pattern type(s)")

    if patterns_detected:
        print("\n  Patterns found:")
        for pattern in patterns_detected:
            usage_count = pattern_usage.get(pattern, 0)
            print(f"    {pattern}: {usage_count} occurrences")

    # Test 6: Breakthrough Signals
    print("\n" + "=" * 70)
    print("TEST 6: Breakthrough Signal Extraction")
    print("=" * 70)

    signals = analyzer.get_breakthrough_signals()
    print(f"✓ Extracted {len(signals)} breakthrough signal type(s)")

    for signal_type, evidence in signals.items():
        print(f"\n  Signal: {signal_type.value}")
        print(f"  Evidence: {evidence}")

    # Validation Summary
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)

    nov_1_expected = {
        "adr_creation": True,
        "adr_040_detected": True,
        "refactoring_events": True,
    }

    # Check expectations
    validation_results = {}

    # ADR creation on Nov 1?
    nov_1_adrs = [a for a in adr_events if "2025-11-01" in a["created"]]
    validation_results["adr_creation"] = len(nov_1_adrs) > 0

    # ADR-040 specifically detected?
    adr_040_found = any(a["adr_number"] == "040" for a in adr_events)
    validation_results["adr_040_detected"] = adr_040_found

    # Refactoring events on Nov 1?
    nov_1_refactorings = [r for r in refactoring_events if "2025-11-01" in r["date"]]
    validation_results["refactoring_events"] = len(nov_1_refactorings) > 0

    print("\n✅ Expected vs Detected:")
    for key, expected in nov_1_expected.items():
        detected = validation_results.get(key, False)
        status = "✅ PASS" if detected == expected else "❌ FAIL"
        print(f"  {key}: Expected={expected}, Detected={detected} {status}")

    # Check for ADR_CREATION signal
    adr_signal_detected = BreakthroughSignal.ADR_CREATION in signals
    print(f"\n  ADR_CREATION signal: {'✅ DETECTED' if adr_signal_detected else '❌ MISSED'}")

    # Overall validation
    passed = sum(1 for v in validation_results.values() if v)
    total = len(validation_results)
    print(f"\n🎯 Validation Score: {passed}/{total} ({100*passed/total:.0f}%)")

    if passed >= 2:  # At least 2/3 tests pass
        print("✅ StructuralAnalyzer validation PASSED")
        return True
    else:
        print("❌ StructuralAnalyzer validation FAILED")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_nov_1_structural_detection())
    sys.exit(0 if success else 1)
