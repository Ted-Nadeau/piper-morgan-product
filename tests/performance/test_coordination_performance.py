"""
Coordination Performance Benchmarking

PM-033d Phase 4: Comprehensive performance testing for multi-agent coordination
under various load conditions and complexity scenarios.
"""

import asyncio
import statistics
import time
from typing import Any, Dict, List

import pytest

from services.domain.models import Intent
from services.orchestration.multi_agent_coordinator import (
    AgentType,
    CoordinationStatus,
    MultiAgentCoordinator,
    TaskComplexity,
)
from services.shared_types import IntentCategory


class CoordinationPerformanceBenchmark:
    """Performance benchmark suite for coordination system"""

    def __init__(self):
        self.coordinator = MultiAgentCoordinator()
        self.benchmark_results = {}

    async def run_latency_benchmark(self) -> Dict[str, Any]:
        """Benchmark coordination latency across different complexity levels"""

        print("🔥 PERFORMANCE BENCHMARK: Coordination Latency")
        print("=" * 55)

        # Test scenarios with varying complexity
        scenarios = [
            (
                "simple",
                Intent(
                    category=IntentCategory.QUERY,
                    action="get_status",
                    original_message="Get current system status",
                    confidence=0.9,
                ),
            ),
            (
                "moderate",
                Intent(
                    category=IntentCategory.EXECUTION,
                    action="implement_feature",
                    original_message="Implement new API endpoint with validation and tests",
                    confidence=0.95,
                ),
            ),
            (
                "complex",
                Intent(
                    category=IntentCategory.EXECUTION,
                    action="refactor_architecture",
                    original_message="Refactor entire system architecture with microservices migration, database changes, and comprehensive testing",
                    confidence=0.98,
                ),
            ),
            (
                "ultra_complex",
                Intent(
                    category=IntentCategory.EXECUTION,
                    action="enterprise_integration",
                    original_message="Build enterprise integration platform with multiple API gateways, message queues, database federation, monitoring, security, and complete documentation",
                    confidence=0.99,
                ),
            ),
        ]

        benchmark_results = {}

        for scenario_name, intent in scenarios:
            print(f"\n📊 Benchmarking {scenario_name.upper()} scenario...")

            # Warm up coordination
            await self.coordinator.coordinate_task(intent)

            # Run multiple benchmark iterations
            latencies = []
            subtask_counts = []
            agent_distributions = []

            for run in range(10):
                start_time = time.time()
                result = await self.coordinator.coordinate_task(intent)
                latency_ms = int((time.time() - start_time) * 1000)

                latencies.append(latency_ms)
                subtask_counts.append(len(result.subtasks))

                # Track agent distribution
                code_tasks = len([t for t in result.subtasks if t.assigned_agent == AgentType.CODE])
                cursor_tasks = len(
                    [t for t in result.subtasks if t.assigned_agent == AgentType.CURSOR]
                )
                agent_distributions.append({"code": code_tasks, "cursor": cursor_tasks})

                assert result.status == CoordinationStatus.ASSIGNED, f"Run {run} failed"

            # Calculate statistics
            stats = {
                "avg_latency_ms": statistics.mean(latencies),
                "min_latency_ms": min(latencies),
                "max_latency_ms": max(latencies),
                "p50_latency_ms": statistics.median(latencies),
                "p95_latency_ms": (
                    statistics.quantiles(latencies, n=20)[18]
                    if len(latencies) >= 20
                    else max(latencies)
                ),
                "p99_latency_ms": (
                    statistics.quantiles(latencies, n=100)[98]
                    if len(latencies) >= 100
                    else max(latencies)
                ),
                "std_dev_ms": statistics.stdev(latencies) if len(latencies) > 1 else 0,
                "avg_subtasks": statistics.mean(subtask_counts),
                "total_runs": len(latencies),
                "success_rate": 1.0,  # All should succeed
            }

            benchmark_results[scenario_name] = stats

            # Display results
            print(f'   Avg Latency: {stats["avg_latency_ms"]:.1f}ms')
            print(f'   P95 Latency: {stats["p95_latency_ms"]:.1f}ms')
            print(f'   Max Latency: {stats["max_latency_ms"]:.1f}ms')
            print(f'   Std Dev: {stats["std_dev_ms"]:.1f}ms')
            print(f'   Avg Subtasks: {stats["avg_subtasks"]:.1f}')

            # Validate performance targets
            target_met = stats["avg_latency_ms"] < 1000
            p95_met = stats["p95_latency_ms"] < 2000

            print(f'   Target (<1000ms): {"✅" if target_met else "❌"}')
            print(f'   P95 Target (<2000ms): {"✅" if p95_met else "❌"}')

        # Overall summary
        print(f"\n🎯 LATENCY BENCHMARK SUMMARY:")
        total_tests = sum(stats["total_runs"] for stats in benchmark_results.values())
        avg_overall = statistics.mean(
            [stats["avg_latency_ms"] for stats in benchmark_results.values()]
        )

        print(f"   Total Test Runs: {total_tests}")
        print(f"   Overall Avg Latency: {avg_overall:.1f}ms")

        targets_met = sum(
            1 for stats in benchmark_results.values() if stats["avg_latency_ms"] < 1000
        )
        print(f"   Scenarios Meeting Target: {targets_met}/{len(scenarios)}")

        self.benchmark_results["latency"] = benchmark_results
        return benchmark_results

    async def run_throughput_benchmark(self) -> Dict[str, Any]:
        """Benchmark coordination throughput under concurrent load"""

        print(f"\n🚀 PERFORMANCE BENCHMARK: Concurrent Throughput")
        print("=" * 55)

        throughput_results = {}

        # Test different concurrency levels
        concurrency_levels = [1, 3, 5, 10, 15]

        base_intent = Intent(
            category=IntentCategory.EXECUTION,
            action="implement_microservice",
            original_message="Implement microservice with REST API, database layer, and comprehensive testing",
            confidence=0.96,
        )

        for concurrency in concurrency_levels:
            print(f"\n📈 Testing {concurrency} concurrent coordinations...")

            # Create intent variations
            intents = []
            for i in range(concurrency):
                intent = Intent(
                    category=base_intent.category,
                    action=f"implement_service_{i}",
                    original_message=f"Implement service {i} with REST API, database layer, and comprehensive testing",
                    confidence=base_intent.confidence,
                )
                intents.append(intent)

            # Run throughput test
            start_time = time.time()

            tasks = [self.coordinator.coordinate_task(intent) for intent in intents]
            results = await asyncio.gather(*tasks)

            total_time_s = time.time() - start_time
            total_time_ms = int(total_time_s * 1000)

            # Calculate throughput metrics
            successful = sum(1 for r in results if r.status == CoordinationStatus.ASSIGNED)
            throughput_ops_per_sec = successful / total_time_s if total_time_s > 0 else 0
            avg_latency_ms = total_time_ms / concurrency if concurrency > 0 else 0

            # Collect individual latencies from coordination results
            individual_latencies = [r.total_duration_ms for r in results]

            throughput_stats = {
                "concurrency": concurrency,
                "total_time_ms": total_time_ms,
                "successful_coordinations": successful,
                "success_rate": successful / concurrency,
                "throughput_ops_per_sec": throughput_ops_per_sec,
                "avg_latency_ms": avg_latency_ms,
                "individual_avg_latency_ms": statistics.mean(individual_latencies),
                "individual_max_latency_ms": max(individual_latencies),
                "individual_min_latency_ms": min(individual_latencies),
            }

            throughput_results[f"concurrency_{concurrency}"] = throughput_stats

            print(f"   Total Time: {total_time_ms}ms")
            print(
                f'   Success Rate: {successful}/{concurrency} ({throughput_stats["success_rate"]*100:.1f}%)'
            )
            print(f"   Throughput: {throughput_ops_per_sec:.2f} ops/sec")
            print(f"   Avg Latency: {avg_latency_ms:.1f}ms")
            print(f'   Individual Coord Avg: {throughput_stats["individual_avg_latency_ms"]:.1f}ms')

            # Performance validation
            latency_ok = avg_latency_ms < 1000
            throughput_ok = throughput_ops_per_sec >= 1.0  # At least 1 coordination per second

            print(f'   Latency Target: {"✅" if latency_ok else "❌"}')
            print(f'   Throughput Target: {"✅" if throughput_ok else "❌"}')

        # Throughput summary
        print(f"\n🎯 THROUGHPUT BENCHMARK SUMMARY:")
        max_throughput = max(
            stats["throughput_ops_per_sec"] for stats in throughput_results.values()
        )
        max_successful_concurrency = max(
            stats["concurrency"]
            for stats in throughput_results.values()
            if stats["success_rate"] >= 0.95
        )

        print(f"   Maximum Throughput: {max_throughput:.2f} ops/sec")
        print(f"   Max Successful Concurrency: {max_successful_concurrency}")

        self.benchmark_results["throughput"] = throughput_results
        return throughput_results

    async def run_stress_benchmark(self) -> Dict[str, Any]:
        """Stress test coordination under extreme conditions"""

        print(f"\n💪 PERFORMANCE BENCHMARK: Stress Testing")
        print("=" * 55)

        stress_results = {}

        # Stress test: 50 rapid-fire coordinations
        print(f"\n🔥 Stress Test: 50 Rapid Coordinations")

        stress_intents = []
        for i in range(50):
            intent = Intent(
                category=IntentCategory.EXECUTION,
                action=f"stress_task_{i}",
                original_message=f"Stress test coordination {i} with moderate complexity",
                confidence=0.93,
            )
            stress_intents.append(intent)

        start_time = time.time()

        # Execute all at once (maximum stress)
        stress_tasks = [self.coordinator.coordinate_task(intent) for intent in stress_intents]
        stress_results_list = await asyncio.gather(*stress_tasks, return_exceptions=True)

        stress_time_s = time.time() - start_time
        stress_time_ms = int(stress_time_s * 1000)

        # Analyze stress test results
        successful_stress = sum(
            1
            for r in stress_results_list
            if not isinstance(r, Exception) and r.status == CoordinationStatus.ASSIGNED
        )
        exceptions = sum(1 for r in stress_results_list if isinstance(r, Exception))

        stress_stats = {
            "total_coordinations": len(stress_intents),
            "successful_coordinations": successful_stress,
            "exceptions": exceptions,
            "total_time_ms": stress_time_ms,
            "success_rate": successful_stress / len(stress_intents),
            "avg_time_per_coordination_ms": stress_time_ms / len(stress_intents),
            "throughput_ops_per_sec": successful_stress / stress_time_s if stress_time_s > 0 else 0,
        }

        print(f'   Total Coordinations: {stress_stats["total_coordinations"]}')
        print(f"   Successful: {successful_stress}")
        print(f"   Exceptions: {exceptions}")
        print(f"   Total Time: {stress_time_ms}ms")
        print(f'   Success Rate: {stress_stats["success_rate"]*100:.1f}%')
        print(f'   Avg Time per Coord: {stress_stats["avg_time_per_coordination_ms"]:.1f}ms')
        print(f'   Throughput: {stress_stats["throughput_ops_per_sec"]:.2f} ops/sec')

        # Stress test validation
        stress_success_ok = stress_stats["success_rate"] >= 0.90  # 90% success under stress
        stress_latency_ok = (
            stress_stats["avg_time_per_coordination_ms"] < 2000
        )  # 2s tolerance under stress

        print(f'   Stress Success Rate (≥90%): {"✅" if stress_success_ok else "❌"}')
        print(f'   Stress Latency (<2000ms): {"✅" if stress_latency_ok else "❌"}')

        stress_results["rapid_stress"] = stress_stats
        self.benchmark_results["stress"] = stress_results

        return stress_results

    async def run_full_benchmark_suite(self) -> Dict[str, Any]:
        """Run complete performance benchmark suite"""

        print("🎯 MULTI-AGENT COORDINATION PERFORMANCE BENCHMARK SUITE")
        print("=" * 70)
        print(f"Starting comprehensive performance testing...\n")

        # Run all benchmark categories
        latency_results = await self.run_latency_benchmark()
        throughput_results = await self.run_throughput_benchmark()
        stress_results = await self.run_stress_benchmark()

        # Generate comprehensive report
        print(f"\n" + "=" * 70)
        print("🏆 BENCHMARK SUITE SUMMARY")
        print("=" * 70)

        # Performance targets validation
        latency_targets_met = sum(
            1 for stats in latency_results.values() if stats["avg_latency_ms"] < 1000
        )
        latency_total = len(latency_results)

        print(f"📊 LATENCY PERFORMANCE:")
        print(f"   Scenarios Meeting <1000ms Target: {latency_targets_met}/{latency_total}")

        max_throughput = max(
            stats["throughput_ops_per_sec"] for stats in throughput_results.values()
        )
        print(f"\n🚀 THROUGHPUT PERFORMANCE:")
        print(f"   Maximum Throughput Achieved: {max_throughput:.2f} ops/sec")

        stress_success = stress_results["rapid_stress"]["success_rate"]
        print(f"\n💪 STRESS TEST PERFORMANCE:")
        print(f"   Success Rate Under Stress: {stress_success*100:.1f}%")

        # Overall performance grade
        overall_latency_ok = latency_targets_met >= latency_total * 0.75  # 75% of scenarios
        overall_throughput_ok = max_throughput >= 10.0  # At least 10 ops/sec
        overall_stress_ok = stress_success >= 0.90  # 90% success under stress

        overall_performance = all([overall_latency_ok, overall_throughput_ok, overall_stress_ok])

        print(f"\n🎯 OVERALL PERFORMANCE ASSESSMENT:")
        print(f'   Latency Performance: {"✅" if overall_latency_ok else "❌"}')
        print(f'   Throughput Performance: {"✅" if overall_throughput_ok else "❌"}')
        print(f'   Stress Performance: {"✅" if overall_stress_ok else "❌"}')
        print(
            f'   Overall Grade: {"🏆 EXCELLENT" if overall_performance else "⚠️ NEEDS OPTIMIZATION"}'
        )

        return {
            "latency": latency_results,
            "throughput": throughput_results,
            "stress": stress_results,
            "overall_performance": overall_performance,
            "summary": {
                "latency_targets_met": f"{latency_targets_met}/{latency_total}",
                "max_throughput_ops_per_sec": max_throughput,
                "stress_success_rate": stress_success,
                "overall_assessment": "excellent" if overall_performance else "needs_optimization",
            },
        }


# Performance Test Integration
async def run_performance_validation():
    """Run performance validation for PM-033d Phase 4"""

    benchmark = CoordinationPerformanceBenchmark()
    results = await benchmark.run_full_benchmark_suite()

    return results


if __name__ == "__main__":
    # Run performance benchmarks directly
    results = asyncio.run(run_performance_validation())
    print(f"\nPerformance validation completed: {results['overall_performance']}")
