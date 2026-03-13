# Prompt for Cursor Agent: GREAT-4B Phase 0 - Bypass Detection Tests

## Your Identity
You are Cursor Agent, starting Phase 0 work on GREAT-4B after completing GREAT-4A documentation.

## Context from Phase -1

Infrastructure discovery confirms intent system is ~95% built. Need to create detection tests to ensure no bypasses exist or get added in future.

**Your task: Create bypass detection test suite.**

## Session Log Management

Create session log at: `dev/2025/10/05/2025-10-05-1540-prog-cursor-log.md`

## Mission

**Create comprehensive test suite** that detects if any entry point bypasses intent classification, preventing future regressions.

---

## Phase 0: Bypass Detection Tests

### Step 1: Create Web Bypass Detection Test

Create: `tests/intent/test_no_web_bypasses.py`

```python
"""
Test that all web routes enforce intent classification.
No direct service access should be possible.
"""
import pytest
from fastapi.testclient import TestClient
from web.app import app

client = TestClient(app)

class TestWebIntentEnforcement:
    """Ensure all web routes use intent classification."""

    def test_intent_endpoint_exists(self):
        """Verify /api/v1/intent endpoint is available."""
        response = client.post("/api/v1/intent", json={
            "text": "What day is it?"
        })
        assert response.status_code in [200, 422]  # 200 success or 422 validation

    def test_no_direct_github_access(self):
        """Ensure GitHub endpoints require intent."""
        # Try to access GitHub service directly
        response = client.post("/api/github/create_issue", json={
            "title": "Test",
            "body": "Test"
        })
        # Should be 404 (doesn't exist) or 403 (forbidden)
        assert response.status_code in [404, 403, 405]

    def test_no_direct_slack_access(self):
        """Ensure Slack endpoints require intent."""
        response = client.post("/api/slack/send_message", json={
            "channel": "test",
            "text": "test"
        })
        assert response.status_code in [404, 403, 405]

    def test_no_direct_notion_access(self):
        """Ensure Notion endpoints require intent."""
        response = client.post("/api/notion/create_page", json={
            "title": "Test"
        })
        assert response.status_code in [404, 403, 405]

    def test_no_direct_calendar_access(self):
        """Ensure Calendar endpoints require intent."""
        response = client.get("/api/calendar/events")
        assert response.status_code in [404, 403, 405]

    def test_health_endpoint_allowed(self):
        """Health checks are explicitly allowed to bypass."""
        response = client.get("/health")
        # Health should work (200) or not exist (404)
        assert response.status_code in [200, 404]

    def test_docs_endpoint_allowed(self):
        """Documentation is explicitly allowed to bypass."""
        response = client.get("/docs")
        # Docs should work or not exist
        assert response.status_code in [200, 404]
```

### Step 2: Create CLI Bypass Detection Test

Create: `tests/intent/test_no_cli_bypasses.py`

```python
"""
Test that all CLI commands use intent classification.
"""
import pytest
from unittest.mock import Mock, patch
from pathlib import Path

class TestCLIIntentEnforcement:
    """Ensure all CLI commands use intent classification."""

    @pytest.fixture
    def mock_classifier(self):
        """Mock intent classifier for testing."""
        with patch('services.intent_service.classifier.classifier') as mock:
            yield mock

    def test_standup_uses_intent(self, mock_classifier):
        """Standup command should use intent."""
        from cli.commands.standup import StandupCommand

        cmd = StandupCommand()
        # Execute command
        # Verify classifier was called
        # mock_classifier.classify.assert_called()
        pass  # Implement based on actual CLI structure

    def test_all_commands_import_intent(self):
        """All CLI commands should import intent service."""
        cli_commands = Path('cli/commands')

        for file in cli_commands.glob('*.py'):
            if file.name == '__init__.py':
                continue

            content = file.read_text()

            # Each command should reference intent somehow
            has_intent_ref = (
                'intent' in content.lower() or
                'CanonicalHandlers' in content or
                'IntentService' in content
            )

            # If this fails, that command bypasses intent
            assert has_intent_ref, f"{file.name} does not use intent classification"
```

### Step 3: Create Slack Bypass Detection Test

Create: `tests/intent/test_no_slack_bypasses.py`

```python
"""
Test that Slack integration uses intent classification.
"""
import pytest
from pathlib import Path

class TestSlackIntentEnforcement:
    """Ensure Slack handlers use intent classification."""

    def test_slack_handlers_use_intent(self):
        """All Slack event handlers should use intent."""
        slack_dir = Path('services/integrations/slack')

        # Find all handler files
        handler_files = [
            f for f in slack_dir.glob('**/*.py')
            if 'handler' in f.name.lower() or 'event' in f.name.lower()
        ]

        for file in handler_files:
            content = file.read_text()

            # Check if file mentions intent
            has_intent = 'intent' in content.lower()

            # If this is a handler file, it should use intent
            if 'handler' in file.name.lower():
                assert has_intent, f"{file.name} handler does not use intent"
```

### Step 4: Create Automated Bypass Scanner

Create: `scripts/scan_for_bypasses.py`

```python
"""
Automated scanner for intent classification bypasses.
Run this in CI to detect regressions.
"""
import re
from pathlib import Path

def scan_for_bypasses():
    """Scan codebase for potential intent bypasses."""

    bypasses = []

    # Scan web routes
    for file in Path('web').glob('**/*.py'):
        content = file.read_text()

        # Find routes that don't mention intent
        routes = re.findall(r'@(?:app|router)\.(get|post|put|delete)\(["\']([^"\']+)', content)

        for method, path in routes:
            # Exempt certain paths
            if path in ['/health', '/metrics', '/docs', '/api/v1/intent']:
                continue

            # Check if this route uses intent
            route_start = content.find(f'@app.{method}')
            if route_start == -1:
                route_start = content.find(f'@router.{method}')

            next_500 = content[route_start:route_start+500]

            if 'intent' not in next_500.lower():
                bypasses.append({
                    'type': 'web_route',
                    'file': str(file),
                    'method': method.upper(),
                    'path': path
                })

    # Scan CLI commands
    for file in Path('cli/commands').glob('*.py'):
        if file.name == '__init__.py':
            continue

        content = file.read_text()
        if 'intent' not in content.lower():
            bypasses.append({
                'type': 'cli_command',
                'file': str(file),
                'command': file.stem
            })

    return bypasses

if __name__ == "__main__":
    bypasses = scan_for_bypasses()

    if bypasses:
        print(f"⚠️  FOUND {len(bypasses)} POTENTIAL BYPASSES:")
        for b in bypasses:
            if b['type'] == 'web_route':
                print(f"  {b['method']:6} {b['path']:40} ({b['file']})")
            elif b['type'] == 'cli_command':
                print(f"  CLI    {b['command']:40} ({b['file']})")
        exit(1)
    else:
        print("✅ NO BYPASSES DETECTED")
        exit(0)
```

### Step 5: Document Test Strategy

Create: `dev/2025/10/05/bypass-detection-strategy.md`

```markdown
# Intent Bypass Detection Strategy

## Purpose
Ensure 100% of user interactions go through intent classification.
Prevent regressions where new code bypasses intent layer.

## Test Types

### 1. Unit Tests (pytest)
- `test_no_web_bypasses.py` - Web route enforcement
- `test_no_cli_bypasses.py` - CLI command enforcement
- `test_no_slack_bypasses.py` - Slack handler enforcement

### 2. Automated Scanner
- `scripts/scan_for_bypasses.py` - Static code analysis
- Runs in CI on every PR
- Fails build if bypasses detected

### 3. Integration Tests
- End-to-end flows verify intent usage
- User scenarios test full path

## Running Tests

```bash
# Run all bypass detection tests
pytest tests/intent/test_no_*_bypasses.py -v

# Run automated scanner
python3 scripts/scan_for_bypasses.py

# Both should pass for GREAT-4B completion
```

## CI Integration

Add to `.github/workflows/`:
```yaml
- name: Scan for intent bypasses
  run: python3 scripts/scan_for_bypasses.py
```
```

---

## Success Criteria

- [ ] Web bypass tests created
- [ ] CLI bypass tests created
- [ ] Slack bypass tests created
- [ ] Automated scanner created
- [ ] Test strategy documented
- [ ] Tests run successfully
- [ ] GitHub #206 updated

---

## Deliverables

1. **Test Files**: 3 test files in `tests/intent/`
2. **Scanner Script**: `scripts/scan_for_bypasses.py`
3. **Documentation**: `bypass-detection-strategy.md`
4. **Evidence**: pytest output showing tests pass/fail

---

## Evidence Format

```bash
$ pytest tests/intent/test_no_web_bypasses.py -v
========================= test session starts =========================
tests/intent/test_no_web_bypasses.py::test_intent_endpoint_exists PASSED
tests/intent/test_no_web_bypasses.py::test_no_direct_github_access PASSED
tests/intent/test_no_web_bypasses.py::test_health_endpoint_allowed PASSED
========================= 3 passed in 0.45s =========================

$ python3 scripts/scan_for_bypasses.py
✅ NO BYPASSES DETECTED
```

---

**Remember**: These are DETECTION tests - they identify bypasses but don't fix them. Code agent will handle actual conversions.

---

*Template Version: 9.0*
*Task: Bypass Detection Tests for GREAT-4B Phase 0*
*Estimated Effort: Small (30-45 minutes)*
