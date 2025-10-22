# Task 1: Reminder Job Implementation - Slack Standup Reminders

**Agent**: Claude Code (Programmer)
**Issue**: #161 (CORE-STAND-SLACK-REMIND)
**Task**: 1 of 4 - Reminder Job Implementation
**Sprint**: A4 "Standup Epic"
**Date**: October 20, 2025, 7:47 AM
**Estimated Effort**: 1 hour

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. ⏸️ **STOP** - Do not continue working
2. 📋 **REPORT** - Summarize what was just completed
3. ❓ **ASK** - "Should I proceed to next task?"
4. ⏳ **WAIT** - For explicit instructions

**DO NOT**:
- ❌ Read old context files to self-direct
- ❌ Assume you should continue
- ❌ Start working on next task without authorization

---

## Mission

Implement the core reminder job system that checks user preferences and sends daily standup reminders via Slack. This is the orchestration layer that coordinates between user preferences, message formatting, and Slack delivery.

**Scope**:
- Create StandupReminderJob class
- Implement daily timer loop
- Query user preferences for enabled users
- Send reminders via existing SlackClient
- Integrate with RobustTaskManager

**NOT in scope**:
- User preference storage (Task 2)
- Message formatting details (Task 3)
- Full integration testing (Task 4)

---

## Context from Discovery

**EXCELLENT NEWS**: 95% of infrastructure already exists!

**What we're building on**:
- ✅ RobustTaskManager (327 lines) - Error handling, retry logic
- ✅ SlackClient (256 lines) - DM sending capability
- ✅ UserPreferenceManager (449 lines) - Preference storage
- ✅ Standup API (#162) - Link generation ready

**Architecture** (from discovery):
```
Timer Loop → StandupReminderJob → UserPreferences → SlackClient
```

**This task**: Build the StandupReminderJob and timer loop

---

## Architecture Document

**YOU HAVE**: `phase-3-discovery-architecture.md` uploaded by PM

**READ IT FIRST** before implementing anything!

Key sections to focus on:
- "Component Overview" - Your place in the system
- "Task 1: Reminder Job Implementation" - Your specific work
- "Design Decisions" - Why we chose this approach

---

## STOP Conditions

If ANY of these occur, STOP and escalate to PM immediately:

1. **Cannot find RobustTaskManager** - Discovery said it exists at `services/infrastructure/task_manager.py`
2. **Cannot find SlackClient** - Should be at `services/integrations/slack/slack_client.py`
3. **Cannot find UserPreferenceManager** - Should be at `services/domain/user_preference_manager.py`
4. **Timer loop approach unclear** - Simple asyncio.sleep(3600) pattern
5. **Method signatures don't match discovery** - Check discovery doc
6. **User preference keys not defined** - Wait for Task 2
7. **Need to modify existing infrastructure** - Should only create new files
8. **Timezone handling too complex** - Use Python zoneinfo standard library
9. **Any infrastructure assumptions needed** - Discovery verified everything
10. **Can't provide verification evidence** - Must show working code

**Remember**: STOP means STOP. Don't try to work around it. Ask PM.

---

## Evidence Requirements

### For EVERY Claim You Make:

- **"Timer loop works"** → Show output of running loop
- **"Queries user preferences"** → Show code calling UserPreferenceManager
- **"Sends Slack DMs"** → Show code calling SlackClient.send_message()
- **"Timezone handling works"** → Show timezone conversion code
- **"Integrated with RobustTaskManager"** → Show wrapper code

### Working Files Location:

**NEVER use /tmp for important files**:
- ❌ /tmp - Can be lost between sessions
- ✅ dev/active/ - For working files, evidence
- ✅ services/scheduler/ - For reminder job code
- ✅ outputs/ - For final reports

---

## Task Requirements

### 1. Review Discovery Architecture

**FIRST**: Read the discovery document uploaded by PM

```bash
# PM uploaded: phase-3-discovery-architecture.md
# Read it thoroughly before coding
cat phase-3-discovery-architecture.md
```

**Focus on**:
- Component Overview (your role)
- Task 1 implementation details
- Integration points
- Design decisions

---

### 2. Verify Infrastructure

**Check that everything from discovery exists**:

```bash
# Verify RobustTaskManager
ls -la services/infrastructure/task_manager.py
grep -n "class RobustTaskManager" services/infrastructure/task_manager.py

# Verify SlackClient
ls -la services/integrations/slack/slack_client.py
grep -n "class SlackClient" services/integrations/slack/slack_client.py
grep -n "def send_message" services/integrations/slack/slack_client.py

# Verify UserPreferenceManager
ls -la services/domain/user_preference_manager.py
grep -n "class UserPreferenceManager" services/domain/user_preference_manager.py
```

**If ANY not found**: STOP (condition #1, #2, or #3)

---

### 3. Create StandupReminderJob Class

**File**: `services/scheduler/standup_reminder_job.py`

**Structure**:

```python
"""
Standup Reminder Job

Sends daily Slack reminders for standup generation.
Queries user preferences, checks timezone/time, and sends DMs via SlackClient.
"""

import asyncio
from datetime import datetime, time
from zoneinfo import ZoneInfo
from typing import List, Dict, Any
import structlog

from services.infrastructure.task_manager import RobustTaskManager
from services.integrations.slack.slack_client import SlackClient
from services.domain.user_preference_manager import UserPreferenceManager

logger = structlog.get_logger()


class StandupReminderJob:
    """
    Daily standup reminder job.

    Responsibilities:
    - Query users with reminders enabled
    - Check if it's reminder time for each user
    - Send Slack DMs via SlackClient
    - Log results for monitoring
    """

    def __init__(
        self,
        task_manager: RobustTaskManager,
        slack_client: SlackClient,
        preference_manager: UserPreferenceManager
    ):
        self.task_manager = task_manager
        self.slack_client = slack_client
        self.preference_manager = preference_manager

    async def execute_daily_reminders(self) -> Dict[str, Any]:
        """
        Execute daily reminder check and send.

        Returns:
            Dict with results: {
                "checked": int,
                "sent": int,
                "failed": int,
                "errors": List[str]
            }
        """
        # Implementation here
        pass

    async def _get_enabled_users(self) -> List[str]:
        """Get list of user IDs with reminders enabled."""
        pass

    async def _should_send_reminder(self, user_id: str) -> bool:
        """Check if reminder should be sent for user based on time/timezone."""
        pass

    async def _send_reminder(self, user_id: str) -> bool:
        """Send reminder DM to user. Returns True if successful."""
        pass
```

**Implementation requirements**:

1. **Query enabled users**:
   ```python
   # Get all users with reminder_enabled = True
   enabled_users = await self._get_enabled_users()
   ```

2. **Check timezone and time**:
   ```python
   # For each user, check if it's their reminder time
   user_time = get_user_preference("reminder_time")  # e.g. "06:00"
   user_tz = get_user_preference("reminder_timezone")  # e.g. "America/Los_Angeles"
   user_days = get_user_preference("reminder_days")  # e.g. [0,1,2,3,4] (Mon-Fri)

   # Convert to user's timezone
   user_now = datetime.now(ZoneInfo(user_tz))

   # Check if current time matches reminder time
   if user_now.hour == reminder_hour and user_now.minute == reminder_minute:
       # Check if today is a reminder day
       if user_now.weekday() in user_days:
           return True
   ```

3. **Send via SlackClient**:
   ```python
   # Use existing SlackClient.send_message()
   # For now, use placeholder message (Task 3 will add formatter)
   message = "🌅 Good morning! Time for your daily standup."

   success = await self.slack_client.send_message(
       channel=user_id,  # User ID as channel = DM
       text=message
   )
   ```

4. **Wrap with RobustTaskManager**:
   ```python
   # Use task manager for error handling and tracking
   result = await self.task_manager.execute_with_tracking(
       self.execute_daily_reminders,
       "daily_standup_reminders"
   )
   ```

---

### 4. Create Daily Timer Loop

**File**: `services/scheduler/reminder_scheduler.py`

**Structure**:

```python
"""
Reminder Scheduler

Simple timer loop for daily standup reminders.
Checks every hour and delegates to StandupReminderJob.
"""

import asyncio
from datetime import datetime
import structlog

from services.scheduler.standup_reminder_job import StandupReminderJob
from services.infrastructure.task_manager import RobustTaskManager
from services.integrations.slack.slack_client import SlackClient
from services.domain.user_preference_manager import UserPreferenceManager

logger = structlog.get_logger()


class ReminderScheduler:
    """
    Scheduler for daily reminders.

    Uses simple asyncio.sleep() loop to check every hour.
    No external scheduler dependencies needed.
    """

    def __init__(self):
        # Initialize dependencies
        self.task_manager = RobustTaskManager()
        self.slack_client = SlackClient()
        self.preference_manager = UserPreferenceManager()

        # Create reminder job
        self.reminder_job = StandupReminderJob(
            self.task_manager,
            self.slack_client,
            self.preference_manager
        )

        self._running = False

    async def start(self):
        """Start the scheduler loop."""
        self._running = True

        logger.info("Reminder scheduler starting")

        while self._running:
            try:
                # Execute reminders
                result = await self.reminder_job.execute_daily_reminders()

                logger.info(
                    "Daily reminder check complete",
                    checked=result.get("checked", 0),
                    sent=result.get("sent", 0),
                    failed=result.get("failed", 0)
                )

            except Exception as e:
                logger.error(
                    "Error in reminder scheduler",
                    error=str(e)
                )

            # Sleep for 1 hour (3600 seconds)
            await asyncio.sleep(3600)

    def stop(self):
        """Stop the scheduler loop."""
        self._running = False
        logger.info("Reminder scheduler stopping")


# Global scheduler instance
_scheduler = None


async def start_reminder_scheduler():
    """Start the global reminder scheduler."""
    global _scheduler

    if _scheduler is None:
        _scheduler = ReminderScheduler()

    # Start in background task
    asyncio.create_task(_scheduler.start())

    logger.info("Reminder scheduler started")


def stop_reminder_scheduler():
    """Stop the global reminder scheduler."""
    global _scheduler

    if _scheduler:
        _scheduler.stop()
```

**Key requirements**:
- Simple `asyncio.sleep(3600)` loop (check every hour)
- Error handling for failed executions
- Logging for monitoring
- Start/stop functions for main app integration

---

### 5. Create Directory Structure

**Ensure scheduler directory exists**:

```bash
# Create scheduler directory if needed
mkdir -p services/scheduler

# Create __init__.py
touch services/scheduler/__init__.py

# Create placeholder for tests
mkdir -p tests/services/scheduler
touch tests/services/scheduler/__init__.py
```

---

## Verification Steps

### Step 1: Verify Infrastructure

```python
# Test imports work
python3 -c "
from services.infrastructure.task_manager import RobustTaskManager
from services.integrations.slack.slack_client import SlackClient
from services.domain.user_preference_manager import UserPreferenceManager
print('All imports successful!')
"
```

**Expected**: No import errors

---

### Step 2: Test Reminder Job (Manual)

```python
# Create test script: dev/active/test_reminder_job.py
import asyncio
from services.scheduler.standup_reminder_job import StandupReminderJob
from services.infrastructure.task_manager import RobustTaskManager
from services.integrations.slack.slack_client import SlackClient
from services.domain.user_preference_manager import UserPreferenceManager

async def test_reminder_job():
    # Create dependencies
    task_manager = RobustTaskManager()
    slack_client = SlackClient()
    preference_manager = UserPreferenceManager()

    # Create job
    job = StandupReminderJob(task_manager, slack_client, preference_manager)

    # Execute
    result = await job.execute_daily_reminders()

    print(f"Result: {result}")

# Run test
asyncio.run(test_reminder_job())
```

**Expected**: Job executes without errors (may send 0 reminders if no users enabled)

---

### Step 3: Test Scheduler Loop (Short Run)

```python
# Create test script: dev/active/test_scheduler_loop.py
import asyncio
from services.scheduler.reminder_scheduler import ReminderScheduler

async def test_scheduler():
    scheduler = ReminderScheduler()

    # Start scheduler
    task = asyncio.create_task(scheduler.start())

    # Let it run for 10 seconds
    await asyncio.sleep(10)

    # Stop scheduler
    scheduler.stop()

    print("Scheduler test complete")

# Run test
asyncio.run(test_scheduler())
```

**Expected**: Scheduler starts, runs one check, stops cleanly

---

### Step 4: Verify File Structure

```bash
# Check files created
ls -la services/scheduler/

# Should see:
# __init__.py
# standup_reminder_job.py
# reminder_scheduler.py

# Verify they have content
wc -l services/scheduler/*.py
```

**Expected**: All files present with reasonable line counts

---

## Success Criteria

Task 1 is complete when:

- [ ] `services/scheduler/` directory created
- [ ] `standup_reminder_job.py` implemented (~150 lines)
- [ ] `reminder_scheduler.py` implemented (~100 lines)
- [ ] StandupReminderJob class functional
- [ ] Timer loop works with asyncio.sleep()
- [ ] Queries user preferences (using placeholder keys for now)
- [ ] Sends DMs via SlackClient (placeholder message)
- [ ] Integrated with RobustTaskManager
- [ ] Timezone handling works (using zoneinfo)
- [ ] Manual tests pass
- [ ] Code committed with evidence
- [ ] Session log updated

---

## Implementation Notes

### Timezone Handling

**Use Python standard library**:

```python
from datetime import datetime
from zoneinfo import ZoneInfo

# Get current time in user's timezone
user_tz = "America/Los_Angeles"
user_now = datetime.now(ZoneInfo(user_tz))

# Check if it's 6 AM
if user_now.hour == 6 and user_now.minute == 0:
    # Send reminder
    pass
```

**No need for pytz** - zoneinfo is built-in (Python 3.9+)

---

### User Preference Placeholder

**For Task 1**, use placeholder preference keys:

```python
# These will be properly implemented in Task 2
# For now, assume they exist or use defaults

def get_user_reminder_preferences(user_id: str) -> dict:
    """Placeholder - Task 2 will implement properly."""
    return {
        "enabled": True,  # Assume enabled for testing
        "time": "06:00",
        "timezone": "America/Los_Angeles",
        "days": [0, 1, 2, 3, 4]  # Mon-Fri
    }
```

**Task 2 will connect to actual UserPreferenceManager**.

---

### Message Placeholder

**For Task 1**, use simple placeholder message:

```python
message = "🌅 Good morning! Time for your daily standup."
```

**Task 3 will implement full ReminderMessageFormatter**.

---

## Files to Create

### Primary Files

- `services/scheduler/__init__.py` - Package init
- `services/scheduler/standup_reminder_job.py` - Reminder job class (~150 lines)
- `services/scheduler/reminder_scheduler.py` - Timer loop (~100 lines)

### Test Files (Manual for now)

- `dev/active/test_reminder_job.py` - Manual test script
- `dev/active/test_scheduler_loop.py` - Manual test script

### Session Log

- `dev/2025/10/20/HHMM-prog-code-log.md` - Your session log

---

## Deliverables

### 1. Reminder Job Implementation

**File**: `services/scheduler/standup_reminder_job.py`

**Should include**:
- StandupReminderJob class
- Methods: execute_daily_reminders, _get_enabled_users, _should_send_reminder, _send_reminder
- Integration with RobustTaskManager
- Timezone handling with zoneinfo
- Comprehensive logging
- Error handling

---

### 2. Scheduler Loop

**File**: `services/scheduler/reminder_scheduler.py`

**Should include**:
- ReminderScheduler class
- Simple asyncio.sleep(3600) loop
- Start/stop functions
- Global scheduler instance
- Error handling
- Logging

---

### 3. Test Evidence

**Files in dev/active/**:
- Test scripts for manual verification
- Output logs showing successful execution
- Evidence of timer loop working

---

### 4. Session Log

**In dev/2025/10/20/HHMM-prog-code-log.md**:
- Implementation approach
- Design decisions
- Any challenges and solutions
- Test results
- Time spent

---

## Remember

**You are building on excellent infrastructure**:
- RobustTaskManager handles errors
- SlackClient handles DMs and rate limiting
- UserPreferenceManager handles storage

**Your job is simple**:
1. Query preferences
2. Check time/timezone
3. Send via SlackClient
4. Wrap with RobustTaskManager

**Keep it simple** - we're orchestrating existing components, not reinventing them!

---

## Next Tasks Preview

**After Task 1 completion**:
- Task 2: Extend UserPreferenceManager with reminder keys
- Task 3: Create ReminderMessageFormatter with links
- Task 4: Integration, unit tests, and verification

**Don't jump ahead** - stick to Task 1 scope only!

---

*Template Version: 10.0*
*Based on: agent-prompt-template.md*
*Discovery-informed implementation*
*All infrastructure verified*
*Ready for deployment*
