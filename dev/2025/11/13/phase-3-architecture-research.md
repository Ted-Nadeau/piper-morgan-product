# Phase 3 Architecture Research
## Investigation Results for Pattern Suggestions

**Date**: November 13, 2025, 3:30 PM PT
**Investigator**: Code Agent
**Duration**: 25 minutes
**Method**: Serena symbolic queries + file analysis

---

## 1. Frontend Architecture

### Framework
**NO REACT/VUE** - Vanilla JavaScript with Jinja2 templates

**Evidence**:
```bash
$ find web -name "*.jsx" -o -name "*.tsx" -o -name "*.vue"
# (no results)
```

### Structure
```
templates/
├── home.html          # Main chat UI
└── standup.html       # Standup page

web/assets/
├── bot-message-renderer.js    # Message rendering logic
├── markdown-renderer-v3.js    # Markdown parsing
└── learning-dashboard.html    # Learning UI (Sprint A5)
```

### Chat UI Location
- **Main Template**: `templates/home.html`
- **Message Renderer**: `web/assets/bot-message-renderer.js`
- **API Endpoint**: `/api/v1/intent` (POST)

**Serena Query**:
```python
mcp__serena__get_symbols_overview("web/app.py")
# Found: process_intent endpoint at line 746
```

### Architecture Pattern
**Single-page application** with:
- Jinja2 templates for initial HTML
- Vanilla JavaScript for dynamic interactions
- Fetch API for `/api/v1/intent` calls
- Message bubbles rendered via `appendMessage()` + `handleDirectResponse()`

### Chat Message Flow
```javascript
// From templates/home.html:636
1. User submits message via form
2. Show "Thinking..." message
3. POST to /api/v1/intent
4. Response handled by handleDirectResponse(result, botDiv)
5. Markdown rendered via marked.parse()
```

### Example Message Rendering
```javascript
// web/assets/bot-message-renderer.js:39
function handleDirectResponse(result, element) {
    console.log('Direct response:', result.message);
    element.innerHTML = renderBotMessage(result.message, 'success', false);
}

function renderBotMessage(content, type = 'success', isThinking = false) {
    if (type === 'success' && typeof marked !== 'undefined') {
        content = marked.parse(content);
    }
    return `<div class="${['result', type].join(' ')}">${content}</div>`;
}
```

**Integration Point for Suggestions**: Add `result.suggestions` array to response, render as interactive elements in `handleDirectResponse()`.

---

## 2. Orchestration Response Structure

### Current Response Model

**Serena Query**:
```python
mcp__serena__find_symbol("IntentProcessingResult",
                         "services/intent/intent_service.py",
                         include_body=true)
```

**Result** (services/intent/intent_service.py:36-53):
```python
@dataclass
class IntentProcessingResult:
    """
    Result from intent processing.
    Contains all data needed by HTTP route to format response.
    Separates business logic result from HTTP concerns.
    """
    success: bool
    message: str
    intent_data: Dict[str, Any]
    workflow_id: Optional[str] = None
    requires_clarification: bool = False
    clarification_type: Optional[str] = None
    error: Optional[str] = None
    error_type: Optional[str] = None
    implemented: bool = True
```

### Where Response is Built

**File**: `services/intent/intent_service.py:102-329`
**Method**: `IntentService.process_intent(message, session_id)`

**Returns**: `IntentProcessingResult`

**HTTP Route** (web/app.py:746-795):
```python
@app.post("/api/v1/intent")
async def process_intent(request: Request):
    # ... parse request ...
    result = await intent_service.process_intent(message, session_id)

    # Format HTTP response from service result
    response = {
        "message": result.message,
        "intent": result.intent_data,
        "workflow_id": result.workflow_id,
        "requires_clarification": result.requires_clarification,
        "clarification_type": result.clarification_type,
    }
    return response
```

### How to Add Suggestions Field

**Option A: Add to IntentProcessingResult** (RECOMMENDED)
```python
@dataclass
class IntentProcessingResult:
    # ... existing fields ...
    suggestions: Optional[List[Dict[str, Any]]] = None  # NEW
```

**Option B: Add to HTTP response only**
```python
# In web/app.py process_intent()
response = {
    "message": result.message,
    # ... existing fields ...
    "suggestions": result.suggestions,  # NEW
}
```

**Recommendation**: Option A - add to dataclass so all layers have access to suggestions.

### Example Response with Suggestions
```json
{
  "message": "Standup scheduled for 9 AM Monday",
  "intent": {"category": "EXECUTION", "action": "schedule_standup"},
  "workflow_id": "abc123",
  "requires_clarification": false,
  "suggestions": [
    {
      "pattern_id": "uuid-1",
      "confidence": 0.85,
      "pattern_type": "time_based",
      "pattern_data": {"intent": "standup", "time": "09:00", "days": ["monday"]},
      "description": "You usually do standup at 9 AM on Mondays"
    }
  ]
}
```

---

## 3. Learning Handler Interface

### Existing Methods

**Serena Query**:
```python
mcp__serena__get_symbols_overview("services/learning/learning_handler.py")
mcp__serena__find_symbol("LearningHandler", depth=1)
```

**Methods Found**:
1. ✅ `capture_action(user_id, action_type, context, session)` - **EXISTS** (Phase 1)
2. ✅ `record_outcome(user_id, pattern_id, success, session)` - **EXISTS** (Phase 1)
3. ✅ `get_suggestions(user_id, context, session)` - **EXISTS** (already implemented!)
4. `find_similar_pattern(user_id, pattern_data, session)` - Pattern matching
5. `_determine_pattern_type(context)` - Private helper

**Constants**:
- `SUGGESTION_THRESHOLD = 0.7` - Minimum confidence to show suggestion
- `AUTOMATION_THRESHOLD = 0.9` - Minimum for auto-execution
- `DISABLE_THRESHOLD = 0.3` - Auto-disable if too low
- `SIMILARITY_THRESHOLD = 0.8` - Pattern matching threshold

### get_suggestions() Signature

**File**: services/learning/learning_handler.py:234-304

```python
async def get_suggestions(
    self,
    user_id: UUID,
    context: Dict[str, Any],
    session: AsyncSession,
) -> List[Dict[str, Any]]:
    """
    Get high-confidence pattern suggestions for current context.

    Returns patterns with confidence >= SUGGESTION_THRESHOLD (0.7)
    that are enabled and match the current context.

    Args:
        user_id: User requesting suggestions
        context: Current context (intent, input, etc.)
        session: Database session

    Returns:
        List of suggestion dicts with pattern_id, confidence, pattern_data

    Performance Target: <1ms (cached)
    """
```

### Pattern Retrieval Logic
```python
# Query high-confidence patterns for user
result = await session.execute(
    select(LearnedPattern)
    .where(
        and_(
            LearnedPattern.user_id == user_id,
            LearnedPattern.confidence >= self.SUGGESTION_THRESHOLD,
            LearnedPattern.enabled == True,
        )
    )
    .order_by(LearnedPattern.confidence.desc())
    .limit(5)  # Top 5 suggestions
)
patterns = result.scalars().all()

# Format suggestions
suggestions = []
for pattern in patterns:
    suggestions.append({
        "pattern_id": str(pattern.id),
        "confidence": round(pattern.confidence, 2),
        "pattern_type": pattern.pattern_type.value,
        "pattern_data": pattern.pattern_data,
        "usage_count": pattern.usage_count,
    })
```

**KEY FINDING**: `get_suggestions()` is **already implemented** and working! No need to build from scratch.

---

## 4. Pattern Model Structure

### LearnedPattern Fields

**Serena Query**:
```python
mcp__serena__find_symbol("LearnedPattern",
                         "services/database/models.py",
                         include_body=true)
```

**Result** (services/database/models.py:1555-1631):
```python
class LearnedPattern(Base, TimestampMixin):
    """Learned patterns for auto-learning system."""

    # Primary key
    id: UUID

    # User association
    user_id: UUID  # FK to users.id (CASCADE delete)

    # Pattern identification
    pattern_type: PatternType  # Enum
    pattern_data: JSON  # Flexible JSONB storage

    # Confidence tracking
    confidence: Float  # 0.0 to 1.0, default 0.5
    usage_count: Integer  # Total uses
    success_count: Integer  # Successful applications
    failure_count: Integer  # Failed applications

    # Status
    enabled: Boolean  # Default True

    # Timestamps
    created_at: DateTime  # From TimestampMixin
    updated_at: DateTime  # From TimestampMixin
    last_used_at: DateTime  # Last trigger

    # Relationships
    user: User  # Back reference
```

### pattern_data Structure (JSONB)

**Examples from tests**:

**User Workflow Pattern**:
```json
{
  "intent": "query_github",
  "context": {"query": "recent PRs"},
  "frequency": "daily"
}
```

**Command Sequence Pattern**:
```json
{
  "commands": ["git status", "git pull", "git push"],
  "frequency": "hourly"
}
```

**Time-Based Pattern**:
```json
{
  "intent": "standup",
  "context": {"time": "09:00"},
  "days": ["monday", "wednesday", "friday"]
}
```

### Pattern Types Available

**Source**: services/shared_types.py

```python
class PatternType(Enum):
    """Types of patterns that can be learned"""

    USER_WORKFLOW = "user_workflow"        # Recurring action sequences
    COMMAND_SEQUENCE = "command_sequence"  # Frequently used commands
    TIME_BASED = "time_based"              # Temporal patterns
    CONTEXT_BASED = "context_based"        # Context-triggered patterns
```

### Confidence Calculation

**Method**: `LearnedPattern.update_confidence()`

```python
# Formula: confidence = (success_rate * 0.8 + previous_confidence * 0.2) * volume_factor
# Volume factor: min(usage_count / 10, 1.0) - caps at 10 uses

success_rate = self.success_count / (self.success_count + self.failure_count)
volume_factor = min(self.usage_count / 10, 1.0)
new_confidence = success_rate * 0.8 + self.confidence * 0.2
self.confidence = new_confidence * volume_factor

# Auto-disable if too low
if self.confidence < 0.3:
    self.enabled = False
```

### Example Pattern from Database
```python
# From Phase 2 tests (dev/2025/11/13/test_phase2_patterns.py)
{
  "id": "c2100d18-97db-4c1a-be61-5371f0a7d57d",
  "pattern_type": "time_based",
  "pattern_data": {
    "intent": "standup",
    "context": {"time": "09:00"},
    "days": ["monday", "wednesday", "friday"]
  },
  "confidence": 0.65,
  "usage_count": 3,
  "success_count": 2,
  "failure_count": 1,
  "enabled": true
}
```

---

## 5. Intent Service Integration

### Execution Flow

**Serena Query**:
```python
mcp__serena__find_symbol("IntentService/process_intent", include_body=true)
```

**Current Flow** (services/intent/intent_service.py:102-329):

```
1. Ethics boundary enforcement (if enabled)
2. Knowledge graph enhancement (if enabled)
3. Tier 1 conversation bypass check
4. Intent classification (intent_classifier.classify)
5. ⭐ LEARNING PHASE 1: capture_action() ← ALREADY DONE
6. Canonical intent handling
7. Workflow creation
8. Intent-specific handlers (QUERY, EXECUTION, ANALYSIS, etc.)
9. ⭐ LEARNING PHASE 1: record_outcome() ← ALREADY DONE
10. Return IntentProcessingResult
```

### Existing Integration Points

**capture_action()** - Line 124-143 (already implemented in Phase 1):
```python
# Issue #300 Phase 1: Learning Handler - Capture Action
pattern_id = None
try:
    async with AsyncSessionFactory.session_scope() as db_session:
        user_id = UUID("3f4593ae-5bc9-468d-b08d-8c4c02a5b963")  # TODO: from auth

        pattern_id = await self.learning_handler.capture_action(
            user_id=user_id,
            action_type=intent.category,
            context={"intent": intent.action, "message": message[:100]},
            session=db_session,
        )
```

**record_outcome()** - Line 310-327 (already implemented in Phase 1):
```python
# Issue #300 Phase 1: Learning Handler - Record Outcome
if pattern_id:
    try:
        async with AsyncSessionFactory.session_scope() as db_session:
            user_id = UUID("3f4593ae-5bc9-468d-b08d-8c4c02a5b963")

            success = await self.learning_handler.record_outcome(
                user_id=user_id,
                pattern_id=pattern_id,
                success=result.success,
                session=db_session,
            )
```

### Recommended Integration Point for Phase 3

**Insert AFTER step 5 (capture_action), BEFORE step 6 (canonical handling)**:

```python
# Line ~145 (after capture_action, before canonical handlers)

# Issue #300 Phase 3: Get pattern suggestions
suggestions = []
try:
    async with AsyncSessionFactory.session_scope() as db_session:
        user_id = UUID("3f4593ae-5bc9-468d-b08d-8c4c02a5b963")

        suggestions = await self.learning_handler.get_suggestions(
            user_id=user_id,
            context={"intent": intent.action, "message": message[:100]},
            session=db_session,
        )

        self.logger.info(
            "Learning Handler: Suggestions retrieved",
            count=len(suggestions),
            intent=intent.action,
        )
except Exception as e:
    self.logger.error(f"Learning Handler: Suggestion retrieval failed: {e}")
    # Continue processing even if suggestions fail
```

**Then modify result creation** to include suggestions:
```python
# Every IntentProcessingResult creation needs:
result = IntentProcessingResult(
    success=True,
    message="...",
    intent_data={...},
    suggestions=suggestions,  # NEW
    # ... other fields ...
)
```

---

## 6. Existing Suggestion UI

### Components Found

**Search Results**:
```bash
$ find web -name "*suggest*" -o -name "*notif*" -o -name "*toast*" -o -name "*banner*"
# (no results)
```

**Verdict**: ❌ No existing suggestion/notification components

### Chat Rendering

**File**: web/assets/bot-message-renderer.js

**Current rendering**:
```javascript
function handleDirectResponse(result, element) {
    element.innerHTML = renderBotMessage(result.message, 'success', false);
}

function renderBotMessage(content, type = 'success', isThinking = false) {
    let processedContent = content;
    if (type === 'success' && typeof marked !== 'undefined') {
        processedContent = marked.parse(content);
    }
    return `<div class="${['result', type].join(' ')}">${processedContent}</div>`;
}
```

### Interactive Elements

**Current pattern** (from workflow responses):
```javascript
// Special case: GitHub issue (web/assets/bot-message-renderer.js:59)
element.innerHTML = `
  <div class="result success">
    <strong>✅ GitHub Issue Created!</strong><br>
    <strong>#${finalResult.number}:</strong> ${finalResult.title}<br>
    <strong>URL:</strong> <a href="${finalResult.url}" target="_blank">View on GitHub</a>
  </div>`;
```

**Pattern for buttons**: Use inline onclick handlers or add event listeners

### How to Add Suggestion UI

**Modify handleDirectResponse()** in bot-message-renderer.js:

```javascript
function handleDirectResponse(result, element) {
    console.log('Direct response:', result.message);

    // Render main message
    let html = renderBotMessage(result.message, 'success', false);

    // Render suggestions if present
    if (result.suggestions && result.suggestions.length > 0) {
        html += renderSuggestions(result.suggestions);
    }

    element.innerHTML = html;

    // Attach event listeners for suggestion buttons
    if (result.suggestions) {
        attachSuggestionListeners(element, result.suggestions);
    }
}

function renderSuggestions(suggestions) {
    let html = '<div class="suggestions-container">';
    html += '<p class="suggestions-header">💡 Suggested patterns:</p>';

    suggestions.forEach((suggestion, index) => {
        html += `
          <div class="suggestion-item">
            <span class="suggestion-text">${formatSuggestion(suggestion)}</span>
            <span class="suggestion-confidence">${Math.round(suggestion.confidence * 100)}% match</span>
            <button class="suggestion-accept" data-pattern-id="${suggestion.pattern_id}" data-index="${index}">
              Apply
            </button>
            <button class="suggestion-dismiss" data-pattern-id="${suggestion.pattern_id}" data-index="${index}">
              Dismiss
            </button>
          </div>
        `;
    });

    html += '</div>';
    return html;
}

function attachSuggestionListeners(element, suggestions) {
    // Accept buttons
    element.querySelectorAll('.suggestion-accept').forEach(button => {
        button.addEventListener('click', async (e) => {
            const patternId = e.target.dataset.patternId;
            const index = e.target.dataset.index;
            await handleSuggestionFeedback(patternId, 'accept');
            // Remove suggestion from UI
            e.target.closest('.suggestion-item').remove();
        });
    });

    // Dismiss buttons
    element.querySelectorAll('.suggestion-dismiss').forEach(button => {
        button.addEventListener('click', async (e) => {
            const patternId = e.target.dataset.patternId;
            await handleSuggestionFeedback(patternId, 'reject');
            // Remove suggestion from UI
            e.target.closest('.suggestion-item').remove();
        });
    });
}

async function handleSuggestionFeedback(patternId, action) {
    try {
        await fetch(`${API_BASE_URL}/api/v1/learning/patterns/${patternId}/feedback`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: action })
        });
    } catch (error) {
        console.error('Feedback submission failed:', error);
    }
}
```

**CSS needed** (add to templates/home.html `<style>` section):
```css
.suggestions-container {
    margin-top: 15px;
    padding: 15px;
    background: #f8f9fa;
    border-radius: 8px;
    border-left: 3px solid #3498db;
}

.suggestions-header {
    font-weight: bold;
    margin-bottom: 10px;
    color: #2c3e50;
}

.suggestion-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px;
    margin-bottom: 8px;
    background: white;
    border-radius: 6px;
    border: 1px solid #dee2e6;
}

.suggestion-text {
    flex-grow: 1;
    color: #495057;
}

.suggestion-confidence {
    font-size: 0.85em;
    color: #6c757d;
    font-weight: 500;
}

.suggestion-accept {
    background: #28a745;
    color: white;
    border: none;
    padding: 6px 12px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9em;
}

.suggestion-accept:hover {
    background: #218838;
}

.suggestion-dismiss {
    background: #6c757d;
    color: white;
    border: none;
    padding: 6px 12px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9em;
}

.suggestion-dismiss:hover {
    background: #5a6268;
}
```

---

## 7. API Endpoint Structure

### Existing Learning Endpoints

**File**: web/api/routes/learning.py

**Endpoints from Phase 2** (7 total):
1. `GET /api/v1/learning/patterns` - List patterns
2. `GET /api/v1/learning/patterns/{id}` - Get pattern details
3. `DELETE /api/v1/learning/patterns/{id}` - Delete pattern
4. `POST /api/v1/learning/patterns/{id}/enable` - Enable pattern
5. `POST /api/v1/learning/patterns/{id}/disable` - Disable pattern
6. `GET /api/v1/learning/settings` - Get learning settings
7. `PUT /api/v1/learning/settings` - Update settings

### Where to Add Feedback Endpoint

**Location**: web/api/routes/learning.py (after existing pattern endpoints)

**New endpoint needed**:
```python
@router.post("/patterns/{pattern_id}/feedback")
async def submit_pattern_feedback(
    pattern_id: UUID,
    feedback: PatternFeedback,
) -> Dict[str, Any]:
    """
    Submit user feedback on a pattern suggestion.

    Used when user accepts/rejects a suggestion from the UI.
    Updates pattern confidence based on user response.
    """
    try:
        async with AsyncSessionFactory.session_scope() as session:
            # TODO: Get user_id from auth context
            user_id = UUID("3f4593ae-5bc9-468d-b08d-8c4c02a5b963")

            # Get pattern
            result = await session.execute(
                select(LearnedPattern)
                .where(
                    and_(
                        LearnedPattern.id == pattern_id,
                        LearnedPattern.user_id == user_id,
                    )
                )
                .with_for_update()
            )
            pattern = result.scalar_one_or_none()

            if not pattern:
                raise HTTPException(status_code=404, detail="Pattern not found")

            # Update based on feedback
            if feedback.action == "accept":
                pattern.success_count += 1
            elif feedback.action == "reject":
                pattern.failure_count += 1

            pattern.usage_count += 1
            pattern.update_confidence()  # Recalculate
            pattern.last_used_at = datetime.utcnow()

            await session.commit()

            return {
                "success": True,
                "message": "Feedback recorded",
                "pattern": {
                    "id": str(pattern.id),
                    "confidence": round(pattern.confidence, 2),
                    "enabled": pattern.enabled,
                }
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Feedback submission failed: {e}")
        raise HTTPException(status_code=500, detail="Feedback submission failed")


class PatternFeedback(BaseModel):
    """Request model for pattern feedback"""
    action: str  # "accept" or "reject"

    @validator('action')
    def validate_action(cls, v):
        if v not in ['accept', 'reject']:
            raise ValueError('action must be "accept" or "reject"')
        return v
```

### Authentication Pattern

**Current approach** (Phase 2):
```python
# Hardcoded test user
TEST_USER_ID = "3f4593ae-5bc9-468d-b08d-8c4c02a5b963"
```

**Future approach** (Phase 3+):
```python
# Extract from JWT token
from web.middleware.auth import get_current_user

@router.post("/patterns/{pattern_id}/feedback")
async def submit_pattern_feedback(
    pattern_id: UUID,
    feedback: PatternFeedback,
    current_user: User = Depends(get_current_user),  # NEW
):
    user_id = current_user.id  # From auth context
    # ...
```

**For Phase 3**: Continue using TEST_USER_ID (consistent with Phase 2)

---

## Phase 3 Implementation Recommendations

### Backend Changes Needed

1. **Modify IntentProcessingResult** (services/intent/intent_service.py:36)
   - Add `suggestions: Optional[List[Dict[str, Any]]] = None`

2. **Call get_suggestions() in IntentService.process_intent()** (line ~145)
   - After `capture_action()`, before canonical handlers
   - Store suggestions in local variable
   - Include in all IntentProcessingResult creations

3. **Add suggestions to HTTP response** (web/app.py:746)
   - Include `result.suggestions` in response dict

4. **Create feedback endpoint** (web/api/routes/learning.py)
   - POST `/api/v1/learning/patterns/{pattern_id}/feedback`
   - Update pattern confidence based on user action
   - Use PatternFeedback Pydantic model for validation

### Frontend Changes Needed

1. **Extend handleDirectResponse()** (web/assets/bot-message-renderer.js:39)
   - Check for `result.suggestions`
   - Render suggestions UI below message
   - Attach event listeners to Accept/Dismiss buttons

2. **Add renderSuggestions() function**
   - Format suggestion items with confidence scores
   - Include Apply/Dismiss buttons with data attributes

3. **Add attachSuggestionListeners() function**
   - Handle Accept button clicks → POST feedback + remove UI
   - Handle Dismiss button clicks → POST feedback + remove UI

4. **Add handleSuggestionFeedback() function**
   - POST to `/api/v1/learning/patterns/{id}/feedback`
   - Error handling for failed submissions

5. **Add CSS styles** (templates/home.html)
   - `.suggestions-container`, `.suggestion-item`, `.suggestion-accept`, `.suggestion-dismiss`
   - Match existing UI aesthetic

### Integration Points

**Backend Integration**:
```
IntentService.process_intent()
  ↓
1. capture_action() (existing - Phase 1)
  ↓
2. get_suggestions() (NEW - Phase 3) ← Insert here
  ↓
3. Canonical/workflow handling (existing)
  ↓
4. Create IntentProcessingResult with suggestions (MODIFIED)
  ↓
5. record_outcome() (existing - Phase 1)
  ↓
Return result to HTTP route
  ↓
HTTP route adds suggestions to response (MODIFIED)
```

**Frontend Integration**:
```
Fetch /api/v1/intent
  ↓
Response includes {message, intent, suggestions}
  ↓
handleDirectResponse(result, element)
  ↓
1. Render message (existing)
  ↓
2. Render suggestions (NEW - Phase 3) ← Insert here
  ↓
3. Attach event listeners (NEW - Phase 3)
  ↓
User clicks Accept/Dismiss
  ↓
POST to /api/v1/learning/patterns/{id}/feedback
  ↓
Update confidence in database
```

### Estimated Complexity

**Backend**:
- ✅ get_suggestions() already exists → SMALL
- Add suggestions field to result → SMALL
- Create feedback endpoint → SMALL
- **Total**: SMALL (1-2 hours)

**Frontend**:
- Modify message renderer → MEDIUM
- Create suggestion UI components → MEDIUM
- Wire up feedback handlers → SMALL
- Add CSS styling → SMALL
- **Total**: MEDIUM (2-3 hours)

**Overall**: SMALL-MEDIUM (3-5 hours total)

**Confidence**: HIGH - All infrastructure exists, just need to connect pieces

---

## Questions for Lead Developer

1. **Suggestion Placement**: Should suggestions appear:
   - Below every response? (current plan)
   - Only when confidence > threshold?
   - Only for certain intent types?

2. **Suggestion Limit**: Phase 1 uses top 5 patterns. Is this appropriate or should we:
   - Show fewer (top 3)?
   - Show all high-confidence patterns?
   - Make it configurable via settings?

3. **Feedback Granularity**: Should feedback endpoint support:
   - Just accept/reject? (current plan)
   - Explicit "apply now" vs "good suggestion"?
   - Rating scale (1-5 stars)?

4. **Auto-application**: If user accepts a suggestion, should we:
   - Just record feedback? (current plan)
   - Actually execute the pattern?
   - Show execution in separate workflow?

5. **Testing Strategy**: Phase 3 manual testing or wait for Phase 5 automated tests?

---

**Evidence Collected**:
- 12+ Serena queries executed
- 8 files examined in detail
- All 7 questions answered with code evidence

**Files Investigated**:
1. templates/home.html (chat UI)
2. web/assets/bot-message-renderer.js (message rendering)
3. web/app.py (HTTP routes)
4. services/intent/intent_service.py (business logic)
5. services/learning/learning_handler.py (learning methods)
6. services/database/models.py (LearnedPattern model)
7. services/shared_types.py (PatternType enum)
8. web/api/routes/learning.py (API endpoints)

**Confidence**: **HIGH** - All architectural questions answered with concrete evidence. get_suggestions() already exists, integration points clear, minimal new code needed.

---

**Time**: 25 minutes
**Status**: Research complete, ready for Phase 3 implementation
**Next Step**: Review findings with Lead Developer, proceed to Phase 3 implementation
