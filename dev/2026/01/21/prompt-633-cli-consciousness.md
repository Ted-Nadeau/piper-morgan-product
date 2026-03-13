# Claude Code Agent Prompt: #633 CLI Consciousness

## Your Identity
You are Claude Code, implementing consciousness patterns for CLI output.

## Session Log Requirement (MANDATORY)

**Create a session log at start**:
```bash
mkdir -p dev/2026/01/21
touch dev/2026/01/21/$(date +%Y-%m-%d-%H%M)-633-cli-code-log.md
```

---

## Mission
Create CLI consciousness wrapper and integrate into main.py. TDD approach: tests first.

**Scope**:
- Create wrapper module with CLI formatters
- Integrate into main.py startup/shutdown/error messages
- Validate with MVC

---

## Phase 1: Create Wrapper (TDD)

### Step 1: Create Test File FIRST

Create `tests/unit/services/consciousness/test_cli_consciousness.py`:

```python
"""
Tests for CLI consciousness wrapper.
Issue #633 CONSCIOUSNESS-TRANSFORM: CLI Output
"""

import pytest
from services.consciousness.validation import validate_mvc


class TestCLIConsciousness:
    """Test consciousness wrapper for CLI output."""

    def test_startup_message_has_identity(self):
        """Startup message must have identity voice."""
        from services.consciousness.cli_consciousness import format_startup_conscious

        result = format_startup_conscious()
        assert "I" in result or "I'" in result or "me" in result.lower(), "Should have identity"

    def test_ready_message_has_identity(self):
        """Ready message must have identity voice."""
        from services.consciousness.cli_consciousness import format_ready_conscious

        result = format_ready_conscious("http://localhost:8001")
        assert "I" in result or "I'" in result, "Should have identity"
        assert "8001" in result or "localhost" in result, "Should include URL info"

    def test_shutdown_message_has_identity(self):
        """Shutdown message must have identity voice."""
        from services.consciousness.cli_consciousness import format_shutdown_conscious

        result = format_shutdown_conscious()
        assert "I" in result or "me" in result.lower(), "Should have identity"

    def test_success_message_has_identity(self):
        """Success confirmations must have identity voice."""
        from services.consciousness.cli_consciousness import format_cli_success_conscious

        result = format_cli_success_conscious("stored", "your API key")
        assert "I" in result or "I'" in result, "Should have identity"

    def test_error_message_has_invitation(self):
        """Error messages must have dialogue invitation."""
        from services.consciousness.cli_consciousness import format_cli_error_conscious

        result = format_cli_error_conscious("Could not connect to database")
        assert "?" in result, "Should have invitation to retry or get help"
        assert "I" in result or "I'" in result, "Should have identity"

    def test_progress_message_has_identity(self):
        """Progress messages should have identity."""
        from services.consciousness.cli_consciousness import format_progress_conscious

        result = format_progress_conscious("Initializing services", 3, 5)
        assert "I" in result.lower() or "working" in result.lower() or "getting" in result.lower()

    def test_services_ready_message(self):
        """Services ready confirmation should be conversational."""
        from services.consciousness.cli_consciousness import format_services_ready_conscious

        result = format_services_ready_conscious(5)
        assert "5" in result, "Should mention count"

    def test_key_stored_success(self):
        """Key storage success should be conversational."""
        from services.consciousness.cli_consciousness import format_cli_success_conscious

        result = format_cli_success_conscious("stored", "your OpenAI key in the OS keychain")
        assert "I" in result, "Should have identity"
        assert "openai" in result.lower() or "key" in result.lower()
```

### Step 2: Create Implementation

Create `services/consciousness/cli_consciousness.py`:

```python
"""
Consciousness Wrapper for CLI Output

Transforms CLI messages into conscious narrative expression.
Part of Consciousness Rollout Wave 2 (#633)

Issue: #633 CONSCIOUSNESS-TRANSFORM: CLI Output
Framework: #407 MUX-VISION-STANDUP-EXTRACT
"""

from typing import Optional


def format_startup_conscious() -> str:
    """Format startup message with consciousness."""
    return "Starting up... let me get everything ready."


def format_ready_conscious(url: str) -> str:
    """Format ready message with consciousness."""
    return f"I'm up and running! You can find me at {url}"


def format_shutdown_conscious() -> str:
    """Format shutdown message with consciousness."""
    return "Shutting down now. See you next time!"


def format_cli_success_conscious(action: str, detail: str) -> str:
    """Format success confirmation with consciousness."""
    return f"I've {action} {detail}."


def format_cli_error_conscious(error: str) -> str:
    """Format error message with consciousness and invitation."""
    return f"I ran into a problem: {error}. Want me to try again, or can I help troubleshoot?"


def format_progress_conscious(task: str, current: int, total: int) -> str:
    """Format progress message with consciousness."""
    return f"Working on it... {task} ({current}/{total})"


def format_services_ready_conscious(count: int) -> str:
    """Format services ready message with consciousness."""
    return f"All {count} services initialized - looking good."
```

### Step 3: Run Tests

```bash
pytest tests/unit/services/consciousness/test_cli_consciousness.py -v
```

Expected: All 8 tests pass.

---

## Phase 2: Integration

### Update main.py

Add import at top:
```python
from services.consciousness.cli_consciousness import (
    format_startup_conscious,
    format_ready_conscious,
    format_shutdown_conscious,
    format_cli_error_conscious,
    format_cli_success_conscious,
    format_services_ready_conscious,
)
```

Replace mechanical messages:

| Line | Current | New |
|------|---------|-----|
| ~109 | `print("🚀 Starting Piper Morgan...")` | `print(format_startup_conscious())` |
| ~127 | `print(f"   ✓ Services initialized ({len(services)}/{len(services)}")` | `print(f"   {format_services_ready_conscious(len(services))}")` |
| ~137-143 | Ready message block | Use `format_ready_conscious()` |
| ~165 | `print("\n👋 Shutting down gracefully...")` | `print(f"\n{format_shutdown_conscious()}")` |
| ~172 | `print(f"❌ Error: {e}")` | `print(format_cli_error_conscious(str(e)))` |
| ~244 | `print(f"✓ Stored {provider} key...")` | `print(format_cli_success_conscious("stored", f"your {provider} key in the OS keychain"))` |

### Update exports

Add to `services/consciousness/__init__.py`:
```python
from services.consciousness.cli_consciousness import (
    format_startup_conscious,
    format_ready_conscious,
    format_shutdown_conscious,
    format_cli_error_conscious,
    format_cli_success_conscious,
    format_services_ready_conscious,
    format_progress_conscious,
)
```

### Verify Integration

```bash
python main.py --help
# Should work without errors

python -c "from services.consciousness.cli_consciousness import format_startup_conscious; print(format_startup_conscious())"
# Should print conscious message
```

---

## Phase 3: Validation

### Test CLI

```bash
# Start server briefly to see new messages
timeout 5 python main.py || true
```

### Score Against Rubric

Target: 14+/20 (CLI is simpler - no source attribution needed)

| Dimension | Target | Notes |
|-----------|--------|-------|
| Identity Voice | 3/4 | "I" statements throughout |
| Epistemic Humility | 2/4 | Less applicable to CLI |
| Dialogue Orientation | 3/4 | Error messages have invitation |
| Source Transparency | 2/4 | N/A for most CLI |
| Contextual Awareness | 2/4 | Shows counts, URLs |

---

## Deliverables

1. `services/consciousness/cli_consciousness.py` (7 functions)
2. `tests/unit/services/consciousness/test_cli_consciousness.py` (8+ tests)
3. Modified `main.py`
4. Updated `services/consciousness/__init__.py`
5. Session log with evidence

---

## Handoff Format

```
## Issue #633 Completion Report
**Status**: Complete/Partial/Blocked

**Tests**:
- X tests in test_cli_consciousness.py
- pytest output: [paste]

**Integration**:
- Import verification: [output]
- CLI help works: [yes/no]

**Files Modified**:
- services/consciousness/cli_consciousness.py (NEW)
- tests/unit/services/consciousness/test_cli_consciousness.py (NEW)
- main.py (+X/-Y lines)
- services/consciousness/__init__.py (+X lines)

**Rubric Score**: X/20

**Blockers** (if any):
```

---

*Prompt Version: 1.0*
*Issue: #633*
