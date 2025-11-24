#!/usr/bin/env python3
"""
Test and validate BreakthroughDetector against known breakthrough moments.

Validates detection of:
- Nov 1: Implementation Breakthrough (ADR-040 + refactoring)
- Nov 3: Discovery Breakthrough (parallel work + semantic emergence)
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pattern_analyzers.base import BreakthroughSignal
from pattern_analyzers.breakthrough_detector import BreakthroughDetector, BreakthroughType


async def test_breakthrough_detection():
    """Test BreakthroughDetector against Nov 1-3, 2025 known breakthroughs"""

    print("🔍 Testing BreakthroughDetector against Nov 1-3, 2025...")
    print("=" * 80)

    # Initialize detector
    project_root = Path(__file__).parent.parent
    detector = BreakthroughDetector(project_root)

    # Analyze period including both breakthroughs
    start_date = datetime(2025, 10, 31)
    end_date = datetime(2025, 11, 4)

    print(f"\n📅 Analysis Period: {start_date.date()} to {end_date.date()}")

    results = await detector.detect_breakthroughs(start_date, end_date)

    # Test 1: Signal Collection
    print("\n" + "=" * 80)
    print("TEST 1: Multi-Analyzer Signal Collection")
    print("=" * 80)

    all_signals = results.get("signals", {})
    print(f"✓ Collected {len(all_signals)} signal type(s) from all analyzers")

    print("\nSignals detected:")
    for signal_type, evidence in all_signals.items():
        print(f"  - {signal_type.value}")
        if isinstance(evidence, dict):
            if "count" in evidence:
                print(f"    Count: {evidence['count']}")
            if "dates" in evidence and evidence["dates"]:
                print(f"    Dates: {', '.join(evidence['dates'][:3])}")

    # Test 2: Signal Grouping by Date
    print("\n" + "=" * 80)
    print("TEST 2: Temporal Signal Clustering")
    print("=" * 80)

    signals_by_date = results.get("signals_by_date", {})
    print(f"✓ Grouped signals into {len(signals_by_date)} date(s)")

    for date, signals_list in sorted(signals_by_date.items()):
        print(f"\n  {date}: {len(signals_list)} signal(s)")
        for signal_type, _ in signals_list:
            print(f"    - {signal_type.value}")

    # Test 3: Breakthrough Event Detection
    print("\n" + "=" * 80)
    print("TEST 3: Breakthrough Event Classification")
    print("=" * 80)

    breakthroughs = results.get("breakthroughs", [])
    print(f"✓ Detected {len(breakthroughs)} breakthrough event(s)")

    for breakthrough in breakthroughs:
        print(f"\n  {breakthrough['type'].upper()}")
        print(f"    Date: {breakthrough['date']}")
        print(f"    Confidence: {breakthrough['confidence']:.0%}")
        print(f"    Signals: {breakthrough['signal_count']} total")
        print(f"    Analyzers: {', '.join(breakthrough['analyzers_involved'])}")
        print(f"    Required: {[s.value for s in breakthrough['required_signals']]}")
        print(f"    Supporting: {[s.value for s in breakthrough['supporting_signals']]}")

    # Test 4: Analysis Metadata
    print("\n" + "=" * 80)
    print("TEST 4: Analysis Metadata Aggregation")
    print("=" * 80)

    metadata = results.get("analysis_metadata", {})

    print("\nTemporal Analysis:")
    print(f"  Baseline velocity: {metadata['temporal']['baseline_velocity']:.2f} commits/day")
    print(f"  Total commits: {metadata['temporal']['total_commits']}")

    print("\nSemantic Analysis:")
    print(f"  Concepts emerged: {metadata['semantic']['total_concepts_emerged']}")
    print(f"  High-validation concepts: {metadata['semantic']['high_validation_concepts']}")

    print("\nStructural Analysis:")
    print(f"  ADRs created: {metadata['structural']['total_adrs_created']}")
    print(f"  Refactoring events: {metadata['structural']['refactoring_events']}")

    # Test 5: Report Generation
    print("\n" + "=" * 80)
    print("TEST 5: Report Generation")
    print("=" * 80)

    report = detector.generate_breakthrough_report(results)
    print("\n" + report)

    # Validation Summary
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)

    expected_breakthroughs = {
        "nov_1_implementation": False,
        "nov_3_discovery": False,
        "multi_analyzer": False,
        "confidence_scores": False,
    }

    # Check for Nov 1 Implementation Breakthrough
    nov_1_breakthroughs = [b for b in breakthroughs if "2025-11-01" in b["date"]]
    implementation_breakthroughs = [
        b for b in nov_1_breakthroughs if b["type"] == BreakthroughType.IMPLEMENTATION
    ]
    expected_breakthroughs["nov_1_implementation"] = len(implementation_breakthroughs) > 0

    # Check for Nov 3 Discovery Breakthrough
    nov_3_breakthroughs = [b for b in breakthroughs if "2025-11-03" in b["date"]]
    discovery_breakthroughs = [
        b for b in nov_3_breakthroughs if b["type"] == BreakthroughType.DISCOVERY
    ]
    expected_breakthroughs["nov_3_discovery"] = len(discovery_breakthroughs) > 0

    # Check for multi-analyzer convergence
    multi_analyzer_breakthroughs = [b for b in breakthroughs if len(b["analyzers_involved"]) >= 2]
    expected_breakthroughs["multi_analyzer"] = len(multi_analyzer_breakthroughs) > 0

    # Check confidence scores
    high_confidence_breakthroughs = [b for b in breakthroughs if b["confidence"] >= 0.6]
    expected_breakthroughs["confidence_scores"] = len(high_confidence_breakthroughs) > 0

    print("\n✅ Expected Breakthroughs vs Detected:")
    for key, detected in expected_breakthroughs.items():
        status = "✅ PASS" if detected else "❌ FAIL"
        print(f"  {key}: {status}")

    # Detailed breakdown
    print("\n📊 Breakthrough Type Breakdown:")
    breakthrough_types = {}
    for b in breakthroughs:
        bt = b["type"]
        if bt not in breakthrough_types:
            breakthrough_types[bt] = []
        breakthrough_types[bt].append(b["date"])

    for bt, dates in breakthrough_types.items():
        print(f"  {bt}: {len(dates)} event(s) on {', '.join(dates)}")

    # Overall validation
    passed = sum(1 for v in expected_breakthroughs.values() if v)
    total = len(expected_breakthroughs)
    print(f"\n🎯 Validation Score: {passed}/{total} ({100*passed/total:.0f}%)")

    if passed >= 3:  # At least 3/4 tests pass
        print("✅ BreakthroughDetector validation PASSED")
        return True
    else:
        print("❌ BreakthroughDetector validation FAILED")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_breakthrough_detection())
    sys.exit(0 if success else 1)
