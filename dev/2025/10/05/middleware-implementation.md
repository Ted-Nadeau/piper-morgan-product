# Intent Enforcement Middleware Implementation
**GREAT-4B Phase 2 - Architectural Enforcement**

**Date**: October 5, 2025, 4:45 PM
**Issue**: #206 (CORE-GREAT-4B)

---

## Purpose

Monitor all HTTP requests and enforce intent classification on natural language endpoints to prevent future bypasses.

**Architectural Principle Enforced**:
> "All natural language user input must go through intent classification."

---

## How It Works

1. **Intercepts all HTTP requests** via FastAPI middleware (BaseHTTPMiddleware)
2. **Logs every request** for compliance monitoring
3. **Marks NL endpoints** as requiring intent classification (sets `request.state.intent_required = True`)
4. **Exempts static/health/output endpoints** from intent requirement
5. **Provides monitoring endpoint** for configuration visibility

---

## Architecture

### Request Flow
```
HTTP Request → IntentEnforcementMiddleware → Route Handler → Response
                         ↓
                  Logs & Marks Intent Required
```

### Classification Logic
```python
if _is_nl_endpoint(path):
    request.state.intent_required = True  # Mark for enforcement

if _is_exempt(path):
    # Allow without intent (documented reason)
```

---

## Configuration

### Natural Language Endpoints (require intent)
```python
NL_ENDPOINTS = [
    "/api/v1/intent",    # IS the intent endpoint
    "/api/standup",      # Proxies to backend (uses intent there)
    "/api/chat",         # Future NL endpoint
    "/api/message",      # Future NL endpoint
]
```

### Exempt Paths (don't need intent)
```python
EXEMPT_PATHS = [
    "/health",                      # Health checks
    "/metrics",                     # Metrics
    "/docs",                        # API docs
    "/openapi.json",                # OpenAPI spec
    "/static",                      # Static files
    "/api/personality/enhance",     # OUTPUT processing (not input)
    "/api/personality/profile",     # Config endpoints (structured)
    "/api/v1/workflows",            # Direct ID lookups
    "/debug-markdown",              # Debug endpoints
    "/personality-preferences",     # Static UI pages
    "/standup",                     # Static UI page
    "/",                            # Root page
]
```

---

## Exemption Rules

### When to Exempt an Endpoint:

1. **Output Transformation** (like `/api/personality/enhance`)
   - Processes Piper's responses, not user input
   - Flow: Response → Enhance → Send (not User → Classify → Route)

2. **Structured Data** (like `/api/personality/profile`)
   - Explicit operations with structured payloads
   - No ambiguity to resolve

3. **Direct Lookups** (like `/api/v1/workflows/{id}`)
   - Resource retrieval by ID
   - No natural language input

4. **Infrastructure** (like `/health`, `/static`)
   - System endpoints
   - No user input to classify

5. **Static UI** (like `/`, `/standup`)
   - HTML page delivery
   - No request body to analyze

---

## Usage

### Adding New Natural Language Endpoints

If adding a new endpoint that accepts natural language user input:

1. **Add to NL_ENDPOINTS list**:
   ```python
   NL_ENDPOINTS = [
       "/api/v1/intent",
       "/api/standup",
       "/api/your-new-endpoint",  # Add here
   ]
   ```

2. **Ensure endpoint uses intent classification**:
   ```python
   @app.post("/api/your-new-endpoint")
   async def your_endpoint(request: Request):
       # Get IntentService and classify
       intent_service = request.app.state.intent_service
       result = await intent_service.process_intent(...)
       return result
   ```

3. **Test with monitoring endpoint**:
   ```bash
   curl http://localhost:8001/api/admin/intent-monitoring
   # Verify your endpoint is listed in nl_endpoints
   ```

### Adding Exempt Endpoints

If adding an endpoint that should be exempt:

1. **Document WHY it's exempt** (output transformation, structured data, etc.)

2. **Add to EXEMPT_PATHS list**:
   ```python
   EXEMPT_PATHS = [
       "/health",
       "/api/your-exempt-endpoint",  # Add with comment explaining why
   ]
   ```

3. **Verify exemption**:
   ```bash
   # Request should NOT be marked as requiring intent
   # Check logs for: "Exempt from intent: /api/your-exempt-endpoint"
   ```

---

## Monitoring

### Check Middleware Status

```bash
curl http://localhost:8001/api/admin/intent-monitoring
```

**Response**:
```json
{
  "middleware_active": true,
  "nl_endpoints": [
    "/api/v1/intent",
    "/api/standup",
    "/api/chat",
    "/api/message"
  ],
  "exempt_paths": [
    "/health",
    "/metrics",
    "/docs",
    "/openapi.json",
    "/static",
    "/api/personality/enhance",
    "/api/personality/profile",
    "/api/v1/workflows",
    "/debug-markdown",
    "/personality-preferences",
    "/standup",
    "/"
  ],
  "monitoring": "All requests logged",
  "principle": "User INPUT → intent classification (enforced)"
}
```

### Check Logs

```bash
# Start server
python main.py

# Logs will show:
INFO: ✅ IntentEnforcementMiddleware registered (GREAT-4B)
INFO: Request: GET /api/standup
DEBUG: Intent required for: /api/standup
INFO: Request: GET /health/config
DEBUG: Exempt from intent: /health/config
```

---

## Files Created

1. **`web/middleware/intent_enforcement.py`** (124 lines)
   - IntentEnforcementMiddleware class
   - Request monitoring logic
   - NL endpoint detection
   - Exemption handling

2. **`web/middleware/__init__.py`**
   - Module initialization

3. **`web/app.py`** (modified)
   - Middleware registration (line 215)
   - Monitoring endpoint (line 528)

4. **`dev/2025/10/05/middleware-implementation.md`** (this file)
   - Complete documentation

---

## Implementation Details

### Middleware Registration
```python
# web/app.py (after app creation)
from web.middleware.intent_enforcement import IntentEnforcementMiddleware

app.add_middleware(IntentEnforcementMiddleware)
logger.info("✅ IntentEnforcementMiddleware registered (GREAT-4B)")
```

### Monitoring Endpoint
```python
@app.get("/api/admin/intent-monitoring")
async def intent_monitoring():
    """Intent enforcement monitoring endpoint."""
    return IntentEnforcementMiddleware.get_monitoring_status()
```

### Request State Marking
```python
async def dispatch(self, request: Request, call_next):
    if self._is_nl_endpoint(request.url.path):
        request.state.intent_required = True  # Future validation hook
    response = await call_next(request)
    return response
```

---

## Future Enhancements

### Phase 3: Strict Enforcement (Future)

Currently, middleware only **monitors** and **marks** intent requirements.

Future enhancement: Add strict enforcement that **blocks** requests to NL endpoints that don't use intent:

```python
async def dispatch(self, request: Request, call_next):
    if self._is_nl_endpoint(request.url.path):
        request.state.intent_required = True

        # Future: Check if handler uses intent
        response = await call_next(request)

        # Future: Validate intent was used
        if not getattr(request.state, 'intent_classified', False):
            logger.error(f"VIOLATION: {request.url.path} did not use intent!")
            # Could return 500 or log to metrics

        return response
```

### Phase 4: Metrics & Alerts (Future)

- Track intent classification usage rates
- Alert on new NL endpoints without intent
- Dashboard for compliance monitoring

---

## Testing Checklist

- [x] Middleware file created (web/middleware/intent_enforcement.py)
- [x] Middleware registered in app.py
- [x] Monitoring endpoint added (/api/admin/intent-monitoring)
- [x] Documentation complete (this file)
- [ ] Server starts without errors (next: test)
- [ ] Monitoring endpoint accessible (next: test)
- [ ] Logs show request tracking (next: test)
- [ ] Git commit created (next: commit)

---

## Related Documentation

- **Baseline Analysis**: `dev/2025/10/05/intent-baseline-FINAL.md`
- **Session Log**: `dev/2025/10/05/2025-10-05-1540-prog-code-log.md`
- **GitHub Issue**: #206 (CORE-GREAT-4B)

---

*Created: October 5, 2025, 4:45 PM*
*Part of GREAT-4B: Universal Intent Enforcement*
