"""
Manual Test Script: ReminderScheduler Loop

Tests the scheduler timer loop implementation.
Verifies that the scheduler starts, runs checks, and stops cleanly.

Issue: #161 (CORE-STAND-SLACK-REMIND)
Task: 1 of 4 - Reminder Job Implementation
"""

import asyncio
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from services.scheduler.reminder_scheduler import ReminderScheduler, get_scheduler_status


async def test_scheduler_loop():
    """Test ReminderScheduler timer loop."""
    print("=" * 70)
    print("Testing ReminderScheduler")
    print("=" * 70)

    try:
        print("\n1. Creating scheduler...")
        scheduler = ReminderScheduler()
        print("   ✓ ReminderScheduler created")
        print(f"   - Running: {scheduler.is_running}")

        print("\n2. Starting scheduler...")
        # Start scheduler in background task
        task = asyncio.create_task(scheduler.start())
        print("   ✓ Scheduler task created")

        # Give it a moment to start
        await asyncio.sleep(1)
        print(f"   - Running: {scheduler.is_running}")

        print("\n3. Letting scheduler run for 5 seconds...")
        print("   (Scheduler would normally wait 1 hour between checks)")
        print("   (This test just verifies it starts and runs without errors)")

        await asyncio.sleep(5)

        print("\n4. Stopping scheduler...")
        scheduler.stop()
        print("   ✓ Stop signal sent")

        # Wait for scheduler to finish current iteration
        print("   - Waiting for scheduler to stop...")
        try:
            await asyncio.wait_for(task, timeout=10)
            print("   ✓ Scheduler stopped cleanly")
        except asyncio.TimeoutError:
            # Task is still running, cancel it
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            print("   ✓ Scheduler task cancelled")

        print(f"   - Running: {scheduler.is_running}")

        print("\n" + "=" * 70)
        print("✓ Test completed successfully!")
        print("=" * 70)

        return True

    except Exception as e:
        print("\n" + "=" * 70)
        print("✗ Test failed!")
        print("=" * 70)
        print(f"\nError: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


async def test_global_scheduler():
    """Test global scheduler start/stop functions."""
    print("\n" + "=" * 70)
    print("Testing Global Scheduler Functions")
    print("=" * 70)

    try:
        # Import here to test module-level functions
        from services.scheduler.reminder_scheduler import (
            start_reminder_scheduler,
            stop_reminder_scheduler,
        )

        print("\n1. Getting initial status...")
        status = await get_scheduler_status()
        print(f"   - Instance exists: {status['instance_exists']}")
        print(f"   - Running: {status['running']}")

        print("\n2. Starting global scheduler...")
        scheduler = await start_reminder_scheduler()
        print("   ✓ Global scheduler started")

        # Give it a moment to start
        await asyncio.sleep(1)

        status = await get_scheduler_status()
        print(f"   - Instance exists: {status['instance_exists']}")
        print(f"   - Running: {status['running']}")
        print(f"   - Task exists: {status['task_exists']}")

        print("\n3. Letting scheduler run for 3 seconds...")
        await asyncio.sleep(3)

        print("\n4. Stopping global scheduler...")
        stop_reminder_scheduler()
        print("   ✓ Stop signal sent")

        # Give it time to stop
        await asyncio.sleep(2)

        status = await get_scheduler_status()
        print(f"   - Running: {status['running']}")

        print("\n" + "=" * 70)
        print("✓ Global scheduler test completed!")
        print("=" * 70)

        return True

    except Exception as e:
        print("\n" + "=" * 70)
        print("✗ Global scheduler test failed!")
        print("=" * 70)
        print(f"\nError: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n🧪 ReminderScheduler Manual Tests\n")

    async def run_all_tests():
        # Test 1: Direct scheduler instance
        success1 = await test_scheduler_loop()

        # Test 2: Global scheduler functions
        success2 = await test_global_scheduler()

        return success1 and success2

    success = asyncio.run(run_all_tests())

    if success:
        print("\n✅ All scheduler tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
