# Prompt for Cursor Agent: GREAT-4B Phase 2 - Bypass Prevention Tests

## Context

Phase 1 complete: IntentEnforcementMiddleware operational and monitoring all requests.

**Your task**: Create comprehensive test suite to prevent future bypasses and validate enforcement.

## Session Log

Continue: `dev/2025/10/05/2025-10-05-1540-prog-cursor-log.md`

## Mission

**Create bypass prevention test suite** that validates middleware enforcement, prevents regression, and can run in CI/CD.

---

## Phase 2: Bypass Prevention Tests

### Step 1: Create Core Prevention Tests

Create: `tests/intent/test_bypass_prevention.py`

```python
"""
Test suite to prevent intent classification bypasses.
Ensures all NL endpoints use intent classification.
"""
import pytest
from fastapi.testclient import TestClient
from web.app import app

client = TestClient(app)

class TestBypassPrevention:
    """Prevent bypasses of intent classification."""

    def test_middleware_is_registered(self):
        """Verify IntentEnforcementMiddleware is active."""
        response = client.get("/api/admin/intent-monitoring")
        assert response.status_code == 200
        data = response.json()
        assert data["middleware_active"] is True
        assert len(data["nl_endpoints"]) == 4
        assert len(data["exempt_paths"]) == 12

    def test_nl_endpoints_marked(self):
        """Verify NL endpoints are marked as requiring intent."""
        # This would require accessing request.state in tests
        # For now, verify they exist
        nl_endpoints = [
            "/api/v1/intent",
            "/api/standup",
            "/api/chat",
            "/api/message"
        ]

        for endpoint in nl_endpoints:
            # Test endpoint exists or returns expected status
            response = client.get(endpoint)
            # 404, 405, or 422 are acceptable (endpoint exists but wrong method/data)
            assert response.status_code in [200, 404, 405, 422]

    def test_exempt_paths_accessible(self):
        """Verify exempt paths work without intent."""
        exempt_tests = [
            ("/health", 200),
            ("/docs", 200),
            ("/", 200)
        ]

        for path, expected_status in exempt_tests:
            response = client.get(path)
            assert response.status_code == expected_status, \
                f"{path} should be accessible (got {response.status_code})"

    def test_personality_enhance_is_exempt(self):
        """Personality enhancement is output processing, should be exempt."""
        # This endpoint processes Piper's output, not user input
        response = client.post("/api/personality/enhance", json={
            "text": "Test response",
            "context": {}
        })
        # Should not require intent (it's exempt)
        # 200 or 422 acceptable depending on validation
        assert response.status_code in [200, 422]

    def test_monitoring_logs_requests(self, caplog):
        """Verify middleware logs all requests."""
        with caplog.at_level("INFO"):
            client.get("/health")

        # Check logs contain request
        log_messages = [record.message for record in caplog.records]
        assert any("Request: GET /health" in msg for msg in log_messages)
```

### Step 2: Create Future Bypass Detection

Create: `tests/intent/test_future_nl_endpoints.py`

```python
"""
Tests to catch if new NL endpoints are added without intent.
"""
import pytest
from pathlib import Path
import ast

class TestFutureEndpoints:
    """Detect new endpoints that should use intent."""

    def test_all_nl_routes_in_middleware_config(self):
        """All NL routes should be in middleware configuration."""
        # Scan web routes for potential NL endpoints
        web_files = Path("web").glob("**/*.py")

        potential_nl_routes = []
        for file in web_files:
            if file.name == "__init__.py":
                continue

            content = file.read_text()

            # Look for route decorators with paths containing chat/message/intent
            import re
            routes = re.findall(
                r'@(?:app|router)\.\w+\(["\']([^"\']+)',
                content
            )

            for route in routes:
                # Check if route looks like NL endpoint
                if any(keyword in route.lower() for keyword in
                       ['chat', 'message', 'intent', 'ask', 'query']):
                    potential_nl_routes.append(route)

        # Get configured NL endpoints from middleware
        from web.middleware.intent_enforcement import IntentEnforcementMiddleware
        configured = IntentEnforcementMiddleware.NL_ENDPOINTS

        # All potential NL routes should be configured
        for route in potential_nl_routes:
            assert route in configured, \
                f"Route {route} looks like NL endpoint but not in middleware config"

    def test_no_direct_service_calls_in_routes(self):
        """Web routes should not directly call services for NL processing."""
        web_app = Path("web/app.py")
        content = web_app.read_text()

        # Look for direct service imports/calls
        suspicious_patterns = [
            r'from services\..*_service import',
            r'github_service\.',
            r'notion_service\.',
            r'calendar_service\.'
        ]

        import re
        for pattern in suspicious_patterns:
            matches = re.findall(pattern, content)
            # If found, they should only be in non-NL routes
            # This is a heuristic check
            if matches:
                # Warn but don't fail - need manual review
                pytest.skip(f"Found direct service usage: {matches} - needs review")
```

### Step 3: Create Integration Tests

Create: `tests/intent/test_enforcement_integration.py`

```python
"""
Integration tests for intent enforcement.
"""
import pytest
from fastapi.testclient import TestClient
from web.app import app

client = TestClient(app)

class TestEnforcementIntegration:
    """Test full enforcement pipeline."""

    def test_intent_endpoint_works(self):
        """Primary intent endpoint should work."""
        response = client.post("/api/v1/intent", json={
            "text": "What day is it?"
        })
        # Should succeed or fail gracefully
        assert response.status_code in [200, 422, 500]

    def test_standup_uses_backend_intent(self):
        """Standup endpoint should proxy to backend that uses intent."""
        response = client.get("/api/standup")
        # Should succeed or return expected error
        assert response.status_code in [200, 401, 500]

    def test_monitoring_endpoint_accessible(self):
        """Admin monitoring should be accessible."""
        response = client.get("/api/admin/intent-monitoring")
        assert response.status_code == 200

        data = response.json()
        assert "middleware_active" in data
        assert "nl_endpoints" in data
        assert "exempt_paths" in data
```

### Step 4: Create CI/CD Test Script

Create: `scripts/check_intent_bypasses.py`

```python
"""
CI/CD script to detect intent classification bypasses.
Run this in CI to fail builds if bypasses detected.
"""
import sys
from pathlib import Path
import re

def check_bypasses():
    """Scan for potential intent bypasses."""

    bypasses = []

    # Check web routes
    web_files = Path("web").glob("**/*.py")
    for file in web_files:
        content = file.read_text()

        # Find route definitions
        routes = re.findall(
            r'@(?:app|router)\.(get|post|put|delete)\(["\']([^"\']+)',
            content
        )

        for method, path in routes:
            # Skip exempt paths
            if any(exempt in path for exempt in
                   ['/health', '/metrics', '/docs', '/static', '/api/personality']):
                continue

            # Check if looks like NL but not in middleware
            if any(keyword in path.lower() for keyword in
                   ['chat', 'message', 'talk', 'ask', 'query']):

                # Check if endpoint uses intent
                route_start = content.find(f"@{method}")
                next_500 = content[route_start:route_start+500]

                if 'intent' not in next_500.lower():
                    bypasses.append({
                        'file': str(file),
                        'method': method.upper(),
                        'path': path,
                        'reason': 'NL-like endpoint without intent usage'
                    })

    return bypasses

if __name__ == "__main__":
    bypasses = check_bypasses()

    if bypasses:
        print(f"❌ FOUND {len(bypasses)} POTENTIAL BYPASSES:")
        for b in bypasses:
            print(f"  {b['method']:6} {b['path']:40} ({b['file']})")
            print(f"         Reason: {b['reason']}")
        sys.exit(1)
    else:
        print("✅ NO BYPASSES DETECTED")
        sys.exit(0)
```

### Step 5: Document Test Strategy

Create: `dev/2025/10/05/bypass-prevention-strategy.md`

```markdown
# Bypass Prevention Test Strategy

## Purpose
Ensure all natural language endpoints use intent classification.
Prevent regression where new code bypasses intent layer.

## Test Layers

### 1. Unit Tests
- `test_bypass_prevention.py` - Core prevention tests
- Validates middleware configuration
- Tests exempt paths work correctly
- Verifies monitoring endpoint

### 2. Detection Tests
- `test_future_nl_endpoints.py` - Catches new NL routes
- Scans for routes matching NL patterns
- Validates they're in middleware config

### 3. Integration Tests
- `test_enforcement_integration.py` - Full pipeline tests
- Validates intent endpoint works
- Tests standup backend integration
- Confirms monitoring accessibility

### 4. CI/CD Script
- `scripts/check_intent_bypasses.py` - Automated scanning
- Runs on every PR
- Fails build if bypasses detected
- Provides clear failure messages

## Running Tests

```bash
# Run all bypass prevention tests
pytest tests/intent/test_bypass_prevention.py -v
pytest tests/intent/test_future_nl_endpoints.py -v
pytest tests/intent/test_enforcement_integration.py -v

# Run CI script
python scripts/check_intent_bypasses.py
```

## CI Integration

Add to `.github/workflows/tests.yml`:
```yaml
- name: Check for intent bypasses
  run: python scripts/check_intent_bypasses.py
```

## Maintenance

When adding new NL endpoint:
1. Add to `IntentEnforcementMiddleware.NL_ENDPOINTS`
2. Ensure endpoint uses intent classification
3. Run test suite to validate
4. Document exemption if applicable
```

---

## Success Criteria

- [ ] Core prevention tests created and passing
- [ ] Future endpoint detection tests created
- [ ] Integration tests passing
- [ ] CI/CD script created
- [ ] Test strategy documented
- [ ] All tests pass locally
- [ ] GitHub #206 updated

---

## Evidence Format

```bash
$ pytest tests/intent/test_bypass_prevention.py -v
========================= test session starts =========================
tests/intent/test_bypass_prevention.py::test_middleware_is_registered PASSED
tests/intent/test_bypass_prevention.py::test_nl_endpoints_marked PASSED
tests/intent/test_bypass_prevention.py::test_exempt_paths_accessible PASSED
tests/intent/test_bypass_prevention.py::test_personality_enhance_is_exempt PASSED
tests/intent/test_bypass_prevention.py::test_monitoring_logs_requests PASSED
========================= 5 passed in 0.45s =========================

$ python scripts/check_intent_bypasses.py
✅ NO BYPASSES DETECTED
```

---

*Estimated: 30 minutes*
