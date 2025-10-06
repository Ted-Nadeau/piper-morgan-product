import asyncio
import time
from statistics import mean, median, stdev

from services.intent_service.classifier import classifier


async def benchmark_category(category_name, test_queries):
    """Benchmark classification performance for a category."""
    times = []
    confidences = []
    successful_queries = []

    print(f"\nBenchmarking {category_name} category:")
    print(f"{'='*60}")

    for query in test_queries:
        try:
            start = time.perf_counter()
            result = await classifier.classify(query)
            elapsed = time.perf_counter() - start

            times.append(elapsed * 1000)  # Convert to ms
            confidences.append(result.confidence)
            successful_queries.append(query)

            print(f"  {elapsed*1000:6.2f}ms | {result.confidence:.3f} | {query[:40]}")
        except Exception as e:
            print(
                f"  FAILED   | N/A     | {query[:40]} (LLM error - expected for non-pattern queries)"
            )

    if not times:
        return {
            "category": category_name,
            "num_queries": len(test_queries),
            "successful_queries": 0,
            "error": "No queries successfully classified",
        }

    return {
        "category": category_name,
        "num_queries": len(test_queries),
        "successful_queries": len(successful_queries),
        "avg_time_ms": mean(times),
        "median_time_ms": median(times),
        "std_time_ms": stdev(times) if len(times) > 1 else 0,
        "min_time_ms": min(times),
        "max_time_ms": max(times),
        "avg_confidence": mean(confidences),
        "min_confidence": min(confidences),
        "max_confidence": max(confidences),
        "successful_query_list": successful_queries,
    }


async def run_benchmarks():
    """Run benchmarks for all three categories using pattern-matching queries."""

    # Use queries that match the exact patterns in pre_classifier.py
    temporal_queries = [
        "What day is it?",  # Matches \bwhat day is it\b
        "What's today's date?",  # Matches \bwhat'?s the date\b
        "What time is it?",  # Matches \bwhat time is it\b
        "What's the date?",  # Matches \bwhat'?s the date\b
        "Today's date",  # Matches \btoday'?s date\b
    ]

    status_queries = [
        "What am I working on?",  # Matches \bwhat am i working on\b
        "What's my current project?",  # Matches \bwhat'?s my current project\b
        "My projects",  # Matches \bmy projects\b
        "Current work",  # Matches \bcurrent work\b
        "What's my status?",  # Matches \bwhat'?s my status\b
    ]

    priority_queries = [
        "What's my top priority?",  # Matches \bwhat'?s my top priority\b
        "Highest priority",  # Matches \bhighest priority\b
        "Most important task",  # Matches \bmost important task\b
        "What should I do first?",  # Matches \bwhat should i do first\b
        "My priorities",  # Matches \bmy priorities\b
    ]

    results = {}
    results["temporal"] = await benchmark_category("TEMPORAL", temporal_queries)
    results["status"] = await benchmark_category("STATUS", status_queries)
    results["priority"] = await benchmark_category("PRIORITY", priority_queries)

    # Summary
    print(f"\n{'='*80}")
    print(f"BASELINE METRICS SUMMARY")
    print(f"{'='*80}")
    print(
        f"{'Category':<12} | {'Success':>8} | {'Avg Time':>10} | {'Median':>10} | {'Avg Conf':>10}"
    )
    print(f"{'-'*12}-+-{'-'*8}-+-{'-'*10}-+-{'-'*10}-+-{'-'*10}")

    for cat, data in results.items():
        if "error" not in data:
            success_rate = f"{data['successful_queries']}/{data['num_queries']}"
            print(
                f"{cat:<12} | {success_rate:>8} | {data['avg_time_ms']:>9.2f}ms | {data['median_time_ms']:>9.2f}ms | {data['avg_confidence']:>9.3f}"
            )
        else:
            print(f"{cat:<12} | {'0/5':>8} | {'N/A':>10} | {'N/A':>10} | {'N/A':>10}")

    # Check against targets
    print(f"\n{'='*80}")
    print(f"TARGET VALIDATION")
    print(f"{'='*80}")
    all_pass = True
    for cat, data in results.items():
        if "error" not in data:
            time_ok = data["avg_time_ms"] < 100
            conf_ok = data["avg_confidence"] > 0.8
            success_ok = data["successful_queries"] >= 3  # At least 3/5 should work
            status = "✅ PASS" if (time_ok and conf_ok and success_ok) else "❌ FAIL"
            print(
                f"{status} | {cat:<12} | Time: {time_ok} (<100ms) | Conf: {conf_ok} (>0.8) | Success: {success_ok} (≥3/5)"
            )
            all_pass = all_pass and time_ok and conf_ok and success_ok
        else:
            print(f"❌ FAIL | {cat:<12} | No successful classifications")
            all_pass = False

    return results, all_pass


if __name__ == "__main__":
    results, passed = asyncio.run(run_benchmarks())

    # Save results to JSON for documentation
    import json

    with open("dev/2025/10/05/baseline_metrics.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nMetrics saved to: dev/2025/10/05/baseline_metrics.json")
    print(f"Overall result: {'✅ ALL TARGETS MET' if passed else '❌ SOME TARGETS MISSED'}")

    # Show which queries worked
    print(f"\n{'='*80}")
    print(f"SUCCESSFUL PATTERN MATCHES")
    print(f"{'='*80}")
    for cat, data in results.items():
        if "error" not in data and data["successful_queries"] > 0:
            print(f"{cat.upper()}:")
            for query in data["successful_query_list"]:
                print(f"  ✅ {query}")
        else:
            print(f"{cat.upper()}: No successful matches")
