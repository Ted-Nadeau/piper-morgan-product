# Slack Integration Debugging Guide

## Quick Reference Checklist

### 1. Server Status
```bash
# Check if server is running
curl http://localhost:8001/health

# Check ngrok tunnel
curl -s http://localhost:4040/api/tunnels | grep public_url
```

### 2. Webhook Receipt
```bash
# Test webhook endpoint
curl -X POST "http://localhost:8001/slack/webhooks/events" \
  -H "Content-Type: application/json" \
  -d '{"challenge": "test_challenge"}'

# Should return: {"status":"ignored"} or challenge response
```

### 3. Integration Flow Tracing

**Real-time log monitoring:**
```bash
tail -f server.log | grep -E "(SUCCESS|ERROR|workflow|spatial|intent)"
```

**Step-by-step debugging:**

#### Step 1: Webhook Receipt ✅
**Success**: `Processing Slack event: app_mention in team XXXX`
**Failure**: `Error handling Slack events webhook`

#### Step 2: Spatial Conversion ✅
**Success**: `Mapped Slack timestamp XXX to position XXX`
**Failure**: `'SpatialEvent' object has no attribute 'position'`

#### Step 3: Response Handler ✅
**Success**: `SlackResponseHandler.handle_spatial_event called`
**Failure**: `Error handling spatial event`

#### Step 4: Intent Creation ✅
**Success**: `intent_classification: action=XXX confidence=X.X`
**Failure**: `Error creating intent from spatial event`

#### Step 5: Orchestration ✅
**Success**: `Category XXX mapped to workflow_type: XXX`
**Failure**: `No workflow type found for intent category`

#### Step 6: Response Posting ✅
**Success**: `✅ COMPLETE INTEGRATION SUCCESS: XXX -> XXX -> workflow -> response sent`
**Failure**: `Error sending Slack response`

## Common Issues & Fixes

### Issue 1: Signature Verification Failure
**Symptom**: `Invalid request signature` (401 error)
**Fix**:
```python
# Temporarily disable in webhook_router.py for testing
# if not await self._verify_slack_signature(request):
#     raise HTTPException(...)
```

### Issue 2: Type Errors in Spatial Adapter
**Symptom**: `'SpatialEvent' object has no attribute 'position'`
**Root Cause**: Passing wrong type to `store_mapping()`
**Fix**: Ensure `position` parameter is `SpatialPosition` object with `.position` integer

### Issue 3: Missing Async Await
**Symptom**: `RuntimeWarning: coroutine 'store_mapping' was never awaited`
**Fix**: Add `await` to all async calls in spatial adapter

### Issue 4: Missing Workflow Mappings
**Symptom**: `No workflow type found for intent category: IntentCategory.XXX`
**Fix**: Add mapping in `workflow_factory.py`:
```python
elif intent.category == IntentCategory.CONVERSATION:
    workflow_type = WorkflowType.GENERATE_REPORT
elif intent.category == IntentCategory.LEARNING:
    workflow_type = WorkflowType.GENERATE_REPORT
```

### Issue 5: SlackClient Configuration
**Symptom**: `Error sending Slack response`
**Check**: Environment variables and Slack app configuration
```bash
echo $SLACK_BOT_TOKEN
echo $SLACK_SIGNING_SECRET
```

## Integration Test Commands

### Test Challenge Response
```bash
curl -X POST "http://localhost:8001/slack/webhooks/events" \
  -H "Content-Type: application/json" \
  -d '{"challenge": "test_challenge"}'
```

### Test App Mention Processing
```bash
curl -X POST "http://localhost:8001/slack/webhooks/events" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "event_callback",
    "event": {
      "type": "app_mention",
      "channel": "C1234567890",
      "user": "U1234567890",
      "text": "@piper-morgan help",
      "ts": "1234567890.123456"
    },
    "team_id": "T1234567890"
  }'
```

### Test Message Processing
```bash
curl -X POST "http://localhost:8001/slack/webhooks/events" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "event_callback",
    "event": {
      "type": "message",
      "channel": "C1234567890",
      "user": "U1234567890",
      "text": "Hello world",
      "ts": "1234567890.123456"
    },
    "team_id": "T1234567890"
  }'
```

## Success Indicators

### Complete Integration Success
Look for log sequence:
1. `Processing Slack event: app_mention`
2. `Mapped Slack timestamp XXX to position XXX`
3. `intent_classification: action=XXX confidence=X.X`
4. `Category XXX mapped to workflow_type: XXX`
5. `✅ COMPLETE INTEGRATION SUCCESS: XXX -> XXX -> workflow -> response sent`

### Performance Benchmarks
- Webhook receipt: < 100ms
- Spatial conversion: < 50ms
- Intent classification: 2-5 seconds (LLM call)
- Orchestration: < 500ms
- Response posting: 1-2 seconds (Slack API)
- **Total**: 3-8 seconds end-to-end

## Architecture Overview

```
Slack Event → Webhook Router → Spatial Adapter → Response Handler
    ↓              ↓               ↓                 ↓
Event Data → SpatialEvent → Intent → Workflow Result → Slack Response
```

## Troubleshooting Checklist

- [ ] Server running on port 8001
- [ ] Ngrok tunnel active and public
- [ ] Slack app webhook URL configured
- [ ] Environment variables set
- [ ] Signature verification disabled for testing
- [ ] All async calls have await
- [ ] Workflow mappings complete
- [ ] Error logging enabled
- [ ] Real-time log monitoring active

## Contact Points for Issues

- **Webhook Issues**: Check `webhook_router.py` signature verification
- **Spatial Issues**: Check `spatial_adapter.py` type handling
- **Intent Issues**: Check `response_handler.py` classification
- **Orchestration Issues**: Check `workflow_factory.py` mappings
- **Response Issues**: Check SlackClient configuration and tokens
