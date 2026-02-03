"""
Key Rotation Reminder Service

Tracks API key age and generates rotation reminders based on policy.
Integrates with status checker and provides proactive notifications.

Issue #250 CORE-KEYS-ROTATION-REMINDERS
"""

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional
from uuid import UUID

import yaml
from sqlalchemy.ext.asyncio import AsyncSession

from services.security.user_api_key_service import UserAPIKeyService

logger = logging.getLogger(__name__)


@dataclass
class RotationReminder:
    """Represents a key rotation reminder"""

    provider: str
    age_days: int
    severity: str  # 'info', 'warning', 'critical'
    message: str
    max_age_days: int
    user_id: str
    key_id: int


@dataclass
class RotationPolicy:
    """Rotation policy for a provider"""

    max_age_days: int
    warning_days: List[int]
    critical_days: int


class KeyRotationReminder:
    """Service for managing key rotation reminders"""

    def __init__(self, user_api_key_service: Optional[UserAPIKeyService] = None):
        """Initialize rotation reminder service"""
        self._user_service = user_api_key_service or UserAPIKeyService()
        self._policies = self._load_policies()

    def _load_policies(self) -> Dict[str, RotationPolicy]:
        """Load rotation policies from configuration"""
        try:
            config_path = Path("config/rotation_policy.yaml")
            if not config_path.exists():
                logger.warning("Rotation policy config not found, using defaults")
                return self._get_default_policies()

            with open(config_path, "r") as f:
                config = yaml.safe_load(f)

            policies = {}

            # Load default policy
            default_config = config["rotation_policies"]["default"]
            default_policy = RotationPolicy(
                max_age_days=default_config["max_age_days"],
                warning_days=default_config["warning_days"],
                critical_days=default_config["critical_days"],
            )
            policies["default"] = default_policy

            # Load provider overrides
            if "provider_overrides" in config["rotation_policies"]:
                for provider, override_config in config["rotation_policies"][
                    "provider_overrides"
                ].items():
                    policies[provider] = RotationPolicy(
                        max_age_days=override_config["max_age_days"],
                        warning_days=override_config["warning_days"],
                        critical_days=override_config["critical_days"],
                    )

            logger.info(f"Loaded rotation policies for {len(policies)} providers")
            return policies

        except Exception as e:
            logger.error(f"Failed to load rotation policies: {e}")
            return self._get_default_policies()

    def _get_default_policies(self) -> Dict[str, RotationPolicy]:
        """Get default rotation policies"""
        return {
            "default": RotationPolicy(max_age_days=90, warning_days=[60, 75, 85], critical_days=88)
        }

    def _get_policy(self, provider: str) -> RotationPolicy:
        """Get rotation policy for provider"""
        return self._policies.get(provider, self._policies["default"])

    def _calculate_key_age(self, key) -> int:
        """Calculate key age in days"""
        # Use rotated_at if available, otherwise created_at
        # Note: key is a dict from list_user_keys(), with ISO format timestamps
        rotated_str = key.get("rotated_at")
        created_str = key["created_at"]

        # Parse ISO format timestamps
        from datetime import datetime, timezone

        if rotated_str:
            last_update = datetime.fromisoformat(rotated_str)
        else:
            last_update = datetime.fromisoformat(created_str)

        return (datetime.now(timezone.utc) - last_update).days

    async def check_key_ages(self, session: AsyncSession, user_id: str) -> List[RotationReminder]:
        """Check all user keys and generate reminders"""
        try:
            # Get all user keys
            keys = await self._user_service.list_user_keys(session, user_id)
            reminders = []

            for key in keys:
                if not key["is_active"]:
                    continue  # Skip inactive keys

                age_days = self._calculate_key_age(key)
                policy = self._get_policy(key["provider"])

                # Check if reminder is needed
                reminder = self._evaluate_key_age(key, age_days, policy, user_id)
                if reminder:
                    reminders.append(reminder)

            logger.info(f"Generated {len(reminders)} rotation reminders for user {user_id}")
            return reminders

        except Exception as e:
            logger.error(f"Failed to check key ages for user {user_id}: {e}")
            return []

    def _evaluate_key_age(
        self, key, age_days: int, policy: RotationPolicy, user_id: str
    ) -> Optional[RotationReminder]:
        """Evaluate if key needs rotation reminder"""

        # Critical reminder
        if age_days >= policy.critical_days:
            return RotationReminder(
                provider=key["provider"],
                age_days=age_days,
                severity="critical",
                message=f"Your {key['provider']} key is {age_days} days old. Rotate immediately!",
                max_age_days=policy.max_age_days,
                user_id=user_id,
                key_id=key["id"],
            )

        # Warning reminders
        if age_days in policy.warning_days:
            return RotationReminder(
                provider=key["provider"],
                age_days=age_days,
                severity="warning",
                message=f"Your {key['provider']} key is {age_days} days old. Consider rotating soon.",
                max_age_days=policy.max_age_days,
                user_id=user_id,
                key_id=key["id"],
            )

        # Info reminder (approaching first warning)
        if policy.warning_days and age_days >= (policy.warning_days[0] - 7):
            return RotationReminder(
                provider=key["provider"],
                age_days=age_days,
                severity="info",
                message=f"Your {key['provider']} key is {age_days} days old. Rotation recommended in {policy.warning_days[0] - age_days} days.",
                max_age_days=policy.max_age_days,
                user_id=user_id,
                key_id=key["id"],
            )

        return None

    def format_reminder_for_status(self, reminders: List[RotationReminder]) -> Dict[str, str]:
        """Format reminders for status checker display"""
        if not reminders:
            return {}

        formatted = {}
        for reminder in reminders:
            if reminder.severity == "critical":
                status_icon = "✗"
            elif reminder.severity == "warning":
                status_icon = "⚠"
            else:
                status_icon = "ℹ"

            formatted[reminder.provider] = f"{status_icon} {reminder.message}"

        return formatted

    async def get_rotation_recommendations(self, session: AsyncSession, user_id: str) -> List[str]:
        """Get rotation recommendations for status checker"""
        reminders = await self.check_key_ages(session, user_id)

        recommendations = []
        for reminder in reminders:
            if reminder.severity == "critical":
                recommendations.append(
                    f"  • Rotate {reminder.provider} key immediately (age: {reminder.age_days} days)"
                )
            elif reminder.severity == "warning":
                recommendations.append(
                    f"  • Consider rotating {reminder.provider} key soon (age: {reminder.age_days} days)"
                )

        return recommendations
