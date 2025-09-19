# Phase 0 Browser Testing Evidence Template

**Date**: September 17, 2025
**Time**: 08:36 AM PDT
**Testing Agent**: Cursor Agent
**Issue**: #172 CORE-UI Layer 3 Intent Processing Pipeline

## Testing Instructions

### Prerequisites

1. Browser open at http://localhost:8001
2. Developer Tools open (F12) → Console tab
3. Paste entire contents of `web/browser_test_script.js` into console

### Test Execution Protocol

#### Phase 1: Working Prompts

```javascript
// Test each working prompt:
await testPrompt("hello");
await testPrompt("good morning");
```

**Evidence to Collect for Each**:

- [ ] Input text entered
- [ ] Response received (Y/N)
- [ ] Response time (seconds)
- [ ] Network tab: Status code
- [ ] Console: Any errors
- [ ] Screenshot: Success state

#### Phase 2: Hanging Prompts

```javascript
// Test each hanging prompt:
await testPrompt("help");
await testPrompt("show standup");
await testPrompt("fixing bugs");
```

**Evidence to Collect for Each**:

- [ ] Input text entered
- [ ] UI stuck in "Thinking..." (Y/N)
- [ ] Time until timeout (seconds)
- [ ] Network tab: Status code/pending
- [ ] Console: Error messages
- [ ] Screenshot: Hanging state

#### Phase 3: Evidence Export

```javascript
exportResults();
```

## Evidence Collection Matrix

| Prompt         | Category | UI Response | Response Time | Network Status | Console Error | Screenshot |
| -------------- | -------- | ----------- | ------------- | -------------- | ------------- | ---------- |
| "hello"        | Working  |             |               |                |               |            |
| "good morning" | Working  |             |               |                |               |            |
| "help"         | Hanging  |             |               |                |               |            |
| "show standup" | Hanging  |             |               |                |               |            |
| "fixing bugs"  | Hanging  |             |               |                |               |            |

## Browser Console Error Patterns

### Expected Working Pattern:

```
🧪 Testing prompt: "hello"
🌐 Network Request: /api/v1/intent
✅ Network Response: {status: 200, timing: <3000ms}
```

### Expected Hanging Pattern:

```
🧪 Testing prompt: "help"
🌐 Network Request: /api/v1/intent
❌ Network Error: {status: 500, error: "Failed to process intent"}
```

## Network Request Analysis

### Working Requests:

- Method: POST
- URL: /api/v1/intent
- Status: 200 OK
- Response time: <3s
- Body contains: intent_category, response

### Hanging Requests:

- Method: POST
- URL: /api/v1/intent
- Status: 500/timeout
- Response time: >10s
- Error: "Failed to process intent" or timeout

## UI State Documentation

### Success State Elements:

- Input field: Clear after submit
- Response area: Shows bot message
- Loading indicator: Brief then hidden
- Console: No errors

### Hanging State Elements:

- Input field: May remain filled
- Response area: Shows "Thinking..." or loading
- Loading indicator: Persistent
- Console: Error messages present

## Screenshots Required

1. **Working State**: Input → Response success
2. **Hanging State**: Input → "Thinking..." timeout
3. **Console Errors**: Developer tools showing errors
4. **Network Tab**: Failed requests in pending state

## Analysis Questions

After collecting evidence, answer:

1. Which prompts consistently work vs hang?
2. What network request patterns differentiate them?
3. What console errors appear for hanging prompts?
4. How long before timeouts occur?
5. Are there UI visual differences between states?

## Coordination with Backend Analysis

- Frontend symptoms documented here
- Backend analysis by Claude Code (separate investigation)
- Cross-reference: UI errors should correlate with backend intent processing failures
- Decision gate: If symptoms don't correlate → escalate for further investigation
