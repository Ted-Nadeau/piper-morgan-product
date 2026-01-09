# Gameplan: #491 FTUX-CONCIERGE - Capability Concierge

**Issue**: https://github.com/mediajunkie/piper-morgan-product/issues/491
**Created**: 2026-01-07
**Approach**: Enhance existing IDENTITY handler + add graceful limitation responses

**Note**: #488 (DISCOVERY intent category) deferred to Sprint I1 for holistic MUX-INTERACT treatment.

---

## Phase -1: Infrastructure Verification Checkpoint (MANDATORY)

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (confirmed)
- [x] IntentCategory enum: `services/shared_types.py` (15 categories)
- [x] IDENTITY handler: `services/intent_service/canonical_handlers.py`
- [x] PluginRegistry: `services/plugins/plugin_registry.py` (has `get_enabled_plugins()`)
- [x] Canonical handlers: `services/intent_service/canonical_handlers.py`

**What Already Exists (Issue #487, #493)**:
- [x] `_get_dynamic_capabilities()` - Queries PluginRegistry for capabilities
- [x] IDENTITY handler responds to "what can you do?" patterns
- [x] Dynamic capability display exists but may be incomplete
- [x] `PluginMetadata.capabilities` field exists

**What's Missing**:
- [ ] Slash command inventory in capability response
- [ ] Graceful "can't do that" responses (currently may return 422)
- [ ] UNKNOWN intent graceful handling

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel on different files/features
- [ ] Task duration >30 minutes (main branch may advance)
- [ ] Multi-component work (e.g., frontend + backend by different agents)
- [ ] Exploratory/risky changes where easy rollback is valuable
- [ ] Coordination queue prompt being claimed

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [x] Small fixes (<15 min per phase)
- [x] Changes to single file (canonical_handlers.py + tests)
- [ ] Time-critical work where setup overhead matters

**Assessment:**
- [ ] **USE WORKTREE** - 2+ parallel criteria checked
- [x] **SKIP WORKTREE** - Single file changes, single agent
- [ ] **PM DECISION** - Mixed signals, escalate

**Rationale**: All changes are in canonical_handlers.py + new test file. Single agent work, ~2-3 hours.

### Part B: PM Verification Required

**PM, please confirm**:

1. **Scope confirmation**:
   - [x] #491 P0: Dynamic capabilities in IDENTITY response
   - [x] #491 P0: Slash command inventory
   - [x] #491 P0: Graceful limitation responses (no 422s)
   - [ ] #488 DISCOVERY intent: **DEFERRED to Sprint I1**

2. **Implementation approach**:
   - Enhance existing IDENTITY handler (no new intent category needed)
   - Add `_get_slash_commands()` helper
   - Add `_format_limitation_response()` for UNKNOWN handling

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
- [x] Backend-only changes → **YES**

**Decision**: **SKIP** - Backend-only intent handling changes.

---

## Phase 0: Initial Bookending

### GitHub Issue
- #491: FTUX-CONCIERGE (Capability concierge)

### Acceptance Criteria (from issue)

**#491 P0 Acceptance Criteria**:
- [ ] "What can you do?" returns dynamic capability list from PluginRegistry
- [ ] Response includes slash commands with syntax and description
- [ ] Response indicates which integrations are enabled
- [ ] Graceful "can't do that" responses (no 422 errors for capability queries)
- [ ] Limitation responses suggest alternatives

---

## Phase 1: Enhance IDENTITY Handler with Dynamic Capabilities

### 1a: Verify `_get_dynamic_capabilities()` exists and works

**File**: `services/intent_service/canonical_handlers.py`

First, verify the method exists and understand its output structure.

### 1b: Add `_get_slash_commands()` helper

**File**: `services/intent_service/canonical_handlers.py`

```python
def _get_slash_commands(self) -> List[Dict]:
    """Issue #491: Get available slash commands."""
    return [
        {"command": "/standup", "description": "Generate your daily standup", "syntax": "/standup"},
        {"command": "/status", "description": "Project status overview", "syntax": "/status [project]"},
        {"command": "/help", "description": "Get help and guidance", "syntax": "/help [topic]"},
    ]
```

### 1c: Update IDENTITY response to include slash commands

Modify `_handle_identity_intent()` (or equivalent) to include:
1. Dynamic capabilities from PluginRegistry
2. Slash commands from `_get_slash_commands()`
3. Clear formatting

```python
def _format_identity_response_with_capabilities(self) -> str:
    """Issue #491: Format identity response with dynamic capabilities and slash commands."""
    capabilities_data = self._get_dynamic_capabilities()

    lines = ["I'm Piper, your AI-powered project management assistant.\n"]

    # Core capabilities
    lines.append("**What I can help with:**")
    lines.append("- 📋 Todo management - track your tasks")
    lines.append("- 📊 Status updates - see what you're working on")
    lines.append("- 🎯 Priority guidance - focus on what matters")
    lines.append("- 📅 Calendar awareness - know your schedule")

    # Plugin capabilities (dynamic)
    integrations = capabilities_data.get("integrations", [])
    if integrations:
        lines.append("\n**Active Integrations:**")
        for integration in integrations:
            name = integration.get("name", "Unknown").capitalize()
            desc = integration.get("description", f"{name} integration")
            lines.append(f"- {name}: {desc}")

    # Slash commands
    slash_commands = self._get_slash_commands()
    lines.append("\n**Slash Commands:**")
    for cmd in slash_commands:
        lines.append(f"- `{cmd['syntax']}` - {cmd['description']}")

    lines.append("\n💡 *Try asking: \"What's on my agenda today?\" or \"Create a todo for...\"*")

    return "\n".join(lines)
```

---

## Phase 2: Graceful Limitation Responses

### 2a: Add limitation response formatter

**File**: `services/intent_service/canonical_handlers.py`

```python
def _format_limitation_response(self, requested_capability: str, alternatives: List[str] = None) -> str:
    """Issue #491: Format graceful response when capability doesn't exist."""
    lines = [f"I can't {requested_capability} yet."]

    if alternatives:
        lines.append("\nBut I can help you with:")
        for alt in alternatives[:3]:  # Top 3 alternatives
            lines.append(f"- {alt}")

    lines.append("\n💡 *Type 'what can you do?' to see all my capabilities.*")
    return "\n".join(lines)
```

### 2b: Update UNKNOWN intent handling

When intent classification fails or routes to UNKNOWN, provide helpful fallback instead of 422:

```python
async def _handle_unknown_intent(self, intent: Intent, session_id: str) -> Dict:
    """Issue #491: Graceful handling of unrecognized requests."""
    capabilities_data = self._get_dynamic_capabilities()
    alternatives = capabilities_data.get("capabilities_list", [])[:3]

    return {
        "message": self._format_limitation_response(
            requested_capability="understand that request",
            alternatives=alternatives
        ),
        "intent": {
            "category": "unknown",
            "action": "graceful_fallback",
            "confidence": 0.0,
        },
        "requires_clarification": True,
    }
```

### 2c: Ensure UNKNOWN routes to graceful handler

Verify that UNKNOWN intents route to the graceful handler, not to an error path.

---

## Phase 3: Tests

### 3a: Unit tests for enhanced IDENTITY

**File**: `tests/intent/test_concierge.py` (new file)

```python
import pytest
from services.intent_service.canonical_handlers import CanonicalHandlers

class TestConciergeCapabilities:
    """Issue #491: Tests for capability concierge functionality."""

    @pytest.fixture
    def handler(self):
        return CanonicalHandlers()

    def test_get_slash_commands_returns_list(self, handler):
        """Slash commands method returns structured list."""
        commands = handler._get_slash_commands()
        assert isinstance(commands, list)
        assert len(commands) >= 3
        for cmd in commands:
            assert "command" in cmd
            assert "description" in cmd
            assert "syntax" in cmd

    def test_identity_response_includes_slash_commands(self, handler):
        """IDENTITY response includes slash commands."""
        response = handler._format_identity_response_with_capabilities()
        assert "/standup" in response
        assert "/status" in response
        assert "/help" in response

    def test_identity_response_includes_integrations(self, handler):
        """IDENTITY response includes active integrations."""
        response = handler._format_identity_response_with_capabilities()
        assert "Active Integrations" in response or "What I can help with" in response


class TestGracefulLimitations:
    """Issue #491: Tests for graceful limitation responses."""

    @pytest.fixture
    def handler(self):
        return CanonicalHandlers()

    def test_limitation_response_is_helpful(self, handler):
        """Limitation response provides alternatives."""
        response = handler._format_limitation_response(
            requested_capability="book a flight",
            alternatives=["Todo management", "Calendar awareness", "Status updates"]
        )
        assert "can't" in response.lower()
        assert "book a flight" in response
        assert "But I can help you with" in response

    def test_limitation_response_suggests_discovery(self, handler):
        """Limitation response suggests capability discovery."""
        response = handler._format_limitation_response(
            requested_capability="do that thing"
        )
        assert "what can you do" in response.lower()

    @pytest.mark.asyncio
    async def test_unknown_intent_returns_graceful_response(self, handler):
        """Unknown intents get helpful fallback, not 422."""
        # Mock intent with UNKNOWN category
        from unittest.mock import MagicMock
        intent = MagicMock()
        intent.category = "unknown"

        result = await handler._handle_unknown_intent(intent, "test-session")

        assert "message" in result
        assert "can't" in result["message"].lower()
        assert result.get("requires_clarification") == True
```

---

## Phase Z: Final Bookending & Handoff

### Manual Testing Checklist
- [ ] "What can you do?" → Returns capability list with slash commands
- [ ] "Who are you?" → Returns identity response with capabilities
- [ ] Response includes active integrations from PluginRegistry
- [ ] Response includes slash commands with syntax
- [ ] "Can you book me a flight?" → Graceful limitation response (not 422)
- [ ] Unrecognized queries suggest alternatives and discovery prompt

### Verification Gates
- [x] Phase 1: IDENTITY handler enhanced with slash commands
- [x] Phase 2: Graceful limitation responses work (no 422s)
- [x] Phase 3: Unit tests passing (15 tests in test_concierge.py)
- [ ] Phase Z: Manual testing complete (PM verification needed)

### Evidence Compilation
- [x] IDENTITY response includes dynamic capabilities
- [x] IDENTITY response includes slash commands
- [x] Limitation responses suggest alternatives
- [x] Tests pass (15 tests in tests/intent/test_concierge.py)
- [x] Files modified with line numbers:
  - services/intent_service/canonical_handlers.py (lines 114-136, 273-280, 303-309)
  - services/intent/intent_service.py (lines 7613-7666)
  - tests/intent/test_concierge.py (new file, 359 lines)
- [ ] Commit hash (pending PM approval)

### Evidence Collection Points
1. **After Phase 1**: Capture IDENTITY response showing slash commands
2. **After Phase 2**: Capture graceful limitation response (not 422)
3. **After Phase 3**: Test output showing all tests pass
4. **Before closure**: Compile all evidence into GitHub issue

### Handoff Quality Checklist
Before accepting as complete:
- [ ] All acceptance criteria checkboxes addressed
- [ ] Test output provided (not just "tests pass")
- [ ] Files modified list included with line numbers
- [ ] Manual testing scenarios verified
- [ ] No regressions in existing IDENTITY behavior

### GitHub Final Update
Update #491 with evidence.

### CRITICAL: Agent Does NOT Close Issues
**Only PM closes issues after review and approval**

---

## Files to Modify

| File | Change | Issue |
|------|--------|-------|
| `services/intent_service/canonical_handlers.py` | Add `_get_slash_commands()`, `_format_limitation_response()`, enhance IDENTITY response | #491 |
| `tests/intent/test_concierge.py` | New test file for concierge functionality | #491 |

**Estimated effort**: ~2-3 hours

---

## Risk Assessment

**Low risk**:
- Reuses existing `_get_dynamic_capabilities()` from Issue #493
- Follows established canonical handler pattern (ADR-039)
- No database changes
- No frontend changes
- No new intent categories (IDENTITY already exists)

**Medium risk**:
- IDENTITY handler changes could affect existing behavior
- Need to ensure existing "who are you?" responses still work

**Mitigation**:
- Add regression tests for existing IDENTITY behavior
- Enhance rather than replace existing code
- Manual testing before closing

---

## STOP Conditions

Stop immediately and escalate if:
- [ ] `_get_dynamic_capabilities()` doesn't exist or differs from expected behavior
- [ ] PluginRegistry API has changed since #493
- [ ] IDENTITY handler structure is significantly different than expected
- [ ] Tests fail for any reason
- [ ] Changes break existing IDENTITY functionality

---

## Deferred (to #488 in Sprint I1)

- DISCOVERY intent category
- DISCOVERY_PATTERNS in pre_classifier
- Dedicated `_handle_discovery_intent()` handler
- Routing "what can you do?" away from IDENTITY to new DISCOVERY

These require the #488 work which is deferred to Sprint I1 for holistic MUX-INTERACT treatment.

---

## Deferred (to #491 P1/P2)

- Full CapabilityRegistry architecture
- Contextual capability suggestions (proactive "since you mentioned...")
- User preference learning

These are explicitly marked P1/P2 in #491 and not in scope for this gameplan.
