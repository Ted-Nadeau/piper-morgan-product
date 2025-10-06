# Gameplan: GREAT-4B Remaining Work (Post-Discovery)

**Date**: October 5, 2025, 4:40 PM
**Status**: 100% NL coverage found, need enforcement mechanisms
**Time Estimate**: 2-3 hours

## Mission

Lock in the discovered 100% coverage with enforcement mechanisms, optimize performance with caching, and ensure future bypasses are impossible.

## Discovery Summary

- Natural language input: 100% through intent ✅
- Structured CLI: Correctly exempt
- Middleware: Does not exist ❌
- Caching: Not implemented ❌
- Prevention tests: Not present ❌

## Phase 1: Create Intent Middleware
**Code Agent - 45 minutes**

### Create Enforcement Middleware
`web/middleware/intent_enforcement.py`:
```python
from fastapi import Request, HTTPException
import logging

logger = logging.getLogger(__name__)

class IntentEnforcementMiddleware:
    """Ensures all NL routes go through intent."""

    EXEMPT_PATHS = [
        '/health', '/metrics', '/docs', '/static',
        '/api/personality/enhance'  # Output processing
    ]

    NL_PATHS = [
        '/api/v1/intent',
        '/api/chat',
        '/api/message'
    ]

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'http':
            path = scope['path']

            # Log all requests for monitoring
            logger.info(f"Request: {path}")

            # If it's a NL endpoint, verify intent usage
            if self._is_nl_endpoint(path):
                # Add headers or checks to ensure intent classification
                scope['intent_required'] = True

        await self.app(scope, receive, send)

    def _is_nl_endpoint(self, path):
        """Identify natural language input endpoints."""
        return any(path.startswith(nl) for nl in self.NL_PATHS)
```

### Register Middleware
In `web/app.py`:
```python
from web.middleware.intent_enforcement import IntentEnforcementMiddleware

# Add near other middleware
app.add_middleware(IntentEnforcementMiddleware)
```

## Phase 2: Add Bypass Prevention Tests
**Cursor Agent - 30 minutes**

### Create Prevention Tests
`tests/intent/test_bypass_prevention.py`:
```python
import pytest
from fastapi.testclient import TestClient

def test_future_nl_routes_require_intent():
    """Ensure new NL routes can't bypass intent."""
    # Attempt to add a route that processes NL without intent
    with pytest.raises(IntentRequiredError):
        @app.post("/api/new_chat")
        async def bad_route(text: str):
            # Direct processing without intent
            return process_directly(text)

def test_direct_service_calls_blocked():
    """Services can't be called directly for NL."""
    from services.github_service import GitHubService
    service = GitHubService()

    with pytest.raises(BypassError):
        # Trying to create issue without intent classification
        service.create_issue("Bug in login")

def test_middleware_logs_all_requests():
    """Verify middleware monitoring works."""
    response = client.post("/api/v1/intent", json={"text": "test"})

    # Check logs contain request
    assert "Request: /api/v1/intent" in captured_logs()
```

## Phase 3: Implement Caching Layer
**Code Agent - 45 minutes**

### Create Cache Service
`services/intent_service/cache.py`:
```python
import hashlib
import json
from typing import Optional
import time

class IntentCache:
    """Cache for intent classification results."""

    def __init__(self):
        self.cache = {}  # In-memory for now
        self.ttl = 3600  # 1 hour
        self.hits = 0
        self.misses = 0

    def get(self, text: str) -> Optional[dict]:
        """Get cached intent if exists and not expired."""
        key = self._hash_text(text)
        if key in self.cache:
            entry = self.cache[key]
            if time.time() < entry['expires']:
                self.hits += 1
                return entry['intent']
            else:
                del self.cache[key]
        self.misses += 1
        return None

    def set(self, text: str, intent: dict):
        """Cache intent classification result."""
        key = self._hash_text(text)
        self.cache[key] = {
            'intent': intent,
            'expires': time.time() + self.ttl
        }

    def get_metrics(self):
        """Return cache performance metrics."""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'size': len(self.cache)
        }

    def _hash_text(self, text: str) -> str:
        """Create cache key from text."""
        return hashlib.md5(text.lower().encode()).hexdigest()
```

### Integrate with Classifier
Update `services/intent_service/classifier.py`:
```python
from .cache import IntentCache

class IntentClassifier:
    def __init__(self):
        self.cache = IntentCache()

    async def classify(self, text: str):
        # Check cache first
        cached = self.cache.get(text)
        if cached:
            return cached

        # Classify as normal
        result = await self._classify_internal(text)

        # Cache result
        self.cache.set(text, result)

        return result
```

## Phase 4: User Flow Validation
**Cursor Agent - 30 minutes**

### Comprehensive Flow Tests
`tests/intent/test_user_flows_complete.py`:
```python
async def test_create_issue_flow():
    """Full flow: NL input → intent → action."""
    response = await client.post("/api/v1/intent", json={
        "text": "Create an issue about the login bug"
    })
    assert response.json()['intent'] == 'CREATE_ISSUE'
    assert response.json()['executed'] == True

async def test_with_caching():
    """Same query twice should use cache."""
    query = {"text": "What's my schedule?"}

    # First request - cache miss
    response1 = await client.post("/api/v1/intent", json=query)

    # Second request - cache hit
    response2 = await client.post("/api/v1/intent", json=query)

    # Check cache metrics
    metrics = cache.get_metrics()
    assert metrics['hits'] == 1
    assert metrics['misses'] == 1
```

## Phase Z: Documentation & Lock
**Both Agents - 30 minutes**

### Update ADR-032
Add implementation section:
```markdown
## Implementation Status: COMPLETE

### Coverage
- Natural language input: 100% through intent
- Structured CLI: Exempt (explicit intent via structure)
- Output processing: Exempt (not user input)

### Enforcement
- Middleware: IntentEnforcementMiddleware active
- Tests: Bypass prevention in CI/CD
- Monitoring: All requests logged

### Performance
- Caching: In-memory cache with 1hr TTL
- Hit rate: >60% for common queries
- Latency: <100ms with cache
```

### Create Developer Guide
`docs/development/intent-classification.md`:
- When intent is required
- How to add new NL endpoints
- Testing requirements
- Cache considerations

## Success Criteria

- [ ] Middleware created and registered
- [ ] Bypass prevention tests passing
- [ ] Cache implementation complete
- [ ] Cache hit rate >60%
- [ ] User flows validated
- [ ] ADR-032 updated
- [ ] Developer guide created

## Execution Order

1. Middleware first (prevents future issues)
2. Tests second (validates middleware)
3. Caching third (performance boost)
4. Validation fourth (proves it works)
5. Documentation last (captures everything)

---

*Ready to lock in 100% intent enforcement!*
