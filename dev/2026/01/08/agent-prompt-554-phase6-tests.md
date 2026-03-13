# Agent Prompt: #554 Phase 6 - Create Chat Widget Tests

**Issue**: #554 STANDUP-CHAT-WIDGET
**Phase**: 6 of 6
**Model**: Haiku
**Deployed By**: Lead Developer
**Depends On**: Phases 1-5 complete

---

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete Phase 6 of GitHub Issue #554. Your work is part of a multi-agent coordination chain.

### Your Acceptance Criteria
- [ ] Unit tests for session management
- [ ] Unit tests for toggle functionality
- [ ] All tests passing
- [ ] Test output provided

**Every checkbox must be addressed in your handoff.**

### Your Handoff Format
Return your work with this structure:
```
## Issue #554 Phase 6 Completion Report
**Status**: Complete/Partial/Blocked

**Tests Created**:
- X tests in [file location]

**Test Output**:
```
[paste actual pytest output here]
```

**Test Coverage**:
- Session management: X tests
- Toggle functionality: X tests
- Message handling: X tests (if applicable)

**Blockers** (if any):
- [Blocker description]
```

---

## Mission

Create unit tests for the chat widget JavaScript functionality.

**Scope**: ONLY Phase 6 tests. Implementation should already be complete.

---

## Context

- **GitHub Issue**: #554 STANDUP-CHAT-WIDGET
- **Current State**: Widget fully implemented (Phases 1-5)
- **Target State**: Test coverage for key JS functions
- **Dependencies**: Phases 1-5 complete
- **Testing Approach**: Python tests using pytest (project standard)

---

## Pre-Flight Verification

Before starting, verify implementation exists:

```bash
# Widget files must exist
ls -la web/static/js/chat.js
ls -la web/static/css/chat.css
ls -la templates/components/chat-widget.html

# Check for key functions in chat.js
grep -n "function" web/static/js/chat.js
```

**STOP if files missing** - previous phases incomplete.

---

## Test Strategy

Since this is a JavaScript widget and the project uses pytest (Python), we have two options:

### Option A: Python Integration Tests (Recommended)

Test the widget behavior through HTTP endpoints and template rendering.

**Location**: `tests/unit/web/templates/test_chat_widget.py`

### Option B: JavaScript Unit Tests

If a JS testing framework exists (Jest, Mocha):

```bash
# Check for existing JS test setup
ls package.json
grep -i "jest\|mocha\|test" package.json
```

**Location**: `web/static/js/chat.test.js`

---

## Implementation: Python Tests (Option A)

Create `tests/unit/web/templates/test_chat_widget.py`:

```python
"""
Tests for chat widget component (#554).

Tests:
- Widget template renders correctly
- Widget includes required elements
- Widget JavaScript functionality
- Session persistence logic
"""

import pytest
from pathlib import Path


class TestChatWidgetTemplate:
    """Tests for chat-widget.html template structure."""

    @pytest.fixture
    def widget_html(self):
        """Load the widget template."""
        widget_path = Path("templates/components/chat-widget.html")
        assert widget_path.exists(), "chat-widget.html not found"
        return widget_path.read_text()

    def test_widget_container_exists(self, widget_html):
        """Widget has required container element."""
        assert "chat-widget-container" in widget_html

    def test_widget_toggle_exists(self, widget_html):
        """Widget has toggle button."""
        assert "chat-widget-toggle" in widget_html

    def test_widget_form_exists(self, widget_html):
        """Widget has chat form."""
        assert "chat-form" in widget_html

    def test_widget_input_exists(self, widget_html):
        """Widget has chat input."""
        assert "chat-input" in widget_html

    def test_widget_window_exists(self, widget_html):
        """Widget has chat window for messages."""
        assert "chat-window" in widget_html


class TestChatWidgetCSS:
    """Tests for chat.css styles."""

    @pytest.fixture
    def widget_css(self):
        """Load the widget CSS."""
        css_path = Path("web/static/css/chat.css")
        assert css_path.exists(), "chat.css not found"
        return css_path.read_text()

    def test_floating_position_styles(self, widget_css):
        """CSS includes fixed positioning for floating widget."""
        assert "position: fixed" in widget_css or "position:fixed" in widget_css

    def test_z_index_defined(self, widget_css):
        """CSS defines z-index for layering."""
        assert "z-index" in widget_css

    def test_expanded_state_styles(self, widget_css):
        """CSS includes expanded state styles."""
        assert ".expanded" in widget_css

    def test_toggle_button_styles(self, widget_css):
        """CSS includes toggle button styles."""
        assert "chat-widget-toggle" in widget_css

    def test_responsive_styles(self, widget_css):
        """CSS includes mobile responsive styles."""
        assert "@media" in widget_css


class TestChatWidgetJS:
    """Tests for chat.js functionality."""

    @pytest.fixture
    def widget_js(self):
        """Load the widget JavaScript."""
        js_path = Path("web/static/js/chat.js")
        assert js_path.exists(), "chat.js not found"
        return js_path.read_text()

    def test_toggle_function_exists(self, widget_js):
        """JS includes toggle function."""
        assert "toggleChatWidget" in widget_js

    def test_append_message_function_exists(self, widget_js):
        """JS includes message append function."""
        assert "appendMessage" in widget_js

    def test_session_storage_used(self, widget_js):
        """JS uses localStorage for session persistence."""
        assert "localStorage" in widget_js

    def test_api_endpoint_correct(self, widget_js):
        """JS calls correct API endpoint."""
        assert "/api/v1/intent" in widget_js

    def test_form_submit_handler(self, widget_js):
        """JS includes form submit handling."""
        assert "submit" in widget_js.lower()

    def test_dom_ready_handler(self, widget_js):
        """JS waits for DOM ready."""
        assert "DOMContentLoaded" in widget_js or "addEventListener" in widget_js


class TestChatWidgetIntegration:
    """Integration tests for widget on actual pages."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        from web.app import app
        from fastapi.testclient import TestClient
        return TestClient(app)

    def test_home_page_includes_widget(self, client):
        """Home page includes chat widget."""
        response = client.get("/")
        assert response.status_code == 200
        assert "chat-widget-container" in response.text

    def test_widget_css_accessible(self, client):
        """Chat CSS file is accessible."""
        response = client.get("/static/css/chat.css")
        assert response.status_code == 200
        assert "text/css" in response.headers.get("content-type", "")

    def test_widget_js_accessible(self, client):
        """Chat JS file is accessible."""
        response = client.get("/static/js/chat.js")
        assert response.status_code == 200
        assert "javascript" in response.headers.get("content-type", "")


class TestSessionPersistence:
    """Tests for session persistence logic."""

    @pytest.fixture
    def widget_js(self):
        """Load the widget JavaScript."""
        js_path = Path("web/static/js/chat.js")
        return js_path.read_text()

    def test_session_key_defined(self, widget_js):
        """Session storage key is defined."""
        # Should have a key like 'piper_chat_session' or similar
        assert "SESSION" in widget_js.upper() or "session" in widget_js

    def test_history_storage_defined(self, widget_js):
        """Chat history storage is defined."""
        # Should have history storage
        assert "history" in widget_js.lower() or "HISTORY" in widget_js

    def test_uuid_generation(self, widget_js):
        """Session ID generation uses UUID."""
        assert "randomUUID" in widget_js or "uuid" in widget_js.lower()
```

### Run Tests

```bash
# Run the tests
python -m pytest tests/unit/web/templates/test_chat_widget.py -v

# Expected output format:
# tests/unit/web/templates/test_chat_widget.py::TestChatWidgetTemplate::test_widget_container_exists PASSED
# tests/unit/web/templates/test_chat_widget.py::TestChatWidgetTemplate::test_widget_toggle_exists PASSED
# ... etc
```

---

## Implementation: JavaScript Tests (Option B)

If JS testing framework exists, create `web/static/js/chat.test.js`:

```javascript
// chat.test.js - Unit tests for chat widget

describe('ChatWidget', () => {
    beforeEach(() => {
        // Set up DOM
        document.body.innerHTML = `
            <div class="chat-widget-container" id="chat-widget-container">
                <div class="chat-container">
                    <div id="chat-window"></div>
                    <form id="chat-form">
                        <input id="chat-input" type="text">
                    </form>
                </div>
                <button class="chat-widget-toggle">💬</button>
            </div>
        `;
        // Clear localStorage
        localStorage.clear();
    });

    describe('toggleChatWidget', () => {
        test('adds expanded class when collapsed', () => {
            const container = document.querySelector('.chat-widget-container');
            expect(container.classList.contains('expanded')).toBe(false);

            toggleChatWidget();

            expect(container.classList.contains('expanded')).toBe(true);
        });

        test('removes expanded class when expanded', () => {
            const container = document.querySelector('.chat-widget-container');
            container.classList.add('expanded');

            toggleChatWidget();

            expect(container.classList.contains('expanded')).toBe(false);
        });
    });

    describe('Session Management', () => {
        test('creates session ID if none exists', () => {
            expect(localStorage.getItem('piper_chat_session')).toBeNull();

            getOrCreateSessionId();

            expect(localStorage.getItem('piper_chat_session')).not.toBeNull();
        });

        test('returns existing session ID', () => {
            localStorage.setItem('piper_chat_session', 'test-id-123');

            const result = getOrCreateSessionId();

            expect(result).toBe('test-id-123');
        });
    });

    describe('appendMessage', () => {
        test('adds user message to chat window', () => {
            const chatWindow = document.getElementById('chat-window');

            appendMessage('Hello!', true);

            expect(chatWindow.innerHTML).toContain('Hello!');
            expect(chatWindow.innerHTML).toContain('user-message');
        });

        test('adds bot message to chat window', () => {
            const chatWindow = document.getElementById('chat-window');

            appendMessage('Hi there!', false);

            expect(chatWindow.innerHTML).toContain('Hi there!');
            expect(chatWindow.innerHTML).toContain('bot-message');
        });
    });
});
```

Run with: `npm test` (if Jest configured)

---

## Test Directory Structure

Ensure test directory exists:

```bash
# Create directory if needed
mkdir -p tests/unit/web/templates

# Create __init__.py files
touch tests/unit/web/__init__.py
touch tests/unit/web/templates/__init__.py
```

---

## STOP Conditions

Stop immediately and report if:
- [ ] Implementation files don't exist
- [ ] Tests fail to import required modules
- [ ] Widget structure doesn't match expected
- [ ] Cannot create test directory

**When stopped**: Document the issue, provide error details, wait for Lead Dev.

---

## Evidence Requirements

For EVERY claim:
- **"Created X tests"** → Show test file with count
- **"All tests pass"** → Paste actual pytest output
- **"Covers session management"** → List specific test names

---

## Files Summary

**Create**:
- `tests/unit/web/templates/test_chat_widget.py` (~150 lines, ~20 tests)
- `tests/unit/web/templates/__init__.py` (if missing)
- `tests/unit/web/__init__.py` (if missing)

---

## Remember

- Test the implementation, don't implement features
- Use Python pytest (project standard)
- All tests must pass before claiming complete
- Paste actual test output in handoff
- Evidence for all claims

---

*Prompt Version: 1.0*
*Template: agent-prompt-template v10.2*
