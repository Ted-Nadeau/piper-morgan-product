# Claude Code Agent Prompt: #632 Phase 2 - Integration

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Session Log Requirement (MANDATORY)

**Create a session log at start**:
```bash
mkdir -p dev/2026/01/21
touch dev/2026/01/21/$(date +%Y-%m-%d-%H%M)-632-phase2-code-log.md
```

**Log format**:
```markdown
# Session Log: #632 Phase 2 - Integration
**Date**: 2026-01-21
**Agent**: Claude Code (Phase 2)
**Issue**: #632 CONSCIOUSNESS-TRANSFORM: Morning Standup

## Prerequisites Check
- Phase 1 complete: [Yes/No]
- Wrapper imports: [Yes/No]

## Work Performed
- [timestamp] Verified Phase 1 complete
- [timestamp] Added imports to standup_bridge.py
- [timestamp] Updated adapt_standup_for_chat
- [timestamp] Created wiring tests
- [timestamp] All standup tests passing

## Evidence
[Paste key terminal outputs]

## Blockers/Issues
[Any problems encountered]

## Handoff Notes
[What Phase 3 validator needs to know]
```

**Update log throughout your work.**

---

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete Phase 2 of GitHub Issue #632. Your work is part of a multi-agent coordination chain.

**Prerequisites**: Phase 1 (wrapper creation) must be complete before you start.

### Your Acceptance Criteria
- [ ] `standup_bridge.py` imports from `standup_consciousness`
- [ ] `adapt_standup_for_chat` uses consciousness formatters
- [ ] Personality system preserved (high warmth, action orientation still work)
- [ ] Wiring tests added and passing
- [ ] All existing standup tests pass (260+)

### Evidence You MUST Provide
1. **Diff summary**: What changed in standup_bridge.py
2. **Wiring tests**: Location and pass status
3. **Full standup test suite**: `pytest tests/ -k standup -v` output
4. **Integration verification**: Show import works

### Your Handoff Format
```
## Issue #632 Phase 2 Completion Report
**Status**: Complete/Partial/Blocked

**Integration**:
- Import verification: [python -c output]
- Wiring tests: X tests in [location]

**Regression Check**:
- `pytest tests/ -k standup -v` output: [paste summary]
- Total: X passed, Y failed

**Files Modified**:
- services/personality/standup_bridge.py (+X/-Y lines)
- services/consciousness/__init__.py (+X lines)
- tests/unit/services/personality/test_standup_bridge_wiring.py (NEW)

**Blockers** (if any):
- [description]
```

---

## Mission
Integrate the consciousness wrapper (from Phase 1) into standup_bridge.py while preserving existing personality system.

**Scope Boundaries**:
- This prompt covers ONLY: Integration into standup_bridge.py
- NOT in scope: Creating the wrapper (Phase 1 - already done)
- NOT in scope: Independent validation (Phase 3)

---

## Context
- **GitHub Issue**: #632 CONSCIOUSNESS-TRANSFORM: Morning Standup
- **Prerequisite**: Phase 1 complete (wrapper exists)
- **Target State**: standup_bridge.py uses consciousness wrapper
- **Constraint**: Personality system must still work

---

## MANDATORY FIRST ACTIONS

### 1. Verify Phase 1 Complete
```bash
# Verify wrapper exists
ls -la services/consciousness/standup_consciousness.py

# Verify wrapper imports work
python -c "from services.consciousness.standup_consciousness import format_full_standup_conscious; print('OK')"

# Verify wrapper tests pass
pytest tests/unit/services/consciousness/test_standup_consciousness.py -v
```

STOP if:
- [ ] Wrapper file doesn't exist
- [ ] Wrapper import fails
- [ ] Wrapper tests failing

### 2. Understand Current Integration
```bash
# See current standup_bridge structure
grep -n "def " services/personality/standup_bridge.py

# See personality system hooks
grep -n "personality\|warmth\|action" services/personality/standup_bridge.py

# Check existing tests
ls -la tests/unit/services/personality/
```

---

## Implementation Approach

### Step 1: Add Consciousness Import

At top of `services/personality/standup_bridge.py`, add:

```python
from services.consciousness.standup_consciousness import (
    format_standup_greeting_conscious,
    format_accomplishments_conscious,
    format_priorities_conscious,
    format_blockers_conscious,
    format_standup_closing_conscious,
)
```

**Validation**:
```bash
python -c "from services.personality.standup_bridge import StandupToChatBridge; print('Import OK')"
```

### Step 2: Update adapt_standup_for_chat

Modify `adapt_standup_for_chat` method to use consciousness formatters:

**Current** (around line 34-68):
```python
def adapt_standup_for_chat(self, standup_response: Dict[str, Any]) -> str:
    """Transform standup JSON to conversational format"""
    # ... mechanical formatting
```

**New**:
```python
def adapt_standup_for_chat(self, standup_response: Dict[str, Any]) -> str:
    """Transform standup JSON to conversational format with consciousness.

    Issue #632: Now uses consciousness wrappers for identity voice,
    epistemic humility, and dialogue invitation.
    """
    try:
        if not standup_response or "data" not in standup_response:
            return "I don't have standup information available right now. Want me to check what's going on?"

        data = standup_response["data"]
        metadata = standup_response.get("metadata", {})

        # Determine data sources for attribution
        sources = []
        if data.get("github_activity", {}).get("commits"):
            sources.append("GitHub")
        if metadata.get("context_source") == "persistent":
            sources.append("our conversations")

        # Build conscious narrative
        sections = []

        # Greeting with source attribution
        sections.append(format_standup_greeting_conscious(sources or ["your recent activity"]))

        # Yesterday's accomplishments
        if data.get("yesterday_accomplishments"):
            sections.append(format_accomplishments_conscious(data["yesterday_accomplishments"]))

        # Today's priorities
        if data.get("today_priorities"):
            sections.append(format_priorities_conscious(data["today_priorities"]))

        # Blockers
        sections.append(format_blockers_conscious(data.get("blockers", [])))

        # Closing with metrics
        metrics = {
            "generation_time_ms": data.get("generation_time_ms"),
            "time_saved_minutes": data.get("time_saved_minutes")
        }
        sections.append(format_standup_closing_conscious(metrics))

        return "\n\n".join(sections)

    except Exception as e:
        logger.error(f"Error adapting standup for chat: {e}")
        return "I ran into something while preparing your standup. Want me to try again?"
```

### Step 3: Preserve Personality System

The `apply_personality_to_standup` method should still work. Verify:

```python
def apply_personality_to_standup(
    self, standup_data: Dict[str, Any], profile: PersonalityProfile
) -> str:
    """Apply personality preferences to standup content.

    Note: Base content now uses consciousness patterns.
    Personality enhancements layer on top.
    """
    try:
        # First convert to conscious chat format
        base_content = self.adapt_standup_for_chat(standup_data)

        # Apply personality enhancements (warmth, action orientation)
        enhanced_content = self._enhance_with_personality(base_content, profile, standup_data)

        return enhanced_content

    except Exception as e:
        logger.error(f"Error applying personality to standup: {e}")
        return self.adapt_standup_for_chat(standup_data)
```

**Validation**: Personality methods should work unchanged:
```bash
grep -n "_add_high_warmth\|_add_action_guidance" services/personality/standup_bridge.py
# Should find these methods still present
```

### Step 4: Update Exports

In `services/consciousness/__init__.py`, add:

```python
from services.consciousness.standup_consciousness import (
    format_standup_greeting_conscious,
    format_accomplishments_conscious,
    format_priorities_conscious,
    format_blockers_conscious,
    format_standup_closing_conscious,
    format_full_standup_conscious,
)

# In __all__, add:
    # Standup consciousness (Wave 2)
    "format_standup_greeting_conscious",
    "format_accomplishments_conscious",
    "format_priorities_conscious",
    "format_blockers_conscious",
    "format_standup_closing_conscious",
    "format_full_standup_conscious",
```

### Step 5: Create Wiring Tests

Create `tests/unit/services/personality/test_standup_bridge_wiring.py`:

```python
"""
Wiring tests for standup bridge consciousness integration.
Issue #632 - Verifies imports and method calls work correctly.

These tests verify the WIRING, not the consciousness output itself.
"""

import pytest


class TestStandupBridgeWiring:
    """Wiring tests for standup_bridge.py consciousness integration."""

    def test_consciousness_import_works(self):
        """Verify consciousness can be imported from standup_bridge."""
        from services.personality.standup_bridge import StandupToChatBridge

        # If this imports, wiring is correct
        bridge = StandupToChatBridge()
        assert bridge is not None

    def test_adapt_standup_for_chat_uses_consciousness(self):
        """Verify adapt_standup_for_chat produces conscious output."""
        from services.personality.standup_bridge import StandupToChatBridge

        bridge = StandupToChatBridge()
        standup_response = {
            "data": {
                "yesterday_accomplishments": ["Fixed bug"],
                "today_priorities": ["Continue work"],
                "blockers": [],
                "generation_time_ms": 1000,
                "time_saved_minutes": 15,
                "github_activity": {"commits": [{"message": "test"}]}
            },
            "metadata": {"context_source": "persistent"}
        }

        result = bridge.adapt_standup_for_chat(standup_response)

        # Should have identity voice
        assert "I " in result or "I'" in result, "Output should have identity voice"
        # Should have invitation
        assert "?" in result, "Output should have dialogue invitation"

    def test_personality_still_applies(self):
        """Verify personality system still works on top of consciousness."""
        from services.personality.standup_bridge import StandupToChatBridge
        from services.personality.personality_profile import PersonalityProfile, ActionLevel

        bridge = StandupToChatBridge()
        standup_response = {
            "data": {
                "yesterday_accomplishments": ["Fixed bug"],
                "today_priorities": ["Continue work"],
                "blockers": []
            },
            "metadata": {}
        }

        profile = PersonalityProfile(
            warmth_level=0.9,  # High warmth
            action_orientation=ActionLevel.HIGH
        )

        result = bridge.apply_personality_to_standup(standup_response, profile)

        # Should still be string output
        assert isinstance(result, str)
        # Should have content
        assert len(result) > 50

    def test_empty_response_handled_gracefully(self):
        """Verify empty response doesn't crash."""
        from services.personality.standup_bridge import StandupToChatBridge

        bridge = StandupToChatBridge()

        # Empty response
        result = bridge.adapt_standup_for_chat({})
        assert "I " in result, "Error message should have identity"
        assert "?" in result, "Error message should have invitation"

        # None response
        result = bridge.adapt_standup_for_chat(None)
        assert "I " in result

    def test_consciousness_exports_available(self):
        """Verify consciousness functions are exported."""
        from services.consciousness import (
            format_standup_greeting_conscious,
            format_accomplishments_conscious,
            format_priorities_conscious,
            format_blockers_conscious,
            format_standup_closing_conscious,
        )

        # All should be callable
        assert callable(format_standup_greeting_conscious)
        assert callable(format_accomplishments_conscious)
        assert callable(format_priorities_conscious)
        assert callable(format_blockers_conscious)
        assert callable(format_standup_closing_conscious)
```

**Validation**:
```bash
pytest tests/unit/services/personality/test_standup_bridge_wiring.py -v
```

### Step 6: Run Full Standup Test Suite

```bash
# Run all standup-related tests
pytest tests/ -k standup -v 2>&1 | tail -50

# Get count
pytest tests/ -k standup --collect-only | grep "test session starts" -A 5
```

Expected: 260+ tests, all pass

---

## Success Criteria

- [ ] Import works: `python -c "from services.personality.standup_bridge import ..."`
- [ ] Wiring tests pass: 5 tests in test_standup_bridge_wiring.py
- [ ] All standup tests pass: 260+ tests
- [ ] Personality system works: warmth/action methods still function
- [ ] Evidence provided for each

---

## STOP Conditions

If ANY of these occur, STOP and report:
1. Phase 1 wrapper doesn't exist or import fails
2. Existing standup tests fail after integration
3. Personality system breaks
4. Import circular dependency
5. Any assumption needed

---

## Deliverables

1. Modified `services/personality/standup_bridge.py`
2. Modified `services/consciousness/__init__.py`
3. New `tests/unit/services/personality/test_standup_bridge_wiring.py`
4. Terminal output showing all tests pass

---

*Prompt Version: 1.0*
*Template: agent-prompt-template v10.2*
*Phase: 2 of 4*
