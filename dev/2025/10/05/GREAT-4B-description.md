# GREAT-4B: Universal Intent Enforcement

## Context
Second sub-epic of GREAT-4. Makes intent classification mandatory for ALL user interactions by creating middleware and removing bypass routes.

## Background
Currently, many endpoints bypass intent classification, leading to inconsistent behavior. Some interfaces use direct service calls, others use intent. This creates confusion and prevents learning system observation. Need to enforce 100% intent routing.

## Scope
1. **Create Intent Middleware**
   - FastAPI middleware for web
   - CLI wrapper for commands
   - Slack event interceptor
   - API gateway enforcement

2. **Convert All Interfaces**
   - Web UI to intent-first
   - CLI to intent-first
   - API to intent-first
   - Slack to intent-first
   - Webhooks to intent-first

3. **Remove Bypass Routes**
   - Delete direct endpoint routes
   - Remove service shortcuts
   - Eliminate fallback mechanisms
   - Block admin overrides

4. **Add Caching Layer**
   - Cache frequent classifications
   - Reduce latency impact
   - Implement cache invalidation
   - Monitor cache hit rates

## Acceptance Criteria
- [ ] Intent middleware created and active
- [ ] Web UI: 100% interactions through intent
- [ ] CLI: All commands through intent
- [ ] API: All endpoints through intent
- [ ] Slack: All messages through intent
- [ ] Webhooks: All calls through intent
- [ ] Zero direct service calls remaining
- [ ] Zero bypass routes accessible
- [ ] Caching layer operational
- [ ] Cache hit rate >60% for common queries
- [ ] No increase in latency >50ms
- [ ] Intent bypass detection test passing

## Success Validation
```bash
# Verify middleware active
grep "IntentMiddleware" web/app.py
# Should show middleware registered

# Check for bypasses
grep -r "@app.route" . --include="*.py" | grep -v "intent"
# Should return nothing (only intent routes)

# Test direct access fails
curl -X POST http://localhost:8001/api/github/create_issue -d '{"title":"test"}'
# Should return 404 or redirect

# Verify CLI uses intent
python cli/piper.py create issue --debug
# Should show "Intent classification: CREATE_ISSUE"

# Check cache working
redis-cli KEYS "intent:*" | wc -l
# Should show cached entries

# Run bypass detection
pytest tests/intent/test_no_bypasses.py -v
# All tests pass
```

## Anti-80% Check
```
Interface    | Mapped | Converted | Tested | Blocked | Cached
------------ | ------ | --------- | ------ | ------- | ------
Web UI       | [ ]    | [ ]       | [ ]    | [ ]     | [ ]
CLI          | [ ]    | [ ]       | [ ]    | [ ]     | [ ]
API          | [ ]    | [ ]       | [ ]    | [ ]     | [ ]
Slack        | [ ]    | [ ]       | [ ]    | [ ]     | [ ]
Webhooks     | [ ]    | [ ]       | [ ]    | [ ]     | [ ]
Middleware   | [ ]    | [ ]       | [ ]    | [ ]     | [ ]
TOTAL: 0/30 checkmarks = 0% (Must reach 100%)
```

## Time Estimate
6-8 hours
