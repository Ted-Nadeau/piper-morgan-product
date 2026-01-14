# Gameplan: #102 CONV-UX-GREET - Calendar Scanning on Greeting

**Issue**: https://github.com/mediajunkie/piper-morgan-product/issues/102
**Created**: 2026-01-07
**Approach**: Enhance ConversationHandler greeting response with calendar awareness

---

## Phase -1: Infrastructure Verification Checkpoint (MANDATORY)

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (confirmed)
- [x] GREETING pattern detection: `services/intent_service/pre_classifier.py` (GREETING_PATTERNS exists)
- [x] CONVERSATION handler: `services/conversation/conversation_handler.py` (handles "greeting" action)
- [x] Calendar plugin: `services/integrations/calendar/calendar_plugin.py` (has CalendarIntegrationRouter)
- [x] Calendar methods available: `get_todays_events()`, `get_temporal_summary()`, `get_next_meeting()`, `get_free_time_blocks()`

**What Already Exists**:
- [x] GREETING_PATTERNS detect "hello", "hi", "good morning", "good afternoon", etc.
- [x] PreClassifier routes greetings to CONVERSATION category with action="greeting"
- [x] ConversationHandler.respond() handles "greeting" action with static responses
- [x] CalendarIntegrationRouter.get_temporal_summary() returns comprehensive calendar overview
- [x] PluginRegistry can check if calendar is configured

**What's Missing**:
- [ ] Calendar-aware greeting response in ConversationHandler
- [ ] Graceful fallback when calendar not configured
- [ ] Time-of-day awareness in greeting (morning vs afternoon)

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel on different files/features
- [ ] Task duration >30 minutes (main branch may advance)
- [ ] Multi-component work (e.g., frontend + backend by different agents)
- [ ] Exploratory/risky changes where easy rollback is valuable

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [x] Small fixes (<30 min)
- [x] Changes to 2-3 files max (ConversationHandler + tests)

**Assessment:**
- [ ] **USE WORKTREE** - 2+ parallel criteria checked
- [x] **SKIP WORKTREE** - Single file enhancement, single agent
- [ ] **PM DECISION** - Mixed signals, escalate

**Rationale**: Primary change is in ConversationHandler.respond() method. Single file + tests.

### Part B: PM Verification Required

**PM, please confirm**:

1. **Scope confirmation**:
   - [x] P0: Calendar-enhanced greeting response
   - [x] P0: Graceful fallback when calendar unavailable
   - [ ] P1: Meeting importance scoring (defer?)
   - [ ] P1: Conflict detection (defer?)

2. **Implementation approach**:
   - Modify ConversationHandler.respond() to check calendar on "greeting" action
   - Use CalendarIntegrationRouter.get_temporal_summary() for calendar data
   - Format response with schedule highlights
   - Fallback to existing static responses if calendar unavailable

3. **Critical context I'm missing?**
   - ____________

### Part C: Proceed/Revise Decision

After PM verification:
- [ ] **PROCEED** - Understanding is correct, gameplan appropriate
- [ ] **REVISE** - Major assumptions wrong, need different approach
- [ ] **CLARIFY** - Need more context on: ____________

---

## Phase 0.5: Frontend-Backend Contract Verification

### Applicability Check
- [ ] Creating new API endpoints + UI that calls them → **NO**
- [ ] Modifying existing API paths → **NO**
- [ ] Adding JavaScript that makes fetch() calls → **NO**
- [x] Backend-only response format changes → **YES**

**Decision**: **SKIP** - Backend-only change to response content, no API contract changes.

---

## Phase 0: Initial Bookending

### GitHub Issue
Already created: #102

### Acceptance Criteria (from issue - scoped to P0)
- [ ] Detect greeting patterns in user messages (already exists)
- [ ] Automatically trigger calendar scan on greeting detection
- [ ] Surface proactive insights in greeting response
- [ ] Graceful handling if calendar unavailable
- [ ] Performance target: Calendar scan completes in <500ms

---

## Phase 1: Enhance ConversationHandler with Calendar Awareness

### 1a: Add calendar integration to ConversationHandler

**File**: `services/conversation/conversation_handler.py`

```python
# Add to imports
from services.integrations.calendar import create_calendar_integration
from services.plugins import get_plugin_registry
import structlog

logger = structlog.get_logger()

# Add to ConversationHandler class
async def _get_calendar_summary(self) -> Optional[Dict[str, Any]]:
    """Issue #102: Get calendar summary for greeting enhancement."""
    try:
        registry = get_plugin_registry()
        calendar_status = registry.get_status("calendar")

        if not calendar_status.get("configured"):
            return None

        calendar_router = create_calendar_integration()
        summary = await calendar_router.get_temporal_summary()
        return summary
    except Exception as e:
        logger.warning(f"Could not fetch calendar for greeting: {e}")
        return None
```

### 1b: Update respond() method for greeting action

**File**: `services/conversation/conversation_handler.py`

Modify the `respond()` method to call calendar enhancement for "greeting" action:

```python
async def respond(self, intent: Intent, session_id: str = None) -> Dict[str, Any]:
    """Generate appropriate conversational response"""
    import random

    # Handle clarification_needed action
    if intent.action == "clarification_needed":
        return await self._handle_clarification_needed(intent, session_id)

    # Issue #102: Enhanced greeting with calendar awareness
    if intent.action == "greeting":
        return await self._respond_to_greeting(intent, session_id)

    # Handle other conversational actions
    responses = self.RESPONSES.get(intent.action, self.RESPONSES["chitchat"])
    response = random.choice(responses)

    return {
        "message": response,
        "intent": intent_to_dict(intent),
        "workflow_id": None,
    }
```

### 1c: Add _respond_to_greeting method

```python
async def _respond_to_greeting(self, intent: Intent, session_id: str = None) -> Dict[str, Any]:
    """Issue #102: Generate calendar-aware greeting response."""
    import random
    from datetime import datetime

    # Get calendar summary (may be None if unavailable)
    calendar_summary = await self._get_calendar_summary()

    if calendar_summary:
        # Build enhanced greeting with calendar insights
        response = self._format_calendar_greeting(calendar_summary)
    else:
        # Fallback to standard greeting
        response = random.choice(self.RESPONSES["greeting"])

    return {
        "message": response,
        "intent": intent_to_dict(intent),
        "workflow_id": None,
    }

def _format_calendar_greeting(self, summary: Dict[str, Any]) -> str:
    """Issue #102: Format greeting with calendar insights."""
    from datetime import datetime

    now = datetime.now()
    time_greeting = self._get_time_of_day_greeting(now.hour)

    lines = [f"{time_greeting}! Here's your day at a glance:\n"]

    # Current/next meeting
    if summary.get("current_meeting"):
        meeting = summary["current_meeting"]
        lines.append(f"📍 **Now**: {meeting.get('title', 'Meeting in progress')}")
    elif summary.get("next_meeting"):
        meeting = summary["next_meeting"]
        start_time = meeting.get("start_time", "soon")
        lines.append(f"📅 **Next**: {meeting.get('title', 'Meeting')} at {start_time}")

    # Free time blocks
    if summary.get("free_blocks"):
        blocks = summary["free_blocks"][:2]  # Show up to 2 free blocks
        if blocks:
            block_text = ", ".join([f"{b.get('start', '')}-{b.get('end', '')}" for b in blocks])
            lines.append(f"⏰ **Free time**: {block_text}")

    # Today's meeting count
    events = summary.get("events", [])
    if events:
        lines.append(f"\n📋 {len(events)} meetings today")
    else:
        lines.append("\n✨ Clear calendar today!")

    lines.append("\nWhat would you like to focus on?")

    return "\n".join(lines)

def _get_time_of_day_greeting(self, hour: int) -> str:
    """Return appropriate time-of-day greeting."""
    if hour < 12:
        return "Good morning"
    elif hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"
```

---

## Phase 2: Tests

### 2a: Unit tests for calendar greeting

**File**: `tests/unit/services/conversation/test_conversation_handler.py` (or new file)

```python
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from services.conversation.conversation_handler import ConversationHandler
from services.domain.models import Intent
from services.shared_types import IntentCategory

class TestCalendarGreeting:
    """Issue #102: Tests for calendar-aware greeting responses."""

    @pytest.fixture
    def handler(self):
        return ConversationHandler(session_manager=None)

    @pytest.fixture
    def greeting_intent(self):
        return Intent(
            category=IntentCategory.CONVERSATION,
            action="greeting",
            confidence=0.95,
            original_message="Good morning",
        )

    @pytest.mark.asyncio
    async def test_greeting_with_calendar_available(self, handler, greeting_intent):
        """Greeting includes calendar summary when available."""
        mock_summary = {
            "next_meeting": {"title": "Sprint Planning", "start_time": "10:00 AM"},
            "free_blocks": [{"start": "9:00", "end": "10:00"}],
            "events": [{"title": "Sprint Planning"}, {"title": "1:1 with Sarah"}],
        }

        with patch.object(handler, "_get_calendar_summary", new_callable=AsyncMock) as mock_cal:
            mock_cal.return_value = mock_summary

            result = await handler.respond(greeting_intent)

            assert "Sprint Planning" in result["message"]
            assert "2 meetings today" in result["message"]

    @pytest.mark.asyncio
    async def test_greeting_without_calendar(self, handler, greeting_intent):
        """Greeting falls back gracefully when calendar unavailable."""
        with patch.object(handler, "_get_calendar_summary", new_callable=AsyncMock) as mock_cal:
            mock_cal.return_value = None

            result = await handler.respond(greeting_intent)

            # Should use standard greeting response
            assert "message" in result
            assert result["message"] in handler.RESPONSES["greeting"]

    @pytest.mark.asyncio
    async def test_greeting_with_empty_calendar(self, handler, greeting_intent):
        """Greeting handles empty calendar gracefully."""
        mock_summary = {
            "next_meeting": None,
            "free_blocks": [],
            "events": [],
        }

        with patch.object(handler, "_get_calendar_summary", new_callable=AsyncMock) as mock_cal:
            mock_cal.return_value = mock_summary

            result = await handler.respond(greeting_intent)

            assert "Clear calendar" in result["message"]

    def test_time_of_day_greeting(self, handler):
        """Time-of-day greeting returns appropriate message."""
        assert handler._get_time_of_day_greeting(8) == "Good morning"
        assert handler._get_time_of_day_greeting(14) == "Good afternoon"
        assert handler._get_time_of_day_greeting(19) == "Good evening"

    @pytest.mark.asyncio
    async def test_non_greeting_actions_unchanged(self, handler):
        """Issue #102: Verify non-greeting actions still work (regression test)."""
        farewell_intent = Intent(
            category=IntentCategory.CONVERSATION,
            action="farewell",
            confidence=0.95,
            original_message="Goodbye",
        )

        result = await handler.respond(farewell_intent)

        # Should use standard farewell response (not calendar-enhanced)
        assert result["message"] in handler.RESPONSES["farewell"]
```

---

## Phase Z: Final Bookending & Handoff

### Manual Testing Checklist
- [ ] "Good morning" → Returns calendar-aware greeting (if calendar configured)
- [ ] "Hello" → Returns calendar-aware greeting
- [ ] "Hi Piper" → Returns calendar-aware greeting
- [ ] Calendar unavailable → Falls back to standard greeting
- [ ] Response includes meeting count, next meeting, free time blocks
- [ ] Performance: Response < 1 second

### Verification Gates
- [x] Phase 1: ConversationHandler enhanced with calendar awareness
- [x] Phase 2: Unit tests passing (11 tests, 24 total with context_tracker)
- [ ] Phase Z: Manual testing complete (PM verification needed)

### Completion Matrix

| Component | Status | Evidence |
|-----------|--------|----------|
| `_get_calendar_summary()` | ✅ | Lines 66-78 in conversation_handler.py |
| `_respond_to_greeting()` | ✅ | Lines 80-100 in conversation_handler.py |
| `_format_calendar_greeting()` | ✅ | Lines 102-164 in conversation_handler.py |
| `_get_time_of_day_greeting()` | ✅ | Lines 166-173 in conversation_handler.py |
| Regression test (non-greeting actions) | ✅ | 3 tests: farewell, thanks, chitchat |
| Calendar available test | ✅ | test_greeting_with_calendar_available |
| Calendar unavailable test | ✅ | test_greeting_without_calendar, test_greeting_with_calendar_error |
| Empty calendar test | ✅ | test_greeting_with_empty_calendar |
| Time-of-day test | ✅ | 3 tests: morning, afternoon, evening |

### Evidence Compilation
- [ ] Calendar-aware greeting response works
- [ ] Fallback to standard greeting works
- [ ] Tests pass
- [ ] Files modified with line numbers:
  - services/conversation/conversation_handler.py
  - tests/unit/services/conversation/test_conversation_handler.py (or new test file)
- [ ] Commit hash (pending PM approval)

### CRITICAL: Agent Does NOT Close Issues
**Only PM closes issues after review and approval**

---

## Files to Modify

| File | Change | Issue |
|------|--------|-------|
| `services/conversation/conversation_handler.py` | Add `_get_calendar_summary()`, `_respond_to_greeting()`, `_format_calendar_greeting()`, `_get_time_of_day_greeting()` | #102 |
| `tests/unit/services/conversation/test_conversation_handler.py` | Add tests for calendar greeting | #102 |

**Estimated effort**: ~1-2 hours

---

## Risk Assessment

**Low risk**:
- Reuses existing CalendarIntegrationRouter
- Follows established ConversationHandler pattern
- No database changes
- No frontend changes
- Graceful fallback when calendar unavailable

**Medium risk**:
- Calendar API latency could slow greeting response
- Need to verify get_temporal_summary() returns expected structure

**Mitigation**:
- Add timeout to calendar fetch
- Verify calendar response structure before using
- Log warnings but don't fail on calendar issues

---

## STOP Conditions

Stop immediately and escalate if:
- [ ] CalendarIntegrationRouter API has changed
- [ ] get_temporal_summary() returns unexpected structure
- [ ] Calendar plugin not properly registered
- [ ] Tests fail for any reason
- [ ] Performance exceeds 1 second for greeting response
- [ ] Existing greeting tests break (regression)

---

## Deferred (to future sprints)

- Meeting importance scoring (P1 in issue)
- Conflict detection (P1 in issue)
- Dependency surfacing between meetings and projects
- Caching and optimization

These are explicitly marked P1/P2 in #102 and not in scope for this gameplan.
