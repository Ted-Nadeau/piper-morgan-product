#!/usr/bin/env python3
"""
Test and validate SemanticAnalyzer against known breakthrough moments.

Validates Nov 3, 2025 detection:
- Expected: "ActionHumanizer" emergence
- Expected: "75% pattern" emergence (3× usage)
- Expected: "EnhancedErrorMiddleware" emergence
- Expected: "archaeological investigation" concept
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pattern_analyzers.base import BreakthroughSignal
from pattern_analyzers.semantic_analyzer import SemanticAnalyzer


async def test_nov_3_semantic_detection():
    """Test SemanticAnalyzer against Nov 3, 2025 known breakthrough"""

    print("🔍 Testing SemanticAnalyzer against Nov 3, 2025 data...")
    print("=" * 70)

    # Initialize analyzer
    project_root = Path(__file__).parent.parent
    analyzer = SemanticAnalyzer(project_root)

    # Analyze period including Nov 3
    start_date = datetime(2025, 11, 1)
    end_date = datetime(2025, 11, 4)

    print(f"\n📅 Analysis Period: {start_date.date()} to {end_date.date()}")

    results = await analyzer.analyze(start_date, end_date)

    # Test 1: Term Emergence Detection
    print("\n" + "=" * 70)
    print("TEST 1: Concept Emergence Detection")
    print("=" * 70)

    term_emergence = results.get("term_emergence", [])
    print(f"✓ Detected {len(term_emergence)} emergent concept(s)")

    for term_data in term_emergence[:10]:  # Show top 10
        print(f"\n  Concept: {term_data['term']}")
        print(f"  First Seen: {term_data['first_seen']}")
        print(f"  First Context: {term_data['first_context']}")
        print(f"  Total Occurrences: {term_data['total_occurrences']}")
        print(f"  Spread: {term_data['spread']} files")
        print(f"  Contexts: {', '.join(term_data['contexts'])}")

    # Test 2: Term Evolution
    print("\n" + "=" * 70)
    print("TEST 2: Concept Evolution Tracking")
    print("=" * 70)

    term_evolution = results.get("term_evolution", {})
    print(f"✓ Tracked evolution for {len(term_evolution)} concept(s)")

    for term, evolution in list(term_evolution.items())[:5]:  # Show top 5
        print(f"\n  Concept: {term}")
        print(f"  Growth Rate: {evolution['growth_rate']:.2f}x")
        print(f"  Trend: {evolution['trend']}")
        print(f"  Spread Velocity: {evolution['spread_velocity']:.2f} files/day")
        print(f"  Total Occurrences: {evolution['total_occurrences']}")

    # Test 3: Context Classification
    print("\n" + "=" * 70)
    print("TEST 3: Context Classification")
    print("=" * 70)

    context_classification = results.get("context_classification", {})
    print(f"✓ Classified contexts for {len(context_classification)} concept(s)")

    # Show concepts with multiple contexts (cross-validated)
    multi_context_terms = {
        term: contexts for term, contexts in context_classification.items() if len(contexts) >= 2
    }

    print(f"\n  Cross-context concepts: {len(multi_context_terms)}")
    for term, contexts in list(multi_context_terms.items())[:5]:
        print(f"    {term}: {', '.join(f'{ctx}({count})' for ctx, count in contexts.items())}")

    # Test 4: Validation Scores
    print("\n" + "=" * 70)
    print("TEST 4: Validation Scores (Cross-Context)")
    print("=" * 70)

    validation_scores = results.get("validation_scores", {})
    print(f"✓ Calculated validation for {len(validation_scores)} concept(s)")

    # Show high-validation concepts (appear in multiple key contexts)
    high_validation = {term: score for term, score in validation_scores.items() if score >= 0.5}

    print(f"\n  High-validation concepts: {len(high_validation)}")
    for term, score in sorted(high_validation.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"    {term}: {score:.2f}")

    # Test 5: Concept Clusters
    print("\n" + "=" * 70)
    print("TEST 5: Concept Clusters (Related Concepts)")
    print("=" * 70)

    concept_clusters = results.get("concept_clusters", [])
    print(f"✓ Detected {len(concept_clusters)} concept cluster(s)")

    for cluster in concept_clusters:
        print(f"\n  Period: {cluster['period']}")
        print(f"  Concepts: {', '.join(cluster['terms'])}")
        print(f"  Cohesion: {cluster['cohesion']:.2f}")
        print(f"  Common Files: {len(cluster['common_files'])}")

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

    # Expected Nov 3 concepts
    expected_concepts = {
        "ActionHumanizer",
        "75% pattern",
        "EnhancedErrorMiddleware",
        "archaeological investigation",
    }

    # Check which expected concepts were detected
    detected_terms = {t["term"] for t in term_emergence}
    found_concepts = expected_concepts & detected_terms

    print(f"\n✅ Expected Concepts vs Detected:")
    for concept in expected_concepts:
        found = concept in detected_terms
        status = "✅ DETECTED" if found else "❌ MISSED"
        print(f"  {concept}: {status}")

    print(f"\n📊 Detection Stats:")
    print(f"  Expected Concepts: {len(expected_concepts)}")
    print(f"  Detected Concepts: {len(found_concepts)}")
    print(f"  Detection Rate: {100*len(found_concepts)/len(expected_concepts):.0f}%")

    # Validation criteria
    semantic_emergence_detected = BreakthroughSignal.SEMANTIC_EMERGENCE in signals
    architectural_insight_detected = BreakthroughSignal.ARCHITECTURAL_INSIGHT in signals
    concepts_detected = len(found_concepts) >= 2  # At least 2/4 expected

    print(f"\n🎯 Validation Checks:")
    print(f"  Semantic Emergence Signal: {'✅' if semantic_emergence_detected else '❌'}")
    print(f"  Architectural Insight Signal: {'✅' if architectural_insight_detected else '❌'}")
    print(f"  Expected Concepts Found: {'✅' if concepts_detected else '❌'}")

    # Overall validation
    passed = sum([semantic_emergence_detected, architectural_insight_detected, concepts_detected])
    total = 3

    print(f"\n🎯 Validation Score: {passed}/{total} ({100*passed/total:.0f}%)")

    if passed >= 2:  # At least 2/3 tests pass
        print("✅ SemanticAnalyzer validation PASSED")
        return True
    else:
        print("❌ SemanticAnalyzer validation FAILED")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_nov_3_semantic_detection())
    sys.exit(0 if success else 1)
