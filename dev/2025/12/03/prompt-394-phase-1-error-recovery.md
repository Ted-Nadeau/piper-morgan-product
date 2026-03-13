# Claude Code Prompt: Issue #394 Phase 1 - Error Recovery Infrastructure

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Essential Context
- **Issue**: #394 CORE-UX-ERROR-QUAL: No error messages or recovery guidance
- **Phase**: 1 of 3 (Core Infrastructure)
- **Gameplan**: dev/2025/12/03/gameplan-394-phase-1-error-recovery.md

---

## CRITICAL: Infrastructure Already Verified

Phase -1 verification completed by Lead Dev. Key findings:
- **Toast system EXISTS**: `web/static/js/toast.js` (Phase 1A COMPLETE)
- **Loading utilities EXIST**: `web/static/js/loading.js`
- **Templates**: 18 HTML files in templates/

DO NOT recreate what exists. Focus on Phase 1B and 1C only.

---

## Mission

Implement error messaging infrastructure:

1. **Phase 1B**: Create `api-wrapper.js` - Global fetch wrapper with error interception
2. **Phase 1C**: Extend `loading.js` with timeout parameters

---

## Context

- **GitHub Issue**: #394
- **Current State**: Toast system complete, no API error handling
- **Target State**: All API errors shown as toasts, loading buttons timeout gracefully
- **Infrastructure Verified**: Yes

---

## MANDATORY FIRST ACTIONS

```bash
# 1. Verify toast.js exists
ls -la web/static/js/toast.js

# 2. Verify loading.js exists
ls -la web/static/js/loading.js

# 3. Check for existing API wrapper
ls -la web/static/js/api*.js
grep -r "ApiWrapper\|api-wrapper" web/static/js/

# 4. Check GitHub issue
gh issue view 394
```

**STOP if**:
- toast.js doesn't exist
- Different API wrapper pattern already exists
- Issue #394 not found

---

## Implementation Approach

### Step 1: Create api-wrapper.js

**File**: `web/static/js/api-wrapper.js`

```javascript
/**
 * API Wrapper with Error Interception
 * WCAG 2.2 AA Accessible
 *
 * Usage:
 *   const response = await ApiWrapper.get('/api/todos')
 *   const data = await ApiWrapper.post('/api/todos', { title: 'New todo' })
 *
 * Automatically shows:
 * - Toast.error for 5xx errors
 * - Toast.warning for 4xx errors
 * - Toast.error for network failures
 */

const ApiWrapper = {
  // Default request timeout (30 seconds)
  defaultTimeout: 30000,

  /**
   * Wrapped fetch with error handling
   * @param {string} url - Request URL
   * @param {Object} options - Fetch options
   * @returns {Promise<Response>}
   */
  async fetch(url, options = {}) {
    const controller = new AbortController();
    const timeout = options.timeout || this.defaultTimeout;

    const timeoutId = setTimeout(() => {
      controller.abort();
    }, timeout);

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        }
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        await this.handleHttpError(response);
      }

      return response;
    } catch (error) {
      clearTimeout(timeoutId);
      this.handleNetworkError(error);
      throw error;
    }
  },

  /**
   * Handle HTTP error responses
   * @param {Response} response - Fetch response
   */
  async handleHttpError(response) {
    let message = 'An error occurred';

    try {
      const data = await response.clone().json();
      message = data.detail || data.message || data.error || message;
    } catch {
      // Response wasn't JSON, use status text
      message = response.statusText || message;
    }

    if (response.status >= 500) {
      Toast.error('Server Error', 'Something went wrong. Please try again later.');
    } else if (response.status === 401) {
      Toast.warning('Session Expired', 'Please log in again.');
    } else if (response.status === 403) {
      Toast.warning('Access Denied', 'You don\'t have permission for this action.');
    } else if (response.status === 404) {
      Toast.warning('Not Found', 'The requested resource was not found.');
    } else if (response.status >= 400) {
      Toast.warning('Request Failed', message);
    }
  },

  /**
   * Handle network/connection errors
   * @param {Error} error - Error object
   */
  handleNetworkError(error) {
    if (error.name === 'AbortError') {
      Toast.error('Request Timeout', 'The request took too long. Please try again.');
    } else if (!navigator.onLine) {
      Toast.error('No Connection', 'You appear to be offline. Check your internet connection.');
    } else {
      Toast.error('Connection Failed', 'Unable to reach the server. Please try again.');
    }
  },

  /**
   * GET request
   */
  async get(url, options = {}) {
    return this.fetch(url, { ...options, method: 'GET' });
  },

  /**
   * POST request
   */
  async post(url, body, options = {}) {
    return this.fetch(url, {
      ...options,
      method: 'POST',
      body: JSON.stringify(body)
    });
  },

  /**
   * PUT request
   */
  async put(url, body, options = {}) {
    return this.fetch(url, {
      ...options,
      method: 'PUT',
      body: JSON.stringify(body)
    });
  },

  /**
   * DELETE request
   */
  async delete(url, options = {}) {
    return this.fetch(url, { ...options, method: 'DELETE' });
  }
};

// Export for modules/bundlers
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ApiWrapper;
}
```

**Validation**:
```bash
ls -la web/static/js/api-wrapper.js
cat web/static/js/api-wrapper.js | head -20
```

### Step 2: Extend loading.js with timeout

**File**: `web/static/js/loading.js`

Add this method to the Loading object:

```javascript
  /**
   * Set button to loading state with timeout
   * @param {HTMLElement} button - Button element
   * @param {Object} options - { timeout: ms, onWarning: fn, onTimeout: fn }
   * @returns {{ stop: Function }} Control object
   */
  buttonWithTimeout(button, options = {}) {
    const timeout = options.timeout || 30000;
    const warningAt = options.warningAt || 10000;

    this.button(button, true);

    let warningTimeoutId = null;
    let errorTimeoutId = null;

    // Show warning after warningAt ms
    warningTimeoutId = setTimeout(() => {
      if (typeof Toast !== 'undefined') {
        Toast.warning('Taking longer than expected', 'Please wait...');
      }
      if (options.onWarning) options.onWarning();
    }, warningAt);

    // Show error and stop after timeout ms
    errorTimeoutId = setTimeout(() => {
      this.button(button, false);
      if (typeof Toast !== 'undefined') {
        Toast.error('Request Failed', 'The operation timed out. Please try again.');
      }
      if (options.onTimeout) options.onTimeout();
    }, timeout);

    return {
      stop: () => {
        clearTimeout(warningTimeoutId);
        clearTimeout(errorTimeoutId);
        this.button(button, false);
      }
    };
  },
```

**Validation**:
```bash
grep -n "buttonWithTimeout" web/static/js/loading.js
cat web/static/js/loading.js | tail -30
```

---

## Evidence Requirements

For EVERY change:
- **Created file**: Show `ls -la` output
- **Modified file**: Show relevant `grep` or `cat` output
- **Works correctly**: Show test in browser or explain manual test

---

## Success Criteria

- [ ] `api-wrapper.js` created with fetch wrapper (show `ls -la`)
- [ ] ApiWrapper.fetch() includes timeout (show code)
- [ ] 4xx errors show Toast.warning (show handleHttpError code)
- [ ] 5xx errors show Toast.error (show handleHttpError code)
- [ ] Network errors show Toast.error (show handleNetworkError code)
- [ ] `loading.js` has buttonWithTimeout method (show `grep`)
- [ ] Warning shown at 10s, error at 30s (show code)
- [ ] No existing patterns broken

---

## Deliverables

1. **New file**: `web/static/js/api-wrapper.js`
2. **Modified file**: `web/static/js/loading.js` (add buttonWithTimeout)
3. **Evidence**: Terminal output for each change
4. **GitHub Update**: Update #394 with Phase 1 complete

---

## Self-Check Before Claiming Complete

1. Did I verify toast.js exists first?
2. Did I check for existing API wrapper patterns?
3. Did I provide `ls -la` or `grep` evidence for each file?
4. Did I test that Toast calls work (or explain why not)?
5. Am I claiming completion without evidence?

---

## STOP Conditions

Stop and escalate if:
- Toast.js has different API than expected
- Existing fetch calls would break
- Loading.js uses different pattern
- Cannot verify changes work

---

*Prompt based on agent-prompt-template.md v10.2*
