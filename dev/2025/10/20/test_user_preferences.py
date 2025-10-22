"""
Manual Test Script: User Reminder Preferences

Tests the UserPreferenceManager reminder preference extensions.
Verifies validation, storage, and retrieval of preferences.

Issue: #161 (CORE-STAND-SLACK-REMIND)
Task: 2 of 4 - User Preference Extension
"""

import asyncio
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from services.domain.user_preference_manager import UserPreferenceManager


async def test_validation():
    """Test preference validation methods."""
    print("=" * 70)
    print("Testing Preference Validation")
    print("=" * 70)

    manager = UserPreferenceManager()

    # Test 1: Valid time format
    print("\n1. Testing time format validation...")
    try:
        manager._validate_reminder_time("06:00")
        print("   ✓ Valid time '06:00' accepted")
    except ValueError as e:
        print(f"   ✗ Valid time rejected: {e}")
        return False

    # Test 2: Invalid time format
    try:
        manager._validate_reminder_time("25:00")  # Invalid hour
        print("   ✗ Invalid time '25:00' was accepted (should reject)")
        return False
    except ValueError:
        print("   ✓ Invalid time '25:00' rejected correctly")

    # Test 3: Invalid time format string
    try:
        manager._validate_reminder_time("not-a-time")
        print("   ✗ Invalid format 'not-a-time' was accepted (should reject)")
        return False
    except ValueError:
        print("   ✓ Invalid format 'not-a-time' rejected correctly")

    # Test 4: Valid timezone
    print("\n2. Testing timezone validation...")
    try:
        manager._validate_timezone("America/Los_Angeles")
        print("   ✓ Valid timezone 'America/Los_Angeles' accepted")
    except ValueError as e:
        print(f"   ✗ Valid timezone rejected: {e}")
        return False

    # Test 5: Invalid timezone
    try:
        manager._validate_timezone("Invalid/Timezone")
        print("   ✗ Invalid timezone 'Invalid/Timezone' was accepted (should reject)")
        return False
    except ValueError:
        print("   ✓ Invalid timezone 'Invalid/Timezone' rejected correctly")

    # Test 6: Valid days list
    print("\n3. Testing days list validation...")
    try:
        manager._validate_reminder_days([0, 1, 2, 3, 4])
        print("   ✓ Valid days list [0,1,2,3,4] accepted")
    except ValueError as e:
        print(f"   ✗ Valid days list rejected: {e}")
        return False

    # Test 7: Invalid days list (out of range)
    try:
        manager._validate_reminder_days([0, 1, 7])  # 7 is invalid
        print("   ✗ Invalid days list [0,1,7] was accepted (should reject)")
        return False
    except ValueError:
        print("   ✓ Invalid days list [0,1,7] rejected correctly")

    # Test 8: Invalid days list (duplicates)
    try:
        manager._validate_reminder_days([0, 1, 1, 2])  # Duplicate 1
        print("   ✗ Days list with duplicates [0,1,1,2] was accepted (should reject)")
        return False
    except ValueError:
        print("   ✓ Days list with duplicates [0,1,1,2] rejected correctly")

    # Test 9: Invalid days list (empty)
    try:
        manager._validate_reminder_days([])
        print("   ✗ Empty days list [] was accepted (should reject)")
        return False
    except ValueError:
        print("   ✓ Empty days list [] rejected correctly")

    print("\n" + "=" * 70)
    print("✓ All validation tests passed!")
    print("=" * 70)
    return True


async def test_preference_storage():
    """Test preference storage and retrieval."""
    print("\n" + "=" * 70)
    print("Testing Preference Storage and Retrieval")
    print("=" * 70)

    manager = UserPreferenceManager()
    test_user_id = "U12345TEST"

    # Test 1: Get default values (no preferences set)
    print("\n1. Testing default values...")
    prefs = await manager.get_reminder_preferences(test_user_id)
    print(f"   - Enabled: {prefs['enabled']}")
    print(f"   - Time: {prefs['time']}")
    print(f"   - Timezone: {prefs['timezone']}")
    print(f"   - Days: {prefs['days']}")

    if prefs["enabled"] != True:
        print("   ✗ Default enabled should be True")
        return False
    if prefs["time"] != "06:00":
        print("   ✗ Default time should be '06:00'")
        return False
    if prefs["timezone"] != "America/Los_Angeles":
        print("   ✗ Default timezone should be 'America/Los_Angeles'")
        return False
    if prefs["days"] != [0, 1, 2, 3, 4]:
        print("   ✗ Default days should be [0,1,2,3,4]")
        return False
    print("   ✓ All default values correct")

    # Test 2: Set individual preferences
    print("\n2. Setting custom preferences...")
    try:
        await manager.set_reminder_enabled(test_user_id, False)
        await manager.set_reminder_time(test_user_id, "08:30")
        await manager.set_reminder_timezone(test_user_id, "America/New_York")
        await manager.set_reminder_days(test_user_id, [1, 2, 3])  # Tue-Thu
        print("   ✓ All preferences set successfully")
    except Exception as e:
        print(f"   ✗ Failed to set preferences: {e}")
        return False

    # Test 3: Retrieve individual preferences
    print("\n3. Retrieving individual preferences...")
    enabled = await manager.get_reminder_enabled(test_user_id)
    time = await manager.get_reminder_time(test_user_id)
    timezone = await manager.get_reminder_timezone(test_user_id)
    days = await manager.get_reminder_days(test_user_id)

    print(f"   - Enabled: {enabled}")
    print(f"   - Time: {time}")
    print(f"   - Timezone: {timezone}")
    print(f"   - Days: {days}")

    if enabled != False:
        print("   ✗ Enabled should be False")
        return False
    if time != "08:30":
        print("   ✗ Time should be '08:30'")
        return False
    if timezone != "America/New_York":
        print("   ✗ Timezone should be 'America/New_York'")
        return False
    if days != [1, 2, 3]:
        print("   ✗ Days should be [1,2,3]")
        return False
    print("   ✓ All retrieved values correct")

    # Test 4: Get all preferences at once
    print("\n4. Retrieving all preferences with get_reminder_preferences()...")
    all_prefs = await manager.get_reminder_preferences(test_user_id)
    print(f"   - Enabled: {all_prefs['enabled']}")
    print(f"   - Time: {all_prefs['time']}")
    print(f"   - Timezone: {all_prefs['timezone']}")
    print(f"   - Days: {all_prefs['days']}")

    if (
        all_prefs["enabled"] != False
        or all_prefs["time"] != "08:30"
        or all_prefs["timezone"] != "America/New_York"
        or all_prefs["days"] != [1, 2, 3]
    ):
        print("   ✗ get_reminder_preferences() returned incorrect values")
        return False
    print("   ✓ get_reminder_preferences() works correctly")

    # Test 5: Test validation on set (should reject invalid values)
    print("\n5. Testing validation on set...")
    try:
        await manager.set_reminder_time(test_user_id, "invalid")
        print("   ✗ Invalid time 'invalid' was accepted")
        return False
    except ValueError:
        print("   ✓ Invalid time rejected by set_reminder_time()")

    try:
        await manager.set_reminder_timezone(test_user_id, "Not/A/Timezone")
        print("   ✗ Invalid timezone was accepted")
        return False
    except ValueError:
        print("   ✓ Invalid timezone rejected by set_reminder_timezone()")

    try:
        await manager.set_reminder_days(test_user_id, [0, 8])
        print("   ✗ Invalid days [0,8] was accepted")
        return False
    except ValueError:
        print("   ✓ Invalid days rejected by set_reminder_days()")

    print("\n" + "=" * 70)
    print("✓ All storage/retrieval tests passed!")
    print("=" * 70)
    return True


async def test_standup_reminder_job_integration():
    """Test that StandupReminderJob uses the real preferences."""
    print("\n" + "=" * 70)
    print("Testing StandupReminderJob Integration")
    print("=" * 70)

    from services.infrastructure.task_manager import RobustTaskManager
    from services.integrations.slack.config_service import SlackConfigService
    from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
    from services.scheduler.standup_reminder_job import StandupReminderJob

    # Create dependencies
    task_manager = RobustTaskManager()
    slack_config_service = SlackConfigService()
    slack_router = SlackIntegrationRouter(slack_config_service)
    preference_manager = UserPreferenceManager()

    # Create job
    job = StandupReminderJob(task_manager, slack_router, preference_manager)

    # Set custom preferences for test user
    test_user_id = "U67890TEST"
    print("\n1. Setting custom preferences for test user...")
    await preference_manager.set_reminder_enabled(test_user_id, True)
    await preference_manager.set_reminder_time(test_user_id, "09:15")
    await preference_manager.set_reminder_timezone(test_user_id, "Europe/London")
    await preference_manager.set_reminder_days(test_user_id, [0, 2, 4])  # Mon, Wed, Fri
    print("   ✓ Preferences set")

    # Get preferences through the job (tests the integration)
    print("\n2. Retrieving preferences through StandupReminderJob...")
    prefs = await job._get_user_reminder_preferences(test_user_id)
    print(f"   - Enabled: {prefs['enabled']}")
    print(f"   - Time: {prefs['time']}")
    print(f"   - Timezone: {prefs['timezone']}")
    print(f"   - Days: {prefs['days']}")

    if (
        prefs["enabled"] != True
        or prefs["time"] != "09:15"
        or prefs["timezone"] != "Europe/London"
        or prefs["days"] != [0, 2, 4]
    ):
        print("   ✗ StandupReminderJob not using real preferences correctly")
        return False

    print("   ✓ StandupReminderJob correctly retrieves real preferences")

    print("\n" + "=" * 70)
    print("✓ Integration test passed!")
    print("=" * 70)
    return True


if __name__ == "__main__":
    print("\n🧪 User Preference Manager Tests\n")

    async def run_all_tests():
        # Test 1: Validation
        success1 = await test_validation()
        if not success1:
            return False

        # Test 2: Storage and retrieval
        success2 = await test_preference_storage()
        if not success2:
            return False

        # Test 3: Integration with StandupReminderJob
        success3 = await test_standup_reminder_job_integration()
        if not success3:
            return False

        return True

    success = asyncio.run(run_all_tests())

    if success:
        print("\n✅ All preference tests passed!")
        print("\nTask 2 Implementation Complete:")
        print("- 4 preference key constants added")
        print("- 3 validation methods implemented")
        print("- 8 helper methods added (get/set for each)")
        print("- 1 convenience method for fetching all preferences")
        print("- StandupReminderJob updated to use real preferences")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
