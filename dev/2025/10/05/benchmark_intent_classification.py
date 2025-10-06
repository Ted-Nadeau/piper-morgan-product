import asyncio
import time
from statistics import mean, median, stdev

from services.intent_service.classifier import classifier


async def benchmark_category(category_name, test_queries):
    """Benchmark classification performance for a category."""
    times = []
    confidences = []

    print(f"\nBenchmarking {category_name} category:")
    print(f"{'='*60}")

    for query in test_queries:
        start = time.perf_counter()
        result = await classifier.classify(query)
        elapsed = time.perf_counter() - start

        times.append(elapsed * 1000)  # Convert to ms
        confidences.append(result.confidence)

        print(f"  {elapsed*1000:6.2f}ms | {result.confidence:.3f} | {query[:40]}")

    return {
        "category": category_name,
        "num_queries": len(test_queries),
        "avg_time_ms": mean(times),
        "median_time_ms": median(times),
        "std_time_ms": stdev(times) if len(times) > 1 else 0,
        "min_time_ms": min(times),
        "max_time_ms": max(times),
        "avg_confidence": mean(confidences),
        "min_confidence": min(confidences),
        "max_confidence": max(confidences),
    }


async def run_benchmarks():
    """Run benchmarks for all three categories."""

    temporal_queries = [
        "What day is it?",
        "What's today's date?",
        "What did we do yesterday?",
        "What's on the agenda for today?",
        "When was the last time we worked on this?",
    ]

    status_queries = [
        "What am I working on?",
        "Show me current projects",
        "What projects are we working on?",
        "What's the status of project X?",
        "Where are we in the project lifecycle?",
    ]

    priority_queries = [
        "What's my top priority?",
        "What should I focus on today?",
        "What's most important today?",
        "Which project should I focus on?",
        "What needs my attention?",
    ]

    results = {}
    results["temporal"] = await benchmark_category("TEMPORAL", temporal_queries)
    results["status"] = await benchmark_category("STATUS", status_queries)
    results["priority"] = await benchmark_category("PRIORITY", priority_queries)

    # Summary
    print(f"\n{'='*80}")
    print(f"BASELINE METRICS SUMMARY")
    print(f"{'='*80}")
    print(f"{'Category':<12} | {'Avg Time':>10} | {'Median':>10} | {'Avg Conf':>10}")
    print(f"{'-'*12}-+-{'-'*10}-+-{'-'*10}-+-{'-'*10}")

    for cat, data in results.items():
        print(
            f"{cat:<12} | {data['avg_time_ms']:>9.2f}ms | {data['median_time_ms']:>9.2f}ms | {data['avg_confidence']:>9.3f}"
        )

    # Check against targets
    print(f"\n{'='*80}")
    print(f"TARGET VALIDATION")
    print(f"{'='*80}")
    all_pass = True
    for cat, data in results.items():
        time_ok = data["avg_time_ms"] < 100
        conf_ok = data["avg_confidence"] > 0.8
        status = "✅ PASS" if (time_ok and conf_ok) else "❌ FAIL"
        print(f"{status} | {cat:<12} | Time: {time_ok} (<100ms) | Conf: {conf_ok} (>0.8)")
        all_pass = all_pass and time_ok and conf_ok

    return results, all_pass


if __name__ == "__main__":
    results, passed = asyncio.run(run_benchmarks())

    # Save results to JSON for documentation
    import json

    with open("dev/2025/10/05/baseline_metrics.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nMetrics saved to: dev/2025/10/05/baseline_metrics.json")
    print(f"Overall result: {'✅ ALL TARGETS MET' if passed else '❌ SOME TARGETS MISSED'}")
