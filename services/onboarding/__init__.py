# onboarding module
"""
Portfolio onboarding services for first-time user experience.

Issue #490: FTUX-PORTFOLIO - Project Portfolio Onboarding
Epic: FTUX (First Time User Experience)

This module provides:
- FirstMeetingDetector: Detects when user has no projects and should be offered onboarding
- PortfolioOnboardingManager: State machine for project setup conversation
- PortfolioOnboardingHandler: Turn-by-turn conversation handling
"""

from services.onboarding.first_meeting_detector import FirstMeetingDetector
from services.onboarding.portfolio_handler import OnboardingResponse, PortfolioOnboardingHandler
from services.onboarding.portfolio_manager import (
    InvalidStateTransitionError,
    PortfolioOnboardingManager,
)

__all__ = [
    "FirstMeetingDetector",
    "InvalidStateTransitionError",
    "OnboardingResponse",
    "PortfolioOnboardingHandler",
    "PortfolioOnboardingManager",
]
