# Prompt for Code Agent: GREAT-4B Phase 1 - Intent Enforcement Middleware

## Context

Discovery complete: 100% NL input coverage exists, but no architectural enforcement to prevent future bypasses.

**Your task**: Create middleware that enforces intent classification and prevents future bypasses.

## Session Log

Continue: `dev/2025/10/05/2025-10-05-1540-prog-code-log.md`

## Mission

**Create IntentEnforcementMiddleware** to monitor requests, enforce intent usage on NL endpoints, and prevent future bypasses architecturally.

---

## Phase 1: Middleware Creation

### Step 1: Create Middleware File

Create: `web/middleware/intent_enforcement.py`

```python
from fastapi import Request
import logging

logger = logging.getLogger(__name__)

class IntentEnforcementMiddleware:
    """
    Enforces intent classification for natural language endpoints.
    Monitors all requests and prevents future bypasses.
    """

    # Paths that explicitly don't need intent
    EXEMPT_PATHS = [
        '/health',
        '/metrics',
        '/docs',
        '/openapi.json',
        '/static',
        '/api/personality/enhance'  # Output processing, not input
    ]

    # Natural language input endpoints (must use intent)
    NL_ENDPOINTS = [
        '/api/v1/intent',
        '/api/chat',
        '/api/message',
        '/api/standup'
    ]

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'http':
            path = scope['path']
            method = scope['method']

            # Log all requests for monitoring
            logger.info(f"Request: {method} {path}")

            # Check if this is a NL endpoint
            if self._is_nl_endpoint(path):
                # Mark that intent is required
                if 'state' not in scope:
                    scope['state'] = {}
                scope['state']['intent_required'] = True
                logger.debug(f"Intent required for: {path}")

            # Check if exempt
            if self._is_exempt(path):
                logger.debug(f"Exempt from intent: {path}")

        await self.app(scope, receive, send)

    def _is_nl_endpoint(self, path: str) -> bool:
        """Check if path is a natural language endpoint."""
        return any(path.startswith(endpoint) for endpoint in self.NL_ENDPOINTS)

    def _is_exempt(self, path: str) -> bool:
        """Check if path is exempt from intent requirement."""
        return any(path.startswith(exempt) for exempt in self.EXEMPT_PATHS)
```

### Step 2: Register Middleware

Edit `web/app.py`:

```python
# Add import at top
from web.middleware.intent_enforcement import IntentEnforcementMiddleware

# Find where middleware is registered (look for app.add_middleware)
# Add after other middleware:
app.add_middleware(IntentEnforcementMiddleware)
```

**Verify location**:
```bash
grep -n "add_middleware" web/app.py
# Add after existing middleware registrations
```

### Step 3: Test Middleware Registration

```bash
# Start server
python main.py

# Should see in logs:
# "IntentEnforcementMiddleware registered"

# Test a request
curl http://localhost:8001/api/v1/intent -X POST -d '{"text":"test"}'

# Check logs for:
# "Request: POST /api/v1/intent"
# "Intent required for: /api/v1/intent"
```

### Step 4: Add Monitoring Endpoint

Add to `web/app.py`:

```python
@app.get("/api/admin/intent-monitoring")
async def intent_monitoring():
    """Show intent enforcement status."""
    return {
        "middleware_active": True,
        "nl_endpoints": IntentEnforcementMiddleware.NL_ENDPOINTS,
        "exempt_paths": IntentEnforcementMiddleware.EXEMPT_PATHS,
        "monitoring": "All requests logged"
    }
```

Test:
```bash
curl http://localhost:8001/api/admin/intent-monitoring
```

### Step 5: Document Middleware

Create: `dev/2025/10/05/middleware-implementation.md`

```markdown
# Intent Enforcement Middleware Implementation

## Purpose
Monitor all HTTP requests and enforce intent classification on natural language endpoints.

## How It Works
1. Intercepts all HTTP requests via FastAPI middleware
2. Logs every request for monitoring
3. Marks NL endpoints as requiring intent
4. Exempts static/health/output endpoints

## Configuration

### NL Endpoints (require intent)
- /api/v1/intent
- /api/chat
- /api/message
- /api/standup

### Exempt Paths (don't need intent)
- /health, /metrics, /docs
- /static/*
- /api/personality/enhance (output processing)

## Adding New Endpoints

If adding a new NL endpoint:
1. Add to NL_ENDPOINTS list
2. Ensure endpoint uses intent classification
3. Test with monitoring endpoint

If adding exempt endpoint:
1. Document WHY it's exempt
2. Add to EXEMPT_PATHS list
```

---

## Success Criteria

- [ ] Middleware file created
- [ ] Middleware registered in app.py
- [ ] Server starts without errors
- [ ] Monitoring endpoint accessible
- [ ] Logs show request tracking
- [ ] Documentation complete
- [ ] Git commit created

---

## Evidence Format

```bash
$ python main.py
INFO: IntentEnforcementMiddleware registered
INFO: Server running on port 8001

$ curl http://localhost:8001/api/v1/intent -X POST -d '{"text":"test"}'
# Check logs:
INFO: Request: POST /api/v1/intent
DEBUG: Intent required for: /api/v1/intent

$ curl http://localhost:8001/api/admin/intent-monitoring
{
  "middleware_active": true,
  "nl_endpoints": [...],
  "monitoring": "All requests logged"
}

$ git log --oneline -1
abc1234 Add IntentEnforcementMiddleware for request monitoring
```

---

*Estimated: 45 minutes*
