# Claude Code Agent Prompt: #632 Phase 1 - Consciousness Wrapper

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology, use TDD, and provide evidence for all claims.

## Session Log Requirement (MANDATORY)

**Create a session log at start**:
```bash
# Create your session log
mkdir -p dev/2026/01/21
# Use format: YYYY-MM-DD-HHMM-[phase]-code-log.md
touch dev/2026/01/21/$(date +%Y-%m-%d-%H%M)-632-phase1-code-log.md
```

**Log format**:
```markdown
# Session Log: #632 Phase 1 - Consciousness Wrapper
**Date**: 2026-01-21
**Agent**: Claude Code (Phase 1)
**Issue**: #632 CONSCIOUSNESS-TRANSFORM: Morning Standup

## Work Performed
- [timestamp] Started phase 1
- [timestamp] Created test file with X tests
- [timestamp] Implemented wrapper with 6 functions
- [timestamp] All tests passing

## Evidence
[Paste key terminal outputs]

## Blockers/Issues
[Any problems encountered]

## Handoff Notes
[What Phase 2 needs to know]
```

**Update log throughout your work** - this is how we maintain continuity.

---

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete Phase 1 of GitHub Issue #632. Your work is part of a multi-agent coordination chain.

### Your Acceptance Criteria
- [ ] Create `tests/unit/services/consciousness/test_standup_consciousness.py` with 10+ tests
- [ ] Create `services/consciousness/standup_consciousness.py` with 6 functions
- [ ] All tests pass
- [ ] MVC validation passes for full standup output

### Evidence You MUST Provide
1. **Test count**: "Added X tests in [file path]"
2. **Test verification**: Actual pytest output showing all pass
3. **Files created**: Complete list
4. **MVC validation**: Show validate_mvc() result

### Your Handoff Format
```
## Issue #632 Phase 1 Completion Report
**Status**: Complete/Partial/Blocked

**Tests**:
- X tests added in tests/unit/services/consciousness/test_standup_consciousness.py
- `pytest tests/unit/services/consciousness/test_standup_consciousness.py -v` output: [paste]

**MVC Validation**:
- validate_mvc(sample_output) result: [paste]

**Files Created**:
- services/consciousness/standup_consciousness.py (+X lines)
- tests/unit/services/consciousness/test_standup_consciousness.py (+X lines)

**Blockers** (if any):
- [description]
```

---

## Mission
Create the consciousness wrapper for morning standup with TDD approach: tests first, then implementation.

**Scope Boundaries**:
- This prompt covers ONLY: Creating the wrapper module and its tests
- NOT in scope: Integration with standup_bridge.py (Phase 2)
- NOT in scope: Running full standup test suite (Phase 3)

---

## Context
- **GitHub Issue**: #632 CONSCIOUSNESS-TRANSFORM: Morning Standup
- **Current State**: Standup works but has mechanical output (5/20 consciousness score)
- **Target State**: Conscious standup output (18+/20 score)
- **Dependencies**: `services/consciousness/validation.py` exists

---

## MANDATORY FIRST ACTIONS

### 1. Infrastructure Verification
```bash
# Verify consciousness framework exists
ls -la services/consciousness/
python -c "from services.consciousness.validation import validate_mvc; print('OK')"

# Verify standup bridge exists (will integrate in Phase 2)
ls -la services/personality/standup_bridge.py

# Check existing consciousness patterns
cat services/consciousness/loading_consciousness.py | head -50
cat services/consciousness/error_consciousness.py | head -50
```

### 2. Understand Current Standup Output
```bash
# See what standup_bridge currently produces
grep -n "def _format" services/personality/standup_bridge.py
grep -n "intro\|header\|section" services/personality/standup_bridge.py
```

STOP if:
- [ ] Consciousness framework doesn't exist
- [ ] validate_mvc import fails
- [ ] Standup bridge doesn't exist

---

## Implementation Approach (TDD)

### Step 1: Create Test File FIRST

Create `tests/unit/services/consciousness/test_standup_consciousness.py`:

```python
"""
Tests for standup consciousness wrapper.
Issue #632 CONSCIOUSNESS-TRANSFORM: Morning Standup
TDD: Tests written FIRST, then implementation.
"""

import pytest
from services.consciousness.validation import validate_mvc


class TestStandupConsciousness:
    """Test consciousness wrapper for standup output."""

    def test_greeting_has_identity(self):
        """Greeting must have identity voice."""
        from services.consciousness.standup_consciousness import format_standup_greeting_conscious

        greeting = format_standup_greeting_conscious(sources=["GitHub", "conversations"])
        assert "I " in greeting or "I'" in greeting, "Greeting must have identity voice"
        assert "GitHub" in greeting or "github" in greeting.lower(), "Should mention sources"

    def test_greeting_has_source_attribution(self):
        """Greeting must attribute data sources."""
        from services.consciousness.standup_consciousness import format_standup_greeting_conscious

        greeting = format_standup_greeting_conscious(sources=["GitHub", "calendar"])
        assert "GitHub" in greeting or "calendar" in greeting, "Should mention data sources"

    def test_accomplishments_has_identity(self):
        """Accomplishments section must have identity voice."""
        from services.consciousness.standup_consciousness import format_accomplishments_conscious

        result = format_accomplishments_conscious(["Fixed bug", "Added feature"])
        assert "I " in result or "you" in result.lower(), "Should have conversational voice"

    def test_accomplishments_adds_context(self):
        """Accomplishments should add helpful context."""
        from services.consciousness.standup_consciousness import format_accomplishments_conscious

        result = format_accomplishments_conscious(["Fixed authentication bug"])
        # Should not just list items but add framing
        assert "Yesterday" in result or "yesterday" in result, "Should frame temporally"

    def test_priorities_has_reasoning(self):
        """Priorities should have reasoning."""
        from services.consciousness.standup_consciousness import format_priorities_conscious

        result = format_priorities_conscious(["Continue A4 work", "Review feedback"])
        assert "today" in result.lower() or "Today" in result, "Should frame temporally"

    def test_blockers_has_epistemic_humility(self):
        """Blockers section should have epistemic humility."""
        from services.consciousness.standup_consciousness import format_blockers_conscious

        result = format_blockers_conscious([])  # No blockers
        # Should say "I didn't spot any" not "No blockers"
        assert "I" in result, "Should have identity even for no blockers"

    def test_blockers_with_items(self):
        """Blockers with items should be helpful."""
        from services.consciousness.standup_consciousness import format_blockers_conscious

        result = format_blockers_conscious(["Waiting for API access"])
        assert "I" in result or "you" in result.lower(), "Should have conversational voice"

    def test_closing_has_dialogue_invitation(self):
        """Closing must invite dialogue."""
        from services.consciousness.standup_consciousness import format_standup_closing_conscious

        result = format_standup_closing_conscious({"generation_time_ms": 1200, "time_saved_minutes": 15})
        assert "?" in result, "Should have question/invitation"

    def test_full_standup_passes_mvc(self):
        """Full standup output must pass MVC validation."""
        from services.consciousness.standup_consciousness import format_full_standup_conscious

        standup_data = {
            "sources": ["GitHub", "conversations"],
            "yesterday_accomplishments": ["Fixed bug", "Added feature"],
            "today_priorities": ["Continue work", "Review feedback"],
            "blockers": [],
            "metrics": {"generation_time_ms": 1200, "time_saved_minutes": 15}
        }

        result = format_full_standup_conscious(standup_data)
        mvc_result = validate_mvc(result)

        assert mvc_result.passes, f"MVC failed: {mvc_result.missing}"

    def test_full_standup_has_all_sections(self):
        """Full standup should have greeting, content, closing."""
        from services.consciousness.standup_consciousness import format_full_standup_conscious

        standup_data = {
            "sources": ["GitHub"],
            "yesterday_accomplishments": ["Did work"],
            "today_priorities": ["More work"],
            "blockers": [],
            "metrics": {"generation_time_ms": 1000}
        }

        result = format_full_standup_conscious(standup_data)

        # Should have identity
        assert "I " in result or "I'" in result
        # Should have invitation
        assert "?" in result
        # Should mention accomplishments
        assert "Did work" in result or "work" in result.lower()
```

**Validation**: `pytest tests/unit/services/consciousness/test_standup_consciousness.py -v`
- Expected: 10 tests collected, all FAIL (no implementation yet)

### Step 2: Create Implementation

Create `services/consciousness/standup_consciousness.py`:

```python
"""
Consciousness Wrapper for Morning Standup

Transforms standup output into conscious narrative expression.
Part of Consciousness Rollout Wave 2 (#632)

Issue: #632 CONSCIOUSNESS-TRANSFORM: Morning Standup
Framework: #407 MUX-VISION-STANDUP-EXTRACT
ADR: ADR-056 Consciousness Expression Patterns
"""

from typing import Any, Dict, List, Optional

from services.consciousness.validation import validate_mvc


def format_standup_greeting_conscious(sources: List[str]) -> str:
    """
    Format standup greeting with consciousness.

    Args:
        sources: List of data sources used (e.g., ["GitHub", "calendar"])

    Returns:
        Conscious greeting with identity and source attribution
    """
    # Build source attribution
    if not sources:
        source_text = "what I know"
    elif len(sources) == 1:
        source_text = f"your {sources[0]} activity"
    else:
        source_text = f"your {', '.join(sources[:-1])} and {sources[-1]}"

    return f"Good morning! I pulled together your standup from yesterday's work.\n\nLooking at {source_text}, here's what I found:"


def format_accomplishments_conscious(accomplishments: List[str]) -> str:
    """
    Format accomplishments with consciousness.

    Args:
        accomplishments: List of accomplishment strings

    Returns:
        Conscious accomplishments section
    """
    if not accomplishments:
        return "**Yesterday**: I didn't find any tracked work, but that might just mean it wasn't captured."

    intro = "**Yesterday** you made solid progress:"
    items = []
    for item in accomplishments:
        # Clean up prefixes
        clean = item.lstrip("✅📋🎯 ")
        items.append(f"• {clean}")

    return f"{intro}\n" + "\n".join(items)


def format_priorities_conscious(priorities: List[str]) -> str:
    """
    Format priorities with consciousness.

    Args:
        priorities: List of priority strings

    Returns:
        Conscious priorities section
    """
    if not priorities:
        return "**For today**: I don't have specific priorities noted. What would you like to focus on?"

    intro = "**For today**, based on your priorities:"
    items = []
    for item in priorities:
        clean = item.lstrip("🎯🔥⭐ ")
        items.append(f"• {clean}")

    return f"{intro}\n" + "\n".join(items)


def format_blockers_conscious(blockers: List[str]) -> str:
    """
    Format blockers with consciousness and epistemic humility.

    Args:
        blockers: List of blocker strings

    Returns:
        Conscious blockers section
    """
    if not blockers:
        return "**Blockers**: I didn't spot any, but let me know if something's come up."

    intro = "**Blockers** I noticed:"
    items = []
    for item in blockers:
        clean = item.lstrip("⚠️❌🚫 ")
        items.append(f"• {clean}")

    return f"{intro}\n" + "\n".join(items)


def format_standup_closing_conscious(metrics: Optional[Dict[str, Any]] = None) -> str:
    """
    Format standup closing with dialogue invitation.

    Args:
        metrics: Optional dict with generation_time_ms, time_saved_minutes

    Returns:
        Conscious closing with invitation
    """
    invitation = "Does this capture it, or should I adjust anything?"

    if metrics and metrics.get("generation_time_ms"):
        time_ms = metrics["generation_time_ms"]
        time_saved = metrics.get("time_saved_minutes", 15)
        return f"\n{invitation}\n\n_(Generated in {time_ms/1000:.1f}s, saved you ~{time_saved}m)_"

    return f"\n{invitation}"


def format_full_standup_conscious(standup_data: Dict[str, Any]) -> str:
    """
    Format complete standup with consciousness.

    Args:
        standup_data: Dict with sources, accomplishments, priorities, blockers, metrics

    Returns:
        Full conscious standup narrative
    """
    sections = []

    # Greeting with source attribution
    sources = standup_data.get("sources", [])
    sections.append(format_standup_greeting_conscious(sources))

    # Content sections
    sections.append(format_accomplishments_conscious(
        standup_data.get("yesterday_accomplishments", [])
    ))
    sections.append(format_priorities_conscious(
        standup_data.get("today_priorities", [])
    ))
    sections.append(format_blockers_conscious(
        standup_data.get("blockers", [])
    ))

    # Closing with invitation
    sections.append(format_standup_closing_conscious(
        standup_data.get("metrics")
    ))

    narrative = "\n\n".join(sections)

    # Validate MVC
    mvc_result = validate_mvc(narrative)
    if not mvc_result.passes:
        # Log but don't fail - consciousness is best-effort
        import logging
        logging.warning(f"Standup MVC validation: {mvc_result}")

    return narrative
```

**Validation**:
```bash
pytest tests/unit/services/consciousness/test_standup_consciousness.py -v
```
- Expected: All 10 tests PASS

### Step 3: Verify MVC Compliance

```bash
python -c "
from services.consciousness.standup_consciousness import format_full_standup_conscious
from services.consciousness.validation import validate_mvc

standup_data = {
    'sources': ['GitHub', 'conversations'],
    'yesterday_accomplishments': ['Fixed authentication bug', 'Added user feedback'],
    'today_priorities': ['Continue A4 work', 'Review user feedback'],
    'blockers': [],
    'metrics': {'generation_time_ms': 1200, 'time_saved_minutes': 15}
}

output = format_full_standup_conscious(standup_data)
print('=== STANDUP OUTPUT ===')
print(output)
print()
print('=== MVC VALIDATION ===')
result = validate_mvc(output)
print(f'Passes: {result.passes}')
print(f'Checks: {result.checks}')
if result.missing:
    print(f'Missing: {result.missing}')
"
```

---

## Success Criteria

- [ ] Test file created with 10+ tests
- [ ] Implementation file created with 6 functions
- [ ] All tests pass (show pytest output)
- [ ] MVC validation passes (show validation output)
- [ ] No assumptions made - all verified

---

## STOP Conditions

If ANY of these occur, STOP and report:
1. Consciousness framework import fails
2. Tests fail after implementation
3. MVC validation cannot pass
4. validate_mvc function behavior unexpected
5. Any assumption needed

---

## Deliverables

1. `tests/unit/services/consciousness/test_standup_consciousness.py` (10+ tests)
2. `services/consciousness/standup_consciousness.py` (6 functions)
3. Terminal output showing all tests pass
4. MVC validation result

---

*Prompt Version: 1.0*
*Template: agent-prompt-template v10.2*
*Phase: 1 of 4*
