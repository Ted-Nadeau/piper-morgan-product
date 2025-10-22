"""
Manual integration test for reminder system.

Run this to manually verify the complete flow without pytest.

Issue: #161 (CORE-STAND-SLACK-REMIND)
Task: 4 of 4 - Integration Testing & Final Verification
"""

import asyncio
import os
import sys
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from zoneinfo import ZoneInfo

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from services.domain.user_preference_manager import UserPreferenceManager
from services.infrastructure.task_manager import RobustTaskManager
from services.integrations.slack.reminder_formatter import ReminderMessageFormatter
from services.scheduler.standup_reminder_job import StandupReminderJob


async def test_full_flow():
    """Manually test the complete reminder flow."""
    print("=" * 70)
    print("Full Reminder Flow Test")
    print("=" * 70)
    print()

    # Create components
    print("1. Creating components...")
    task_manager = RobustTaskManager()
    preference_manager = UserPreferenceManager()
    formatter = ReminderMessageFormatter()

    # Mock Slack router
    mock_slack_router = AsyncMock()
    mock_response = MagicMock()
    mock_response.success = True
    mock_slack_router.send_message.return_value = mock_response

    reminder_job = StandupReminderJob(
        task_manager=task_manager,
        slack_router=mock_slack_router,
        preference_manager=preference_manager,
    )
    print("   ✅ Components created")
    print()

    # Set up test user
    print("2. Setting up test user...")
    test_user = "test_user_manual"
    await preference_manager.set_reminder_enabled(test_user, True)
    await preference_manager.set_reminder_time(test_user, "06:00")
    await preference_manager.set_reminder_timezone(test_user, "America/Los_Angeles")
    await preference_manager.set_reminder_days(test_user, [0, 1, 2, 3, 4])
    print("   ✅ User preferences set")
    print()

    # Get preferences
    print("3. Verifying preferences...")
    prefs = await preference_manager.get_reminder_preferences(test_user)
    print(f"   Enabled: {prefs['enabled']}")
    print(f"   Time: {prefs['time']}")
    print(f"   Timezone: {prefs['timezone']}")
    print(f"   Days: {prefs['days']}")
    print()

    # Format message
    print("4. Formatting reminder message...")
    message = formatter.format_reminder_message(test_user, prefs["timezone"])
    print("   Message:")
    print("   " + "\n   ".join(message.split("\n")))
    print()

    # Execute reminder job
    print("5. Executing reminder job...")
    result = await reminder_job.execute_daily_reminders()
    print(f"   Result:")
    print(f"   - Checked: {result.get('checked', 0)} users")
    print(f"   - Sent: {result.get('sent', 0)} reminders")
    print(f"   - Failed: {result.get('failed', 0)}")
    print(f"   - Errors: {len(result.get('errors', []))}")
    print()

    # Check if message would be sent
    print("6. Checking Slack mock calls...")
    if mock_slack_router.send_message.called:
        call_args = mock_slack_router.send_message.call_args
        print(f"   ✅ Message sent to: {call_args[1]['channel']}")
        print(f"   Message preview: {call_args[1]['text'][:100]}...")
    else:
        print("   ℹ️  No message sent (timing or day mismatch)")
    print()

    # Test timezone greetings
    print("7. Testing timezone-aware greetings...")
    timezones = {
        "America/Los_Angeles": "Pacific Time",
        "America/New_York": "Eastern Time",
        "Europe/London": "London",
        "Asia/Tokyo": "Tokyo",
    }

    for tz, name in timezones.items():
        msg = formatter.format_reminder_message("test", tz)
        greeting = msg.split("\n")[0]
        print(f"   {name:20s}: {greeting}")
    print()

    # Test all components present
    print("8. Verifying message components...")
    test_message = formatter.format_reminder_message("test", "America/Los_Angeles")
    components = [
        ("Web link", "Web:"),
        ("CLI command", "CLI:"),
        ("API endpoint", "API:"),
        ("Disable instructions", "Disable reminders:"),
    ]

    all_present = True
    for component_name, component_text in components:
        if component_text in test_message:
            print(f"   ✅ {component_name} present")
        else:
            print(f"   ❌ {component_name} MISSING")
            all_present = False
    print()

    # Final summary
    print("=" * 70)
    if all_present:
        print("✅ Test Complete - All components working!")
    else:
        print("❌ Test Failed - Some components missing")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_full_flow())
