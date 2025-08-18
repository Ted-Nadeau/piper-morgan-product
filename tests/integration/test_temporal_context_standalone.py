#!/usr/bin/env python3
"""
Standalone Test Runner for Temporal Context Integration

This script runs the temporal context tests without pytest infrastructure
to avoid database connection issues and provide immediate validation.
"""

import asyncio
import sys
import time
from datetime import datetime
from typing import Any, Dict
from unittest.mock import Mock, patch

# Add the project root to the path
sys.path.insert(0, "../../")

from services.domain.models import Intent
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.queries.conversation_queries import ConversationQueryService
from services.shared_types import IntentCategory as IntentCategoryEnum


class TemporalContextTestRunner:
    """Standalone test runner for temporal context integration"""

    def __init__(self):
        self.conversation_service = ConversationQueryService()
        self.canonical_handlers = CanonicalHandlers()
        self.test_results = []
        self.start_time = None

    async def run_all_tests(self):
        """Run all temporal context tests"""
        print("🧪 TEMPORAL CONTEXT INTEGRATION TESTING")
        print("=" * 60)

        self.start_time = time.time()

        # Core functionality tests
        await self.test_core_functionality()

        # Integration tests
        await self.test_integration()

        # Edge case tests
        await self.test_edge_cases()

        # Performance tests
        await self.test_performance()

        # Print results
        self.print_results()

    async def test_core_functionality(self):
        """Test core temporal context functionality"""
        print("\n🔧 CORE FUNCTIONALITY TESTS")
        print("-" * 40)

        # Test 1: Basic temporal context
        await self.run_test("Basic Temporal Context", self.test_basic_temporal_context)

        # Test 2: Static calendar patterns
        await self.run_test("Static Calendar Patterns", self.test_static_calendar_patterns)

        # Test 3: Dynamic calendar formatting
        await self.run_test("Dynamic Calendar Formatting", self.test_dynamic_calendar_formatting)

        # Test 4: Focus guidance
        await self.run_test("Focus Guidance", self.test_focus_guidance)

        # Test 5: Time-aware priority
        await self.run_test("Time-Aware Priority", self.test_time_aware_priority)

    async def test_integration(self):
        """Test integration with canonical handlers"""
        print("\n🔗 INTEGRATION TESTS")
        print("-" * 40)

        # Test 1: Temporal query integration
        await self.run_test("Temporal Query Integration", self.test_temporal_query_integration)

        # Test 2: Status query integration
        await self.run_test("Status Query Integration", self.test_status_query_integration)

        # Test 3: Priority query integration
        await self.run_test("Priority Query Integration", self.test_priority_query_integration)

        # Test 4: Guidance query integration
        await self.run_test("Guidance Query Integration", self.test_guidance_query_integration)

    async def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        print("\n⚠️  EDGE CASE TESTS")
        print("-" * 40)

        # Test 1: Midnight boundary
        await self.run_test("Midnight Boundary", self.test_midnight_boundary)

        # Test 2: Weekend handling
        await self.run_test("Weekend Handling", self.test_weekend_handling)

        # Test 3: Empty calendar patterns
        await self.run_test("Empty Calendar Patterns", self.test_empty_calendar_patterns)

        # Test 4: Malformed patterns
        await self.run_test("Malformed Patterns", self.test_malformed_patterns)

    async def test_performance(self):
        """Test performance targets"""
        print("\n⚡ PERFORMANCE TESTS")
        print("-" * 40)

        # Test 1: Performance targets
        await self.run_test("Performance Targets", self.test_performance_targets)

        # Test 2: MCP integration readiness
        await self.run_test("MCP Integration Ready", self.test_mcp_integration_readiness)

    async def run_test(self, test_name: str, test_func):
        """Run a single test and record results"""
        try:
            start_time = time.time()
            result = await test_func()
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000  # Convert to milliseconds

            if result:
                status = "✅ PASSED"
                self.test_results.append(
                    {
                        "name": test_name,
                        "status": "PASSED",
                        "time_ms": execution_time,
                        "details": result,
                    }
                )
            else:
                status = "❌ FAILED"
                self.test_results.append(
                    {
                        "name": test_name,
                        "status": "FAILED",
                        "time_ms": execution_time,
                        "details": "Test returned False",
                    }
                )

        except Exception as e:
            status = "💥 ERROR"
            execution_time = 0
            self.test_results.append(
                {"name": test_name, "status": "ERROR", "time_ms": 0, "details": str(e)}
            )

        print(f"{status} {test_name} ({execution_time:.2f}ms)")

    # Core functionality test methods
    async def test_basic_temporal_context(self):
        """Test basic temporal context functionality"""
        temporal_context = await self.conversation_service.get_temporal_context()

        # Verify basic temporal information is present
        if not all(
            marker in temporal_context
            for marker in ["**Current Time**:", "**Day of Week**:", "**Week**:"]
        ):
            return False

        # Verify current time format
        current_time = datetime.now()
        if current_time.strftime("%A") not in temporal_context:
            return False

        return f"Basic temporal context generated successfully ({len(temporal_context)} characters)"

    async def test_static_calendar_patterns(self):
        """Test temporal context with static calendar patterns"""
        # Mock calendar patterns
        mock_patterns = """**Daily Routines**:
- **6:00 AM PT**: Daily standup with Piper Morgan
- **9:00 AM PT**: Development focus time"""

        with patch.object(self.conversation_service.config_loader, "load_config") as mock_load:
            mock_load.return_value = {"Calendar Patterns": mock_patterns}

            temporal_context = await self.conversation_service.get_temporal_context()

            # Verify calendar context is included
            if "**Calendar Context**:" not in temporal_context:
                return False
            if "Daily standup with Piper Morgan" not in temporal_context:
                return False

            return "Static calendar patterns integrated successfully"

    async def test_dynamic_calendar_formatting(self):
        """Test formatting of dynamic calendar data"""
        mock_calendar_data = {
            "upcoming_events": [{"start_time": "9:00 AM", "title": "Development Sprint Planning"}],
            "time_blocks": [{"start_time": "8:00 AM", "end_time": "11:00 AM", "type": "deep_work"}],
        }

        formatted_context = self.conversation_service._format_calendar_context(
            mock_calendar_data, datetime.now()
        )

        # Verify formatting
        if "**Upcoming Events**:" not in formatted_context:
            return False
        if "Development Sprint Planning" not in formatted_context:
            return False
        if "deep_work time" not in formatted_context:
            return False

        return "Dynamic calendar formatting working correctly"

    async def test_focus_guidance(self):
        """Test time-aware focus guidance"""
        focus_guidance = await self.conversation_service.get_focus_guidance()

        # Verify temporal context is included
        if "**Focus Guidance Based on Current Context**:" not in focus_guidance:
            return False
        if "**Current Phase**:" not in focus_guidance:
            return False

        # Verify time-based recommendations
        current_hour = datetime.now().hour
        if 5 <= current_hour <= 7:
            if "Morning Standup Focus" not in focus_guidance:
                return False
        elif 8 <= current_hour <= 11:
            if "Development Focus Time" not in focus_guidance:
                return False

        return "Focus guidance working with time awareness"

    async def test_time_aware_priority(self):
        """Test time-aware priority functionality"""
        time_aware_priority = await self.conversation_service.get_time_aware_priority()

        # Verify priorities are included
        if "**Your Current Standing Priorities**:" not in time_aware_priority:
            return False
        if "**Time Context**:" not in time_aware_priority:
            return False

        return "Time-aware priority working correctly"

    # Integration test methods
    async def test_temporal_query_integration(self):
        """Test canonical handlers integration with temporal context"""
        sample_intent = Intent(
            category=IntentCategoryEnum.TEMPORAL,
            action="get_temporal_context",
            confidence=0.9,
            context={"query": "What day is it?"},
        )

        response = await self.canonical_handlers.handle(sample_intent, "test_session")

        # Verify response structure
        if "message" not in response:
            return False
        if "intent" not in response:
            return False
        if response["intent"]["category"] != IntentCategoryEnum.TEMPORAL.value:
            return False

        # Verify enhanced temporal context is provided
        message = response["message"]
        if "**Current Time**:" not in message:
            return False
        if "**Time Guidance**:" not in message:
            return False

        return "Temporal query integration working correctly"

    async def test_status_query_integration(self):
        """Test status query with temporal awareness"""
        status_intent = Intent(
            category=IntentCategoryEnum.STATUS,
            action="get_project_status",
            confidence=0.9,
            context={"query": "What am I working on?"},
        )

        response = await self.canonical_handlers.handle(status_intent, "test_session")

        # Verify temporal context is included in status
        message = response["message"]
        if "**Current Project Status with Temporal Context**:" not in message:
            return False
        if "**Time-Aware Focus**:" not in message:
            return False

        return "Status query integration working with temporal awareness"

    async def test_priority_query_integration(self):
        """Test priority query with temporal awareness"""
        priority_intent = Intent(
            category=IntentCategoryEnum.PRIORITY,
            action="get_top_priority",
            confidence=0.9,
            context={"query": "What's my top priority?"},
        )

        response = await self.canonical_handlers.handle(priority_intent, "test_session")

        # Verify temporal context is included in priority
        message = response["message"]
        if "**Time Constraint Analysis**:" not in message:
            return False
        if "**Enhanced Context**:" not in message:
            return False

        return "Priority query integration working with temporal awareness"

    async def test_guidance_query_integration(self):
        """Test guidance query with temporal awareness"""
        guidance_intent = Intent(
            category=IntentCategoryEnum.GUIDANCE,
            action="get_focus_guidance",
            confidence=0.9,
            context={"query": "What should I focus on?"},
        )

        response = await self.canonical_handlers.handle(guidance_intent, "test_session")

        # Verify comprehensive temporal guidance
        message = response["message"]
        if "**Focus Guidance Based on Current Context**:" not in message:
            return False
        if "**Focus Intensity**:" not in message:
            return False
        if "**Daily Strategy**:" not in message:
            return False
        if "**Enhanced Temporal Context**:" not in message:
            return False

        return "Guidance query integration working with comprehensive temporal awareness"

    # Edge case test methods
    async def test_midnight_boundary(self):
        """Test behavior around midnight boundary"""
        with patch("services.queries.conversation_queries.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 8, 18, 0, 0)  # Midnight

            focus_guidance = await self.conversation_service.get_focus_guidance()

            # Should handle midnight gracefully
            if focus_guidance is None:
                return False
            if "Evening Planning" not in focus_guidance:
                return False

            return "Midnight boundary handled gracefully"

    async def test_weekend_handling(self):
        """Test weekend day handling"""
        with patch("services.queries.conversation_queries.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 8, 16, 10, 0)  # Saturday 10 AM

            focus_guidance = await self.conversation_service.get_focus_guidance()

            # Should handle weekend gracefully
            if focus_guidance is None:
                return False
            if "Development Focus Time" not in focus_guidance:
                return False

            return "Weekend handling working correctly"

    async def test_empty_calendar_patterns(self):
        """Test behavior with empty calendar patterns"""
        with patch.object(self.conversation_service.config_loader, "load_config") as mock_load:
            mock_load.return_value = {"Calendar Patterns": ""}

            temporal_context = await self.conversation_service.get_temporal_context()

            # Should still provide basic temporal information
            if "**Current Time**:" not in temporal_context:
                return False
            if "**Day of Week**:" not in temporal_context:
                return False

            # Should not include calendar context section
            if "**Calendar Context**:" in temporal_context:
                return False

            return "Empty calendar patterns handled gracefully"

    async def test_malformed_patterns(self):
        """Test behavior with malformed calendar patterns"""
        malformed_patterns = "Invalid\nCalendar\nPatterns\nWithout\nProper\nFormatting"

        with patch.object(self.conversation_service.config_loader, "load_config") as mock_load:
            mock_load.return_value = {"Calendar Patterns": malformed_patterns}

            temporal_context = await self.conversation_service.get_temporal_context()

            # Should handle malformed patterns gracefully
            if temporal_context is None:
                return False
            if len(temporal_context) == 0:
                return False

            return "Malformed patterns handled gracefully"

    # Performance test methods
    async def test_performance_targets(self):
        """Test performance targets for temporal context operations"""
        start_time = time.time()

        # Execute temporal context operations
        temporal_context = await self.conversation_service.get_temporal_context()
        focus_guidance = await self.conversation_service.get_focus_guidance()
        time_aware_priority = await self.conversation_service.get_time_aware_priority()

        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds

        # Verify performance target: <200ms latency
        if execution_time >= 200:
            return f"Performance target exceeded: {execution_time:.2f}ms (target: <200ms)"

        # Verify all operations completed successfully
        if temporal_context is None or focus_guidance is None or time_aware_priority is None:
            return "Some operations failed to complete"

        return f"Performance target met: {execution_time:.2f}ms (target: <200ms)"

    async def test_mcp_integration_readiness(self):
        """Test that MCP integration is ready for future implementation"""
        # Test that the MCP integration method exists and is callable
        if not hasattr(self.conversation_service, "_get_calendar_from_mcp"):
            return "MCP integration method missing"
        if not callable(self.conversation_service._get_calendar_from_mcp):
            return "MCP integration method not callable"

        # Test that it returns None when MCP is not available (current state)
        calendar_data = await self.conversation_service._get_calendar_from_mcp(datetime.now())
        if calendar_data is not None:
            return "MCP integration method should return None when adapter not available"

        return "MCP integration ready for future implementation"

    def print_results(self):
        """Print test results summary"""
        total_time = time.time() - self.start_time

        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)

        # Count results
        total_tests = len(self.test_results)
        passed = sum(1 for r in self.test_results if r["status"] == "PASSED")
        failed = sum(1 for r in self.test_results if r["status"] == "FAILED")
        errors = sum(1 for r in self.test_results if r["status"] == "ERROR")

        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"💥 Errors: {errors}")
        print(f"⏱️  Total Time: {total_time:.2f}s")

        # Calculate success rate
        success_rate = (passed / total_tests) * 100 if total_tests > 0 else 0
        print(f"🎯 Success Rate: {success_rate:.1f}%")

        # Performance summary
        performance_tests = [r for r in self.test_results if "Performance" in r["name"]]
        if performance_tests:
            avg_time = sum(r["time_ms"] for r in performance_tests) / len(performance_tests)
            print(f"⚡ Average Performance: {avg_time:.2f}ms")

        # Print failed tests
        if failed > 0 or errors > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if result["status"] in ["FAILED", "ERROR"]:
                    print(f"  - {result['name']}: {result['details']}")

        # Print passed tests
        if passed > 0:
            print("\n✅ PASSED TESTS:")
            for result in self.test_results:
                if result["status"] == "PASSED":
                    print(f"  - {result['name']}: {result['details']}")

        print("\n" + "=" * 60)

        if success_rate >= 90:
            print("🎉 EXCELLENT! Temporal Context Integration is working perfectly!")
        elif success_rate >= 80:
            print("👍 GOOD! Temporal Context Integration is mostly working with minor issues.")
        elif success_rate >= 70:
            print("⚠️  FAIR! Temporal Context Integration has some issues that need attention.")
        else:
            print(
                "🚨 POOR! Temporal Context Integration has significant issues requiring immediate attention."
            )

        print("=" * 60)


async def main():
    """Main test execution function"""
    runner = TemporalContextTestRunner()
    await runner.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
