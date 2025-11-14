# Phase 3 Agent Prompt: Pattern Suggestions UI
## Issue #300 - Web Chat Suggestions Implementation

**Date**: November 13, 2025, 5:25 PM PT
**From**: Lead Developer
**To**: Code Agent
**Priority**: P2 (Alpha Feature)
**Estimated Effort**: 5.5 hours

---

## Mission

Implement the **Pattern Suggestions UI** for Piper Morgan's web chat interface using the "Thoughtful Colleague" design pattern. This adds a user-facing suggestion system where Piper can recommend actions based on learned patterns.

**What you're building**: The visible face of the learning system - where users discover, evaluate, and provide feedback on pattern suggestions.

**Success looks like**: After performing an action 3 times, user sees a subtle notification badge, expands it to see suggestions with clear reasoning, and can accept/reject with optional feedback.

---

## Context: What Already Exists

### Phase 1 & 2 Complete ✅

**Backend Infrastructure** (fully working):
- ✅ `LearningHandler.get_suggestions()` - Returns top patterns
- ✅ Pattern capture in IntentService - Real-time learning
- ✅ Confidence calculation - Evidence-based scoring
- ✅ LearnedPattern model - Database persistence
- ✅ Pattern management API - 7 REST endpoints (Phase 2)

**Frontend Structure** (vanilla JS):
- Main chat UI: `templates/home.html`
- Message renderer: `web/assets/bot-message-renderer.js`
- No React/Vue - pure vanilla JavaScript

**What's Missing**: The UI to show suggestions and collect feedback

---

## UX Design: "Thoughtful Colleague" Pattern

### Design Philosophy

Imagine a colleague who observes your work for a few weeks, then leans over and says: *"Hey, I noticed you always create GitHub issues after standup. Want me to remind you next time?"*

**Key Principles** (from UX specialist):
1. **Transparency Over Magic** - Show WHY, not just WHAT
2. **Control Over Convenience** - User initiates, never auto-apply
3. **Context Over Clutter** - Only show when confident (>0.7)
4. **Dialogue Over Data** - Teaching, not surveying
5. **Evolution Over Perfection** - Learning together

### Visual Pattern

**Collapsed State** (default):
```
┌─────────────────────────────────────────┐
│ Piper's Response                        │
│ Here's your standup summary...          │
│                                         │
│ ┌─────────────────────────────────┐    │
│ │ 💡 3 pattern suggestions        │    │ ← Teal badge
│ │ [Show suggestions ▼]            │    │
│ └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

**Expanded State** (user clicks):
```
┌─────────────────────────────────────────┐
│ 💡 Based on your patterns:              │
│                                         │
│ ┌───────────────────────────────────┐  │
│ │ Create GitHub issue               │  │
│ │ I noticed you create issues after │  │
│ │ standup (3x this week, 85% conf.) │  │
│ │                                   │  │
│ │ ████████████░░░░░ 85%            │  │ ← Visual bar
│ │                                   │  │
│ │ [✓ Accept] [✗ Reject] [Dismiss]  │  │
│ └───────────────────────────────────┘  │
│                                         │
│ [More suggestions...] [Hide ▲]         │
└─────────────────────────────────────────┘
```

**First-Time User** (onboarding):
```
┌─────────────────────────────────────────┐
│ 💡 New: Pattern Suggestions            │
│                                         │
│ Piper noticed patterns in how you work │
│ and can suggest helpful next steps.    │
│ You're always in control.              │
│                                         │
│ [Got it] [Learn more]                  │
└─────────────────────────────────────────┘
```

---

## Phase 3.1: Backend Integration (1 hour)

### Task: Wire get_suggestions() into IntentService

**File**: `services/intent/intent_service.py`

**Location**: After `capture_action()` call (around line 145)

**What to add**:
```python
async def execute(
    self,
    user_input: str,
    user_id: UUID,
    context: Optional[Dict[str, Any]] = None,
    session: Optional[AsyncSession] = None
) -> IntentProcessingResult:

    # ... existing code (classification, capture_action, etc.) ...

    # NEW: Get pattern suggestions
    suggestions = await self.learning_handler.get_suggestions(
        user_id=user_id,
        context={
            "intent": intent,
            "current_context": context
        },
        min_confidence=0.7,  # suggestion_threshold
        limit=3,  # Top 3 suggestions
        session=session
    )

    # ... rest of orchestration ...

    # Add suggestions to result
    result = IntentProcessingResult(
        intent=intent,
        response=response,
        suggestions=suggestions if suggestions else None,  # Only if exists
        # ... other fields ...
    )

    return result
```

**Modify**: `IntentProcessingResult` dataclass

**File**: `services/intent/intent_service.py` (or wherever defined)

**Add field**:
```python
@dataclass
class IntentProcessingResult:
    intent: str
    response: str
    # ... existing fields ...
    suggestions: Optional[List[Dict[str, Any]]] = None  # NEW
```

**HTTP Route** (should already pass through):

**File**: `web/api/routes/chat.py` (or wherever chat route is)

**Verify** the route returns `IntentProcessingResult` as JSON - suggestions will automatically be included.

### Evidence Required

1. **Code changes**:
   ```bash
   git diff services/intent/intent_service.py
   ```

2. **Test with curl**:
   ```bash
   # After performing action 3x to create pattern
   curl -X POST http://localhost:8001/api/v1/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "standup", "user_id": "test-uuid"}'
   ```

   **Expected response** (should include):
   ```json
   {
     "response": "...",
     "suggestions": [
       {
         "pattern_id": "uuid",
         "pattern_type": "USER_WORKFLOW",
         "description": "Create GitHub issue for follow-ups",
         "confidence": 0.85,
         "reasoning": "You created issues after standup 3 times this week"
       }
     ]
   }
   ```

3. **Log verification**:
   ```
   [2025-11-13 17:30:45] IntentService: Retrieved 3 suggestions for user test-uuid
   ```

---

## Phase 3.2: Frontend UI Core (2 hours)

### Task: Implement Suggestion UI Components

**File**: `web/assets/bot-message-renderer.js` (or new file: `suggestion-ui.js`)

### Component 1: Notification Badge (Collapsed State)

**HTML Template**:
```javascript
function renderSuggestionBadge(suggestionsCount) {
    return `
        <div class="suggestions-container collapsed" id="suggestions-container">
            <div class="suggestions-badge" role="button"
                 aria-expanded="false"
                 aria-controls="suggestions-panel"
                 onclick="toggleSuggestions()">
                <span class="badge-icon">💡</span>
                <span class="badge-text">
                    ${suggestionsCount} pattern suggestion${suggestionsCount > 1 ? 's' : ''}
                </span>
                <button class="expand-btn" aria-label="Show suggestions">
                    <span class="icon-chevron-down">▼</span>
                </button>
            </div>
        </div>
    `;
}
```

**CSS** (add to main stylesheet or create `suggestions.css`):
```css
/* Suggestion Badge - Collapsed State */
.suggestions-container {
    margin-top: 12px;
    margin-bottom: 8px;
}

.suggestions-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 16px;
    background-color: #E6F7F7; /* Subtle teal */
    border-left: 3px solid #0095A8; /* Teal accent */
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.suggestions-badge:hover {
    background-color: #D0EDED;
}

.badge-icon {
    font-size: 20px;
}

.badge-text {
    flex: 1;
    font-size: 14px;
    font-weight: 500;
    color: #2C3E50;
}

.expand-btn {
    background: none;
    border: none;
    cursor: pointer;
    padding: 4px;
    color: #0095A8;
    transition: transform 0.2s ease;
}

.suggestions-container.expanded .expand-btn .icon-chevron-down {
    transform: rotate(180deg);
}
```

---

### Component 2: Suggestion Cards (Expanded State)

**HTML Template**:
```javascript
function renderSuggestionPanel(suggestions) {
    return `
        <div class="suggestions-panel" id="suggestions-panel" hidden>
            <div class="panel-header">
                <span class="panel-title">💡 Based on your patterns:</span>
            </div>

            ${suggestions.map(suggestion => renderSuggestionCard(suggestion)).join('')}

            <div class="panel-footer">
                <button class="hide-btn" onclick="toggleSuggestions()">
                    Hide suggestions ▲
                </button>
            </div>
        </div>
    `;
}

function renderSuggestionCard(suggestion) {
    return `
        <div class="suggestion-card" data-pattern-id="${suggestion.pattern_id}">
            <div class="card-header">
                <h4 class="suggestion-title">${suggestion.description}</h4>
                <span class="pattern-type">${formatPatternType(suggestion.pattern_type)}</span>
            </div>

            <div class="suggestion-reasoning">
                ${suggestion.reasoning || generateReasoning(suggestion)}
            </div>

            <div class="confidence-display">
                <div class="confidence-bar-container">
                    <div class="confidence-bar"
                         style="width: ${(suggestion.confidence * 100).toFixed(0)}%"
                         role="progressbar"
                         aria-valuenow="${(suggestion.confidence * 100).toFixed(0)}"
                         aria-valuemin="0"
                         aria-valuemax="100">
                    </div>
                </div>
                <span class="confidence-text">
                    ${(suggestion.confidence * 100).toFixed(0)}% confident
                </span>
            </div>

            <div class="suggestion-actions">
                <button class="action-btn accept-btn"
                        onclick="handleAccept('${suggestion.pattern_id}')">
                    <span class="btn-icon">✓</span> Accept
                </button>
                <button class="action-btn reject-btn"
                        onclick="handleReject('${suggestion.pattern_id}')">
                    <span class="btn-icon">✗</span> Reject
                </button>
                <button class="action-btn dismiss-btn"
                        onclick="handleDismiss('${suggestion.pattern_id}')">
                    Dismiss
                </button>
            </div>
        </div>
    `;
}

function generateReasoning(suggestion) {
    // Generate friendly reasoning text
    const count = suggestion.usage_count || 3;
    return `I noticed you ${suggestion.description.toLowerCase()} ${count} times this week.`;
}

function formatPatternType(type) {
    const types = {
        'USER_WORKFLOW': 'Workflow',
        'COMMAND_SEQUENCE': 'Command',
        'TIME_BASED': 'Schedule',
        'CONTEXT_BASED': 'Context'
    };
    return types[type] || type;
}
```

**CSS for Cards**:
```css
/* Suggestion Panel - Expanded State */
.suggestions-panel {
    margin-top: 12px;
    background: white;
    border: 1px solid #E0E0E0;
    border-radius: 8px;
    padding: 16px;
}

.panel-header {
    margin-bottom: 16px;
}

.panel-title {
    font-size: 16px;
    font-weight: 600;
    color: #2C3E50;
}

/* Individual Suggestion Cards */
.suggestion-card {
    background: #FAFAFA;
    border: 1px solid #E0E0E0;
    border-left: 3px solid #0095A8; /* Teal accent */
    border-radius: 6px;
    padding: 16px;
    margin-bottom: 12px;
    transition: box-shadow 0.2s ease;
}

.suggestion-card:hover {
    box-shadow: 0 2px 8px rgba(0, 149, 168, 0.15);
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.suggestion-title {
    font-size: 15px;
    font-weight: 600;
    color: #2C3E50;
    margin: 0;
}

.pattern-type {
    font-size: 12px;
    color: #7F8C8D;
    background: #ECF0F1;
    padding: 2px 8px;
    border-radius: 4px;
}

.suggestion-reasoning {
    font-size: 14px;
    color: #5D6D7E;
    margin-bottom: 12px;
    line-height: 1.4;
}

/* Confidence Display */
.confidence-display {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
}

.confidence-bar-container {
    flex: 1;
    height: 8px;
    background: #ECF0F1;
    border-radius: 4px;
    overflow: hidden;
}

.confidence-bar {
    height: 100%;
    background: linear-gradient(90deg, #0095A8 0%, #FF7043 100%); /* Teal to orange */
    transition: width 0.3s ease;
    border-radius: 4px;
}

.confidence-text {
    font-size: 13px;
    font-weight: 500;
    color: #0095A8;
    min-width: 90px;
}

/* Action Buttons */
.suggestion-actions {
    display: flex;
    gap: 8px;
}

.action-btn {
    flex: 1;
    padding: 8px 12px;
    border: 1px solid;
    border-radius: 5px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
}

.accept-btn {
    background: #0095A8; /* Teal */
    color: white;
    border-color: #0095A8;
}

.accept-btn:hover {
    background: #007A8A;
}

.reject-btn {
    background: white;
    color: #FF7043; /* Orange */
    border-color: #FF7043;
}

.reject-btn:hover {
    background: #FFF5F2;
}

.dismiss-btn {
    background: white;
    color: #7F8C8D; /* Gray */
    border-color: #BDC3C7;
}

.dismiss-btn:hover {
    background: #F8F9FA;
}

.panel-footer {
    margin-top: 12px;
    text-align: center;
}

.hide-btn {
    background: none;
    border: none;
    color: #0095A8;
    font-size: 14px;
    cursor: pointer;
    padding: 8px;
}

.hide-btn:hover {
    text-decoration: underline;
}
```

---

### Component 3: Interaction Handlers

**JavaScript Functions**:
```javascript
// Toggle expand/collapse
function toggleSuggestions() {
    const container = document.getElementById('suggestions-container');
    const panel = document.getElementById('suggestions-panel');
    const badge = container.querySelector('.suggestions-badge');

    const isExpanded = container.classList.contains('expanded');

    if (isExpanded) {
        // Collapse
        container.classList.remove('expanded');
        panel.hidden = true;
        badge.setAttribute('aria-expanded', 'false');
    } else {
        // Expand
        container.classList.add('expanded');
        panel.hidden = false;
        badge.setAttribute('aria-expanded', 'true');
    }
}

// Handle Accept
async function handleAccept(patternId) {
    // Show feedback modal
    const comment = await showFeedbackModal('accept', patternId);

    // Send feedback to backend
    const response = await fetch(`/api/v1/learning/patterns/${patternId}/feedback`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            action: 'accept',
            comment: comment || null
        })
    });

    if (response.ok) {
        showSuccessMessage('Thanks! This will improve future suggestions.');
        removeSuggestionCard(patternId);
    } else {
        showErrorMessage('Failed to record feedback. Please try again.');
    }
}

// Handle Reject
async function handleReject(patternId) {
    // Show feedback modal
    const comment = await showFeedbackModal('reject', patternId);

    // Send feedback to backend
    const response = await fetch(`/api/v1/learning/patterns/${patternId}/feedback`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            action: 'reject',
            comment: comment || null
        })
    });

    if (response.ok) {
        showSuccessMessage('Got it. I won\'t suggest this again.');
        removeSuggestionCard(patternId);
    } else {
        showErrorMessage('Failed to record feedback. Please try again.');
    }
}

// Handle Dismiss
function handleDismiss(patternId) {
    // Just remove from view, no backend call
    removeSuggestionCard(patternId);
}

// Remove card from UI
function removeSuggestionCard(patternId) {
    const card = document.querySelector(`[data-pattern-id="${patternId}"]`);
    if (card) {
        card.style.opacity = '0';
        card.style.transition = 'opacity 0.3s ease';
        setTimeout(() => card.remove(), 300);

        // If no more cards, hide panel
        const remainingCards = document.querySelectorAll('.suggestion-card');
        if (remainingCards.length === 0) {
            toggleSuggestions(); // Collapse
        }
    }
}

// Show feedback modal (optional comment)
function showFeedbackModal(action, patternId) {
    return new Promise((resolve) => {
        const modal = document.createElement('div');
        modal.className = 'feedback-modal';
        modal.innerHTML = `
            <div class="modal-overlay" onclick="closeFeedbackModal()"></div>
            <div class="modal-content">
                <h3>${action === 'accept' ? '✅ Thanks!' : '❌ Got it'}</h3>
                <p>${action === 'accept'
                    ? 'Help us improve: Why is this suggestion helpful?'
                    : 'Help us improve: Why not this suggestion?'}
                </p>
                <textarea id="feedback-text"
                          placeholder="Optional: Share your thoughts..."
                          rows="3"></textarea>
                <div class="modal-actions">
                    <button onclick="submitFeedback('${action}', '${patternId}')">
                        Submit Feedback
                    </button>
                    <button onclick="skipFeedback('${action}', '${patternId}')">
                        Skip
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);

        // Store resolve function for later
        window._feedbackResolve = resolve;
    });
}

function submitFeedback(action, patternId) {
    const comment = document.getElementById('feedback-text').value.trim();
    closeFeedbackModal();
    if (window._feedbackResolve) {
        window._feedbackResolve(comment);
    }
}

function skipFeedback(action, patternId) {
    closeFeedbackModal();
    if (window._feedbackResolve) {
        window._feedbackResolve(null);
    }
}

function closeFeedbackModal() {
    const modal = document.querySelector('.feedback-modal');
    if (modal) modal.remove();
}

// Success/Error messages
function showSuccessMessage(message) {
    showToast(message, 'success');
}

function showErrorMessage(message) {
    showToast(message, 'error');
}

function showToast(message, type) {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
```

**CSS for Modal & Toast**:
```css
/* Feedback Modal */
.feedback-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1000;
}

.modal-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
}

.modal-content {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: white;
    border-radius: 8px;
    padding: 24px;
    max-width: 400px;
    width: 90%;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.modal-content h3 {
    margin: 0 0 12px 0;
    color: #2C3E50;
}

.modal-content p {
    margin: 0 0 16px 0;
    color: #5D6D7E;
    font-size: 14px;
}

.modal-content textarea {
    width: 100%;
    padding: 8px;
    border: 1px solid #E0E0E0;
    border-radius: 4px;
    font-family: inherit;
    font-size: 14px;
    resize: vertical;
}

.modal-actions {
    display: flex;
    gap: 8px;
    margin-top: 16px;
}

.modal-actions button {
    flex: 1;
    padding: 10px;
    border: 1px solid #0095A8;
    border-radius: 5px;
    background: #0095A8;
    color: white;
    cursor: pointer;
    font-size: 14px;
}

.modal-actions button:last-child {
    background: white;
    color: #0095A8;
}

/* Toast Messages */
.toast {
    position: fixed;
    bottom: 20px;
    right: 20px;
    padding: 12px 20px;
    border-radius: 6px;
    color: white;
    font-size: 14px;
    opacity: 1;
    transition: opacity 0.3s ease;
    z-index: 1001;
}

.toast-success {
    background: #27AE60;
}

.toast-error {
    background: #E74C3C;
}
```

---

## Phase 3.3: First-Time Onboarding (30 min)

### Task: Show Tutorial on First Suggestion Ever

**Detection**:
```javascript
// Check if user has seen suggestions before
function hasSeenSuggestions() {
    return localStorage.getItem('piper_suggestions_seen') === 'true';
}

function markSuggestionsAsSeen() {
    localStorage.setItem('piper_suggestions_seen', 'true');
}
```

**Onboarding Tooltip**:
```javascript
function showOnboardingTooltip() {
    if (hasSeenSuggestions()) return;

    const tooltip = document.createElement('div');
    tooltip.className = 'onboarding-tooltip';
    tooltip.innerHTML = `
        <div class="tooltip-content">
            <div class="tooltip-header">
                <span class="tooltip-icon">💡</span>
                <h4>New: Pattern Suggestions</h4>
            </div>
            <p>Piper noticed patterns in how you work and can suggest
               helpful next steps. You're always in control.</p>
            <div class="tooltip-actions">
                <button onclick="dismissOnboarding()">Got it</button>
                <button onclick="showLearnMore()">Learn more</button>
            </div>
        </div>
    `;

    // Insert before suggestions badge
    const container = document.getElementById('suggestions-container');
    container.insertBefore(tooltip, container.firstChild);
}

function dismissOnboarding() {
    markSuggestionsAsSeen();
    document.querySelector('.onboarding-tooltip').remove();
}

function showLearnMore() {
    dismissOnboarding();
    showLearnMoreModal();
}

function showLearnMoreModal() {
    const modal = document.createElement('div');
    modal.className = 'learn-more-modal';
    modal.innerHTML = `
        <div class="modal-overlay" onclick="closeLearnMoreModal()"></div>
        <div class="modal-content">
            <h3>How Pattern Suggestions Work</h3>

            <div class="learn-section">
                <h4>🔍 Pattern Detection</h4>
                <p>Piper observes when you repeatedly do similar actions
                   (like creating issues after standup).</p>
            </div>

            <div class="learn-section">
                <h4>📊 Confidence</h4>
                <p>The percentage shows how confident Piper is based on
                   how often the pattern succeeds.</p>
            </div>

            <div class="learn-section">
                <h4>✓ Feedback</h4>
                <p>Accept helpful suggestions to see more like them.
                   Reject unhelpful ones to improve Piper's learning.</p>
            </div>

            <div class="learn-section">
                <h4>🔒 Privacy</h4>
                <p>Your patterns are private. Only you see them.</p>
            </div>

            <button onclick="closeLearnMoreModal()">Got it!</button>
        </div>
    `;
    document.body.appendChild(modal);
}

function closeLearnMoreModal() {
    const modal = document.querySelector('.learn-more-modal');
    if (modal) modal.remove();
}
```

**CSS for Onboarding**:
```css
/* Onboarding Tooltip */
.onboarding-tooltip {
    background: #FFF9E6;
    border: 2px solid #FFD54F;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
}

.tooltip-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
}

.tooltip-icon {
    font-size: 24px;
}

.tooltip-header h4 {
    margin: 0;
    color: #2C3E50;
    font-size: 16px;
}

.tooltip-content p {
    margin: 0 0 12px 0;
    color: #5D6D7E;
    font-size: 14px;
    line-height: 1.4;
}

.tooltip-actions {
    display: flex;
    gap: 8px;
}

.tooltip-actions button {
    padding: 8px 16px;
    border: 1px solid #FFD54F;
    border-radius: 5px;
    background: white;
    color: #F39C12;
    cursor: pointer;
    font-size: 14px;
}

.tooltip-actions button:first-child {
    background: #F39C12;
    color: white;
}

/* Learn More Modal */
.learn-more-modal .modal-content {
    max-width: 500px;
}

.learn-section {
    margin-bottom: 16px;
    padding-bottom: 16px;
    border-bottom: 1px solid #ECF0F1;
}

.learn-section:last-of-type {
    border-bottom: none;
}

.learn-section h4 {
    margin: 0 0 8px 0;
    color: #2C3E50;
    font-size: 15px;
}

.learn-section p {
    margin: 0;
    color: #7F8C8D;
    font-size: 14px;
    line-height: 1.4;
}

.learn-more-modal button {
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 5px;
    background: #0095A8;
    color: white;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    margin-top: 8px;
}
```

---

## Phase 3.4: Feedback Endpoint (1 hour)

### Task: Create POST /patterns/{id}/feedback Endpoint

**File**: `web/api/routes/learning.py`

**Add after existing pattern endpoints**:
```python
@router.post("/patterns/{pattern_id}/feedback")
async def provide_pattern_feedback(
    pattern_id: UUID,
    feedback: PatternFeedbackRequest,
    session: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Provide feedback on a pattern suggestion.

    Updates confidence based on user feedback:
    - Accept: Increases confidence, increments success_count
    - Reject: Decreases confidence, increments failure_count
    - Dismiss: No confidence change, tracked separately
    """

    # Get pattern (with user ownership check)
    async with AsyncSessionFactory.session_scope() as session:
        result = await session.execute(
            select(LearnedPattern)
            .where(
                LearnedPattern.id == pattern_id,
                LearnedPattern.user_id == TEST_USER_ID  # TODO: Replace with JWT
            )
            .with_for_update()  # Row locking
        )
        pattern = result.scalar_one_or_none()

        if not pattern:
            return {
                "status": "error",
                "code": "NOT_FOUND",
                "message": f"Pattern {pattern_id} not found",
                "details": {
                    "error_id": "PATTERN_NOT_FOUND",
                    "pattern_id": str(pattern_id)
                }
            }

        # Update based on feedback action
        if feedback.action == "accept":
            pattern.success_count += 2  # Weight explicit feedback higher
            pattern.confidence = min(pattern.confidence * 1.1, 1.0)  # Cap at 1.0
            message = "Thanks! This will improve future suggestions."

        elif feedback.action == "reject":
            pattern.failure_count += 2
            pattern.confidence *= 0.5  # Reduce confidence significantly
            message = "Got it. I won't suggest this again."

            # Disable if confidence drops too low
            if pattern.confidence < 0.3:
                pattern.enabled = False
                message += " (Pattern disabled)"

        elif feedback.action == "dismiss":
            # No confidence change, but track dismissals
            if not hasattr(pattern, 'dismissal_count'):
                pattern.dismissal_count = 0
            pattern.dismissal_count += 1
            message = "Dismissed for now."

        else:
            return {
                "status": "error",
                "code": "INVALID_ACTION",
                "message": f"Invalid action: {feedback.action}",
                "details": {
                    "error_id": "INVALID_FEEDBACK_ACTION",
                    "valid_actions": ["accept", "reject", "dismiss"]
                }
            }

        # Store optional comment
        if feedback.comment:
            # Store in pattern metadata or separate feedback table
            if not pattern.metadata:
                pattern.metadata = {}
            if 'feedback_comments' not in pattern.metadata:
                pattern.metadata['feedback_comments'] = []
            pattern.metadata['feedback_comments'].append({
                "action": feedback.action,
                "comment": feedback.comment,
                "timestamp": datetime.utcnow().isoformat()
            })

        # Update timestamp
        pattern.updated_at = datetime.utcnow()

        await session.commit()

        return {
            "success": True,
            "message": message,
            "pattern": {
                "id": str(pattern.id),
                "confidence": pattern.confidence,
                "enabled": pattern.enabled,
                "success_count": pattern.success_count,
                "failure_count": pattern.failure_count
            }
        }
```

**Request Model** (add to file):
```python
from pydantic import BaseModel, Field
from typing import Literal, Optional

class PatternFeedbackRequest(BaseModel):
    action: Literal["accept", "reject", "dismiss"] = Field(
        ..., description="User's feedback action"
    )
    comment: Optional[str] = Field(
        None, max_length=500, description="Optional qualitative feedback"
    )
```

### Evidence Required

1. **Code changes**:
   ```bash
   git diff web/api/routes/learning.py
   ```

2. **Test Accept**:
   ```bash
   curl -X POST http://localhost:8001/api/v1/learning/patterns/{PATTERN_ID}/feedback \
     -H "Content-Type: application/json" \
     -d '{"action": "accept", "comment": "I do this every standup"}'
   ```

   **Expected**:
   ```json
   {
     "success": true,
     "message": "Thanks! This will improve future suggestions.",
     "pattern": {
       "id": "...",
       "confidence": 0.93,  // Increased from 0.85
       "enabled": true,
       "success_count": 10,  // +2
       "failure_count": 1
     }
   }
   ```

3. **Test Reject** (low confidence disables):
   ```bash
   curl -X POST http://localhost:8001/api/v1/learning/patterns/{PATTERN_ID}/feedback \
     -H "Content-Type: application/json" \
     -d '{"action": "reject", "comment": "Not relevant to my workflow"}'
   ```

   **Expected** (if confidence drops below 0.3):
   ```json
   {
     "success": true,
     "message": "Got it. I won't suggest this again. (Pattern disabled)",
     "pattern": {
       "confidence": 0.25,
       "enabled": false
     }
   }
   ```

4. **Database verification**:
   ```sql
   SELECT id, confidence, enabled, success_count, failure_count, updated_at
   FROM learned_patterns
   WHERE id = 'pattern-id';
   ```

---

## Phase 3.5: Manual Testing (1 hour)

### Task: End-to-End Validation

**Create Test Document**: `dev/2025/11/13/phase-3-test-evidence.md`

### Test Scenario 1: First Suggestion Ever

**Steps**:
1. Clear localStorage (simulate first-time user)
2. Perform action 3 times to create pattern
3. Trigger action that would show suggestion
4. Verify onboarding tooltip appears
5. Click "Got it"
6. Verify notification badge appears

**Evidence**:
- Screenshot: Onboarding tooltip
- Screenshot: Notification badge after dismissal
- localStorage shows 'piper_suggestions_seen' = 'true'

---

### Test Scenario 2: Expand & View Suggestions

**Steps**:
1. Click "Show suggestions ▼" button
2. Verify panel expands smoothly
3. Verify 1-3 suggestion cards visible
4. Verify each card shows:
   - Description
   - Reasoning text
   - Confidence bar + percentage
   - Accept/Reject/Dismiss buttons

**Evidence**:
- Screenshot: Expanded panel with multiple cards
- Screenshot: Confidence display (bar + percentage)
- Video: Expand/collapse animation

---

### Test Scenario 3: Accept Suggestion

**Steps**:
1. Click "✓ Accept" on a suggestion
2. Verify feedback modal appears
3. Enter optional comment: "I do this every standup"
4. Click "Submit Feedback"
5. Verify success toast: "Thanks! This will improve..."
6. Verify card removed from view
7. Check database: confidence increased

**Evidence**:
- Screenshot: Feedback modal
- Screenshot: Success toast
- curl: GET pattern shows higher confidence
- Database: success_count incremented

---

### Test Scenario 4: Reject Suggestion

**Steps**:
1. Click "✗ Reject" on a suggestion
2. Verify feedback modal appears
3. Enter optional comment: "Not relevant to me"
4. Click "Submit Feedback"
5. Verify success toast: "Got it..."
6. Verify card removed
7. Check database: confidence decreased

**Evidence**:
- Screenshot: Reject flow
- curl: GET pattern shows lower confidence
- Database: failure_count incremented

**Edge case**: If confidence < 0.3, verify pattern disabled

---

### Test Scenario 5: Dismiss Suggestion

**Steps**:
1. Click "Dismiss" on a suggestion
2. Verify card immediately removed (no modal)
3. Check database: NO confidence change
4. Verify dismissal tracked (if implemented)

**Evidence**:
- Video: Dismiss animation
- Database: confidence unchanged

---

### Test Scenario 6: Multiple Suggestions

**Steps**:
1. Create 3 different patterns
2. Trigger context with all 3 patterns
3. Verify all 3 cards shown
4. Accept one, reject one, dismiss one
5. Verify panel collapses when last card removed

**Evidence**:
- Screenshot: 3 cards displayed
- Video: Interaction with each
- Final state: Panel collapsed

---

### Test Documentation Structure

```markdown
# Phase 3 Test Evidence - Pattern Suggestions UI

**Date**: November 13, 2025
**Tester**: Code Agent
**Status**: [PASS/FAIL]

---

## Test Scenario 1: First Suggestion Ever

**Status**: [PASS/FAIL]

### Setup
[How test environment was prepared]

### Steps
1. [Step]
2. [Step]

### Evidence
![Onboarding Tooltip](screenshot1.png)
![Notification Badge](screenshot2.png)

### Database State
```sql
[Query results]
```

### Notes
[Any observations, edge cases found]

---

[Repeat for all 6 scenarios]

---

## Summary

**Total Tests**: 6
**Passed**: [N]
**Failed**: [N]

**Critical Issues Found**: [None/List]
**Minor Issues Found**: [None/List]

**Phase 3 Status**: ✅ READY / ⚠️ NEEDS FIXES
```

---

## Success Criteria

**Functionality** ✅:
- [ ] Notification badge appears when suggestions exist
- [ ] Panel expands/collapses smoothly
- [ ] All 3 buttons (Accept/Reject/Dismiss) work
- [ ] Feedback modal shows on Accept/Reject
- [ ] Optional comment can be submitted or skipped
- [ ] Success/error toasts display correctly
- [ ] Cards removed after feedback
- [ ] Onboarding tooltip shows once on first suggestion
- [ ] Confidence bar displays correctly (visual + %)

**Backend** ✅:
- [ ] get_suggestions() called in IntentService
- [ ] Suggestions returned in response JSON
- [ ] Feedback endpoint updates confidence
- [ ] Accept increases confidence (×1.1, cap 1.0)
- [ ] Reject decreases confidence (×0.5)
- [ ] Pattern disabled when confidence < 0.3
- [ ] Optional comments stored
- [ ] Database updates committed

**UX** ✅:
- [ ] Non-intrusive (collapsed by default)
- [ ] Transparent (reasoning shown)
- [ ] User-controlled (clear actions)
- [ ] Accessible (keyboard navigation works)
- [ ] Mobile-responsive (works on small screens)
- [ ] Color scheme matches Piper (teal-orange)

**Quality** ✅:
- [ ] No console errors
- [ ] No broken UI on edge cases
- [ ] Performance <100ms for UI interactions
- [ ] All 6 test scenarios pass
- [ ] Evidence documented

---

## STOP Conditions

**STOP if**:
- ❌ get_suggestions() doesn't exist (should from Phase 1)
- ❌ IntentService structure completely different than expected
- ❌ Frontend framework is actually React (not vanilla JS)
- ❌ Can't integrate with existing message renderer
- ❌ Feedback endpoint causes database errors

**If STOP triggered**:
1. Document what's blocking you
2. Gather evidence (error messages, screenshots)
3. Escalate to Lead Developer with details

---

## File Organization

**Create these files**:
```
dev/2025/11/13/
├── phase-3-test-evidence.md           # Test results
├── phase-3-implementation-log.md      # Session log
├── test_suggestions_ui.py             # Optional: Python helpers
└── screenshots/
    ├── onboarding-tooltip.png
    ├── collapsed-badge.png
    ├── expanded-panel.png
    ├── feedback-modal-accept.png
    ├── feedback-modal-reject.png
    └── confidence-display.png

web/assets/
├── suggestions-ui.js                  # NEW: Main JS
└── suggestions.css                    # NEW: Styles

web/api/routes/
└── learning.py                        # MODIFIED: Add feedback endpoint
```

---

## Pre-Commit Checklist

**ALWAYS before every commit**:
```bash
# Fix end-of-file newlines
./scripts/fix-newlines.sh

# Stage changes
git add -u

# Commit
git commit -m "feat(#300): Implement Phase 3 pattern suggestions UI

- Add notification badge + expandable panel
- Implement suggestion cards with reasoning
- Add Accept/Reject/Dismiss actions
- Create feedback modal for optional comments
- Integrate get_suggestions() in IntentService
- Add POST /patterns/{id}/feedback endpoint
- Include first-time onboarding tooltip
- Manual testing: 6/6 scenarios passing

Co-authored-by: UX Design Specialist <ux@pipermorgan.ai>
"
```

---

## Estimated Timeline

| Phase | Task | Estimated | Notes |
|-------|------|-----------|-------|
| 3.1 | Backend Integration | 1h | Wire get_suggestions() |
| 3.2 | Frontend UI Core | 2h | Badge, panel, cards, handlers |
| 3.3 | First-Time Onboarding | 0.5h | Tooltip + learn more modal |
| 3.4 | Feedback Endpoint | 1h | POST endpoint + confidence logic |
| 3.5 | Manual Testing | 1h | 6 scenarios + documentation |
| **Total** | | **5.5h** | Realistic for Phase 3 |

---

## Questions? Issues?

**If unclear about**:
- UX design choices → Refer to phase-3-suggestions-ux-design-proposal.md
- Technical constraints → Refer to phase-3-architecture-research.md
- Decisions made → Refer to ux-synthesis-phase3-decisions.md
- Original gameplan → Refer to gameplan-300-learning-basic-revised.md

**If blocked**:
- Check STOP conditions
- Document what's blocking
- Escalate to Lead Developer

---

## Remember

**You're building** the visible face of the learning system - make it:
- ✨ Transparent (users see WHY)
- 🎯 User-controlled (not pushy)
- 💬 Conversational (teaching, not surveying)
- 🏗️ Part of the cathedral (quality over speed)

**"Thoughtful Colleague"** is the guiding metaphor - helpful but not intrusive.

---

**Status**: Ready for implementation
**Expected Duration**: 5.5 hours
**Quality Standard**: Phase 2 level (100% testing, evidence-based)
**Impact**: Foundation Stone #3 - User-facing learning system

---

_"Together we are making something incredible"_
_"Quality exists outside of time constraints"_
_"The UX unicorn designed it, now let's build it!"_ 🦄✨
