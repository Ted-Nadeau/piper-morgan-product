"""
Budget Management Service

Manages user budgets, spending alerts, and cost controls for API usage.
Provides proactive notifications and spending recommendations.

Issue #253 CORE-KEYS-COST-ANALYTICS
"""

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class BudgetType(Enum):
    """Budget period types"""

    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class AlertSeverity(Enum):
    """Budget alert severity levels"""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class Budget:
    """User budget configuration"""

    user_id: UUID
    budget_type: BudgetType
    amount: Decimal
    provider: Optional[str] = None  # None = all providers
    alert_thresholds: List[float] = None  # [0.5, 0.75, 0.9, 1.0]
    created_at: Optional[datetime] = None
    is_active: bool = True

    def __post_init__(self):
        if self.alert_thresholds is None:
            self.alert_thresholds = [0.5, 0.75, 0.9, 1.0]
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)


@dataclass
class BudgetStatus:
    """Current budget status and usage"""

    budget: Budget
    current_spending: Decimal
    percentage_used: float
    remaining_amount: Decimal
    days_remaining: int
    projected_spending: Decimal
    alerts_triggered: List[Dict[str, Any]]
    recommendations: List[str]


@dataclass
class BudgetAlert:
    """Budget alert notification"""

    user_id: UUID
    budget_id: str
    threshold: float
    current_percentage: float
    severity: AlertSeverity
    message: str
    triggered_at: datetime
    acknowledged: bool = False


class BudgetManager:
    """Manages user budgets and spending alerts"""

    def __init__(self):
        """Initialize budget manager"""
        self.default_thresholds = [0.5, 0.75, 0.9, 1.0]  # 50%, 75%, 90%, 100%

    async def set_budget(
        self,
        session: AsyncSession,
        user_id: UUID,
        budget_type: BudgetType,
        amount: Decimal,
        provider: Optional[str] = None,
        alert_thresholds: Optional[List[float]] = None,
    ) -> Budget:
        """
        Set or update user budget

        Args:
            session: Database session
            user_id: User ID
            budget_type: Budget period (daily, weekly, monthly, yearly)
            amount: Budget amount in USD
            provider: Optional provider filter (None = all providers)
            alert_thresholds: Custom alert thresholds (0.0-1.0)

        Returns:
            Created/updated Budget object
        """
        try:
            budget = Budget(
                user_id=user_id,
                budget_type=budget_type,
                amount=amount,
                provider=provider,
                alert_thresholds=alert_thresholds or self.default_thresholds,
            )

            # TODO: Store in database
            await self._store_budget(session, budget)

            logger.info(f"Set {budget_type.value} budget of ${amount} for user {user_id}")
            return budget

        except Exception as e:
            logger.error(f"Failed to set budget: {e}")
            raise

    async def get_budget_status(
        self,
        session: AsyncSession,
        user_id: UUID,
        budget_type: BudgetType,
        provider: Optional[str] = None,
    ) -> Optional[BudgetStatus]:
        """
        Get current budget status for user

        Args:
            session: Database session
            user_id: User ID
            budget_type: Budget period to check
            provider: Optional provider filter

        Returns:
            BudgetStatus or None if no budget set
        """
        try:
            # Get budget configuration
            budget = await self._get_budget(session, user_id, budget_type, provider)
            if not budget:
                return None

            # Get current spending for the period
            current_spending = await self._get_current_spending(
                session, user_id, budget_type, provider
            )

            # Calculate status
            percentage_used = (
                float((current_spending / budget.amount) * 100) if budget.amount > 0 else 0
            )
            remaining_amount = budget.amount - current_spending

            # Calculate days remaining in period
            days_remaining = self._get_days_remaining_in_period(budget_type)

            # Project spending to end of period
            days_elapsed = self._get_days_elapsed_in_period(budget_type)
            if days_elapsed > 0:
                daily_rate = current_spending / days_elapsed
                projected_spending = daily_rate * (days_elapsed + days_remaining)
            else:
                projected_spending = current_spending

            # Check for triggered alerts
            alerts_triggered = self._check_alert_thresholds(budget, percentage_used / 100)

            # Generate recommendations
            recommendations = self._generate_budget_recommendations(
                budget, current_spending, projected_spending, days_remaining
            )

            return BudgetStatus(
                budget=budget,
                current_spending=current_spending,
                percentage_used=percentage_used,
                remaining_amount=remaining_amount,
                days_remaining=days_remaining,
                projected_spending=projected_spending,
                alerts_triggered=alerts_triggered,
                recommendations=recommendations,
            )

        except Exception as e:
            logger.error(f"Failed to get budget status: {e}")
            return None

    async def check_spending_against_budget(
        self, session: AsyncSession, user_id: UUID, additional_cost: Decimal
    ) -> List[BudgetAlert]:
        """
        Check if additional spending would trigger budget alerts

        Args:
            session: Database session
            user_id: User ID
            additional_cost: Cost to add to current spending

        Returns:
            List of budget alerts that would be triggered
        """
        alerts = []

        try:
            # Check all active budgets for user
            budgets = await self._get_user_budgets(session, user_id)

            for budget in budgets:
                current_spending = await self._get_current_spending(
                    session, user_id, budget.budget_type, budget.provider
                )

                new_spending = current_spending + additional_cost
                new_percentage = float(new_spending / budget.amount) if budget.amount > 0 else 0

                # Check if any new thresholds would be crossed
                current_percentage = (
                    float(current_spending / budget.amount) if budget.amount > 0 else 0
                )

                for threshold in budget.alert_thresholds:
                    if current_percentage < threshold <= new_percentage:
                        alert = BudgetAlert(
                            user_id=user_id,
                            budget_id=f"{budget.budget_type.value}_{budget.provider or 'all'}",
                            threshold=threshold,
                            current_percentage=new_percentage,
                            severity=self._get_alert_severity(threshold),
                            message=self._generate_alert_message(budget, threshold, new_spending),
                            triggered_at=datetime.now(timezone.utc),
                        )
                        alerts.append(alert)

            return alerts

        except Exception as e:
            logger.error(f"Failed to check spending against budget: {e}")
            return []

    def _get_alert_severity(self, threshold: float) -> AlertSeverity:
        """Determine alert severity based on threshold"""
        if threshold >= 1.0:
            return AlertSeverity.CRITICAL
        elif threshold >= 0.9:
            return AlertSeverity.WARNING
        else:
            return AlertSeverity.INFO

    def _generate_alert_message(self, budget: Budget, threshold: float, spending: Decimal) -> str:
        """Generate alert message"""
        percentage = int(threshold * 100)
        provider_text = f" for {budget.provider}" if budget.provider else ""

        if threshold >= 1.0:
            return f"🚨 Budget exceeded! You've spent ${spending} of your ${budget.amount} {budget.budget_type.value} budget{provider_text}"
        else:
            return f"⚠️ Budget alert: You've used {percentage}% of your ${budget.amount} {budget.budget_type.value} budget{provider_text}"

    def _check_alert_thresholds(self, budget: Budget, percentage: float) -> List[Dict[str, Any]]:
        """Check which alert thresholds have been triggered"""
        triggered = []

        for threshold in budget.alert_thresholds:
            if percentage >= threshold:
                triggered.append(
                    {
                        "threshold": threshold,
                        "percentage": int(threshold * 100),
                        "severity": self._get_alert_severity(threshold).value,
                        "message": self._generate_alert_message(
                            budget, threshold, budget.amount * Decimal(str(percentage))
                        ),
                    }
                )

        return triggered

    def _generate_budget_recommendations(
        self,
        budget: Budget,
        current_spending: Decimal,
        projected_spending: Decimal,
        days_remaining: int,
    ) -> List[str]:
        """Generate budget management recommendations"""
        recommendations = []

        # Check if over budget
        if current_spending > budget.amount:
            overage = current_spending - budget.amount
            recommendations.append(f"🚨 Over budget by ${overage:.2f}")
            recommendations.append("💡 Consider pausing non-essential API usage")

        # Check if projected to go over budget
        elif projected_spending > budget.amount:
            projected_overage = projected_spending - budget.amount
            recommendations.append(f"⚠️ Projected to exceed budget by ${projected_overage:.2f}")
            recommendations.append("💡 Reduce usage or increase budget to stay on track")

        # Check spending rate
        percentage_used = (
            float((current_spending / budget.amount) * 100) if budget.amount > 0 else 0
        )
        period_elapsed = self._get_period_elapsed_percentage(budget.budget_type)

        if percentage_used > period_elapsed * 1.2:  # Spending 20% faster than expected
            recommendations.append("📈 Spending faster than expected for this period")
            recommendations.append("💡 Monitor usage more closely or adjust budget")

        # Positive feedback
        if not recommendations and percentage_used < 80:
            recommendations.append("✅ Budget on track")

        return recommendations

    def _get_days_remaining_in_period(self, budget_type: BudgetType) -> int:
        """Get days remaining in current budget period"""
        now = datetime.now(timezone.utc)

        if budget_type == BudgetType.DAILY:
            tomorrow = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
            return (tomorrow - now).days

        elif budget_type == BudgetType.WEEKLY:
            # Week starts on Monday
            days_since_monday = now.weekday()
            next_monday = now + timedelta(days=7 - days_since_monday)
            next_monday = next_monday.replace(hour=0, minute=0, second=0, microsecond=0)
            return (next_monday - now).days

        elif budget_type == BudgetType.MONTHLY:
            # Next month
            if now.month == 12:
                next_month = now.replace(
                    year=now.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0
                )
            else:
                next_month = now.replace(
                    month=now.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0
                )
            return (next_month - now).days

        elif budget_type == BudgetType.YEARLY:
            next_year = now.replace(
                year=now.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0
            )
            return (next_year - now).days

        return 0

    def _get_days_elapsed_in_period(self, budget_type: BudgetType) -> int:
        """Get days elapsed in current budget period"""
        now = datetime.now(timezone.utc)

        if budget_type == BudgetType.DAILY:
            start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
            return (now - start_of_day).days + 1

        elif budget_type == BudgetType.WEEKLY:
            days_since_monday = now.weekday()
            return days_since_monday + 1

        elif budget_type == BudgetType.MONTHLY:
            return now.day

        elif budget_type == BudgetType.YEARLY:
            start_of_year = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            return (now - start_of_year).days + 1

        return 1

    def _get_period_elapsed_percentage(self, budget_type: BudgetType) -> float:
        """Get percentage of budget period that has elapsed"""
        elapsed = self._get_days_elapsed_in_period(budget_type)
        remaining = self._get_days_remaining_in_period(budget_type)
        total = elapsed + remaining

        return elapsed / total if total > 0 else 0

    async def _store_budget(self, session: AsyncSession, budget: Budget) -> None:
        """Store budget in database"""
        # TODO: Implement actual database storage
        logger.debug(f"Would store budget: {budget}")

    async def _get_budget(
        self,
        session: AsyncSession,
        user_id: UUID,
        budget_type: BudgetType,
        provider: Optional[str] = None,
    ) -> Optional[Budget]:
        """Get budget from database"""
        # TODO: Implement actual database query
        return None

    async def _get_user_budgets(self, session: AsyncSession, user_id: UUID) -> List[Budget]:
        """Get all active budgets for user"""
        # TODO: Implement actual database query
        return []

    async def _get_current_spending(
        self,
        session: AsyncSession,
        user_id: UUID,
        budget_type: BudgetType,
        provider: Optional[str] = None,
    ) -> Decimal:
        """Get current spending for budget period"""
        # TODO: Implement actual database query
        return Decimal("0.00")
