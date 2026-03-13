# Gameplan: GREAT-4B - Universal Intent Enforcement (REVISED)

**Date**: October 5, 2025
**Epic**: GREAT-4B (Second sub-epic of GREAT-4)
**Context**: Intent classification works but needs universal enforcement
**Expected**: Partial implementation exists (60-75% complete)

## Mission

Find all places where intent classification is bypassed, complete partial implementations, and enforce universal usage. Focus on consistency rather than ground-up building.

## Background from 4A

- Intent classification infrastructure excellent
- Performance <1ms confirmed
- Categories and patterns comprehensive (44 patterns)
- Test coverage 92%
- Now need 100% enforcement

## Phase -1: Infrastructure Discovery
**Lead Developer - ALWAYS DO FIRST**

Map the current state before making changes:
```bash
# Count all entry points
echo "=== Web Routes ==="
grep -r "@app\." web/ --include="*.py" | wc -l
grep -r "@router\." services/ --include="*.py" | wc -l

echo "=== CLI Commands ==="
ls -la cli/commands/*.py | wc -l
grep -r "def execute" cli/ --include="*.py" | wc -l

echo "=== Slack Handlers ==="
grep -r "slack.*event\|@slack" services/integrations/slack/ --include="*.py"

echo "=== Direct Service Calls ==="
grep -r "services\.[a-z_]*\." web/ --include="*.py" | grep -v "intent" | wc -l

echo "=== Existing Middleware ==="
grep -r "middleware\|Middleware" web/ --include="*.py"
find . -name "*middleware*" -type f
```

Create `dev/2025/10/05/infrastructure-discovery.md` with findings.

## Phase 0: Baseline Measurement
**Both Agents - Simple task**

### Create Measurement Script
`scripts/map_intent_usage.py`:
```python
import os
import re
from pathlib import Path

def map_intent_usage():
    """Map current intent classification usage."""

    results = {
        'web_routes': {'total': 0, 'using_intent': 0, 'bypassing': []},
        'cli_commands': {'total': 0, 'using_intent': 0, 'bypassing': []},
        'api_endpoints': {'total': 0, 'using_intent': 0, 'bypassing': []},
        'slack_handlers': {'total': 0, 'using_intent': 0, 'bypassing': []},
        'direct_calls': {'total': 0, 'locations': []}
    }

    # Scan each category
    # Document WHY each bypass exists (comment in code?)

    return {
        'summary': {
            'total_entry_points': sum_totals,
            'using_intent': sum_intent,
            'percentage': (sum_intent / sum_totals * 100),
            'bypassing': sum_bypassing
        },
        'details': results
    }
```

### Document Bypass Reasons
For each bypass, note:
- Performance concern?
- Legacy code (pre-intent)?
- Developer shortcut?
- Special requirement?

## Phase 1: Middleware Completion
**Code Agent - Medium complexity**

### Check Existing Middleware
```python
# Expected locations (check all)
possible_middleware = [
    'web/middleware/intent_middleware.py',
    'web/middleware.py',
    'services/intent_service/middleware.py',
    'web/intent.py'
]
```

### Create or Complete Middleware
```python
# web/middleware/intent_middleware.py
from fastapi import Request, Response
from services.intent_service import classifier
import logging

logger = logging.getLogger(__name__)

class IntentMiddleware:
    """Universal intent classification middleware."""

    def __init__(self, app):
        self.app = app
        self.bypass_paths = ['/health', '/metrics', '/docs']

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'http':
            path = scope['path']

            # Allow certain paths to bypass
            if path in self.bypass_paths:
                await self.app(scope, receive, send)
                return

            # Extract and classify intent
            # Attach to request state
            # Log for monitoring

        await self.app(scope, receive, send)
```

### Register Middleware
```python
# In web/app.py
from web.middleware.intent_middleware import IntentMiddleware

app.add_middleware(IntentMiddleware)
```

## Phase 2: Interface Conversion
**Both Agents - Complex task**

### Web UI Routes (Code)
Convert each bypassing route:
```python
# Pattern to find bypasses
# @app.post("/api/github/...")  # Direct service call

# Convert to:
@app.post("/api/intent")
async def universal_intent_handler(request: IntentRequest):
    intent = await classifier.classify(request.text)
    return await intent_router.route(intent)
```

### CLI Commands (Cursor)
Wrap all commands with intent:
```python
# cli/commands/base_command.py
def execute_with_intent(self, *args, **kwargs):
    # Convert command to natural language
    user_input = self.to_natural_language(*args, **kwargs)

    # Classify intent
    intent = classifier.classify(user_input)

    # Route through intent system
    return intent_service.process(intent)
```

### Slack Handlers (Code)
Intercept all events:
```python
# services/integrations/slack/event_handler.py
async def handle_slack_event(event):
    # Extract message text
    text = event.get('text', '')

    # Classify intent
    intent = await classifier.classify(text)

    # Process through intent system
    return await intent_service.process(intent)
```

## Phase 3: Bypass Elimination
**Code Agent - Medium complexity**

### Remove Direct Routes
```bash
# Find all direct routes
grep -r "@app.route\|@router" . --include="*.py" | grep -v "intent"

# Delete or comment with explanation
# Document in removal-log.md
```

### Add Service Guards
```python
# services/base_service.py
class BaseService:
    def _require_intent(self):
        """Ensure service called via intent."""
        import inspect
        frame = inspect.currentframe().f_back
        if 'intent' not in frame.f_locals:
            raise BypassError("Service must be called via intent classification")
```

### Create Detection Tests
```python
# tests/intent/test_no_bypasses.py
import pytest
from fastapi.testclient import TestClient

def test_no_direct_github_access():
    """Ensure GitHub endpoints require intent."""
    response = client.post("/api/github/create_issue", json={})
    assert response.status_code in [404, 403]

def test_cli_uses_intent(mock_classifier):
    """Ensure CLI commands use intent."""
    from cli.commands import create_issue
    create_issue.execute(title="Test")
    mock_classifier.classify.assert_called()
```

## Phase 4: Caching Implementation
**Cursor Agent - Medium complexity**

### Add Caching Layer
```python
# services/intent_service/cache.py
import hashlib
from typing import Optional
import redis

class IntentCache:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.ttl = 3600  # 1 hour

    def get_cached_intent(self, text: str) -> Optional[Intent]:
        key = self._generate_key(text)
        cached = self.redis.get(key)
        if cached:
            return Intent.from_json(cached)
        return None

    def cache_intent(self, text: str, intent: Intent):
        key = self._generate_key(text)
        self.redis.setex(key, self.ttl, intent.to_json())
```

### Monitor Cache Performance
```python
# Add metrics
cache_hits = 0
cache_misses = 0
cache_hit_rate = cache_hits / (cache_hits + cache_misses)
```

## Phase 5: User Flow Validation
**Both Agents - Medium complexity**

### Test All Documented Flows
```python
# tests/intent/test_user_flows.py
class TestUserFlows:
    async def test_create_issue_flow(self):
        """Create GitHub issue through intent."""
        response = await client.post("/api/intent", json={
            "text": "Create an issue about the login bug"
        })
        assert response.status_code == 200
        assert response.json()['intent'] == 'CREATE_ISSUE'

    async def test_standup_flow(self):
        """Get standup through intent."""
        response = await client.post("/api/intent", json={
            "text": "Show me my standup"
        })
        assert response.status_code == 200
        assert response.json()['intent'] == 'STATUS'
```

## Phase Z: Final Validation
**Both Agents**

### Run Final Measurement
```bash
# Compare before and after
echo "=== BEFORE ==="
cat dev/2025/10/05/baseline-intent-usage.json

echo "=== AFTER ==="
python scripts/map_intent_usage.py

# Should show 100% intent usage
```

### Performance Check
```bash
python scripts/benchmark_intent.py --with-cache
# Should show <100ms with cache benefits
```

### Documentation
- Update ADR-032 with enforcement details
- Create migration guide for future developers
- Document caching strategy

## Success Criteria

- [ ] Baseline measurement documented
- [ ] All entry points mapped
- [ ] Middleware completed and active
- [ ] 100% endpoints using intent
- [ ] 0 bypass routes remain
- [ ] Cache hit rate >60%
- [ ] Performance <100ms maintained
- [ ] All user flows validated
- [ ] Detection tests passing

## Anti-80% Tracking

Update after each phase:
```
Interface    | Found | Mapped | Converted | Tested | Blocked | Cached
------------ | ----- | ------ | --------- | ------ | ------- | ------
Web UI       | [ ]   | [ ]    | [ ]       | [ ]    | [ ]     | [ ]
CLI          | [ ]   | [ ]    | [ ]       | [ ]    | [ ]     | [ ]
API          | [ ]   | [ ]    | [ ]       | [ ]    | [ ]     | [ ]
Slack        | [ ]   | [ ]    | [ ]       | [ ]    | [ ]     | [ ]
Webhooks     | [ ]   | [ ]    | [ ]       | [ ]    | [ ]     | [ ]
Middleware   | [ ]   | [ ]    | [ ]       | [ ]    | [ ]     | [ ]
Direct calls | [ ]   | [ ]    | [ ]       | [ ]    | [ ]     | [ ]
```

## Effort Indicators

- Phase -1: Discovery (simple)
- Phase 0: Baseline (simple)
- Phase 1: Middleware (medium)
- Phase 2: Conversion (complex)
- Phase 3: Elimination (medium)
- Phase 4: Caching (medium)
- Phase 5: Validation (medium)
- Phase Z: Final (simple)

## Critical Notes

- **Expect partial implementation** - Don't rebuild what exists
- **Document bypass reasons** - Understand the why
- **Preserve performance** - Caching is critical
- **No files in root** - Use dev/2025/10/05/

---

*Ready to enforce universal intent classification!*
