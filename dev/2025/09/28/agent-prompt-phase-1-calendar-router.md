# Claude Code Prompt: Phase 1 - Calendar Integration Router Implementation

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first in docs/briefing/:
- PROJECT.md - What Piper Morgan is
- CURRENT-STATE.md - Current epic and focus
- role/PROGRAMMER.md - Your role requirements
- METHODOLOGY.md - Inchworm Protocol

## Session Log Management

Continue using your existing session log at: `dev/2025/09/28/2025-09-28-1724-prog-code-log.md`
- Add timestamped entry for Phase 1 work
- Document router implementation progress
- Include all evidence from testing

## Mission: Implement CalendarIntegrationRouter

**Context**: Phase 0 established comprehensive MCP architecture understanding. Calendar adapter (GoogleCalendarMCPAdapter) is complete with OAuth2 and 7 core methods. This router will serve as the reference implementation for the MCP delegation pattern.

**Objective**: Create CalendarIntegrationRouter following GitHubIntegrationRouter pattern, enabling feature flag control between spatial (MCP) and legacy implementations.

## Phase 0 Key Findings Reference

From your investigation:
- **Adapter**: `services/mcp/consumer/google_calendar_adapter.py` (499 lines)
- **Base Class**: `BaseSpatialAdapter`
- **Auth**: OAuth2 with credentials.json + token.json
- **Methods**: 7 async methods (authenticate, get_todays_events, get_current_meeting, get_next_meeting, get_free_time_blocks, get_temporal_summary, health_check)
- **Pattern**: MCP Consumer with circuit breaker

## Implementation Tasks

### Task 1: Create Router File Structure

Create the router following GitHub pattern:

```bash
# Create router file
touch services/integrations/calendar/calendar_integration_router.py

# Verify directory structure
ls -la services/integrations/calendar/
```

### Task 2: Implement Router Class

Following GitHubIntegrationRouter pattern exactly:

```python
# services/integrations/calendar/calendar_integration_router.py
"""
CalendarIntegrationRouter - Feature flag controlled access to calendar integrations

Provides unified interface for calendar operations with support for:
- Spatial intelligence (MCP-based GoogleCalendarAdapter)
- Legacy basic calendar operations (if future implementation exists)
- Feature flag control via USE_SPATIAL_CALENDAR
"""

import os
import warnings
from typing import Optional, List, Dict, Any, Tuple

class CalendarIntegrationRouter:
    """
    Router for calendar integration with spatial/legacy delegation.

    Follows pattern established in CORE-GREAT-2B GitHubIntegrationRouter.
    Delegates to GoogleCalendarMCPAdapter (spatial) or future legacy implementation.
    """

    def __init__(self):
        """Initialize router with feature flag checking"""
        # Check feature flags (following GitHub router pattern)
        self.use_spatial = os.getenv('USE_SPATIAL_CALENDAR', 'true').lower() == 'true'
        self.allow_legacy = os.getenv('ALLOW_LEGACY_CALENDAR', 'false').lower() == 'true'

        # Initialize spatial integration
        self.spatial_calendar = None
        if self.use_spatial:
            try:
                from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter
                self.spatial_calendar = GoogleCalendarMCPAdapter()
            except ImportError as e:
                warnings.warn(f"Spatial calendar unavailable: {e}")

        # Initialize legacy integration (placeholder for future)
        self.legacy_calendar = None
        if self.allow_legacy:
            # Future: Import legacy calendar client if exists
            # For now, no legacy implementation exists
            pass

    def _get_preferred_integration(self, operation: str) -> Tuple[Optional[Any], bool]:
        """
        Get preferred integration based on feature flags.

        Args:
            operation: Name of operation being performed

        Returns:
            Tuple of (integration_instance, is_legacy_bool)
        """
        # Try spatial first if enabled
        if self.use_spatial and self.spatial_calendar:
            return self.spatial_calendar, False

        # Fall back to legacy if allowed (future)
        elif self.allow_legacy and self.legacy_calendar:
            return self.legacy_calendar, True

        # No integration available
        else:
            return None, False

    def _warn_deprecation_if_needed(self, operation: str, is_legacy: bool):
        """Warn about legacy usage for future migration"""
        if is_legacy:
            warnings.warn(
                f"Using legacy calendar for {operation}. "
                "Consider enabling USE_SPATIAL_CALENDAR=true for spatial intelligence.",
                DeprecationWarning,
                stacklevel=3
            )

    # Delegate all 7 GoogleCalendarMCPAdapter methods

    async def authenticate(self) -> bool:
        """Authenticate with Google Calendar via OAuth2"""
        integration, is_legacy = self._get_preferred_integration("authenticate")

        if integration:
            self._warn_deprecation_if_needed("authenticate", is_legacy)
            return await integration.authenticate()
        else:
            raise RuntimeError(
                "No calendar integration available. "
                "Enable USE_SPATIAL_CALENDAR=true or check GoogleCalendarMCPAdapter setup."
            )

    async def get_todays_events(self) -> List[Dict[str, Any]]:
        """Get today's calendar events"""
        integration, is_legacy = self._get_preferred_integration("get_todays_events")

        if integration:
            self._warn_deprecation_if_needed("get_todays_events", is_legacy)
            return await integration.get_todays_events()
        else:
            raise RuntimeError("No calendar integration available")

    async def get_current_meeting(self) -> Optional[Dict[str, Any]]:
        """Get currently active meeting if any"""
        integration, is_legacy = self._get_preferred_integration("get_current_meeting")

        if integration:
            self._warn_deprecation_if_needed("get_current_meeting", is_legacy)
            return await integration.get_current_meeting()
        else:
            raise RuntimeError("No calendar integration available")

    async def get_next_meeting(self) -> Optional[Dict[str, Any]]:
        """Get next upcoming meeting"""
        integration, is_legacy = self._get_preferred_integration("get_next_meeting")

        if integration:
            self._warn_deprecation_if_needed("get_next_meeting", is_legacy)
            return await integration.get_next_meeting()
        else:
            raise RuntimeError("No calendar integration available")

    async def get_free_time_blocks(self,
                                   start_time: Optional[str] = None,
                                   end_time: Optional[str] = None,
                                   duration_minutes: int = 30) -> List[Dict[str, Any]]:
        """Find available time blocks in calendar"""
        integration, is_legacy = self._get_preferred_integration("get_free_time_blocks")

        if integration:
            self._warn_deprecation_if_needed("get_free_time_blocks", is_legacy)
            return await integration.get_free_time_blocks(start_time, end_time, duration_minutes)
        else:
            raise RuntimeError("No calendar integration available")

    async def get_temporal_summary(self) -> Dict[str, Any]:
        """Get temporal summary for standup/reports"""
        integration, is_legacy = self._get_preferred_integration("get_temporal_summary")

        if integration:
            self._warn_deprecation_if_needed("get_temporal_summary", is_legacy)
            return await integration.get_temporal_summary()
        else:
            raise RuntimeError("No calendar integration available")

    async def health_check(self) -> Dict[str, Any]:
        """Check calendar integration health"""
        integration, is_legacy = self._get_preferred_integration("health_check")

        if integration:
            self._warn_deprecation_if_needed("health_check", is_legacy)
            return await integration.health_check()
        else:
            raise RuntimeError("No calendar integration available")
```

### Task 3: Verify Router Implementation

Test the router before proceeding:

```python
# Test router initialization
python -c "
import asyncio
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter

async def test_router():
    router = CalendarIntegrationRouter()
    print(f'✅ Router initialized')
    print(f'   Use spatial: {router.use_spatial}')
    print(f'   Allow legacy: {router.allow_legacy}')
    print(f'   Spatial calendar: {router.spatial_calendar is not None}')

    # Test method availability
    methods = ['authenticate', 'get_todays_events', 'get_current_meeting',
               'get_next_meeting', 'get_free_time_blocks', 'get_temporal_summary',
               'health_check']
    for method in methods:
        has_method = hasattr(router, method) and callable(getattr(router, method))
        print(f'   {method}: {\"✅\" if has_method else \"❌\"}')

asyncio.run(test_router())
"
```

### Task 4: Test Feature Flag Control

Verify feature flags actually control behavior:

```bash
# Test spatial mode (default)
echo "=== Testing Spatial Mode ==="
USE_SPATIAL_CALENDAR=true python -c "
import asyncio
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter

async def test():
    router = CalendarIntegrationRouter()
    integration, is_legacy = router._get_preferred_integration('test')
    print(f'Integration: {type(integration).__name__ if integration else None}')
    print(f'Is legacy: {is_legacy}')

asyncio.run(test())
"

# Test with spatial disabled
echo "=== Testing with Spatial Disabled ==="
USE_SPATIAL_CALENDAR=false python -c "
import asyncio
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter

async def test():
    router = CalendarIntegrationRouter()
    integration, is_legacy = router._get_preferred_integration('test')
    print(f'Integration: {type(integration).__name__ if integration else None}')
    print(f'Is legacy: {is_legacy}')
    # Should be None since no legacy exists

asyncio.run(test())
"
```

### Task 5: Test OAuth Preservation

Critical: Verify OAuth still works through router:

```python
# Test OAuth flow preservation
python -c "
import asyncio
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter

async def test_oauth():
    router = CalendarIntegrationRouter()

    # Check if authenticate method exists and is async
    import inspect
    is_async = inspect.iscoroutinefunction(router.authenticate)
    print(f'authenticate is async: {is_async}')

    # Test health check (doesn't require auth)
    try:
        health = await router.health_check()
        print(f'✅ Health check works through router')
        print(f'   Status: {health.get(\"status\")}')
    except Exception as e:
        print(f'❌ Health check failed: {e}')

asyncio.run(test_oauth())
"
```

## Evidence Requirements

Document in Phase 1 completion report:

```markdown
# Phase 1: Calendar Router Implementation Report

## Router File Created
**Location**: services/integrations/calendar/calendar_integration_router.py
**Size**: [line count]
**Pattern**: Follows GitHubIntegrationRouter delegation pattern

## Implementation Completeness

### Methods Implemented: 7/7
- [ ] authenticate()
- [ ] get_todays_events()
- [ ] get_current_meeting()
- [ ] get_next_meeting()
- [ ] get_free_time_blocks()
- [ ] get_temporal_summary()
- [ ] health_check()

### Delegation Pattern
- [ ] _get_preferred_integration() follows GitHub pattern
- [ ] _warn_deprecation_if_needed() implemented
- [ ] Feature flag checking in __init__
- [ ] RuntimeError when no integration available

## Testing Results

### Router Initialization
[Output from initialization test showing spatial calendar loaded]

### Method Availability
[Output showing all 7 methods are callable]

### Feature Flag Control
**Spatial Mode (USE_SPATIAL_CALENDAR=true)**:
[Output showing GoogleCalendarMCPAdapter used]

**Spatial Disabled (USE_SPATIAL_CALENDAR=false)**:
[Output showing no integration available]

### OAuth Preservation
[Output showing authenticate is async and health_check works]

## Comparison with GitHub Router

### Pattern Compliance
- [ ] Same __init__ structure
- [ ] Same _get_preferred_integration logic
- [ ] Same deprecation warning pattern
- [ ] Same RuntimeError handling

### Differences Noted
[Any intentional differences from GitHub router pattern]

## Ready for Phase 2
[YES/NO - with evidence]
```

## Update Requirements

After completing implementation:

1. **Update Session Log**: Add Phase 1 completion with router evidence
2. **Update GitHub Issue #199**: Add comment with Calendar router completion evidence
3. **Tag Cursor**: Request cross-validation before proceeding to Notion router

## Critical Success Factors

- **Pattern Consistency**: Follow GitHub router exactly - don't deviate without reason
- **OAuth Preservation**: All async patterns must work through router
- **Method Signature Match**: Router methods must match GoogleCalendarMCPAdapter exactly
- **Feature Flag Control**: Must actually work, not just exist
- **Error Handling**: RuntimeError when no integration available (not silent failure)

## STOP Conditions

- If OAuth doesn't work through router
- If async patterns break
- If feature flags don't control behavior
- If methods have signature mismatches

Report any STOP conditions immediately rather than proceeding with broken functionality.

---

**Your Mission**: Implement CalendarIntegrationRouter as reference implementation of MCP delegation pattern. Ensure OAuth preservation and feature flag control work correctly.

**Quality Standard**: Complete, tested, pattern-compliant router before proceeding to Notion implementation.
