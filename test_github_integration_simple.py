#!/usr/bin/env python3
"""
Simple test to verify GitHub integration works.
Run with: python test_github_integration_simple.py
"""
import asyncio
import os

from services.domain.models import Intent, IntentCategory
from services.orchestration import engine
from services.shared_types import WorkflowType


async def test_github_issue_creation():
    """Test creating a GitHub issue through orchestration."""
    print("Testing GitHub Issue Creation...")

    # Check for GitHub token
    if not os.getenv("GITHUB_TOKEN"):
        print("❌ ERROR: GITHUB_TOKEN environment variable not set")
        return

    # Create test intent
    intent = Intent(
        category=IntentCategory.EXECUTION,
        action="create_github_issue",
        context={
            "project_id": "test-piper-project",
            "title": "Test Issue from Piper Morgan",
            "body": "This is a test issue created by the GitHub integration.",
            "labels": ["test", "automated"],
        },
    )

    try:
        # Create and execute workflow
        print("Creating workflow...")
        workflow = await engine.create_workflow_from_intent(intent)
        print(f"Workflow created: {workflow.id} (type: {workflow.type})")
        print(f"Workflow context: {workflow.context}")

        print("\nExecuting workflow...")
        result = await engine.execute_workflow(workflow.id)
        print(f"DEBUG - Result type: {type(result)}")
        print(f"DEBUG - Result: {result}")

        if result["status"] == "completed":
            print(f"✅ SUCCESS! Workflow completed")
            # Get issue URL from first task
            if result["tasks"] and len(result["tasks"]) > 0:
                task = result["tasks"][0]
                if task.get("result") and task["result"].get("output_data"):
                    issue_url = task["result"]["output_data"].get("issue_url", "N/A")
                    print(f"   Issue URL: {issue_url}")
                    print(f"   Issue #: {task['result']['output_data'].get('issue_number', 'N/A')}")
        else:
            print(f"❌ FAILED: Workflow status: {result['status']}")
            if result.get("error"):
                print(f"   Error: {result['error']}")

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    print("GitHub Integration Test")
    print("=" * 50)
    asyncio.run(test_github_issue_creation())
