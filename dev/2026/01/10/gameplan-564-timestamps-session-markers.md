# Gameplan: Issue #564 - CONV-PERSIST-2: Timestamps & Session Markers

**Date**: 2026-01-10
**Issue**: https://github.com/mediajunkie/piper-morgan-product/issues/564
**Parent**: #314 (CONV-UX-PERSIST)
**Priority**: P2 (Medium)
**Dependency**: #563 (Session Continuity) - ✅ COMPLETE

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Frontend: Jinja2 templates with vanilla JavaScript
- [x] Chat rendering: `templates/components/chat-widget.html` and `chat-inline.html`
- [x] Chat JS: `web/static/js/chat.js` handles message rendering
- [x] Timestamps stored: `ConversationTurnDB.created_at` in database
- [x] Backend endpoint: `/api/v1/conversations/{id}/turns` (from #563) returns timestamps

**My understanding of the task**:
This is a **frontend-only** feature with these components:
1. Date dividers between different calendar days
2. Session dividers for 8+ hour gaps
3. On-hover timestamps for individual messages
4. Always-visible dates for messages > 7 days old

### Part A.2: Work Characteristics Assessment

**Worktree Assessment:**
- [ ] Multiple agents will work in parallel - NO
- [ ] Task duration >30 minutes - YES
- [x] Frontend-only changes (templates + JS)
- [x] No database changes needed

**Assessment: SKIP WORKTREE** - Single agent, frontend-focused, moderate scope.

### Part B: PM Verification (Infrastructure Investigation)

**Verification commands run:**
```bash
ls -la templates/components/chat*.html
ls -la web/static/js/chat*.js
ls -la web/static/css/chat*.css
grep -n "appendMessage\|renderMessage" web/static/js/chat.js
```

**What actually exists:**
```
templates/components/chat-widget.html  # Chat widget template
templates/components/chat-inline.html  # Inline chat template
web/static/js/chat.js                  # Chat JavaScript logic
web/static/css/chat.css                # Chat styling
```

**Current message rendering** (from chat.js):
- Messages rendered via `appendMessage()` function (line 161)
- Uses `marked.js` for markdown
- Already stores `timestamp: Date.now()` in chatHistory for persistence
- **Key Integration Point**: Current timestamps are client-side; backend `created_at` needed for restored conversations

**Message structure** (from lines 161-185):
```javascript
// Current appendMessage signature:
function appendMessage(html, isUser = false, persist = true)

// Current chatHistory format (line 180):
chatHistory.push({ content: html, isUser, timestamp: Date.now() });
```

**Implementation Note**: Need to either:
1. Pass backend `created_at` to appendMessage for restored turns, OR
2. Store backend timestamps when restoring from API

**Backend data available**:
- `GET /api/v1/conversations/{id}/turns` returns `created_at` for each turn
- Format: ISO 8601 (`"2026-01-10T17:56:11.838235"`)

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Infrastructure understood, pure frontend work

---

## Phase 0: Initial Bookending

### Required Actions

```bash
# 1. Verify issue exists
gh issue view 564

# 2. Update issue status to indicate work started
gh issue comment 564 -b "## Status: Implementation Started
- [x] Dependency #563 complete
- [ ] Phase 1: Date dividers
- [ ] Phase 2: Session dividers
- [ ] Phase 3: Hover timestamps
- [ ] Phase 4: Staleness indicator"
```

---

## Phase 0.6-0.8: Skipped Phases (Documented)

**Phase 0.6 (Data Flow & Integration)**: SKIP - Frontend-only feature, no multi-layer data propagation.

**Phase 0.7 (Conversation Design)**: SKIP - Not a conversational/multi-turn feature.

**Phase 0.8 (Post-Completion Integration)**: SKIP - No database state changes, no side-effects on other features.

---

## Phase 0.5: Frontend-Backend Contract Verification

### Endpoints Used

| Endpoint | Full Path | Returns |
|----------|-----------|---------|
| get_turns | `/api/v1/conversations/{id}/turns` | `[{id, turn_number, user_message, assistant_response, created_at}]` |

### Timestamp Format
```javascript
// Backend returns ISO 8601
"created_at": "2026-01-10T17:56:11.838235"

// Frontend uses Intl.DateTimeFormat for localization
new Date("2026-01-10T17:56:11.838235")
```

---

## Phase 1: Date Dividers

### 1.1 Create Timestamp Utility Functions

**File**: `web/static/js/timestamp-utils.js` (NEW)

```javascript
/**
 * Timestamp utilities for chat UI (Issue #564)
 */
const TimestampUtils = {
  /**
   * Format date for divider display
   * Returns: "Today", "Yesterday", or "January 9, 2026"
   */
  formatDateDivider(date) {
    const now = new Date();
    const messageDate = new Date(date);

    // Reset to start of day for comparison
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const messageDay = new Date(messageDate.getFullYear(), messageDate.getMonth(), messageDate.getDate());

    const diffDays = Math.floor((today - messageDay) / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return "Today";
    if (diffDays === 1) return "Yesterday";

    return messageDate.toLocaleDateString(undefined, {
      month: 'long',
      day: 'numeric',
      year: 'numeric'
    });
  },

  /**
   * Check if two dates are on different calendar days
   */
  isDifferentDay(date1, date2) {
    const d1 = new Date(date1);
    const d2 = new Date(date2);
    return d1.toDateString() !== d2.toDateString();
  },

  /**
   * Check if gap between dates is > 8 hours
   */
  isSessionGap(date1, date2) {
    const gap = Math.abs(new Date(date2) - new Date(date1));
    return gap > (8 * 60 * 60 * 1000); // 8 hours in ms
  },

  /**
   * Format time for hover tooltip
   * Today: "2:30 PM"
   * Older: "Jan 9, 2:30 PM"
   */
  formatHoverTime(date) {
    const now = new Date();
    const messageDate = new Date(date);
    const isToday = now.toDateString() === messageDate.toDateString();

    if (isToday) {
      return messageDate.toLocaleTimeString(undefined, {
        hour: 'numeric',
        minute: '2-digit'
      });
    }

    return messageDate.toLocaleDateString(undefined, {
      month: 'short',
      day: 'numeric'
    }) + ', ' + messageDate.toLocaleTimeString(undefined, {
      hour: 'numeric',
      minute: '2-digit'
    });
  },

  /**
   * Check if date is more than 7 days ago
   */
  isStale(date) {
    const now = new Date();
    const messageDate = new Date(date);
    const diffDays = Math.floor((now - messageDate) / (1000 * 60 * 60 * 24));
    return diffDays > 7;
  }
};

// Export for module usage or attach to window
if (typeof module !== 'undefined') {
  module.exports = TimestampUtils;
} else {
  window.TimestampUtils = TimestampUtils;
}
```

### 1.2 Add Date Divider HTML/CSS

**File**: `web/static/css/chat.css` (APPEND)

```css
/* Date/Session Dividers - Issue #564 */
.chat-date-divider {
  display: flex;
  align-items: center;
  margin: 16px 0;
  color: #666;
  font-size: 12px;
}

.chat-date-divider::before,
.chat-date-divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid #e0e0e0;
}

.chat-date-divider::before {
  margin-right: 12px;
}

.chat-date-divider::after {
  margin-left: 12px;
}

.chat-date-divider span {
  white-space: nowrap;
}
```

### 1.3 Modify Message Rendering

**File**: `web/static/js/chat.js` (MODIFY)

**Step 1**: Extend `appendMessage()` signature to accept timestamp:
```javascript
// BEFORE (line 161):
function appendMessage(html, isUser = false, persist = true)

// AFTER:
function appendMessage(html, isUser = false, persist = true, timestamp = null)
```

**Step 2**: Add module-level variable for tracking last message date:
```javascript
let lastMessageDate = null;  // Track for divider logic
```

**Step 3**: Add divider logic inside `appendMessage()`, before creating msgContainer:
```javascript
// Determine timestamp to use
const msgTimestamp = timestamp || Date.now();

// Check if we need a date divider
if (lastMessageDate && TimestampUtils.isDifferentDay(lastMessageDate, msgTimestamp)) {
  const divider = document.createElement('div');
  divider.className = 'chat-date-divider';
  divider.innerHTML = `<span>${TimestampUtils.formatDateDivider(msgTimestamp)}</span>`;
  chatWindow.appendChild(divider);
}
lastMessageDate = msgTimestamp;
```

**Step 4**: Update chatHistory to use provided timestamp:
```javascript
// Line 180 becomes:
chatHistory.push({ content: html, isUser, timestamp: msgTimestamp });
```

**Step 5**: Update `restoreChatHistory()` to pass stored timestamp:
```javascript
// Line 201 becomes:
appendMessage(msg.content, msg.isUser, false, msg.timestamp);
```

### Acceptance Criteria - Phase 1

- [ ] `timestamp-utils.js` created with formatting functions
- [ ] Date dividers appear between different calendar days
- [ ] Format: "Today", "Yesterday", "January 9, 2026"
- [ ] Styling matches rest of UI

---

## Phase 2: Session Dividers

### 2.1 Add Session Divider Logic

Extend the divider check in chat.js:
```javascript
// After date divider check, check for session gap on same day
if (!TimestampUtils.isDifferentDay(lastMessageDate, messageTimestamp) &&
    TimestampUtils.isSessionGap(lastMessageDate, messageTimestamp)) {
  const divider = document.createElement('div');
  divider.className = 'chat-date-divider chat-session-divider';
  divider.innerHTML = `<span>Earlier today</span>`;
  chatWindow.appendChild(divider);
}
```

### 2.2 Session Divider Styling (Optional Variation)

```css
.chat-session-divider {
  color: #888;  /* Slightly lighter than date divider */
}
```

### Acceptance Criteria - Phase 2

- [ ] Session dividers appear after 8+ hour gaps
- [ ] Shows "Earlier today" (or time like "9:00 AM")
- [ ] Works correctly with restored conversations

---

## Phase 3: On-Hover Timestamps

### 3.1 Add Timestamp Attribute to Messages

When rendering messages, add data attribute:
```javascript
messageDiv.dataset.timestamp = messageTimestamp;
```

### 3.2 Add Hover Tooltip CSS

```css
/* Hover Timestamps - Issue #564 */
.message[data-timestamp] {
  position: relative;
}

.message-timestamp-tooltip {
  position: absolute;
  right: 8px;
  top: 4px;
  background: rgba(0, 0, 0, 0.75);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 11px;
  opacity: 0;
  transition: opacity 0.2s ease-in-out;
  pointer-events: none;
  white-space: nowrap;
}

.message:hover .message-timestamp-tooltip {
  opacity: 1;
}
```

### 3.3 Add Hover Handler

```javascript
// Add tooltip element to each message
function addTimestampTooltip(messageDiv, timestamp) {
  const tooltip = document.createElement('div');
  tooltip.className = 'message-timestamp-tooltip';
  tooltip.textContent = TimestampUtils.formatHoverTime(timestamp);
  messageDiv.appendChild(tooltip);
}
```

### Acceptance Criteria - Phase 3

- [ ] Hovering on message shows timestamp
- [ ] Format: "2:30 PM" for today, "Jan 9, 2:30 PM" for older
- [ ] ~200-300ms delay via CSS transition (no JS hover delay needed)
- [ ] No flicker on quick mouse movement

---

## Phase 4: Staleness Indicator

### 4.1 Always-Visible Date for Old Messages

```javascript
// In message rendering
if (TimestampUtils.isStale(messageTimestamp)) {
  const dateLabel = document.createElement('div');
  dateLabel.className = 'message-stale-date';
  dateLabel.textContent = TimestampUtils.formatHoverTime(messageTimestamp);
  messageDiv.appendChild(dateLabel);
}
```

### 4.2 Staleness Styling

```css
.message-stale-date {
  font-size: 10px;
  color: #888;
  margin-top: 4px;
}
```

### Acceptance Criteria - Phase 4

- [ ] Messages > 7 days old show date always (not just on hover)
- [ ] Consistent styling with hover timestamps

---

## Agent Deployment

**Single Agent Assignment**: This is frontend-only work with sequential dependencies (CSS must exist before JS uses classes). No parallel agent deployment needed.

| Phase | Agent | Evidence Required |
|-------|-------|-------------------|
| 1-4 | Claude Code | Screenshots, test output |
| Z | Claude Code | Manual verification, PM approval |

---

## Phase Z: Final Verification

### Testing Checklist

**JavaScript Unit Tests** (Note: Uses browser APIs, consider manual verification or Jest if configured):

If Jest is available: `tests/unit/web/test_timestamp_utils.js`
Otherwise: Manual console testing in browser DevTools

**Test Cases** (`tests/unit/web/test_timestamp_utils.py` - Python equivalent for logic verification):
- [ ] `test_format_today_time_only`
- [ ] `test_format_yesterday`
- [ ] `test_format_older_date`
- [ ] `test_detect_day_boundary`
- [ ] `test_detect_session_gap_8_hours`
- [ ] `test_no_gap_for_continuous_conversation`

**Manual Testing**:
- [ ] Date dividers between days work
- [ ] Session dividers after 8+ hours work
- [ ] Hover timestamps work (correct format)
- [ ] No flicker on quick mouse movement
- [ ] Staleness dates visible for old messages
- [ ] Works with restored conversations

### Evidence Required

```bash
# Screenshot of date dividers
# Screenshot of hover timestamp
# Screenshot of stale message with date

# Test output
python -m pytest tests/unit/web/test_timestamp_utils.py -v
```

### Files Modified/Created

| File | Action |
|------|--------|
| `web/static/js/timestamp-utils.js` | CREATE |
| `web/static/js/chat.js` | MODIFY |
| `web/static/css/chat.css` | MODIFY |
| `templates/components/chat-widget.html` | MODIFY (script include) |
| `tests/unit/web/test_timestamp_utils.py` | CREATE |

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Timestamp utils | ❌ | |
| Date dividers | ❌ | |
| Session dividers | ❌ | |
| Hover timestamps | ❌ | |
| Staleness indicator | ❌ | |
| Unit tests | ❌ | |
| Manual testing | ❌ | |

---

## STOP Conditions

- #563 not complete - ✅ CLEARED (complete)
- Hover behavior causes performance issues
- Timezone handling creates bugs
- Design doesn't match rest of UI
- Static file path mismatch (verify with `grep -n "StaticFiles" web/app.py`)
- `chat.js` structure differs from assumptions (verify `appendMessage` exists)

---

## Success Criteria (Issue Completion Requires)

- [ ] All acceptance criteria met (Phases 1-4)
- [ ] Evidence provided for each criterion (screenshots + test output)
- [ ] Manual testing complete (6 test cases)
- [ ] No regressions to existing chat functionality
- [ ] GitHub issue #564 fully updated with evidence
- [ ] PM approval received

---

## PM Approval Request Template

```markdown
@PM - Issue #564 complete and ready for review:
- All acceptance criteria met ✓
- Evidence provided (screenshots in issue) ✓
- Manual testing complete ✓
- No regressions confirmed ✓

Please review and close if satisfied.
```

---

## Notes

- Use browser timezone via `Intl.DateTimeFormat` - no timezone selection UI
- CSS transitions handle hover delay (no JS setTimeout needed)
- Session dividers only within same day; date dividers take precedence
- This is frontend-only; no backend changes required
