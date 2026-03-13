# Task 3: Message Formatting - Reminder Messages

**Agent**: Claude Code (Programmer)
**Issue**: #161 (CORE-STAND-SLACK-REMIND)
**Task**: 3 of 4 - Message Formatting
**Sprint**: A4 "Standup Epic"
**Date**: October 20, 2025, 8:39 AM
**Estimated Effort**: 30 minutes (likely 20!)

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. ⏸️ **STOP** - Do not continue working
2. 📋 **REPORT** - Summarize what was just completed
3. ❓ **ASK** - "Should I proceed to next task?"
4. ⏳ **WAIT** - For explicit instructions

---

## Mission

Create the ReminderMessageFormatter class that generates beautifully formatted Slack reminder messages with links to web/CLI/API standup generation. This is the final piece to make reminders user-friendly and actionable.

**Scope**:
- Create ReminderMessageFormatter class
- Generate web link (standup page)
- Format CLI command
- Include API endpoint
- Add disable instructions
- Integrate with StandupReminderJob from Task 1
- Test message formatting

**NOT in scope**:
- Actually sending messages (SlackClient already does this)
- User preference management (Task 2 completed)
- Full integration testing (Task 4)

---

## Context from Tasks 1 & 2

**EXCELLENT PROGRESS**: Tasks 1 & 2 completed in 31 minutes! 🎉

**What was built**:
- ✅ Task 1: StandupReminderJob (13 min) - Timer loop, orchestration
- ✅ Task 2: UserPreferenceManager (18 min) - Preference storage, validation

**What Task 3 does**:
- Create the actual reminder message text
- Include multiple access methods (web, CLI, API)
- Make it actionable and user-friendly

---

## Architecture Document

**YOU HAVE**: `phase-3-discovery-architecture.md` uploaded by PM

**Key sections**:
- "Message Format: Rich Text with Links" - Design decision
- "Task 3: Message Formatting" - Your specific work
- Example message template

---

## STOP Conditions

If ANY of these occur, STOP and escalate to PM immediately:

1. **Cannot determine standup web URL** - Need to know base URL
2. **CLI command unclear** - Should be `piper standup` but verify
3. **API endpoint different from Task 1** - Check discovery doc
4. **Message format not Slack-compatible** - Plain text + emoji only
5. **Can't integrate with StandupReminderJob** - Need Task 1 code
6. **Timezone greeting unclear** - Need to determine greeting based on time
7. **Can't provide verification evidence** - Must show formatted messages

---

## Evidence Requirements

### For EVERY Claim You Make:

- **"Message formatted"** → Show example formatted message
- **"Links generated"** → Show actual web/CLI/API links
- **"Integration works"** → Show StandupReminderJob using formatter
- **"Greeting correct"** → Show timezone-aware greeting
- **"Tests pass"** → Show test output

### Working Files Location:

- ✅ dev/active/ - For test scripts, examples
- ✅ services/integrations/slack/ - For message formatter
- ✅ services/scheduler/ - For StandupReminderJob updates

---

## Task Requirements

### 1. Review Example Message

**From discovery document**:

```
🌅 Good morning! Time for your daily standup.

Generate your standup:
• Web: https://piper-morgan.com/standup
• CLI: `piper standup`
• API: POST /api/v1/standup/generate

Disable reminders: Reply "STOP" or update preferences
```

**Your mission**: Implement this formatter!

---

### 2. Create ReminderMessageFormatter Class

**File**: `services/integrations/slack/reminder_formatter.py`

**Structure**:

```python
"""
Reminder Message Formatter

Formats daily standup reminder messages for Slack.
Includes web, CLI, and API access methods.
"""

from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Dict, Any
import structlog

logger = structlog.get_logger()


class ReminderMessageFormatter:
    """
    Formats daily standup reminder messages.

    Responsibilities:
    - Generate timezone-aware greeting
    - Format web/CLI/API links
    - Create user-friendly message
    - Include disable instructions
    """

    def __init__(self, base_url: str = "https://piper-morgan.com"):
        """
        Initialize formatter.

        Args:
            base_url: Base URL for web links (default: https://piper-morgan.com)
        """
        self.base_url = base_url.rstrip('/')

    def format_reminder_message(
        self,
        user_id: str,
        user_timezone: str = "America/Los_Angeles"
    ) -> str:
        """
        Format reminder message for user.

        Args:
            user_id: User ID for personalization
            user_timezone: User's timezone for greeting

        Returns:
            Formatted Slack message text
        """
        # Get timezone-aware greeting
        greeting = self._get_greeting(user_timezone)

        # Generate links
        web_link = self._generate_web_link()
        cli_command = self._generate_cli_command()
        api_endpoint = self._generate_api_endpoint()

        # Format message
        message = f"""{greeting}

Generate your standup:
• Web: {web_link}
• CLI: `{cli_command}`
• API: {api_endpoint}

Disable reminders: Reply "STOP" or update preferences"""

        return message

    def _get_greeting(self, timezone: str) -> str:
        """
        Get timezone-aware greeting.

        Args:
            timezone: IANA timezone name

        Returns:
            Greeting string with emoji
        """
        try:
            # Get current hour in user's timezone
            user_time = datetime.now(ZoneInfo(timezone))
            hour = user_time.hour

            # Choose greeting based on time of day
            if 5 <= hour < 12:
                return "🌅 Good morning! Time for your daily standup."
            elif 12 <= hour < 17:
                return "☀️ Good afternoon! Time for your daily standup."
            elif 17 <= hour < 21:
                return "🌆 Good evening! Time for your daily standup."
            else:
                return "🌙 Hello! Time for your daily standup."

        except Exception as e:
            logger.warning(
                "Error getting timezone-aware greeting",
                timezone=timezone,
                error=str(e)
            )
            # Fallback to neutral greeting
            return "👋 Hello! Time for your daily standup."

    def _generate_web_link(self) -> str:
        """
        Generate web standup link.

        Returns:
            Full URL to standup page
        """
        return f"{self.base_url}/standup"

    def _generate_cli_command(self) -> str:
        """
        Generate CLI command.

        Returns:
            CLI command string
        """
        return "piper standup"

    def _generate_api_endpoint(self) -> str:
        """
        Generate API endpoint.

        Returns:
            API endpoint description
        """
        return "POST /api/v1/standup/generate"

    def format_example_message(self) -> str:
        """
        Generate example message for testing.

        Returns:
            Example formatted message
        """
        return self.format_reminder_message(
            user_id="example_user",
            user_timezone="America/Los_Angeles"
        )


# Global formatter instance
_formatter = None


def get_reminder_formatter(base_url: str = "https://piper-morgan.com") -> ReminderMessageFormatter:
    """
    Get or create global reminder formatter.

    Args:
        base_url: Base URL for web links

    Returns:
        ReminderMessageFormatter instance
    """
    global _formatter

    if _formatter is None:
        _formatter = ReminderMessageFormatter(base_url)

    return _formatter
```

---

### 3. Update StandupReminderJob

**File**: `services/scheduler/standup_reminder_job.py`

**Find the _send_reminder method and update**:

```python
# OLD (placeholder from Task 1)
async def _send_reminder(self, user_id: str) -> bool:
    """Send reminder DM to user. Returns True if successful."""
    try:
        # Placeholder message
        message = "🌅 Good morning! Time for your daily standup."

        # Send via Slack router
        success = await self.slack_router.send_message(
            channel=user_id,
            text=message
        )

        return success

    except Exception as e:
        logger.error(
            "Error sending reminder to user",
            user_id=user_id,
            error=str(e)
        )
        return False


# NEW (using ReminderMessageFormatter)
async def _send_reminder(self, user_id: str) -> bool:
    """Send reminder DM to user. Returns True if successful."""
    try:
        # Get user's timezone for personalized greeting
        user_tz = await self.preference_manager.get_reminder_timezone(user_id)

        # Format message using ReminderMessageFormatter
        from services.integrations.slack.reminder_formatter import get_reminder_formatter
        formatter = get_reminder_formatter()
        message = formatter.format_reminder_message(user_id, user_tz)

        # Send via Slack router
        success = await self.slack_router.send_message(
            channel=user_id,
            text=message
        )

        if success:
            logger.info(
                "Reminder sent successfully",
                user_id=user_id,
                timezone=user_tz
            )

        return success

    except Exception as e:
        logger.error(
            "Error sending reminder to user",
            user_id=user_id,
            error=str(e)
        )
        return False
```

**Also add import at top of file**:

```python
from services.integrations.slack.reminder_formatter import get_reminder_formatter
```

---

### 4. Create Test Script

**File**: `dev/active/test_message_formatter.py`

```python
"""
Test script for reminder message formatter.

Verifies:
- Message formatting with all components
- Timezone-aware greetings
- Link generation
- Integration with StandupReminderJob
"""

from services.integrations.slack.reminder_formatter import (
    ReminderMessageFormatter,
    get_reminder_formatter
)


def test_message_formatting():
    """Test reminder message formatting."""
    print("Testing Reminder Message Formatter\n")

    formatter = ReminderMessageFormatter()

    # Test 1: Format message for PT morning
    print("Test 1: Morning message (Pacific Time)")
    message = formatter.format_reminder_message(
        user_id="test_user",
        user_timezone="America/Los_Angeles"
    )
    print(message)
    print()

    # Test 2: Format message for ET morning
    print("Test 2: Morning message (Eastern Time)")
    message = formatter.format_reminder_message(
        user_id="test_user",
        user_timezone="America/New_York"
    )
    print(message)
    print()

    # Test 3: Format message for UK afternoon
    print("Test 3: Afternoon message (London)")
    message = formatter.format_reminder_message(
        user_id="test_user",
        user_timezone="Europe/London"
    )
    print(message)
    print()

    # Test 4: Verify web link
    print("Test 4: Web link generation")
    web_link = formatter._generate_web_link()
    assert web_link == "https://piper-morgan.com/standup"
    print(f"  ✅ Web link: {web_link}")
    print()

    # Test 5: Verify CLI command
    print("Test 5: CLI command generation")
    cli_command = formatter._generate_cli_command()
    assert cli_command == "piper standup"
    print(f"  ✅ CLI command: {cli_command}")
    print()

    # Test 6: Verify API endpoint
    print("Test 6: API endpoint generation")
    api_endpoint = formatter._generate_api_endpoint()
    assert api_endpoint == "POST /api/v1/standup/generate"
    print(f"  ✅ API endpoint: {api_endpoint}")
    print()

    # Test 7: Example message
    print("Test 7: Example message")
    example = formatter.format_example_message()
    assert "Good morning" in example or "Good afternoon" in example or "Good evening" in example or "Hello" in example
    assert "Web:" in example
    assert "CLI:" in example
    assert "API:" in example
    assert "Disable reminders" in example
    print("  ✅ Example message contains all components")
    print()

    # Test 8: Global formatter instance
    print("Test 8: Global formatter instance")
    formatter1 = get_reminder_formatter()
    formatter2 = get_reminder_formatter()
    assert formatter1 is formatter2
    print("  ✅ Singleton pattern working")
    print()

    # Test 9: Custom base URL
    print("Test 9: Custom base URL")
    custom_formatter = ReminderMessageFormatter(base_url="https://custom.example.com")
    custom_link = custom_formatter._generate_web_link()
    assert custom_link == "https://custom.example.com/standup"
    print(f"  ✅ Custom URL: {custom_link}")
    print()

    # Test 10: Greeting variations
    print("Test 10: Greeting variations by timezone")
    timezones = [
        "America/Los_Angeles",
        "America/New_York",
        "Europe/London",
        "Asia/Tokyo"
    ]
    for tz in timezones:
        message = formatter.format_reminder_message("test", tz)
        greeting = message.split('\n')[0]
        print(f"  {tz}: {greeting}")
    print()

    print("✅ All message formatter tests passed!")


if __name__ == "__main__":
    test_message_formatting()
```

---

### 5. Create Example Message File

**File**: `dev/active/example-reminder-message.txt`

**Save example formatted message for reference**:

```bash
# Generate example and save
python3 -c "
from services.integrations.slack.reminder_formatter import get_reminder_formatter
formatter = get_reminder_formatter()
message = formatter.format_example_message()
print(message)
" > dev/active/example-reminder-message.txt

# View the example
cat dev/active/example-reminder-message.txt
```

---

## Verification Steps

### Step 1: Test Message Formatter

```bash
# Run test script
python3 dev/active/test_message_formatter.py

# Expected output:
# Testing Reminder Message Formatter
#
# Test 1: Morning message (Pacific Time)
# 🌅 Good morning! Time for your daily standup.
# ...
# ✅ All message formatter tests passed!
```

---

### Step 2: Verify Integration with Task 1

```bash
# Check that StandupReminderJob imports formatter
grep -n "reminder_formatter import" services/scheduler/standup_reminder_job.py

# Check that _send_reminder uses formatter
grep -n "format_reminder_message" services/scheduler/standup_reminder_job.py
```

---

### Step 3: View Example Message

```bash
# View the formatted message
cat dev/active/example-reminder-message.txt

# Should see:
# 🌅 Good morning! Time for your daily standup.
#
# Generate your standup:
# • Web: https://piper-morgan.com/standup
# • CLI: `piper standup`
# • API: POST /api/v1/standup/generate
#
# Disable reminders: Reply "STOP" or update preferences
```

---

## Success Criteria

Task 3 is complete when:

- [ ] ReminderMessageFormatter class created (~150 lines)
- [ ] Timezone-aware greeting implemented
- [ ] Web link generation working
- [ ] CLI command included
- [ ] API endpoint included
- [ ] Disable instructions included
- [ ] StandupReminderJob updated to use formatter
- [ ] Test script created and passing
- [ ] Example message file created
- [ ] Code committed with evidence
- [ ] Session log updated

---

## Design Notes

### Greeting Selection

**Time-based greetings**:
- 5 AM - 12 PM: 🌅 Good morning!
- 12 PM - 5 PM: ☀️ Good afternoon!
- 5 PM - 9 PM: 🌆 Good evening!
- 9 PM - 5 AM: 🌙 Hello!

**Fallback**: 👋 Hello! (if timezone error)

---

### Link Generation

**Web**: `https://piper-morgan.com/standup`
- Configurable base URL
- Direct link to standup page

**CLI**: `piper standup`
- Simple command
- Assumes piper CLI installed

**API**: `POST /api/v1/standup/generate`
- From Issue #162 (completed)
- Matches actual endpoint

---

### Slack Formatting

**Plain text + emoji only**:
- No Markdown (Slack has its own formatting)
- Emoji for visual appeal
- Bullet points with • character
- Backticks for code (CLI command)

---

## Files to Create/Modify

### Create

- `services/integrations/slack/reminder_formatter.py` (~150 lines)
- `dev/active/test_message_formatter.py` (~150 lines)
- `dev/active/example-reminder-message.txt` (formatted message)

### Modify

- `services/scheduler/standup_reminder_job.py` (update _send_reminder method)

### Session Log

- `dev/2025/10/20/HHMM-prog-code-log.md` (continue from Tasks 1-2)

---

## Expected Timeline

**Estimated**: 30 minutes
**Likely**: 20 minutes (based on Tasks 1-2 speed!)

**Breakdown**:
- 5 min: Create ReminderMessageFormatter
- 5 min: Implement greeting logic
- 5 min: Update StandupReminderJob
- 5 min: Create and run tests

---

## Remember

**This is the simplest task yet**:
- Just message formatting
- No infrastructure needed
- Clear template to follow
- Straightforward logic

**Keep it simple**:
- Plain text + emoji
- Timezone-aware greeting
- Include all three access methods
- User-friendly instructions

---

**Ready to format beautiful messages!** 💬

*Template Version: 10.0*
*Based on Tasks 1-2 success*
*Building on completed work*
*Ready for deployment*
