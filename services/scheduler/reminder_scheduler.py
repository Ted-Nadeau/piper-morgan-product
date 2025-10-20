"""
Reminder Scheduler

Simple timer loop for daily standup reminders.
Checks every hour and delegates to StandupReminderJob.

Issue: #161 (CORE-STAND-SLACK-REMIND)
Task: 1 of 4 - Reminder Job Implementation
"""

import asyncio
from datetime import datetime
from typing import Optional

import structlog

from services.domain.user_preference_manager import UserPreferenceManager
from services.infrastructure.task_manager import RobustTaskManager
from services.integrations.slack.config_service import SlackConfigService
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
from services.scheduler.standup_reminder_job import StandupReminderJob

logger = structlog.get_logger(__name__)


class ReminderScheduler:
    """
    Scheduler for daily standup reminders.

    Uses simple asyncio.sleep() loop to check every hour.
    No external scheduler dependencies needed (no APScheduler, Celery, etc.).

    Architecture:
    - Hourly timer loop with asyncio.sleep(3600)
    - Delegates reminder logic to StandupReminderJob
    - Integrated with RobustTaskManager for reliability
    - Comprehensive error handling and logging
    """

    def __init__(
        self,
        task_manager: Optional[RobustTaskManager] = None,
        slack_router: Optional[SlackIntegrationRouter] = None,
        slack_config_service: Optional[SlackConfigService] = None,
        preference_manager: Optional[UserPreferenceManager] = None,
    ):
        """
        Initialize scheduler with dependencies.

        Args:
            task_manager: RobustTaskManager instance (creates new if None)
            slack_router: SlackIntegrationRouter instance (creates new if None)
            slack_config_service: SlackConfigService instance (creates new if None)
            preference_manager: UserPreferenceManager instance (creates new if None)
        """
        # Initialize dependencies (create if not provided)
        self.task_manager = task_manager or RobustTaskManager()

        # Create SlackConfigService if needed
        if slack_config_service is None:
            slack_config_service = SlackConfigService()

        # Create SlackIntegrationRouter with config service
        self.slack_router = slack_router or SlackIntegrationRouter(slack_config_service)

        self.preference_manager = preference_manager or UserPreferenceManager()

        # Create reminder job
        self.reminder_job = StandupReminderJob(
            self.task_manager, self.slack_router, self.preference_manager
        )

        self._running = False
        self._task: Optional[asyncio.Task] = None

    async def start(self):
        """
        Start the scheduler loop.

        Runs continuously, checking for reminders every hour.
        Uses asyncio.sleep(3600) for hourly intervals.

        Error handling:
        - Individual reminder failures logged but don't stop loop
        - Critical errors logged but loop continues
        - Graceful shutdown on stop()
        """
        if self._running:
            logger.warning("Scheduler already running, ignoring start request")
            return

        self._running = True
        logger.info("Reminder scheduler starting")

        while self._running:
            try:
                # Execute reminder check
                logger.debug("Executing hourly reminder check")

                result = await self.reminder_job.execute_daily_reminders()

                logger.info(
                    "Hourly reminder check complete",
                    checked=result.get("checked", 0),
                    sent=result.get("sent", 0),
                    failed=result.get("failed", 0),
                    errors=len(result.get("errors", [])),
                )

                # Log any errors (but don't stop loop)
                if result.get("errors"):
                    for error in result["errors"]:
                        logger.warning("Reminder error occurred", error=error)

            except Exception as e:
                logger.error(
                    "Unexpected error in reminder scheduler loop",
                    error=str(e),
                    exc_info=True,
                )

            # Sleep for 1 hour (3600 seconds) before next check
            # Break sleep into smaller chunks to allow faster shutdown
            if self._running:
                logger.debug("Sleeping for 1 hour until next check")

                # Sleep in 60-second chunks to allow responsive shutdown
                for _ in range(60):  # 60 * 60 = 3600 seconds
                    if not self._running:
                        break
                    await asyncio.sleep(60)

        logger.info("Reminder scheduler stopped")

    def stop(self):
        """
        Stop the scheduler loop.

        Sets _running flag to False, which will cause the loop to exit
        at the next iteration or sleep chunk.
        """
        if not self._running:
            logger.warning("Scheduler not running, ignoring stop request")
            return

        logger.info("Reminder scheduler stopping...")
        self._running = False

    @property
    def is_running(self) -> bool:
        """Check if scheduler is currently running."""
        return self._running


# Global scheduler instance
_scheduler: Optional[ReminderScheduler] = None
_scheduler_task: Optional[asyncio.Task] = None


async def start_reminder_scheduler(
    task_manager: Optional[RobustTaskManager] = None,
    slack_router: Optional[SlackIntegrationRouter] = None,
    slack_config_service: Optional[SlackConfigService] = None,
    preference_manager: Optional[UserPreferenceManager] = None,
) -> ReminderScheduler:
    """
    Start the global reminder scheduler.

    Creates scheduler instance if needed and starts it as background task.

    Args:
        task_manager: Optional RobustTaskManager instance
        slack_router: Optional SlackIntegrationRouter instance
        slack_config_service: Optional SlackConfigService instance
        preference_manager: Optional UserPreferenceManager instance

    Returns:
        ReminderScheduler instance
    """
    global _scheduler, _scheduler_task

    if _scheduler is None:
        logger.info("Creating reminder scheduler instance")
        _scheduler = ReminderScheduler(
            task_manager=task_manager,
            slack_router=slack_router,
            slack_config_service=slack_config_service,
            preference_manager=preference_manager,
        )

    if _scheduler_task is None or _scheduler_task.done():
        logger.info("Starting reminder scheduler background task")

        # Start scheduler in background task
        _scheduler_task = asyncio.create_task(_scheduler.start())

        logger.info("Reminder scheduler started successfully")
    else:
        logger.warning("Reminder scheduler already running")

    return _scheduler


def stop_reminder_scheduler():
    """
    Stop the global reminder scheduler.

    Stops the scheduler loop and waits for background task to complete.
    """
    global _scheduler, _scheduler_task

    if _scheduler is None:
        logger.warning("No scheduler instance to stop")
        return

    logger.info("Stopping global reminder scheduler")
    _scheduler.stop()

    # Note: Caller should await _scheduler_task if they want to wait for completion
    # We don't await here since this might be called from non-async context


async def get_scheduler_status() -> dict:
    """
    Get status of global reminder scheduler.

    Returns:
        Dict with scheduler status:
        {
            "running": bool,
            "instance_exists": bool,
            "task_exists": bool,
            "task_done": bool
        }
    """
    global _scheduler, _scheduler_task

    return {
        "running": _scheduler.is_running if _scheduler else False,
        "instance_exists": _scheduler is not None,
        "task_exists": _scheduler_task is not None,
        "task_done": _scheduler_task.done() if _scheduler_task else None,
    }
