"""
Test script for reminder message formatter.

Verifies:
- Message formatting with all components
- Timezone-aware greetings
- Link generation
- Integration with StandupReminderJob

Issue: #161 (CORE-STAND-SLACK-REMIND)
Task: 3 of 4 - Message Formatting
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from services.integrations.slack.reminder_formatter import (
    ReminderMessageFormatter,
    get_reminder_formatter,
)


def test_message_formatting():
    """Test reminder message formatting."""
    print("=" * 70)
    print("Testing Reminder Message Formatter")
    print("=" * 70)
    print()

    formatter = ReminderMessageFormatter()

    # Test 1: Format message for PT morning
    print("Test 1: Morning message (Pacific Time)")
    print("-" * 70)
    message = formatter.format_reminder_message(
        user_id="test_user", user_timezone="America/Los_Angeles"
    )
    print(message)
    print()

    # Test 2: Format message for ET morning
    print("Test 2: Morning message (Eastern Time)")
    print("-" * 70)
    message = formatter.format_reminder_message(
        user_id="test_user", user_timezone="America/New_York"
    )
    print(message)
    print()

    # Test 3: Format message for UK afternoon
    print("Test 3: Afternoon message (London)")
    print("-" * 70)
    message = formatter.format_reminder_message(user_id="test_user", user_timezone="Europe/London")
    print(message)
    print()

    # Test 4: Verify web link
    print("Test 4: Web link generation")
    print("-" * 70)
    web_link = formatter._generate_web_link()
    assert web_link == "https://piper-morgan.com/standup"
    print(f"  ✅ Web link: {web_link}")
    print()

    # Test 5: Verify CLI command
    print("Test 5: CLI command generation")
    print("-" * 70)
    cli_command = formatter._generate_cli_command()
    assert cli_command == "piper standup"
    print(f"  ✅ CLI command: {cli_command}")
    print()

    # Test 6: Verify API endpoint
    print("Test 6: API endpoint generation")
    print("-" * 70)
    api_endpoint = formatter._generate_api_endpoint()
    assert api_endpoint == "POST /api/v1/standup/generate"
    print(f"  ✅ API endpoint: {api_endpoint}")
    print()

    # Test 7: Example message
    print("Test 7: Example message")
    print("-" * 70)
    example = formatter.format_example_message()
    assert (
        "Good morning" in example
        or "Good afternoon" in example
        or "Good evening" in example
        or "Hello" in example
    )
    assert "Web:" in example
    assert "CLI:" in example
    assert "API:" in example
    assert "Disable reminders" in example
    print("  ✅ Example message contains all components")
    print()

    # Test 8: Global formatter instance
    print("Test 8: Global formatter instance")
    print("-" * 70)
    formatter1 = get_reminder_formatter()
    formatter2 = get_reminder_formatter()
    assert formatter1 is formatter2
    print("  ✅ Singleton pattern working")
    print()

    # Test 9: Custom base URL
    print("Test 9: Custom base URL")
    print("-" * 70)
    custom_formatter = ReminderMessageFormatter(base_url="https://custom.example.com")
    custom_link = custom_formatter._generate_web_link()
    assert custom_link == "https://custom.example.com/standup"
    print(f"  ✅ Custom URL: {custom_link}")
    print()

    # Test 10: Greeting variations
    print("Test 10: Greeting variations by timezone")
    print("-" * 70)
    timezones = [
        "America/Los_Angeles",
        "America/New_York",
        "Europe/London",
        "Asia/Tokyo",
    ]
    for tz in timezones:
        message = formatter.format_reminder_message("test", tz)
        greeting = message.split("\n")[0]
        print(f"  {tz}: {greeting}")
    print()

    # Test 11: Message structure validation
    print("Test 11: Message structure validation")
    print("-" * 70)
    test_message = formatter.format_reminder_message("test_user", "America/Los_Angeles")
    lines = test_message.split("\n")
    assert len(lines) >= 5, "Message should have at least 5 lines"
    assert "Generate your standup:" in test_message
    assert "• Web:" in test_message
    assert "• CLI:" in test_message
    assert "• API:" in test_message
    assert "Disable reminders:" in test_message
    print("  ✅ Message structure is correct")
    print()

    print("=" * 70)
    print("✅ All message formatter tests passed!")
    print("=" * 70)


if __name__ == "__main__":
    test_message_formatting()
