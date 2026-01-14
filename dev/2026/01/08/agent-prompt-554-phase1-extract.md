# Agent Prompt: #554 Phase 1 - Extract Chat Component

**Issue**: #554 STANDUP-CHAT-WIDGET
**Phase**: 1 of 6
**Model**: Haiku
**Deployed By**: Lead Developer

---

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete Phase 1 of GitHub Issue #554. Your work is part of a multi-agent coordination chain.

### Your Acceptance Criteria
- [ ] `web/static/css/chat.css` created
- [ ] `web/static/js/chat.js` created
- [ ] `templates/components/chat-widget.html` created
- [ ] `templates/home.html` updated to use component
- [ ] Home page chat still functional (manual verification)

**Every checkbox must be addressed in your handoff.**

### Your Handoff Format
Return your work with this structure:
```
## Issue #554 Phase 1 Completion Report
**Status**: Complete/Partial/Blocked

**Files Created**:
- web/static/css/chat.css (+X lines)
- web/static/js/chat.js (+X lines)
- templates/components/chat-widget.html (+X lines)

**Files Modified**:
- templates/home.html (extraction complete)

**Verification**:
[Manual test result - chat form works on home page]

**User Testing Steps**:
1. Run `python main.py`
2. Open http://localhost:8001/
3. Type message in chat, verify response appears

**Blockers** (if any):
- [Blocker description]
```

---

## Mission

Extract the inline chat UI from `templates/home.html` into standalone, reusable files.

**Scope**: ONLY Phase 1 extraction. Do NOT add floating positioning (Phase 2) or session persistence (Phase 3).

---

## Context

- **GitHub Issue**: #554 STANDUP-CHAT-WIDGET
- **Current State**: Chat CSS/JS/HTML inline in home.html
- **Target State**: Modular component files that home.html includes
- **Dependencies**: None (first phase)
- **Risk**: Must not break home.html chat functionality

---

## Source Locations (Verified)

| Asset | Location | Lines to Extract |
|-------|----------|------------------|
| Chat CSS | `templates/home.html` | Lines 45-106 (~62 lines) |
| Chat JS | `templates/home.html` | Lines 1068-1392 (~324 lines) |
| Chat HTML | `templates/home.html` | Lines 957-966 (~10 lines) |

---

## Implementation Steps

### Step 1: Create chat.css

Create `web/static/css/chat.css` with CSS extracted from home.html:

```bash
# Verify target directory exists
ls -la web/static/css/
```

**Extract these selectors** (from home.html lines 45-106):
- `.chat-*` classes (chat-form, chat-input, chat-window, etc.)
- `#chat-window` styles
- `.user-message`, `.bot-message` styles
- `.thinking` indicator styles
- Any related message/response styling

**Validation**: `ls -la web/static/css/chat.css`

### Step 2: Create chat.js

Create `web/static/js/chat.js` with JavaScript extracted from home.html:

```bash
# Verify target directory exists
ls -la web/static/js/
```

**Extract these functions** (from home.html lines 1068-1392):
- `appendMessage(html, isUser)` - Add message to chat window
- Chat form submit handler (the `fetch('/api/v1/intent', ...)` code)
- `handleDirectResponse(result, element)` - Process API responses
- `handleErrorResponse(error, element)` - Display errors
- `pollWorkflowStatus(workflowId, element)` - Long-running task polling
- Session ID generation/management

**Dependencies to handle**:
- `API_BASE_URL` - Pass as parameter or use global
- `sessionId` - Initialize in the module
- `marked` - Assume loaded via CDN
- Toast/Loading utilities - Assume available globally

**Structure suggestion**:
```javascript
// chat.js - Modular chat widget functionality
(function() {
    'use strict';

    // Session management
    let sessionId = null;

    function initChat() {
        sessionId = crypto.randomUUID();
        // Set up form handler
    }

    function appendMessage(html, isUser) {
        // ... extracted code
    }

    // ... other functions

    // Initialize on DOM ready
    document.addEventListener('DOMContentLoaded', initChat);

    // Export for testing if needed
    window.ChatWidget = { appendMessage, initChat };
})();
```

**Validation**: `ls -la web/static/js/chat.js`

### Step 3: Create chat-widget.html

Create `templates/components/chat-widget.html`:

```bash
# Verify target directory exists
ls -la templates/components/
```

**Content** (from home.html lines 957-966):
```html
<!-- Chat Widget Component -->
<!-- Include CSS: <link rel="stylesheet" href="/static/css/chat.css"> -->
<!-- Include JS: <script src="/static/js/chat.js"></script> -->

<div class="chat-container" id="chat-container">
    <div id="chat-window" class="chat-window">
        <!-- Messages appear here -->
    </div>
    <form class="chat-form" id="chat-form">
        <input type="text" class="chat-input" id="chat-input"
               placeholder="Type a message..." autocomplete="off">
        <button type="submit" class="chat-submit">Send</button>
    </form>
</div>
```

**Validation**: `ls -la templates/components/chat-widget.html`

### Step 4: Update home.html

Modify `templates/home.html` to use the extracted component:

1. **Remove inline CSS** (lines 45-106) - Replace with:
   ```html
   <link rel="stylesheet" href="/static/css/chat.css">
   ```

2. **Remove inline HTML** (lines 957-966) - Replace with:
   ```html
   {% include 'components/chat-widget.html' %}
   ```

3. **Remove inline JS** (lines 1068-1392) - Replace with:
   ```html
   <script src="/static/js/chat.js"></script>
   ```

**CRITICAL**: Preserve all other home.html functionality. Only extract chat-related code.

### Step 5: Verify Home Page Works

```bash
# Start server
python main.py

# In another terminal or browser:
# 1. Open http://localhost:8001/
# 2. Type "hello" in chat input
# 3. Click Send
# 4. Verify response appears in chat window
```

**Evidence required**: Describe what you see when testing.

---

## STOP Conditions

Stop immediately and report if:
- [ ] home.html breaks after extraction
- [ ] CSS/JS file locations don't work
- [ ] Chat form doesn't submit
- [ ] Responses don't appear
- [ ] Any JavaScript errors in console
- [ ] Infrastructure doesn't match expectations
- [ ] Cannot provide verification evidence
- [ ] Tests fail for any reason

**When stopped**: Document the issue, provide error details, wait for Lead Dev. Do NOT continue or rationalize gaps.

---

## Post-Compaction Protocol

**If context was just reset/compacted**:
1. ⏸️ **STOP** - Do not continue working
2. 📋 **REPORT** - Summarize what was completed so far
3. ❓ **ASK** - "Should I proceed?"
4. ⏳ **WAIT** - For explicit Lead Dev instructions

**DO NOT**: Continue blindly, read old context to self-direct, or assume next steps.

---

## Self-Check Before Claiming Complete

Ask yourself:
1. Did I create ALL 3 files (chat.css, chat.js, chat-widget.html)?
2. Did I update home.html to use the extracted components?
3. Did I manually verify the chat still works on home page?
4. Did I provide evidence (ls -la, line counts) for every claim?
5. Am I claiming work done that I didn't actually verify?
6. Is there a gap between my claims and reality?

**If ANY answer is uncertain**: Verify first, then claim.

---

## When Tests/Verification Fail

**If chat functionality breaks**:
1. **STOP immediately** - Do NOT continue
2. **Do NOT decide** if failure is "minor"
3. **Do NOT rationalize** ("mostly works", "just styling")

**Report format**:
```
⚠️ STOP - Verification Failed

What broke: [description]
Error details: [console errors, behavior observed]

Root cause (if known): [diagnosis]

Options:
1. [fix approach]
2. [rollback approach]

Awaiting Lead Dev decision.
```

---

## Evidence Requirements

For EVERY claim:
- **"Created file X"** → Show `ls -la` output
- **"Extracted CSS"** → Show line count
- **"Chat works"** → Describe manual test result

---

## Files Summary

**Create**:
- `web/static/css/chat.css` (~62 lines)
- `web/static/js/chat.js` (~324 lines)
- `templates/components/chat-widget.html` (~15 lines)

**Modify**:
- `templates/home.html` (remove inline, add includes)

---

## Remember

- This is extraction only - preserve existing functionality
- Do NOT add new features (floating, persistence, etc.)
- Evidence for all claims
- Test before claiming complete
- Report blockers immediately

---

*Prompt Version: 1.1*
*Template: agent-prompt-template v10.2*
*Updated: Added Post-Compaction Protocol, Self-Check Questions, When Tests Fail sections*
