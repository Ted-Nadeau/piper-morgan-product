"""
Calendar Integration Module

Provides router-based access to calendar integrations with feature flag control.
"""

from .calendar_integration_router import CalendarIntegrationRouter, create_calendar_integration

__all__ = ["CalendarIntegrationRouter", "create_calendar_integration"]
