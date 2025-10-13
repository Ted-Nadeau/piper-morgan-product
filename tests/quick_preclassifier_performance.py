"""Quick pre-classifier performance verification for GAP-3 Phase 4"""

import time

from services.intent_service.pre_classifier import PreClassifier


def test_preclassifier_performance():
    """Verify pre-classifier performance with new GUIDANCE patterns"""

    test_queries = [
        # New GUIDANCE patterns (added in GAP-3 Phase 2)
        "what should I do about this issue",
        "advise me on the best approach",
        "what's the process for creating an issue",
        # Existing canonical patterns
        "what's my top priority",
        "what's on my calendar today",
        "what am I working on",
        "who are you",
        # Control queries (no pre-classifier match)
        "tell me about quantum computing",
        "how do neural networks work",
    ]

    print("\n" + "=" * 80)
    print("PRE-CLASSIFIER PERFORMANCE TEST")
    print("=" * 80)
    print(f"Testing {len(test_queries)} queries with new GUIDANCE patterns")
    print("=" * 80 + "\n")

    times = []
    results = []

    for query in test_queries:
        start = time.perf_counter()
        result = PreClassifier.pre_classify(query)
        end = time.perf_counter()
        elapsed = (end - start) * 1000  # Convert to milliseconds
        times.append(elapsed)

        category = result.category.value if result else "None (LLM fallback)"
        status = "✅" if result else "➡️"

        results.append({"query": query, "time": elapsed, "category": category, "status": status})

        print(f"{status} {query[:45]:45s} | {elapsed:6.3f}ms | {category}")

    avg_time = sum(times) / len(times)
    max_time = max(times)
    min_time = min(times)
    pre_classifier_hits = sum(1 for r in results if r["status"] == "✅")

    print("\n" + "=" * 80)
    print("PERFORMANCE SUMMARY")
    print("=" * 80)
    print(f"Queries tested:       {len(test_queries)}")
    print(f"Pre-classifier hits:  {pre_classifier_hits}/{len(test_queries)}")
    print(f"Average time:         {avg_time:.3f}ms")
    print(f"Min time:             {min_time:.3f}ms")
    print(f"Max time:             {max_time:.3f}ms")
    print(f"Target:               <1.0ms (average)")
    print(f"Tolerance:            <5.0ms (max)")
    print("=" * 80)

    # Assertions
    passed = True

    if avg_time >= 1.0:
        print(f"\n❌ FAIL: Average time {avg_time:.3f}ms exceeds 1ms target")
        passed = False
    else:
        print(f"\n✅ PASS: Average time {avg_time:.3f}ms < 1ms target")

    if max_time >= 5.0:
        print(f"⚠️  WARNING: Max time {max_time:.3f}ms exceeds 5ms tolerance")
        passed = False
    else:
        print(f"✅ PASS: Max time {max_time:.3f}ms < 5ms tolerance")

    # Check that new GUIDANCE patterns work
    new_guidance_queries = [q for q in test_queries[:3]]
    new_guidance_hits = sum(
        1 for r in results[:3] if r["status"] == "✅" and r["category"] == "guidance"
    )

    if new_guidance_hits == 3:
        print(f"✅ PASS: All 3 new GUIDANCE patterns working ({new_guidance_hits}/3)")
    else:
        print(f"❌ FAIL: New GUIDANCE patterns not all working ({new_guidance_hits}/3)")
        passed = False

    print("\n" + "=" * 80)
    if passed:
        print("✅ PRE-CLASSIFIER PERFORMANCE VERIFICATION PASSED")
    else:
        print("❌ PRE-CLASSIFIER PERFORMANCE VERIFICATION FAILED")
    print("=" * 80 + "\n")

    assert passed, "Performance verification failed"


if __name__ == "__main__":
    test_preclassifier_performance()
