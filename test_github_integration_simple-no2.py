#!/usr/bin/env python3
"""
Simple test to verify GitHub integration works.
Run with: python test_github_integration_simple.py
"""
import asyncio
import os

from services.domain.models import Intent, IntentCategory
from services.orchestration.engine import OrchestrationEngine
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
            "project_id": "test-project-id",  # You'll need a real project ID
            "title": "Test Issue from Piper Morgan",
            "body": "This is a test issue created by the GitHub integration.",
            "labels": ["test", "automated"],
        },
    )

    try:
        # Get engine instance
        engine = OrchestrationEngine.get_instance()

        # Create and execute workflow
        print("Creating workflow...")
        workflow = await engine.create_workflow_from_intent(intent)
        print(f"Workflow created: {workflow.id} (type: {workflow.type})")
        print(f"Workflow context: {workflow.context}")

        print("\nExecuting workflow...")
        result = await engine.execute_workflow(workflow.id)

        if result.success:
            print(f"✅ SUCCESS! Issue created:")
            print(
                f"   Issue URL: {result.data.get('tasks', [{}])[0].get('result', {}).get('output_data', {}).get('issue_url', 'N/A')}"
            )
        else:
            print(f"❌ FAILED: {result.error}")

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    print("GitHub Integration Test")
    print("=" * 50)
    asyncio.run(test_github_issue_creation())
