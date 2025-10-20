"""
User approval system for intelligent automation.

Manages user approval preferences and handles approval requests for
actions that require confirmation.

Issue: #225 (CORE-LEARN-E)
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set

from services.domain.user_preference_manager import UserPreferenceManager


class ApprovalStatus(Enum):
    """Status of an approval request."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


@dataclass
class ApprovalRequest:
    """An approval request for an automation action."""

    request_id: str
    user_id: str
    action_type: str
    confidence: float
    safety_level: str
    context: Dict
    status: ApprovalStatus = ApprovalStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
    resolution_reason: Optional[str] = None


class UserApprovalSystem:
    """
    User approval system for automation.

    Manages approval preferences and pending approval requests.
    Integrates with UserPreferenceManager for per-user settings.
    """

    def __init__(self):
        self.preference_manager = UserPreferenceManager()
        self._pending_requests: Dict[str, ApprovalRequest] = {}
        self._approval_history: List[ApprovalRequest] = []

    async def should_auto_approve(self, user_id: str, action_type: str, confidence: float) -> bool:
        """
        Check if action should be auto-approved based on user preferences.

        Args:
            user_id: User ID
            action_type: Type of action
            confidence: Confidence score

        Returns:
            True if should auto-approve, False if needs manual approval
        """
        # Check user's global automation setting
        try:
            automation_enabled = await self.preference_manager.get_preference(
                user_id, "automation_enabled"
            )
            if automation_enabled is False:
                return False
        except Exception:
            # Default to requiring approval if preference not set
            return False

        # Check action-specific auto-approval
        try:
            auto_approve_key = f"auto_approve_{action_type.lower()}"
            auto_approve = await self.preference_manager.get_preference(user_id, auto_approve_key)
            if auto_approve is True:
                return True
        except Exception:
            pass

        # Check confidence threshold preference
        try:
            min_confidence = await self.preference_manager.get_preference(
                user_id, "automation_min_confidence"
            )
            if min_confidence and confidence >= min_confidence:
                return True
        except Exception:
            pass

        # Default to requiring approval
        return False

    async def request_approval(
        self,
        user_id: str,
        action_type: str,
        confidence: float,
        safety_level: str,
        context: Optional[Dict] = None,
    ) -> ApprovalRequest:
        """
        Create an approval request.

        Args:
            user_id: User ID
            action_type: Type of action requiring approval
            confidence: Confidence score
            safety_level: Safety classification
            context: Additional context

        Returns:
            ApprovalRequest object
        """
        request_id = f"{user_id}_{action_type}_{datetime.utcnow().isoformat()}"

        request = ApprovalRequest(
            request_id=request_id,
            user_id=user_id,
            action_type=action_type,
            confidence=confidence,
            safety_level=safety_level,
            context=context or {},
        )

        self._pending_requests[request_id] = request
        return request

    def approve_request(
        self, request_id: str, reason: Optional[str] = None
    ) -> Optional[ApprovalRequest]:
        """
        Approve a pending request.

        Args:
            request_id: Request ID to approve
            reason: Optional reason for approval

        Returns:
            Approved ApprovalRequest, or None if not found
        """
        if request_id not in self._pending_requests:
            return None

        request = self._pending_requests[request_id]
        request.status = ApprovalStatus.APPROVED
        request.resolved_at = datetime.utcnow()
        request.resolution_reason = reason

        # Move to history
        self._approval_history.append(request)
        del self._pending_requests[request_id]

        return request

    def reject_request(
        self, request_id: str, reason: Optional[str] = None
    ) -> Optional[ApprovalRequest]:
        """
        Reject a pending request.

        Args:
            request_id: Request ID to reject
            reason: Optional reason for rejection

        Returns:
            Rejected ApprovalRequest, or None if not found
        """
        if request_id not in self._pending_requests:
            return None

        request = self._pending_requests[request_id]
        request.status = ApprovalStatus.REJECTED
        request.resolved_at = datetime.utcnow()
        request.resolution_reason = reason

        # Move to history
        self._approval_history.append(request)
        del self._pending_requests[request_id]

        return request

    def get_pending_requests(self, user_id: Optional[str] = None) -> List[ApprovalRequest]:
        """
        Get pending approval requests.

        Args:
            user_id: Optional filter by user ID

        Returns:
            List of pending ApprovalRequests
        """
        requests = list(self._pending_requests.values())

        if user_id:
            requests = [r for r in requests if r.user_id == user_id]

        # Sort by creation time (oldest first)
        requests.sort(key=lambda r: r.created_at)

        return requests

    def get_approval_history(
        self, user_id: Optional[str] = None, limit: int = 100
    ) -> List[ApprovalRequest]:
        """
        Get approval history.

        Args:
            user_id: Optional filter by user ID
            limit: Maximum number of records to return

        Returns:
            List of historical ApprovalRequests
        """
        history = self._approval_history

        if user_id:
            history = [r for r in history if r.user_id == user_id]

        # Sort by resolution time descending (most recent first)
        history = sorted(history, key=lambda r: r.resolved_at or r.created_at, reverse=True)

        return history[:limit]

    def get_approval_statistics(self, user_id: Optional[str] = None) -> Dict:
        """
        Get approval statistics.

        Args:
            user_id: Optional filter by user ID

        Returns:
            Dictionary with approval statistics
        """
        history = self.get_approval_history(user_id, limit=None)

        if not history:
            return {
                "total_requests": 0,
                "approved_count": 0,
                "rejected_count": 0,
                "approval_rate": 0.0,
                "pending_count": len(self.get_pending_requests(user_id)),
            }

        total = len(history)
        approved = sum(1 for r in history if r.status == ApprovalStatus.APPROVED)
        rejected = sum(1 for r in history if r.status == ApprovalStatus.REJECTED)

        return {
            "total_requests": total,
            "approved_count": approved,
            "rejected_count": rejected,
            "approval_rate": approved / total if total > 0 else 0.0,
            "pending_count": len(self.get_pending_requests(user_id)),
        }

    async def set_automation_preferences(
        self,
        user_id: str,
        enabled: bool,
        min_confidence: Optional[float] = None,
        auto_approve_actions: Optional[Set[str]] = None,
    ):
        """
        Set user automation preferences.

        Args:
            user_id: User ID
            enabled: Enable/disable automation globally
            min_confidence: Minimum confidence for auto-approval
            auto_approve_actions: Set of action types to auto-approve
        """
        # Set global automation preference
        await self.preference_manager.set_preference(user_id, "automation_enabled", enabled)

        # Set minimum confidence threshold
        if min_confidence is not None:
            await self.preference_manager.set_preference(
                user_id, "automation_min_confidence", min_confidence
            )

        # Set action-specific auto-approval
        if auto_approve_actions:
            for action_type in auto_approve_actions:
                auto_approve_key = f"auto_approve_{action_type.lower()}"
                await self.preference_manager.set_preference(user_id, auto_approve_key, True)

    def clear_history(self):
        """Clear approval history (for testing only)."""
        self._approval_history.clear()
        self._pending_requests.clear()


# Global user approval system instance
_user_approval_system: Optional[UserApprovalSystem] = None


def get_user_approval_system() -> UserApprovalSystem:
    """Get global user approval system instance."""
    global _user_approval_system
    if _user_approval_system is None:
        _user_approval_system = UserApprovalSystem()
    return _user_approval_system
