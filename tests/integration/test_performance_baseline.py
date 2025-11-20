"""
Performance baseline measurement for Morning Standup intelligence trifecta
Created for PM-127 integration testing - measures individual and combined performance
"""

import asyncio
import time
from typing import Dict

from services.domain.user_preference_manager import UserPreferenceManager
from services.features.morning_standup import MorningStandupWorkflow
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.orchestration.session_persistence import SessionPersistenceManager


async def measure_individual_performance() -> Dict[str, float]:
    """Measure each component's performance impact."""
    user_id = "test_performance"
    results = {}

    # Initialize services
    preference_manager = UserPreferenceManager()
    session_manager = SessionPersistenceManager(preference_manager)
    github_agent = GitHubAgent()
    canonical_handlers = CanonicalHandlers()

    # Base standup
    print("🧪 Testing base standup performance...")
    workflow = MorningStandupWorkflow(
        preference_manager=preference_manager,
        session_manager=session_manager,
        github_agent=github_agent,
        canonical_handlers=canonical_handlers,
    )

    start = time.time()
    await workflow.generate_standup(user_id)
    results["base"] = time.time() - start
    print(f"   ✅ Base: {results['base']:.3f}s")

    # Issues only
    print("🧪 Testing issues intelligence performance...")
    start = time.time()
    await workflow.generate_with_issues(user_id)
    results["issues"] = time.time() - start
    print(f"   ✅ Issues: {results['issues']:.3f}s")

    # Documents only
    print("🧪 Testing documents intelligence performance...")
    start = time.time()
    await workflow.generate_with_documents(user_id)
    results["documents"] = time.time() - start
    print(f"   ✅ Documents: {results['documents']:.3f}s")

    # Calendar only
    print("🧪 Testing calendar intelligence performance...")
    start = time.time()
    await workflow.generate_with_calendar(user_id)
    results["calendar"] = time.time() - start
    print(f"   ✅ Calendar: {results['calendar']:.3f}s")

    return results


async def measure_combination_performance() -> Dict[str, float]:
    """Measure combination performance."""
    user_id = "test_performance"
    results = {}

    # Initialize services
    preference_manager = UserPreferenceManager()
    session_manager = SessionPersistenceManager(preference_manager)
    github_agent = GitHubAgent()
    canonical_handlers = CanonicalHandlers()

    workflow = MorningStandupWorkflow(
        preference_manager=preference_manager,
        session_manager=session_manager,
        github_agent=github_agent,
        canonical_handlers=canonical_handlers,
    )

    # Two-component combinations
    print("🧪 Testing two-component combinations...")

    # Issues + Documents
    start = time.time()
    await workflow.generate_with_trifecta(
        user_id, with_issues=True, with_documents=True, with_calendar=False
    )
    results["issues_documents"] = time.time() - start
    print(f"   ✅ Issues + Documents: {results['issues_documents']:.3f}s")

    # Issues + Calendar
    start = time.time()
    await workflow.generate_with_trifecta(
        user_id, with_issues=True, with_documents=False, with_calendar=True
    )
    results["issues_calendar"] = time.time() - start
    print(f"   ✅ Issues + Calendar: {results['issues_calendar']:.3f}s")

    # Documents + Calendar
    start = time.time()
    await workflow.generate_with_trifecta(
        user_id, with_issues=False, with_documents=True, with_calendar=True
    )
    results["documents_calendar"] = time.time() - start
    print(f"   ✅ Documents + Calendar: {results['documents_calendar']:.3f}s")

    # Full trifecta (CRITICAL TEST)
    print("🧪 Testing FULL TRIFECTA performance...")
    start = time.time()
    await workflow.generate_with_trifecta(
        user_id, with_issues=True, with_documents=True, with_calendar=True
    )
    results["full_trifecta"] = time.time() - start
    print(f"   🎯 FULL TRIFECTA: {results['full_trifecta']:.3f}s")

    return results


async def performance_analysis():
    """Complete performance analysis for integration testing."""
    print("🚀 Morning Standup Intelligence Trifecta Performance Analysis")
    print("=" * 60)

    try:
        # Individual component performance
        print("\n📊 INDIVIDUAL COMPONENT PERFORMANCE")
        print("-" * 40)
        individual_results = await measure_individual_performance()

        # Combination performance
        print("\n📊 COMBINATION PERFORMANCE")
        print("-" * 40)
        combination_results = await measure_combination_performance()

        # Analysis
        print("\n📈 PERFORMANCE ANALYSIS")
        print("-" * 40)

        # Individual analysis
        fastest_individual = min(individual_results.values())
        slowest_individual = max(individual_results.values())
        print(f"Fastest individual component: {fastest_individual:.3f}s")
        print(f"Slowest individual component: {slowest_individual:.3f}s")
        print(f"Individual performance range: {slowest_individual - fastest_individual:.3f}s")

        # Combination analysis
        full_trifecta_time = combination_results["full_trifecta"]
        print(f"\n🎯 FULL TRIFECTA PERFORMANCE: {full_trifecta_time:.3f}s")

        # Performance targets
        print("\n🎯 TARGET COMPLIANCE")
        print("-" * 40)
        individual_target = 2.0  # <2 seconds for individual
        trifecta_target = 3.0  # <3 seconds for full trifecta

        for component, time_taken in individual_results.items():
            status = "✅ PASS" if time_taken < individual_target else "❌ FAIL"
            print(f"{component.ljust(15)}: {time_taken:.3f}s {status}")

        print(
            f"\nFull trifecta      : {full_trifecta_time:.3f}s {'✅ PASS' if full_trifecta_time < trifecta_target else '❌ FAIL'}"
        )

        # Overall readiness
        all_individual_pass = all(t < individual_target for t in individual_results.values())
        trifecta_pass = full_trifecta_time < trifecta_target

        print("\n🚦 DEPLOYMENT READINESS")
        print("-" * 40)
        if all_individual_pass and trifecta_pass:
            print("✅ READY FOR DEPLOYMENT")
            print("   All performance targets met")
            print("   6 AM standup demo: GO")
        else:
            print("❌ PERFORMANCE ISSUES DETECTED")
            print("   Review slow components before demo")
            print("   6 AM standup demo: CAUTION")

        return {
            "individual": individual_results,
            "combinations": combination_results,
            "targets_met": all_individual_pass and trifecta_pass,
            "full_trifecta_time": full_trifecta_time,
        }

    except Exception as e:
        print(f"❌ Performance testing failed: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    results = asyncio.run(performance_analysis())

    if "error" not in results:
        print(f"\n📄 SUMMARY FOR HANDOFF")
        print("-" * 40)
        print(f"Individual components: {len(results['individual'])} tested")
        print(f"Combinations: {len(results['combinations'])} tested")
        print(f"Full trifecta: {results['full_trifecta_time']:.3f}s")
        print(f"Demo ready: {'YES' if results['targets_met'] else 'NEEDS REVIEW'}")
    else:
        print(f"Testing incomplete due to: {results['error']}")
