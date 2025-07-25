#!/usr/bin/env python3
"""
Direct Task Handler Testing Script

Tests the newly implemented task handlers without database dependencies.
Focuses on PM-062 missing task handler verification.

Usage:
    python scripts/test_task_handlers_direct.py
"""

import asyncio
import sys
import os
from typing import Dict, Any

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.domain.models import Workflow, Task, Intent, IntentCategory
from services.orchestration.engine import OrchestrationEngine
from services.shared_types import WorkflowType, TaskType, TaskStatus, WorkflowStatus


class TaskHandlerTester:
    """Test task handlers directly without database dependencies"""
    
    def __init__(self):
        self.engine = OrchestrationEngine()
        self.test_results = []
    
    def create_test_workflow(self, workflow_type: WorkflowType, task_type: TaskType, context: Dict[str, Any]) -> Workflow:
        """Create a test workflow with the specified task"""
        workflow = Workflow(
            id="test-workflow-123",
            type=workflow_type,
            status=WorkflowStatus.PENDING,
            context=context
        )
        
        task = Task(
            id="test-task-456",
            name=f"Test {task_type.value}",
            type=task_type,
            status=TaskStatus.PENDING
        )
        
        workflow.tasks.append(task)
        return workflow
    
    async def test_task_handler(self, task_type: TaskType, context: Dict[str, Any]) -> Dict[str, Any]:
        """Test a specific task handler"""
        print(f"🧪 Testing {task_type.value}...")
        
        # Create test workflow
        workflow = self.create_test_workflow(WorkflowType.CREATE_TICKET, task_type, context)
        
        # Get the task handler
        handler = self.engine.task_handlers.get(task_type)
        if not handler:
            return {
                "task_type": task_type.value,
                "status": "FAIL",
                "error": f"No handler found for {task_type.value}"
            }
        
        try:
            # Execute the handler
            task = workflow.tasks[0]
            result = await handler(workflow, task)
            
            return {
                "task_type": task_type.value,
                "status": "PASS" if result.success else "FAIL",
                "success": result.success,
                "output_data": result.output_data,
                "error": result.error
            }
            
        except Exception as e:
            return {
                "task_type": task_type.value,
                "status": "ERROR",
                "error": str(e)
            }
    
    async def run_all_tests(self):
        """Run tests for all newly implemented task handlers"""
        print("🚀 Starting Direct Task Handler Tests")
        print("=" * 50)
        
        # Test contexts for each task type
        test_contexts = {
            TaskType.UPDATE_WORK_ITEM: {
                "original_message": "Update the priority of task #123 to high",
                "work_item_id": "task-123"
            },
            TaskType.GENERATE_DOCUMENT: {
                "original_message": "Generate a project requirements document",
                "document_type": "requirements"
            },
            TaskType.CREATE_SUMMARY: {
                "original_message": "Summarize the quarterly performance metrics",
                "summary_type": "quarterly_report"
            },
            TaskType.PROCESS_USER_FEEDBACK: {
                "original_message": "User reported that the login page is slow",
                "feedback_type": "performance_issue"
            }
        }
        
        # Test each task handler
        for task_type, context in test_contexts.items():
            result = await self.test_task_handler(task_type, context)
            self.test_results.append(result)
            
            # Print result
            status_emoji = "✅" if result["status"] == "PASS" else "❌"
            print(f"{status_emoji} {result['task_type']}: {result['status']}")
            if result.get("error"):
                print(f"   Error: {result['error']}")
            if result.get("output_data"):
                print(f"   Output: {list(result['output_data'].keys())}")
            print()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        
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
            print("\n🎉 ALL TASK HANDLERS WORKING CORRECTLY!")
        else:
            print("\n⚠️  Some task handlers need attention:")
            for result in self.test_results:
                if result["status"] != "PASS":
                    print(f"   - {result['task_type']}: {result.get('error', 'Unknown error')}")


async def main():
    """Main test runner"""
    tester = TaskHandlerTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main()) 