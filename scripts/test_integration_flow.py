#!/usr/bin/env python3
"""
Integration Flow Testing Script

Tests the complete flow: WorkflowFactory → OrchestrationEngine → Task Handlers
Focuses on PM-062 integration verification without database dependencies.

Usage:
    python scripts/test_integration_flow.py
"""

import asyncio
import sys
import os
from typing import Dict, Any

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.domain.models import Intent, IntentCategory
from services.orchestration.engine import OrchestrationEngine
from services.orchestration.workflow_factory import WorkflowFactory
from services.shared_types import WorkflowType, TaskType, TaskStatus, WorkflowStatus


class IntegrationTester:
    """Test the complete integration flow"""
    
    def __init__(self):
        self.engine = OrchestrationEngine()
        self.factory = WorkflowFactory()
        self.test_results = []
    
    async def test_integration_flow(self, workflow_type: WorkflowType, context: Dict[str, Any]) -> Dict[str, Any]:
        """Test the complete integration flow for a workflow type"""
        print(f"🔄 Testing integration flow for {workflow_type.value}...")
        
        try:
            # Step 1: Create intent
            intent = Intent(
                category=IntentCategory.EXECUTION,
                action=workflow_type.value,
                confidence=1.0,
                context=context
            )
            
            # Step 2: Factory creates workflow
            workflow = await self.factory.create_from_intent(intent)
            if not workflow:
                return {
                    "workflow_type": workflow_type.value,
                    "status": "FAIL",
                    "error": "Factory failed to create workflow"
                }
            
            # Step 3: Verify workflow has tasks
            if not workflow.tasks:
                return {
                    "workflow_type": workflow_type.value,
                    "status": "FAIL",
                    "error": "Workflow has no tasks"
                }
            
            # Step 4: Test task handler execution
            task = workflow.tasks[0]
            handler = self.engine.task_handlers.get(task.type)
            if not handler:
                return {
                    "workflow_type": workflow_type.value,
                    "status": "FAIL",
                    "error": f"No handler found for task type {task.type.value}"
                }
            
            # Step 5: Execute task handler
            result = await handler(workflow, task)
            
            return {
                "workflow_type": workflow_type.value,
                "status": "PASS" if result.success else "FAIL",
                "task_type": task.type.value,
                "success": result.success,
                "error": result.error
            }
            
        except Exception as e:
            return {
                "workflow_type": workflow_type.value,
                "status": "ERROR",
                "error": str(e)
            }
    
    async def run_integration_tests(self):
        """Run integration tests for workflow types that use new task handlers"""
        print("🚀 Starting Integration Flow Tests")
        print("=" * 60)
        
        # Test workflow types that should use the new task handlers
        test_cases = [
            (WorkflowType.GENERATE_REPORT, {
                "original_message": "Generate a quarterly report",
                "document_type": "quarterly_report"
            }),
            (WorkflowType.PLAN_STRATEGY, {
                "original_message": "Plan strategy for Q4",
                "summary_type": "strategy_plan"
            }),
            (WorkflowType.ANALYZE_FEEDBACK, {
                "original_message": "Analyze user feedback about the new feature",
                "feedback_type": "feature_feedback"
            })
        ]
        
        for workflow_type, context in test_cases:
            result = await self.test_integration_flow(workflow_type, context)
            self.test_results.append(result)
            
            # Print result
            status_emoji = "✅" if result["status"] == "PASS" else "❌"
            print(f"{status_emoji} {result['workflow_type']} → {result.get('task_type', 'N/A')}: {result['status']}")
            if result.get("error"):
                print(f"   Error: {result['error']}")
            print()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print integration test summary"""
        print("=" * 60)
        print("📊 INTEGRATION TEST SUMMARY")
        print("=" * 60)
        
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r["status"] == "PASS")
        failed = sum(1 for r in self.test_results if r["status"] == "FAIL")
        errors = sum(1 for r in self.test_results if r["status"] == "ERROR")
        
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"🐛 Errors: {errors}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 ALL INTEGRATION FLOWS WORKING CORRECTLY!")
            print("   Factory → Engine → Task Handlers: ✅")
        else:
            print("\n⚠️  Some integration flows need attention:")
            for result in self.test_results:
                if result["status"] != "PASS":
                    print(f"   - {result['workflow_type']}: {result.get('error', 'Unknown error')}")


async def main():
    """Main integration test runner"""
    tester = IntegrationTester()
    await tester.run_integration_tests()


if __name__ == "__main__":
    asyncio.run(main()) 