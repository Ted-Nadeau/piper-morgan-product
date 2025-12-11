# Code Agent Prompt: Issue #455 - Add credentials to fetch calls

## Assignment

Add `credentials: 'include'` to all fetch() calls that hit authenticated API endpoints in templates.

## Context

Users who are logged in cannot use chat, create todos/lists/projects because the auth cookie isn't being sent with fetch requests. The fix is simple: add `credentials: 'include'` to each fetch call.

## Reference Pattern

This is the correct pattern (already used in some places):

```javascript
const response = await fetch('/api/v1/endpoint', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(data),
  credentials: 'include'  // <-- ADD THIS
});
```

For GET requests without body:
```javascript
const response = await fetch('/api/v1/endpoint', {
  credentials: 'include'  // <-- ADD THIS
});
```

## Files to Modify

### 1. templates/home.html

Find and fix these fetch calls:
- Around line 1199: `fetch(\`${API_BASE_URL}/api/v1/intent\`, {` - add credentials
- Around line 1115: `fetch(\`${API_BASE_URL}/api/v1/workflows/${workflowId}\`)` - needs options object with credentials

### 2. templates/todos.html

Find and fix ALL fetch calls (around lines 224, 284, 363, 389):
- POST /api/v1/todos
- GET shares
- POST share
- DELETE share

### 3. templates/lists.html

Same pattern as todos.html (around lines 226, 286, 365, 391)

### 4. templates/projects.html

Fix fetch calls around lines 256, 335, 361

### 5. Audit remaining templates

Check these and fix if needed:
- templates/files.html
- templates/standup.html
- templates/learning-dashboard.html
- templates/account.html
- templates/settings-index.html
- templates/personality-preferences.html

## Verification

After making changes, run:
```bash
# Should show credentials: 'include' for all API fetch calls
grep -n "fetch.*api" templates/*.html | grep -v "credentials"
```

This should return empty or only show non-API fetch calls.

## DO NOT

- Do not refactor to use a wrapper (that's future work)
- Do not change endpoint paths
- Do not modify any other functionality
- Do not add new dependencies

## Success Criteria

1. All fetch calls to /api/v1/* endpoints have `credentials: 'include'`
2. No syntax errors introduced
3. Existing functionality preserved

## Evidence Required

Provide:
1. List of all files modified
2. Grep output showing credentials added
3. Any issues discovered during audit
