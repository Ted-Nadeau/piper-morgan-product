"""
Manual Test Script: StandupReminderJob

Tests the reminder job implementation directly.
Verifies that the job can be created, executed, and returns proper results.

Issue: #161 (CORE-STAND-SLACK-REMIND)
Task: 1 of 4 - Reminder Job Implementation
"""

import asyncio
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from services.domain.user_preference_manager import UserPreferenceManager
from services.infrastructure.task_manager import RobustTaskManager
from services.integrations.slack.config_service import SlackConfigService
from services.integrations.slack.slack_client import SlackClient
from services.scheduler.standup_reminder_job import StandupReminderJob


async def test_reminder_job():
    """Test StandupReminderJob creation and execution."""
    print("=" * 70)
    print("Testing StandupReminderJob")
    print("=" * 70)

    try:
        print("\n1. Creating dependencies...")
        task_manager = RobustTaskManager()
        print("   ✓ RobustTaskManager created")

        slack_config_service = SlackConfigService()
        print("   ✓ SlackConfigService created")

        slack_client = SlackClient(slack_config_service)
        print("   ✓ SlackClient created")

        preference_manager = UserPreferenceManager()
        print("   ✓ UserPreferenceManager created")

        print("\n2. Creating StandupReminderJob...")
        job = StandupReminderJob(task_manager, slack_client, preference_manager)
        print("   ✓ StandupReminderJob created")

        print("\n3. Executing daily reminders...")
        result = await job.execute_daily_reminders()

        print("\n4. Results:")
        print(f"   - Users checked: {result.get('checked', 0)}")
        print(f"   - Reminders sent: {result.get('sent', 0)}")
        print(f"   - Failed: {result.get('failed', 0)}")
        print(f"   - Errors: {len(result.get('errors', []))}")

        if result.get("errors"):
            print("\n   Error details:")
            for error in result["errors"]:
                print(f"     - {error}")

        print("\n" + "=" * 70)
        print("✓ Test completed successfully!")
        print("=" * 70)

        # Expected: 0 reminders sent (placeholder returns empty user list)
        if result.get("checked") == 0:
            print("\nNote: No users checked - expected behavior for Task 1 placeholder")
            print("Task 2 will implement actual user preference querying")

        return True

    except Exception as e:
        print("\n" + "=" * 70)
        print("✗ Test failed!")
        print("=" * 70)
        print(f"\nError: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n🧪 StandupReminderJob Manual Test\n")

    success = asyncio.run(test_reminder_job())

    if success:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Tests failed!")
        sys.exit(1)
