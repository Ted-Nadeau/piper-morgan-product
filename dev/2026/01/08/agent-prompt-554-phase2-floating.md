# Agent Prompt: #554 Phase 2 - Floating Widget Positioning

**Issue**: #554 STANDUP-CHAT-WIDGET
**Phase**: 2 of 6
**Model**: Haiku
**Deployed By**: Lead Developer
**Depends On**: Phase 1 complete

---

## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete Phase 2 of GitHub Issue #554. Your work is part of a multi-agent coordination chain.

### Your Acceptance Criteria
- [ ] Widget positioned bottom-right corner
- [ ] Expand/collapse toggle works
- [ ] Smooth animations
- [ ] Z-index handles modals/toasts correctly

**Every checkbox must be addressed in your handoff.**

### Your Handoff Format
Return your work with this structure:
```
## Issue #554 Phase 2 Completion Report
**Status**: Complete/Partial/Blocked

**Files Modified**:
- web/static/css/chat.css (+X lines)
- web/static/js/chat.js (+X lines)
- templates/components/chat-widget.html (+X lines)

**Verification**:
[Manual test - widget in corner, toggle works]

**User Testing Steps**:
1. Open any page with widget
2. Widget visible in bottom-right corner (collapsed)
3. Click toggle button - widget expands
4. Click again - widget collapses
5. Open a modal - widget stays behind modal

**Blockers** (if any):
- [Blocker description]
```

---

## Mission

Add floating widget positioning to the chat component extracted in Phase 1.

**Scope**: ONLY Phase 2 positioning. Do NOT add session persistence (Phase 3) or site-wide integration (Phase 4).

---

## Context

- **GitHub Issue**: #554 STANDUP-CHAT-WIDGET
- **Current State**: Chat component exists as separate files (Phase 1 complete)
- **Target State**: Widget floats in bottom-right corner with expand/collapse
- **Dependencies**: Phase 1 files must exist
- **Risk**: Z-index conflicts with existing modals/toasts

---

## Pre-Flight Verification

Before starting, verify Phase 1 is complete:

```bash
# These files must exist
ls -la web/static/css/chat.css
ls -la web/static/js/chat.js
ls -la templates/components/chat-widget.html
```

**STOP if any file is missing** - Phase 1 not complete.

---

## Implementation Steps

### Step 1: Add Floating Container CSS

Update `web/static/css/chat.css` - add floating widget styles:

```css
/* Floating Widget Container */
.chat-widget-container {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 1000;  /* Below modals (typically 1050+) */
    display: flex;
    flex-direction: column;
    align-items: flex-end;
}

/* Collapsed State - Just the toggle button */
.chat-widget-container .chat-container {
    display: none;
    width: 380px;
    max-height: 500px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    overflow: hidden;
    transition: opacity 0.2s ease, transform 0.2s ease;
}

/* Expanded State */
.chat-widget-container.expanded .chat-container {
    display: flex;
    flex-direction: column;
}

/* Toggle Button */
.chat-widget-toggle {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: #3498db;
    color: white;
    border: none;
    cursor: pointer;
    font-size: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    transition: transform 0.2s ease, background 0.2s ease;
}

.chat-widget-toggle:hover {
    background: #2980b9;
    transform: scale(1.05);
}

/* Hide toggle when expanded (optional - or change icon) */
.chat-widget-container.expanded .chat-widget-toggle {
    /* Option A: Hide button */
    /* display: none; */

    /* Option B: Change to close icon (preferred) */
    background: #e74c3c;
}

/* Chat window sizing for floating mode */
.chat-widget-container .chat-window {
    height: 350px;
    overflow-y: auto;
}

.chat-widget-container .chat-form {
    border-top: 1px solid #eee;
    padding: 10px;
}
```

### Step 2: Add Toggle JavaScript

Update `web/static/js/chat.js` - add toggle functionality:

```javascript
// Add to chat.js

function toggleChatWidget() {
    const container = document.querySelector('.chat-widget-container');
    if (container) {
        container.classList.toggle('expanded');

        // Update toggle button icon
        const toggle = container.querySelector('.chat-widget-toggle');
        if (toggle) {
            toggle.innerHTML = container.classList.contains('expanded') ? '✕' : '💬';
        }

        // Focus input when expanded
        if (container.classList.contains('expanded')) {
            const input = container.querySelector('.chat-input');
            if (input) input.focus();
        }
    }
}

// Make toggle globally available
window.toggleChatWidget = toggleChatWidget;
```

### Step 3: Update HTML Structure

Update `templates/components/chat-widget.html`:

```html
<!-- Chat Widget Component - Floating Version -->
<div class="chat-widget-container" id="chat-widget-container">
    <!-- Chat Container (hidden when collapsed) -->
    <div class="chat-container" id="chat-container">
        <div class="chat-header">
            <span>Chat with Piper</span>
            <button type="button" class="chat-close" onclick="toggleChatWidget()">&times;</button>
        </div>
        <div id="chat-window" class="chat-window">
            <!-- Messages appear here -->
        </div>
        <form class="chat-form" id="chat-form">
            <input type="text" class="chat-input" id="chat-input"
                   placeholder="Type a message..." autocomplete="off">
            <button type="submit" class="chat-submit">Send</button>
        </form>
    </div>

    <!-- Toggle Button (always visible) -->
    <button type="button" class="chat-widget-toggle" onclick="toggleChatWidget()">
        💬
    </button>
</div>
```

Also add header styling to CSS:

```css
.chat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    background: #3498db;
    color: white;
    font-weight: 500;
}

.chat-close {
    background: none;
    border: none;
    color: white;
    font-size: 20px;
    cursor: pointer;
    padding: 0;
    line-height: 1;
}

.chat-close:hover {
    opacity: 0.8;
}
```

### Step 4: Verify Z-Index Hierarchy

Check existing z-index values in the codebase:

```bash
# Find existing z-index values
grep -r "z-index" web/static/css/ templates/ --include="*.css" --include="*.html"
```

**Common z-index hierarchy**:
- Dropdowns: 100-200
- Sticky headers: 500-600
- **Chat widget: 1000** (our target)
- Modals: 1050+
- Toasts: 1100+

If conflicts found, adjust chat widget z-index accordingly.

### Step 5: Manual Testing

```bash
# Start server
python main.py
```

**Test checklist**:
1. [ ] Widget visible in bottom-right corner
2. [ ] Toggle button shows chat icon (💬)
3. [ ] Click toggle - chat expands with animation
4. [ ] Toggle button changes to close icon (✕)
5. [ ] Click again - chat collapses
6. [ ] Input auto-focuses when expanded
7. [ ] Send message - still works in floating mode
8. [ ] Open any existing modal - widget behind modal
9. [ ] Toast notification - toast above widget

---

## STOP Conditions

Stop immediately and report if:
- [ ] Phase 1 files don't exist
- [ ] Toggle doesn't work
- [ ] Z-index conflicts with modals (widget covers modal)
- [ ] Animation causes layout issues
- [ ] Chat functionality broken after changes

**When stopped**: Document the issue, provide error details, wait for Lead Dev.

---

## Evidence Requirements

For EVERY claim:
- **"Added CSS"** → Show new line count
- **"Toggle works"** → Describe click test result
- **"Z-index correct"** → Show grep output and test result

---

## Files Summary

**Modify**:
- `web/static/css/chat.css` (+~60 lines for floating styles)
- `web/static/js/chat.js` (+~15 lines for toggle)
- `templates/components/chat-widget.html` (restructure for floating)

---

## Remember

- This is positioning only - preserve chat functionality
- Do NOT add session persistence (Phase 3)
- Do NOT integrate into other pages (Phase 4)
- Test z-index against existing modals
- Evidence for all claims

---

*Prompt Version: 1.0*
*Template: agent-prompt-template v10.2*
