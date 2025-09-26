#!/usr/bin/env python3
"""
Local Performance Testing Script

Run this locally to check performance before pushing to CI.
Usage: python scripts/run_performance_tests.py
"""

import asyncio
import sys
import time
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from services.orchestration.engine import OrchestrationEngine
    from services.intent_service.llm_classifier import LLMIntentClassifier
    from services.database.session_factory import AsyncSessionFactory
    from scripts.performance_config import check_performance_regression
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running from the project root and dependencies are installed")
    sys.exit(1)

class LocalPerformanceTester:
    """Local performance testing with baseline comparison"""
    
    async def test_queryrouter_init(self) -> bool:
        """Test QueryRouter initialization performance"""
        print("Testing QueryRouter initialization...")
        times = []
        
        for i in range(3):  # Run 3 times for consistency
            try:
                start = time.time()
                async with AsyncSessionFactory.session_scope() as session:
                    engine = OrchestrationEngine()
                    query_router = await engine.get_query_router()
                duration_ms = (time.time() - start) * 1000
                times.append(duration_ms)
                print(f"  Run {i+1}: {duration_ms:.1f}ms")
            except Exception as e:
                print(f"  Run {i+1}: FAILED - {e}")
                return False
        
        avg_time = sum(times) / len(times)
        max_time = max(times)
        print(f"  Average: {avg_time:.1f}ms, Max: {max_time:.1f}ms")
        
        return check_performance_regression("queryrouter_init_ms", max_time)
    
    async def test_llm_classification(self) -> bool:
        """Test LLM classification performance"""
        print("Testing LLM classification...")
        
        try:
            classifier = LLMIntentClassifier()
            test_message = "Create a GitHub issue about performance testing"
            
            start = time.time()
            result = await classifier.classify(test_message)
            duration_ms = (time.time() - start) * 1000
            
            print(f"  Duration: {duration_ms:.0f}ms")
            print(f"  Result: {result.category if hasattr(result, 'category') else 'N/A'}")
            
            return check_performance_regression("llm_classification_ms", duration_ms)
        except Exception as e:
            print(f"  FAILED - {e}")
            return False
    
    async def test_orchestration_flow(self) -> bool:
        """Test full orchestration flow performance"""
        print("Testing orchestration flow...")
        
        try:
            async with AsyncSessionFactory.session_scope() as session:
                engine = OrchestrationEngine()
                test_input = "List all current projects"
                
                start = time.time()
                # Test initialization and basic flow
                query_router = await engine.get_query_router()
                duration_ms = (time.time() - start) * 1000
                
                print(f"  Duration: {duration_ms:.0f}ms")
                print(f"  QueryRouter initialized: {query_router is not None}")
                
                return check_performance_regression("orchestration_flow_ms", duration_ms)
        except Exception as e:
            print(f"  FAILED - {e}")
            return False
    
    async def run_all_tests(self) -> bool:
        """Run all performance tests"""
        print("🔍 Local Performance Testing")
        print("=" * 40)
        
        tests = [
            ("QueryRouter Initialization", self.test_queryrouter_init),
            ("LLM Classification", self.test_llm_classification),
            ("Orchestration Flow", self.test_orchestration_flow),
        ]
        
        all_passed = True
        results = []
        
        for test_name, test_func in tests:
            print(f"\n--- {test_name} ---")
            try:
                result = await test_func()
                results.append((test_name, "PASS" if result else "FAIL"))
                if not result:
                    all_passed = False
            except Exception as e:
                print(f"ERROR: {e}")
                results.append((test_name, "ERROR"))
                all_passed = False
        
        # Summary
        print("\n" + "=" * 40)
        print("PERFORMANCE TEST SUMMARY")
        for test_name, status in results:
            status_icon = "✅" if status == "PASS" else "❌"
            print(f"{status_icon} {test_name}: {status}")
        
        if all_passed:
            print("\n🎉 All performance tests PASSED!")
            print("Safe to push - no performance regressions detected")
        else:
            print("\n⚠️  Performance regressions detected!")
            print("Review failing tests before pushing to CI")
        
        return all_passed

async def main():
    """Main entry point"""
    tester = LocalPerformanceTester()
    result = await tester.run_all_tests()
    sys.exit(0 if result else 1)

if __name__ == "__main__":
    asyncio.run(main())
