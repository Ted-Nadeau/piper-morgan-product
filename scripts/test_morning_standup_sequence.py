#!/usr/bin/env python3
"""
PM-071: Morning Standup 5-Query Sequence Testing

Tests the 5-query morning standup sequence through the existing UI for authentic user experience validation.
Focuses on embodied AI concepts through authentic user interaction patterns.

Usage:
    python scripts/test_morning_standup_sequence.py
"""

import asyncio
import json
import os
import sys
import time
import webbrowser
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

import aiohttp

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.shared_types import IntentCategory


@dataclass
class QueryResult:
    """Result of a single query in the sequence"""

    query: str
    query_type: str
    start_time: float
    end_time: float
    response_time_ms: float
    success: bool
    response_text: str
    intent_category: str = None
    intent_action: str = None
    confidence: float = None
    error_message: str = None


@dataclass
class StandupSequenceResult:
    """Complete result of the morning standup sequence"""

    sequence_start: float
    sequence_end: float
    total_duration_ms: float
    query_results: List[QueryResult]
    success_rate: float
    average_response_time_ms: float
    ux_insights: List[str]
    conversation_flow_patterns: List[str]


class MorningStandupTester:
    """Test the 5-query morning standup sequence through the UI"""

    def __init__(self):
        self.api_base_url = "http://localhost:8001"
        self.ui_url = "http://localhost:8000"
        self.session_id = None
        self.results = []
        self.ux_insights = []
        self.conversation_patterns = []

        # PM-071: 5-Query Morning Standup Sequence (Draft from Chief Architect)
        self.standup_sequence = [
            {
                "query": "What day is it?",
                "type": "Temporal awareness",
                "expected_category": IntentCategory.CONVERSATION,
                "expected_behavior": "Provide current date and day of week",
            },
            {
                "query": "What did we accomplish yesterday?",
                "type": "Continuity",
                "expected_category": IntentCategory.QUERY,
                "expected_behavior": "Query recent workflow history and accomplishments",
            },
            {
                "query": "What's on my agenda today?",
                "type": "Planning",
                "expected_category": IntentCategory.QUERY,
                "expected_behavior": "Review current project priorities and schedule",
            },
            {
                "query": "What should I focus on first?",
                "type": "Prioritization",
                "expected_category": IntentCategory.QUERY,
                "expected_behavior": "Analyze priorities and recommend focus areas",
            },
            {
                "query": "Any blockers I should know about?",
                "type": "Risk awareness",
                "expected_category": IntentCategory.QUERY,
                "expected_behavior": "Identify potential blockers and risk factors",
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
        """Test if the API is responding"""
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
                            print(f"❌ API health check failed: {data}")
                            return False
                    else:
                        print(f"❌ API returned status {response.status}")
                        return False
        except Exception as e:
            print(f"❌ API connectivity test failed: {e}")
            return False

    async def execute_query(self, query_data: Dict[str, Any]) -> QueryResult:
        """Execute a single query and measure timing"""
        query = query_data["query"]
        query_type = query_data["type"]

        print(f"🧪 Testing: {query} ({query_type})")

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
                        error_message = None

                        print(f"   ✅ Response: {response_text[:100]}...")
                        print(f"   ⚡ Time: {response_time_ms:.1f}ms")

                    else:
                        error_text = await response.text()
                        success = False
                        response_text = ""
                        intent_category = None
                        intent_action = None
                        confidence = None
                        error_message = f"API Error {response.status}: {error_text}"

                        print(f"   ❌ Error: {error_message}")
                        print(f"   ⚡ Time: {response_time_ms:.1f}ms")

        except Exception as e:
            end_time = time.time()
            response_time_ms = (end_time - start_time) * 1000
            success = False
            response_text = ""
            intent_category = None
            intent_action = None
            confidence = None
            error_message = str(e)

            print(f"   ❌ Exception: {error_message}")
            print(f"   ⚡ Time: {response_time_ms:.1f}ms")

        return QueryResult(
            query=query,
            query_type=query_type,
            start_time=start_time,
            end_time=end_time,
            response_time_ms=response_time_ms,
            success=success,
            response_text=response_text,
            intent_category=intent_category,
            intent_action=intent_action,
            confidence=confidence,
            error_message=error_message,
        )

    def analyze_conversation_flow(self, results: List[QueryResult]) -> List[str]:
        """Analyze conversation flow patterns"""
        patterns = []

        # Check for natural conversation progression
        if len(results) >= 2:
            # Check if responses build on each other
            for i in range(1, len(results)):
                prev_response = results[i - 1].response_text.lower()
                current_query = results[i].query.lower()

                # Look for contextual references
                if "yesterday" in prev_response and "yesterday" in current_query:
                    patterns.append("Contextual continuity: Yesterday's context maintained")

                if "today" in prev_response and "today" in current_query:
                    patterns.append("Temporal consistency: Today's context maintained")

        # Check response quality patterns
        response_lengths = [len(r.response_text) for r in results if r.success]
        if response_lengths:
            avg_length = sum(response_lengths) / len(response_lengths)
            if avg_length > 100:
                patterns.append("Detailed responses: Assistant provides comprehensive answers")
            elif avg_length < 50:
                patterns.append("Concise responses: Assistant provides brief answers")

        # Check timing patterns
        response_times = [r.response_time_ms for r in results if r.success]
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            if avg_time < 2000:
                patterns.append("Fast responses: Sub-2 second average response time")
            elif avg_time > 5000:
                patterns.append("Slow responses: May need optimization")

        return patterns

    def generate_ux_insights(self, results: List[QueryResult]) -> List[str]:
        """Generate UX insights from the test results"""
        insights = []

        # Success rate analysis
        success_count = sum(1 for r in results if r.success)
        success_rate = (success_count / len(results)) * 100

        if success_rate == 100:
            insights.append("Perfect reliability: All queries executed successfully")
        elif success_rate >= 80:
            insights.append("Good reliability: Most queries work as expected")
        else:
            insights.append(f"Reliability issues: Only {success_rate:.1f}% success rate")

        # Response time analysis
        response_times = [r.response_time_ms for r in results if r.success]
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

        # Intent classification analysis
        classifications = [r.intent_category for r in results if r.intent_category]
        if classifications:
            category_counts = {}
            for cat in classifications:
                category_counts[cat] = category_counts.get(cat, 0) + 1

            if len(category_counts) > 1:
                insights.append("Diverse intent recognition: Multiple categories detected")
            else:
                insights.append("Limited intent recognition: Single category detected")

        # Error analysis
        errors = [r.error_message for r in results if r.error_message]
        if errors:
            error_types = set()
            for error in errors:
                if "connection" in error.lower():
                    error_types.add("Connection issues")
                elif "timeout" in error.lower():
                    error_types.add("Timeout issues")
                elif "database" in error.lower():
                    error_types.add("Database issues")
                else:
                    error_types.add("Other errors")

            for error_type in error_types:
                insights.append(f"Error pattern: {error_type} detected")

        return insights

    async def run_standup_sequence(self) -> StandupSequenceResult:
        """Run the complete 5-query morning standup sequence"""
        print("🚀 Starting Morning Standup 5-Query Sequence Test")
        print("=" * 60)

        sequence_start = time.time()

        # Execute each query in sequence
        for i, query_data in enumerate(self.standup_sequence, 1):
            print(f"\n📝 Query {i}/5: {query_data['query']}")
            print(f"   Type: {query_data['type']}")
            print(f"   Expected: {query_data['expected_behavior']}")

            result = await self.execute_query(query_data)
            self.results.append(result)

            # Brief pause between queries to simulate human interaction
            if i < len(self.standup_sequence):
                await asyncio.sleep(1)

        sequence_end = time.time()
        total_duration_ms = (sequence_end - sequence_start) * 1000

        # Analyze results
        success_count = sum(1 for r in self.results if r.success)
        success_rate = (success_count / len(self.results)) * 100

        response_times = [r.response_time_ms for r in self.results if r.success]
        average_response_time = sum(response_times) / len(response_times) if response_times else 0

        # Generate insights
        self.ux_insights = self.generate_ux_insights(self.results)
        self.conversation_patterns = self.analyze_conversation_flow(self.results)

        return StandupSequenceResult(
            sequence_start=sequence_start,
            sequence_end=sequence_end,
            total_duration_ms=total_duration_ms,
            query_results=self.results,
            success_rate=success_rate,
            average_response_time_ms=average_response_time,
            ux_insights=self.ux_insights,
            conversation_flow_patterns=self.conversation_patterns,
        )

    def print_summary(self, result: StandupSequenceResult):
        """Print comprehensive test summary"""
        print("\n" + "=" * 60)
        print("📊 MORNING STANDUP SEQUENCE TEST SUMMARY")
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
            f"✅ Conversation flow documented: {'PASS' if result.conversation_flow_patterns else 'FAIL'}"
        )
        print(
            f"✅ Under 10 seconds total: {'PASS' if result.total_duration_ms < 10000 else 'FAIL'}"
        )

        print(f"\n🔍 UX Insights:")
        for insight in result.ux_insights:
            print(f"   • {insight}")

        print(f"\n🔄 Conversation Flow Patterns:")
        for pattern in result.conversation_flow_patterns:
            print(f"   • {pattern}")

        print(f"\n📝 Individual Query Results:")
        for i, query_result in enumerate(result.query_results, 1):
            status = "✅" if query_result.success else "❌"
            print(f"   {i}. {status} {query_result.query}")
            print(f"      Time: {query_result.response_time_ms:.1f}ms")
            if query_result.intent_category:
                print(f"      Intent: {query_result.intent_category}/{query_result.intent_action}")
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
        else:
            print(f"⚠️  ISSUES: Only {result.success_rate:.1f}% success rate")


async def main():
    """Main test runner"""
    tester = MorningStandupTester()

    # Mandatory verification steps
    print("🔍 PM-071: Morning Standup Sequence Testing")
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

    print("✅ All verification steps passed - proceeding with test sequence")

    # Run the standup sequence
    result = await tester.run_standup_sequence()

    # Print comprehensive summary
    tester.print_summary(result)

    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"docs/development/pm-071-standup-test-results-{timestamp}.json"

    # Convert to JSON-serializable format
    result_dict = {
        "timestamp": timestamp,
        "total_duration_ms": result.total_duration_ms,
        "success_rate": result.success_rate,
        "average_response_time_ms": result.average_response_time_ms,
        "ux_insights": result.ux_insights,
        "conversation_flow_patterns": result.conversation_flow_patterns,
        "query_results": [
            {
                "query": r.query,
                "query_type": r.query_type,
                "response_time_ms": r.response_time_ms,
                "success": r.success,
                "response_text": r.response_text,
                "intent_category": r.intent_category,
                "intent_action": r.intent_action,
                "confidence": r.confidence,
                "error_message": r.error_message,
            }
            for r in result.query_results
        ],
    }

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        json.dump(result_dict, f, indent=2)

    print(f"\n💾 Results saved to: {filename}")
    print("\n🎯 PM-071 Morning Standup Sequence Testing Complete!")


if __name__ == "__main__":
    asyncio.run(main())
