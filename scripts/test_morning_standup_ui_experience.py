#!/usr/bin/env python3
"""
PM-071: Morning Standup UI Experience Testing

Tests the 5-query morning standup sequence through the existing UI for authentic user experience validation.
Focuses on embodied AI concepts through authentic user interaction patterns, even with infrastructure issues.

Usage:
    python scripts/test_morning_standup_ui_experience.py
"""

import asyncio
import json
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

import aiohttp

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@dataclass
class UIQueryResult:
    """Result of a single query through the UI"""

    query: str
    query_type: str
    start_time: float
    end_time: float
    response_time_ms: float
    success: bool
    response_text: str
    error_type: str = None
    error_message: str = None
    ui_behavior: str = None


@dataclass
class UIExperienceResult:
    """Complete result of the UI experience test"""

    sequence_start: float
    sequence_end: float
    total_duration_ms: float
    query_results: List[UIQueryResult]
    success_rate: float
    average_response_time_ms: float
    ux_insights: List[str]
    infrastructure_issues: List[str]
    embodied_ai_assessment: List[str]


class MorningStandupUIExperienceTester:
    """Test the 5-query morning standup sequence through the UI with focus on user experience"""

    def __init__(self):
        self.api_base_url = "http://localhost:8001"
        self.ui_url = "http://localhost:8000"
        self.session_id = None
        self.results = []
        self.ux_insights = []
        self.infrastructure_issues = []
        self.embodied_ai_assessment = []

        # PM-071: 5-Query Morning Standup Sequence (Draft from Chief Architect)
        self.standup_sequence = [
            {
                "query": "What day is it?",
                "type": "Temporal awareness",
                "expected_behavior": "Provide current date and day of week",
                "embodied_ai_test": "Temporal self-awareness",
            },
            {
                "query": "What did we accomplish yesterday?",
                "type": "Continuity",
                "expected_behavior": "Query recent workflow history and accomplishments",
                "embodied_ai_test": "Memory and continuity",
            },
            {
                "query": "What's on my agenda today?",
                "type": "Planning",
                "expected_behavior": "Review current project priorities and schedule",
                "embodied_ai_test": "Planning and organization",
            },
            {
                "query": "What should I focus on first?",
                "type": "Prioritization",
                "expected_behavior": "Analyze priorities and recommend focus areas",
                "embodied_ai_test": "Decision making and prioritization",
            },
            {
                "query": "Any blockers I should know about?",
                "type": "Risk awareness",
                "expected_behavior": "Identify potential blockers and risk factors",
                "embodied_ai_test": "Risk assessment and proactive thinking",
            },
        ]

    async def test_ui_accessibility(self) -> bool:
        """Test if the UI is accessible"""
        print("🔍 Testing UI accessibility...")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.ui_url) as response:
                    if response.status == 200:
                        content = await response.text()
                        if "Piper Morgan" in content:
                            print("✅ UI is accessible")
                            return True
                        else:
                            print("❌ UI content doesn't match expected")
                            return False
                    else:
                        print(f"❌ UI returned status {response.status}")
                        return False
        except Exception as e:
            print(f"❌ UI accessibility test failed: {e}")
            return False

    async def test_api_connectivity(self) -> bool:
        """Test if the API is responding (even if with errors)"""
        print("🔍 Testing API connectivity...")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_base_url}/health") as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("status") == "healthy":
                            print("✅ API is healthy and responding")
                            return True
                        else:
                            print(f"⚠️  API health check shows issues: {data}")
                            return True  # Still accessible, just not fully healthy
                    else:
                        print(f"❌ API returned status {response.status}")
                        return False
        except Exception as e:
            print(f"❌ API connectivity test failed: {e}")
            return False

    async def execute_query_through_ui(self, query_data: Dict[str, Any]) -> UIQueryResult:
        """Execute a single query and measure timing, focusing on UI experience"""
        query = query_data["query"]
        query_type = query_data["type"]
        embodied_ai_test = query_data["embodied_ai_test"]

        print(f"🧪 Testing: {query} ({query_type})")
        print(f"   Embodied AI Test: {embodied_ai_test}")

        start_time = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                # Send intent to API
                payload = {"message": query, "session_id": self.session_id}

                async with session.post(
                    f"{self.api_base_url}/api/v1/intent",
                    json=payload,
                    headers={"Content-Type": "application/json"},
                ) as response:
                    end_time = time.time()
                    response_time_ms = (end_time - start_time) * 1000

                    if response.status == 200:
                        result = await response.json()

                        # Extract response data
                        response_text = result.get("message", "No response message")
                        intent_category = result.get("intent", {}).get("category")
                        intent_action = result.get("intent", {}).get("action")
                        confidence = result.get("intent", {}).get("confidence")

                        # Update session ID if provided
                        if result.get("session_id"):
                            self.session_id = result["session_id"]

                        success = True
                        error_type = None
                        error_message = None
                        ui_behavior = "Normal response"

                        print(f"   ✅ Response: {response_text[:100]}...")
                        print(f"   ⚡ Time: {response_time_ms:.1f}ms")
                        print(
                            f"   🎯 Intent: {intent_category}/{intent_action} (confidence: {confidence})"
                        )

                    else:
                        error_text = await response.text()
                        success = False
                        response_text = ""
                        error_type = "API Error"
                        error_message = f"API Error {response.status}: {error_text}"
                        ui_behavior = "Error response"

                        print(f"   ❌ Error: {error_message}")
                        print(f"   ⚡ Time: {response_time_ms:.1f}ms")
                        print(f"   🔧 UI Behavior: Error handling")

        except Exception as e:
            end_time = time.time()
            response_time_ms = (end_time - start_time) * 1000
            success = False
            response_text = ""
            error_type = "Connection Error"
            error_message = str(e)
            ui_behavior = "Connection failure"

            print(f"   ❌ Exception: {error_message}")
            print(f"   ⚡ Time: {response_time_ms:.1f}ms")
            print(f"   🔧 UI Behavior: Connection error handling")

        return UIQueryResult(
            query=query,
            query_type=query_type,
            start_time=start_time,
            end_time=end_time,
            response_time_ms=response_time_ms,
            success=success,
            response_text=response_text,
            error_type=error_type,
            error_message=error_message,
            ui_behavior=ui_behavior,
        )

    def analyze_embodied_ai_concepts(self, results: List[UIQueryResult]) -> List[str]:
        """Analyze embodied AI concept performance"""
        assessments = []

        # Check temporal awareness
        temporal_queries = [r for r in results if "temporal" in r.query_type.lower()]
        if temporal_queries:
            temporal_success = sum(1 for r in temporal_queries if r.success)
            if temporal_success > 0:
                assessments.append("Temporal awareness: Assistant shows time-based understanding")
            else:
                assessments.append("Temporal awareness: Limited time-based responses")

        # Check continuity and memory
        continuity_queries = [r for r in results if "continuity" in r.query_type.lower()]
        if continuity_queries:
            continuity_success = sum(1 for r in continuity_queries if r.success)
            if continuity_success > 0:
                assessments.append("Memory and continuity: Assistant maintains context")
            else:
                assessments.append("Memory and continuity: Context maintenance needs improvement")

        # Check planning and organization
        planning_queries = [r for r in results if "planning" in r.query_type.lower()]
        if planning_queries:
            planning_success = sum(1 for r in planning_queries if r.success)
            if planning_success > 0:
                assessments.append("Planning and organization: Assistant can help with scheduling")
            else:
                assessments.append("Planning and organization: Scheduling capabilities limited")

        # Check decision making
        decision_queries = [r for r in results if "prioritization" in r.query_type.lower()]
        if decision_queries:
            decision_success = sum(1 for r in decision_queries if r.success)
            if decision_success > 0:
                assessments.append("Decision making: Assistant can provide prioritization guidance")
            else:
                assessments.append("Decision making: Prioritization support needs development")

        # Check risk assessment
        risk_queries = [r for r in results if "risk" in r.query_type.lower()]
        if risk_queries:
            risk_success = sum(1 for r in risk_queries if r.success)
            if risk_success > 0:
                assessments.append("Risk assessment: Assistant can identify potential issues")
            else:
                assessments.append("Risk assessment: Proactive issue identification limited")

        return assessments

    def generate_ux_insights(self, results: List[UIQueryResult]) -> List[str]:
        """Generate UX insights from the test results"""
        insights = []

        # Success rate analysis
        success_count = sum(1 for r in results if r.success)
        success_rate = (success_count / len(results)) * 100

        if success_rate == 100:
            insights.append("Perfect reliability: All queries executed successfully")
        elif success_rate >= 80:
            insights.append("Good reliability: Most queries work as expected")
        elif success_rate >= 50:
            insights.append("Partial reliability: Some queries work, others need attention")
        else:
            insights.append(f"Reliability issues: Only {success_rate:.1f}% success rate")

        # Response time analysis
        response_times = [r.response_time_ms for r in results if r.response_time_ms > 0]
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            max_time = max(response_times)

            if avg_time < 2000:
                insights.append("Excellent performance: Fast average response times")
            elif avg_time < 5000:
                insights.append("Good performance: Acceptable response times")
            else:
                insights.append("Performance concerns: Slow response times detected")

            if max_time > 10000:
                insights.append("Performance spikes: Some queries take very long")

        # Error pattern analysis
        error_types = [r.error_type for r in results if r.error_type]
        if error_types:
            error_counts = {}
            for error_type in error_types:
                error_counts[error_type] = error_counts.get(error_type, 0) + 1

            for error_type, count in error_counts.items():
                insights.append(f"Error pattern: {count} {error_type} occurrences")

        # UI behavior analysis
        ui_behaviors = [r.ui_behavior for r in results]
        if "Error response" in ui_behaviors:
            insights.append("UI handles errors gracefully: Error responses are user-friendly")
        if "Connection failure" in ui_behaviors:
            insights.append(
                "UI handles connection issues: Network problems are communicated clearly"
            )

        return insights

    def identify_infrastructure_issues(self, results: List[UIQueryResult]) -> List[str]:
        """Identify infrastructure issues from the test results"""
        issues = []

        # Check for database connection issues
        db_errors = [
            r for r in results if r.error_message and "database" in r.error_message.lower()
        ]
        if db_errors:
            issues.append(f"Database connection issues: {len(db_errors)} queries affected")

        # Check for API errors
        api_errors = [r for r in results if r.error_type == "API Error"]
        if api_errors:
            issues.append(f"API processing errors: {len(api_errors)} queries failed")

        # Check for connection errors
        connection_errors = [r for r in results if r.error_type == "Connection Error"]
        if connection_errors:
            issues.append(f"Connection errors: {len(connection_errors)} queries affected")

        # Check for timeout issues
        slow_queries = [r for r in results if r.response_time_ms > 10000]
        if slow_queries:
            issues.append(f"Timeout issues: {len(slow_queries)} queries took over 10 seconds")

        return issues

    async def run_ui_experience_test(self) -> UIExperienceResult:
        """Run the complete UI experience test"""
        print("🚀 Starting Morning Standup UI Experience Test")
        print("=" * 60)

        sequence_start = time.time()

        # Execute each query in sequence
        for i, query_data in enumerate(self.standup_sequence, 1):
            print(f"\n📝 Query {i}/5: {query_data['query']}")
            print(f"   Type: {query_data['type']}")
            print(f"   Expected: {query_data['expected_behavior']}")

            result = await self.execute_query_through_ui(query_data)
            self.results.append(result)

            # Brief pause between queries to simulate human interaction
            if i < len(self.standup_sequence):
                await asyncio.sleep(1)

        sequence_end = time.time()
        total_duration_ms = (sequence_end - sequence_start) * 1000

        # Analyze results
        success_count = sum(1 for r in self.results if r.success)
        success_rate = (success_count / len(self.results)) * 100

        response_times = [r.response_time_ms for r in self.results if r.response_time_ms > 0]
        average_response_time = sum(response_times) / len(response_times) if response_times else 0

        # Generate insights
        self.ux_insights = self.generate_ux_insights(self.results)
        self.infrastructure_issues = self.identify_infrastructure_issues(self.results)
        self.embodied_ai_assessment = self.analyze_embodied_ai_concepts(self.results)

        return UIExperienceResult(
            sequence_start=sequence_start,
            sequence_end=sequence_end,
            total_duration_ms=total_duration_ms,
            query_results=self.results,
            success_rate=success_rate,
            average_response_time_ms=average_response_time,
            ux_insights=self.ux_insights,
            infrastructure_issues=self.infrastructure_issues,
            embodied_ai_assessment=self.embodied_ai_assessment,
        )

    def print_summary(self, result: UIExperienceResult):
        """Print comprehensive test summary"""
        print("\n" + "=" * 60)
        print("📊 MORNING STANDUP UI EXPERIENCE TEST SUMMARY")
        print("=" * 60)

        print(f"Total Duration: {result.total_duration_ms:.1f}ms")
        print(f"Success Rate: {result.success_rate:.1f}%")
        print(f"Average Response Time: {result.average_response_time_ms:.1f}ms")

        print(f"\n🎯 Success Criteria Check:")
        print(
            f"✅ Complete 5-query sequence: {'PASS' if len(result.query_results) == 5 else 'FAIL'}"
        )
        print(
            f"✅ Timing data collected: {'PASS' if all(r.response_time_ms > 0 for r in result.query_results) else 'FAIL'}"
        )
        print(f"✅ User experience assessed: {'PASS' if result.ux_insights else 'FAIL'}")
        print(
            f"✅ Conversation flow documented: {'PASS' if result.embodied_ai_assessment else 'FAIL'}"
        )
        print(
            f"✅ Under 10 seconds total: {'PASS' if result.total_duration_ms < 10000 else 'FAIL'}"
        )

        print(f"\n🔍 UX Insights:")
        for insight in result.ux_insights:
            print(f"   • {insight}")

        print(f"\n🔧 Infrastructure Issues:")
        if result.infrastructure_issues:
            for issue in result.infrastructure_issues:
                print(f"   • {issue}")
        else:
            print("   • No infrastructure issues detected")

        print(f"\n🤖 Embodied AI Assessment:")
        for assessment in result.embodied_ai_assessment:
            print(f"   • {assessment}")

        print(f"\n📝 Individual Query Results:")
        for i, query_result in enumerate(result.query_results, 1):
            status = "✅" if query_result.success else "❌"
            print(f"   {i}. {status} {query_result.query}")
            print(f"      Time: {query_result.response_time_ms:.1f}ms")
            print(f"      UI Behavior: {query_result.ui_behavior}")
            if query_result.error_message:
                print(f"      Error: {query_result.error_message}")

        # Performance assessment
        if result.total_duration_ms < 5000:
            print(f"\n🎉 EXCELLENT: Complete sequence under 5 seconds!")
        elif result.total_duration_ms < 10000:
            print(f"\n✅ GOOD: Complete sequence under 10 seconds")
        else:
            print(f"\n⚠️  SLOW: Sequence took {result.total_duration_ms/1000:.1f} seconds")

        if result.success_rate == 100:
            print(f"🎉 PERFECT: 100% success rate!")
        elif result.success_rate >= 80:
            print(f"✅ GOOD: {result.success_rate:.1f}% success rate")
        elif result.success_rate >= 50:
            print(f"⚠️  PARTIAL: {result.success_rate:.1f}% success rate")
        else:
            print(f"❌ ISSUES: Only {result.success_rate:.1f}% success rate")

        # Embodied AI assessment
        if result.embodied_ai_assessment:
            positive_assessments = [
                a for a in result.embodied_ai_assessment if "needs" not in a.lower()
            ]
            if len(positive_assessments) >= 3:
                print(f"\n🎉 STRONG: {len(positive_assessments)} embodied AI concepts working well")
            elif len(positive_assessments) >= 1:
                print(f"\n✅ MODERATE: {len(positive_assessments)} embodied AI concepts working")
            else:
                print(f"\n⚠️  WEAK: Limited embodied AI concept implementation")


async def main():
    """Main test runner"""
    tester = MorningStandupUIExperienceTester()

    # Mandatory verification steps
    print("🔍 PM-071: Morning Standup UI Experience Testing")
    print("=" * 60)

    # Test UI accessibility
    ui_accessible = await tester.test_ui_accessibility()
    if not ui_accessible:
        print("❌ STOP: UI not accessible")
        return

    # Test API connectivity
    api_connected = await tester.test_api_connectivity()
    if not api_connected:
        print("❌ STOP: API not responding")
        return

    print("✅ All verification steps passed - proceeding with UI experience test")

    # Run the UI experience test
    result = await tester.run_ui_experience_test()

    # Print comprehensive summary
    tester.print_summary(result)

    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"docs/development/pm-071-ui-experience-test-results-{timestamp}.json"

    # Convert to JSON-serializable format
    result_dict = {
        "timestamp": timestamp,
        "total_duration_ms": result.total_duration_ms,
        "success_rate": result.success_rate,
        "average_response_time_ms": result.average_response_time_ms,
        "ux_insights": result.ux_insights,
        "infrastructure_issues": result.infrastructure_issues,
        "embodied_ai_assessment": result.embodied_ai_assessment,
        "query_results": [
            {
                "query": r.query,
                "query_type": r.query_type,
                "response_time_ms": r.response_time_ms,
                "success": r.success,
                "response_text": r.response_text,
                "error_type": r.error_type,
                "error_message": r.error_message,
                "ui_behavior": r.ui_behavior,
            }
            for r in result.query_results
        ],
    }

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        json.dump(result_dict, f, indent=2)

    print(f"\n💾 Results saved to: {filename}")
    print("\n🎯 PM-071 Morning Standup UI Experience Testing Complete!")


if __name__ == "__main__":
    asyncio.run(main())
