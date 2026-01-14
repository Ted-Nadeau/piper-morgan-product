# STANDUP-CHAT-WIDGET: Chat Interface Integration

**Priority**: P0
**Labels**: `enhancement`, `component: ui`, `standup`
**Milestone**: MVP
**Epic**: #242 (CONV-MCP-STANDUP-INTERACTIVE)
**Related**: #242-A (dependency), #242-B (dependency)

---

## Problem Statement

### Current State
Interactive standup conversation (#242-A, #242-B) works at the service layer, but users need a chat interface to access it. Current web UI shows static standup output with no conversation capability.

### Impact
- **Blocks**: User-facing interactive standup experience
- **User Impact**: Cannot access conversation features without chat UI
- **Technical Debt**: Web interface doesn't support real-time conversation

### Strategic Context
This bridges the backend conversation capability to the user-facing web interface. Completes the interactive standup user journey.

---

## Goal

**Primary Objective**: Integrate chat widget into web interface that enables interactive standup conversations.

**Example User Experience**:
```
[User opens Piper web app]
[Chat widget visible in corner or dedicated page]
User types: "standup"
[Real-time response appears in chat]
Piper: "Ready for your standup? Focus on GitHub work?"
[User types response, conversation continues]
```

**Not In Scope** (explicitly):
- ❌ State management (done in #242-A)
- ❌ Conversation flow logic (done in #242-B)
- ❌ Preference learning (see #242-D)
- ❌ Performance optimization (see #242-E)
- ❌ Mobile native app (web-responsive only)

---

## What Already Exists

### Infrastructure ✅
- Web interface at `templates/` + `web/static/`
- Chat endpoint at `/api/v1/chat` (verify)
- JavaScript utilities in `web/static/js/`
- Responsive CSS framework

### What's Missing ❌
- Chat widget component
- Real-time message display
- Conversation history UI
- Integration with existing auth
- Mobile-responsive chat layout

---

## Requirements

### Phase 0: Investigation & Setup
- [ ] Verify existing chat API endpoints
- [ ] Review current web interface patterns
- [ ] Assess WebSocket vs polling for real-time
- [ ] Confirm auth integration approach

### Phase 1: Chat Widget Component
**Objective**: Create reusable chat widget

**Tasks**:
- [ ] Create `templates/components/chat_widget.html`
- [ ] Create `web/static/js/chat.js`
- [ ] Create `web/static/css/chat.css`
- [ ] Implement message input/display

**Deliverables**:
- Expandable/collapsible chat widget
- Message history display
- Typing indicator
- Send button + enter key support

### Phase 2: API Integration
**Objective**: Connect widget to conversation API

**Tasks**:
- [ ] Implement fetch-based message sending
- [ ] Handle response streaming (if available) or polling
- [ ] Integrate with session/auth
- [ ] Handle connection errors gracefully

**Deliverables**:
- Messages sent to `/api/v1/chat` (or appropriate endpoint)
- Responses displayed in real-time
- Session context preserved

### Phase 3: UI Polish
**Objective**: Production-quality user experience

**Tasks**:
- [ ] Mobile-responsive layout
- [ ] Conversation history scroll behavior
- [ ] Loading states
- [ ] Error states with retry

**Deliverables**:
- Works on mobile browsers
- Smooth scrolling to new messages
- Clear feedback during loading/errors

### Phase 4: Integration Points
**Objective**: Integrate with existing pages

**Tasks**:
- [ ] Add chat widget to home page
- [ ] Add chat widget to standup page (if separate)
- [ ] Ensure non-interference with existing UI

### Phase 5: Tests

**Tasks**:
- [ ] Unit tests for chat.js
- [ ] Integration tests for API calls
- [ ] Manual testing checklist for UI

### Phase Z: Completion & Handoff
- [ ] All acceptance criteria met
- [ ] Evidence provided
- [ ] GitHub issue updated

---

## Acceptance Criteria

### Chat Interface
- [ ] Web chat widget functional
- [ ] Real-time message handling working
- [ ] Mobile-responsive conversation UI
- [ ] Context preservation across browser sessions
- [ ] Integration with existing auth system
- [ ] Conversation history accessible

### Quality
- [ ] No regressions in existing UI
- [ ] Follows existing CSS/JS patterns
- [ ] Accessible (keyboard navigation, screen reader basics)

### Testing
- [ ] JavaScript unit tests
- [ ] Manual testing scenarios verified

---

## Completion Matrix

| Component | Status | Evidence |
|-----------|--------|----------|
| `chat_widget.html` | ⏸️ | |
| `chat.js` | ⏸️ | |
| `chat.css` | ⏸️ | |
| API integration | ⏸️ | |
| Mobile responsive | ⏸️ | |
| Auth integration | ⏸️ | |
| Tests | ⏸️ | |

---

## Testing Strategy

### Manual Testing Checklist
- [ ] Open chat widget on desktop
- [ ] Send "standup" message
- [ ] Verify response appears
- [ ] Complete multi-turn conversation
- [ ] Test on mobile browser
- [ ] Test with slow network
- [ ] Test error recovery

---

## STOP Conditions

Stop immediately and escalate if:
- [ ] Chat API endpoint doesn't exist or differs from expected
- [ ] WebSocket infrastructure needed but not available
- [ ] Auth integration blocked
- [ ] #242-A or #242-B not complete
- [ ] Tests fail for any reason

---

## Effort Estimate

**Overall Size**: Medium-Large (2-3 days)

**Breakdown**:
- Phase 0: Small (investigation)
- Phase 1: Medium (widget component)
- Phase 2: Medium (API integration)
- Phase 3: Small (polish)
- Phase 4: Small (integration)
- Phase 5: Small (tests)

---

## Dependencies

### Required
- [ ] #242-A (State Management) - backend ready
- [ ] #242-B (Conversation Flow) - backend ready
- [ ] Chat API endpoint operational

### Can Parallelize With
- #242-D (Learning) - independent frontend vs backend work

---

_Issue created: 2026-01-07_
