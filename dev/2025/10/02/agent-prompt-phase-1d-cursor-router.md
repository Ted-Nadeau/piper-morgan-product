# Cursor Agent Prompt: GREAT-3A Phase 1D - Calendar Router Integration

## Session Log Management
Continue using existing session log. Update with timestamped entries for your Phase 1D work.

## Mission
**Update Calendar Router**: Integrate CalendarConfigService into router for service injection pattern.

## Context

Code agent is creating CalendarConfigService and updating the adapter. Your task is updating the router to use service injection pattern.

**Target**: CalendarIntegrationRouter follows same pattern as Slack/Notion/GitHub

## Your Tasks

### Task 1: Analyze Current Router Pattern

```bash
cd ~/Development/piper-morgan

# Check current router __init__
cat services/integrations/calendar/calendar_integration_router.py | grep -A 30 "def __init__"

# Check what router currently does
grep "spatial\|adapter\|mcp" services/integrations/calendar/calendar_integration_router.py | head -20
```

**Document**: How does router currently initialize the adapter?

### Task 2: Update Router to Accept Config Service

**File**: `services/integrations/calendar/calendar_integration_router.py`

**Pattern** (follow Slack/Notion/GitHub):

```python
from typing import Optional
from .config_service import CalendarConfigService

class CalendarIntegrationRouter:
    def __init__(self, config_service: Optional[CalendarConfigService] = None):
        """Initialize router with feature flag checking and config service"""

        # Use FeatureFlags service for consistency
        self.use_spatial = FeatureFlags.should_use_spatial_calendar()
        self.allow_legacy = FeatureFlags.is_legacy_calendar_allowed()

        # Store config service
        self.config_service = config_service or CalendarConfigService()

        # Initialize spatial integration with config
        self.spatial_calendar = None
        if self.use_spatial:
            try:
                from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

                # Pass config to adapter
                self.spatial_calendar = GoogleCalendarMCPAdapter(self.config_service)

            except ImportError as e:
                warnings.warn(f"Spatial Calendar unavailable: {e}")
```

**Changes**:
1. Add import for CalendarConfigService
2. Add optional config_service parameter
3. Create default config if not provided
4. Pass config to GoogleCalendarMCPAdapter

### Task 3: Verify Pattern Matches Other Routers

**Compare with Slack pattern**:
```bash
# Check Slack router for reference
grep -A 25 "def __init__" services/integrations/slack/slack_integration_router.py

# Check Notion router
grep -A 25 "def __init__" services/integrations/notion/notion_integration_router.py

# Check GitHub router
grep -A 25 "def __init__" services/integrations/github/github_integration_router.py

# Verify Calendar matches
grep -A 25 "def __init__" services/integrations/calendar/calendar_integration_router.py
```

**Ensure**:
- Same parameter pattern (Optional[ConfigService] = None)
- Same default behavior (create default if not provided)
- Same adapter passing pattern

### Task 4: Test Router Integration

```bash
# Test 1: Router instantiates without parameter
python -c "from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter; r = CalendarIntegrationRouter(); print('Router OK without config')"

# Test 2: Router accepts explicit config
python -c "from services.integrations.calendar.config_service import CalendarConfigService; from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter; c = CalendarConfigService(); r = CalendarIntegrationRouter(c); print('Router OK with config')"

# Test 3: Router has config_service attribute
python -c "from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter; r = CalendarIntegrationRouter(); print('Has config_service:', hasattr(r, 'config_service')); assert r.config_service is not None"

# Test 4: Adapter receives config
python -c "from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter; r = CalendarIntegrationRouter(); print('Spatial calendar:', r.spatial_calendar); print('Config passed to adapter:', r.spatial_calendar.config_service if r.spatial_calendar else 'None')"
```

### Task 5: Run Compliance Test Suite

```bash
# Run full test suite on Calendar
pytest tests/integration/config_pattern_compliance/ -k calendar -v

# Should pass all 6 checks
# Expected: 6/6 PASS for Calendar

# Generate final compliance report
python tests/integration/config_pattern_compliance/generate_report.py
```

**Expected Output**:
```
Calendar Integration Compliance: ✅ PASS (6/6 checks)
Overall Compliance: 100% (4 of 4 integrations)
```

### Task 6: Cross-Validation with Code Agent

**Wait for Code to finish adapter changes**, then:

1. Verify adapter accepts config_service parameter
2. Test full integration (router → adapter → config)
3. Run compliance tests
4. Generate final report

**Coordination**: Code updates adapter, you update router, both must work together.

## Deliverable

Create: `dev/2025/10/02/phase-1d-cursor-router-integration.md`

Include:
1. **Current Pattern Analysis**: How router initialized adapter before
2. **Router Updates**: Changes made with diffs
3. **Pattern Compliance**: Verification matches other routers
4. **Test Results**: All 4 test commands passing
5. **Compliance Report**: Final 100% compliance achieved
6. **Integration Validation**: Full router → adapter → config flow working

## Time Estimate
30-45 minutes (coordinate with Code agent)

## Success Criteria
- [ ] Router accepts config_service parameter
- [ ] Router creates default config if not provided
- [ ] Router passes config to adapter
- [ ] Pattern matches Slack/Notion/GitHub
- [ ] All test commands pass
- [ ] Compliance tests pass (6/6 checks)
- [ ] 100% compliance achieved

---

**Deploy at 4:37 PM**
**Coordinate with Code on adapter completion**
**Final task to achieve 100% pattern compliance**
