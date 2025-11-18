# Phase 4 Agent Prompt: Proactive Pattern Application
## Issue #300 - Smart Proactive Suggestions (Simplified)

**Date**: Friday, November 14, 2025, 10:20 AM PT  
**From**: Lead Developer  
**To**: Code Agent  
**Priority**: P2 (Alpha Feature)  
**Estimated Effort**: 2-3 hours  
**Based On**: Chief Architect recommendations (approved 7:00-7:20 AM)

---

## 🚨 CRITICAL: COMPLETION DISCIPLINE

YOU MUST COMPLETE ALL WORK DEFINED IN THIS PROMPT.

- ❌ You CANNOT defer steps without PM approval
- ❌ You CANNOT decide something is "optional"
- ❌ You CANNOT modify scope independently
- ✅ You MUST complete all steps or STOP and escalate

If you think a step should be deferred:
1. STOP working immediately
2. Document your reasoning
3. Create summary for Lead Developer
4. Wait for PM decision
5. DO NOT proceed without approval

**The PM decides scope. You execute scope.**

---

## MANDATORY COMPLETION MATRIX

Check off each step as completed:

- [ ] Step 1: Action Registry + Commands (30 min)
  - Deliverable: Action registry with 3 low-risk commands
  - Evidence: Unit tests passing
  
- [ ] Step 2: Context Matcher (30 min)
  - Deliverable: Hybrid context matcher (temporal + sequential)
  - Evidence: Integration tests passing

- [ ] Step 3: Proactive Suggestions UI (45 min)
  - Deliverable: Auto-triggered suggestions with visual distinction
  - Evidence: Screenshots showing ⚡ icon and orange styling

- [ ] Step 4: Integration & Testing (45 min)
  - Deliverable: Wired into IntentService, manual testing complete
  - Evidence: 3 test scenarios documented

**All checkboxes MUST be checked before session ends.**  
**You CANNOT check a box without delivering the required evidence.**  
**You CANNOT skip steps without explicit PM approval.**

---

## Mission

Implement **Proactive Pattern Application** for Piper Morgan - when patterns reach high confidence (0.9+) and context matches, show **proactive suggestions** (NOT full auto-execution).

**Key Distinction**: This is NOT auto-execution. User still approves before action. We're making suggestions **proactive** (Piper initiates when context matches) instead of **reactive** (waiting for user to ask).

**Success looks like**: Pattern confidence hits 0.92, user does standup, Piper says *"⚡ Ready to create GitHub issue based on your workflow pattern"* with "Execute Now" button. User clicks → issue created.

---

## Context: What Already Exists

### Phase 1-3 Complete ✅

**Backend**:
- ✅ Real-time pattern capture (Phase 1)
- ✅ Confidence tracking and updates (Phase 1)
- ✅ User controls API - 7 endpoints (Phase 2)
- ✅ `get_suggestions()` method (Phase 1)
- ✅ Feedback endpoint (Phase 3)

**Frontend**:
- ✅ Suggestions UI (badge, panel, cards) (Phase 3)
- ✅ Accept/Reject/Dismiss buttons (Phase 3)
- ✅ Onboarding tooltip (Phase 3.3)
- ✅ Visual styling (teal-orange theme) (Phase 3)

**What's Missing**: Proactive triggering when confidence >= 0.9

---

## Chief Architect's Recommendations

### Decision 1: Action Execution ✅

**Approach**: Action Registry + Command Pattern

**Why**: Extensible, testable, avoids circular dependencies

**Implementation guidance**:
```python
# Each action is a Command with execute()
class BaseCommand:
    async def execute(self) -> dict:
        raise NotImplementedError

class GithubIssueCommand(BaseCommand):
    def __init__(self, params: dict, context: dict):
        self.params = params
        self.context = context
    
    async def execute(self) -> dict:
        # Implementation
        return {"status": "success", "issue_id": "..."}

# Registry maps action types to command classes
class ActionRegistry:
    _actions = {
        "create_github_issue": GithubIssueCommand,
        "update_notion": NotionUpdateCommand,
    }
    
    @classmethod
    async def execute(cls, action_type: str, params: dict, context: dict):
        command_class = cls._actions.get(action_type)
        if not command_class:
            raise ValueError(f"Unknown action: {action_type}")
        
        command = command_class(params, context)
        return await command.execute()
```

---

### Decision 2: Safety Model ✅

**Approach**: Two-tier consent (for future full auto)

**For Alpha**: All actions are HIGH_RISK (user approves before execute)

**Implementation guidance**:
```python
# Risk classification (for future use)
LOW_RISK_ACTIONS = [
    "read_github_issue",
    "fetch_notion_page",
    "search_slack",
    "draft_document",  # Not sent/published
]

HIGH_RISK_ACTIONS = [
    "create_github_issue",
    "send_slack_message",
    "publish_notion_page",
    "delete_anything",
]

# Alpha: Everything goes through preview-first
# (User sees proactive suggestion, clicks "Execute Now")
```

**Note**: For alpha, we're showing ALL as proactive suggestions (high-risk behavior). Low-risk auto-execution is post-alpha.

---

### Decision 3: Context Matching ✅

**Approach**: Hybrid (explicit triggers + similarity)

**For Alpha**: Focus on temporal + sequential (defer conditional/event)

**Implementation guidance**:
```python
class ContextMatcher:
    """Match current context to pattern triggers"""
    
    @classmethod
    async def matches(cls, pattern_context: dict, current_context: dict) -> bool:
        """Check if pattern applies to current context"""
        
        # 1. Temporal triggers (explicit)
        # Example: "after standup", "9am monday", "end of day"
        if pattern_context.get("trigger_time"):
            if not cls._check_temporal(
                pattern_context["trigger_time"], 
                current_context
            ):
                return False
        
        # 2. Sequential triggers (explicit)  
        # Example: "after creating issue", "before sending message"
        if pattern_context.get("after_action"):
            last_action = current_context.get("last_action")
            if last_action != pattern_context["after_action"]:
                return False
        
        # 3. Conditional (similarity-based) - DEFER to post-alpha
        # 4. Event-based (exact match) - DEFER to post-alpha
        
        return True  # All checked conditions met
    
    @staticmethod
    def _check_temporal(trigger_time: str, current_context: dict) -> bool:
        """Check if current time matches trigger"""
        # Parse trigger_time (e.g., "after standup", "9am")
        # Compare to current_context["current_time"]
        # Return True if matches
        pass  # Simple implementation for alpha
```

**Architect's note**: "Start simple. Explicit is better than implicit. No LLM for alpha (latency/cost)."

---

### Decision 4: Integration Point ✅

**Approach**: Before canonical handlers with fallback

**Implementation guidance**:
```python
async def execute(self, user_input, user_id, context, session):
    """Modified IntentService.execute with Phase 4 integration"""
    
    # 1. Classify intent (existing)
    intent = await self.intent_classifier.classify(user_input)
    
    # 2. Capture action (existing - Phase 1)
    await self.learning_handler.capture_action(
        user_id, intent, context, session
    )
    
    # 3. Check for HIGH-CONFIDENCE patterns (NEW - Phase 4)
    auto_patterns = await self.learning_handler.get_automation_patterns(
        user_id=user_id,
        context=context,
        min_confidence=0.9,
        session=session
    )
    
    # 4. If pattern matches context, show PROACTIVE suggestion
    if auto_patterns:
        for pattern in auto_patterns:
            if await context_matcher.matches(pattern.pattern_data, context):
                # Add to suggestions with auto_triggered flag
                proactive_suggestion = {
                    **pattern.to_dict(),
                    "auto_triggered": True,  # Visual distinction
                    "proactive": True
                }
                # Don't execute yet - user will click "Execute Now"
                break
    
    # 5. Get regular suggestions (existing - Phase 3)
    suggestions = await self.learning_handler.get_suggestions(
        user_id, context, session
    )
    
    # 6. Execute canonical handlers (existing)
    result = await self.canonical_handlers.execute(intent, context, session)
    
    # 7. Return result with suggestions (including proactive)
    all_suggestions = []
    if 'proactive_suggestion' in locals():
        all_suggestions.append(proactive_suggestion)
    all_suggestions.extend(suggestions or [])
    
    return IntentProcessingResult(
        intent=intent,
        response=result,
        suggestions=all_suggestions if all_suggestions else None
    )
```

**Important**: Patterns take precedence but canonical still runs for side effects (logging, etc.)

---

### Decision 5: Alpha Scope ✅

**CRITICAL**: This is **SIMPLIFIED** scope - proactive suggestions, NOT auto-execution

**What we're building**:
- When confidence >= 0.9 AND context matches
- Show suggestion with `auto_triggered: True` flag
- User sees ⚡ icon (lightning bolt) instead of 💡 (lightbulb)
- Orange badge instead of teal
- "Execute Now" button prominent
- User must click to execute

**What we're NOT building** (deferred to post-alpha):
- Auto-execution without user approval
- Undo mechanism
- Full low-risk/high-risk execution split

**Architect's rationale**:
> "⚠️ Risk of surprising users, ⚠️ No undo yet, ⚠️ Need feedback first.
> ✅ Faster (2-3h), ✅ User control, ✅ Still feels smart, ✅ Can evolve based on data."

---

## Step 1: Action Registry + Commands (30 min)

### Task: Create extensible action execution system

**Files to create**:
```
services/actions/
├── __init__.py
├── action_registry.py
└── commands/
    ├── __init__.py
    ├── base_command.py
    ├── github_issue_command.py  # Example - LOW_RISK for now
    └── notion_update_command.py  # Example - LOW_RISK for now
```

### Implementation

**File: `services/actions/commands/base_command.py`**
```python
"""Base command for all executable actions"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseCommand(ABC):
    """Abstract base class for action commands"""
    
    def __init__(self, params: Dict[str, Any], context: Dict[str, Any]):
        """
        Initialize command with parameters and context
        
        Args:
            params: Action-specific parameters (from pattern_data)
            context: Current execution context (user_id, session, etc.)
        """
        self.params = params
        self.context = context
    
    @abstractmethod
    async def execute(self) -> Dict[str, Any]:
        """
        Execute the action
        
        Returns:
            dict: Result with at least {"status": "success"|"error", ...}
        """
        raise NotImplementedError("Subclasses must implement execute()")
    
    def validate_params(self) -> None:
        """Validate required parameters (override if needed)"""
        pass
    
    async def rollback(self) -> None:
        """Rollback/undo action (future - not implemented in alpha)"""
        raise NotImplementedError("Rollback not implemented in alpha")
```

**File: `services/actions/commands/github_issue_command.py`**
```python
"""Command for creating GitHub issues"""
from typing import Dict, Any
from .base_command import BaseCommand


class GithubIssueCommand(BaseCommand):
    """Create a GitHub issue (LOW_RISK - draft mode for alpha)"""
    
    async def execute(self) -> Dict[str, Any]:
        """
        Create GitHub issue draft
        
        For alpha: Create draft, don't auto-publish
        Future: Can auto-publish for low-risk
        """
        try:
            # Extract parameters
            title = self.params.get("title", "Action item from standup")
            labels = self.params.get("labels", ["standup", "action-item"])
            assignee = self.params.get("assignee", "self")
            
            # TODO: Integrate with actual GitHub service
            # For now, return mock result
            result = {
                "status": "success",
                "action": "create_github_issue",
                "issue_id": "mock-123",  # Would be real issue ID
                "title": title,
                "labels": labels,
                "message": f"Created issue draft: {title}"
            }
            
            return result
            
        except Exception as e:
            return {
                "status": "error",
                "action": "create_github_issue",
                "error": str(e)
            }
```

**File: `services/actions/action_registry.py`**
```python
"""Central registry for all executable actions"""
from typing import Dict, Any, Type
from .commands.base_command import BaseCommand
from .commands.github_issue_command import GithubIssueCommand
# from .commands.notion_update_command import NotionUpdateCommand  # Future


class ActionRegistry:
    """Registry mapping action types to command classes"""
    
    # Low-risk actions (for alpha, all require user approval)
    _actions: Dict[str, Type[BaseCommand]] = {
        "create_github_issue": GithubIssueCommand,
        # "update_notion": NotionUpdateCommand,  # Add when ready
        # "search_slack": SlackSearchCommand,    # Add when ready
    }
    
    @classmethod
    async def execute(
        cls,
        action_type: str,
        params: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute an action via its command
        
        Args:
            action_type: Type of action (e.g., "create_github_issue")
            params: Action parameters from pattern
            context: Execution context (user_id, session, etc.)
            
        Returns:
            dict: Execution result
            
        Raises:
            ValueError: If action type not registered
        """
        command_class = cls._actions.get(action_type)
        
        if not command_class:
            available = ", ".join(cls._actions.keys())
            raise ValueError(
                f"Unknown action type: {action_type}. "
                f"Available: {available}"
            )
        
        # Create command instance
        command = command_class(params, context)
        
        # Validate parameters
        command.validate_params()
        
        # Execute
        result = await command.execute()
        
        return result
    
    @classmethod
    def is_registered(cls, action_type: str) -> bool:
        """Check if action type is registered"""
        return action_type in cls._actions
    
    @classmethod
    def list_actions(cls) -> list[str]:
        """List all registered action types"""
        return list(cls._actions.keys())
```

### Tests Required

**File: `tests/services/actions/test_action_registry.py`**
```python
import pytest
from services.actions.action_registry import ActionRegistry


@pytest.mark.asyncio
async def test_github_issue_command():
    """Test GitHub issue creation command"""
    params = {
        "title": "Test issue",
        "labels": ["test"],
        "assignee": "self"
    }
    context = {"user_id": "test-user"}
    
    result = await ActionRegistry.execute(
        "create_github_issue",
        params,
        context
    )
    
    assert result["status"] == "success"
    assert result["action"] == "create_github_issue"
    assert "issue_id" in result


@pytest.mark.asyncio
async def test_unknown_action():
    """Test unknown action raises error"""
    with pytest.raises(ValueError, match="Unknown action type"):
        await ActionRegistry.execute(
            "unknown_action",
            {},
            {}
        )


def test_list_actions():
    """Test listing registered actions"""
    actions = ActionRegistry.list_actions()
    assert "create_github_issue" in actions
```

### Evidence Required

1. ✅ All files created
2. ✅ Unit tests passing: `pytest tests/services/actions/ -v`
3. ✅ No import errors: `python -c "from services.actions import ActionRegistry"`
4. ✅ Git commit: `feat(#300): Phase 4.1 - Action Registry + Commands`

---

## Step 2: Context Matcher (30 min)

### Task: Implement hybrid context matching

**Files to create**:
```
services/learning/
├── context_matcher.py  # NEW
└── __init__.py         # Update imports
```

### Implementation

**File: `services/learning/context_matcher.py`**
```python
"""Context matching for pattern application"""
from typing import Dict, Any
from datetime import datetime, time


class ContextMatcher:
    """Match current context to pattern trigger conditions"""
    
    @classmethod
    async def matches(
        cls,
        pattern_context: Dict[str, Any],
        current_context: Dict[str, Any]
    ) -> bool:
        """
        Check if pattern applies to current context
        
        Args:
            pattern_context: Trigger conditions from pattern.pattern_data
            current_context: Current execution context
            
        Returns:
            bool: True if pattern should trigger
        """
        # No triggers defined = always matches (for testing)
        if not pattern_context:
            return True
        
        # Check temporal triggers
        if "trigger_time" in pattern_context:
            if not cls._check_temporal(
                pattern_context["trigger_time"],
                current_context
            ):
                return False
        
        # Check sequential triggers (after specific action)
        if "after_action" in pattern_context:
            last_action = current_context.get("last_action")
            if last_action != pattern_context["after_action"]:
                return False
        
        # Check intent matching (optional)
        if "trigger_intent" in pattern_context:
            current_intent = current_context.get("intent")
            if current_intent != pattern_context["trigger_intent"]:
                return False
        
        # All conditions met
        return True
    
    @staticmethod
    def _check_temporal(
        trigger_time: str,
        current_context: Dict[str, Any]
    ) -> bool:
        """
        Check if current time matches trigger
        
        Args:
            trigger_time: Time specification (e.g., "after standup", "9am", "eod")
            current_context: Must contain "current_time" or "current_event"
            
        Returns:
            bool: True if time matches
        """
        # Simple keyword matching for alpha
        trigger_lower = trigger_time.lower()
        
        # Check for event-based temporal triggers
        current_event = current_context.get("current_event", "").lower()
        if current_event:
            # "after standup" matches if current_event is "standup_complete"
            if "standup" in trigger_lower and "standup" in current_event:
                return True
            # "end of day" matches if current_event is "eod" or "end_of_day"
            if ("eod" in trigger_lower or "end of day" in trigger_lower):
                if "eod" in current_event or "end_of_day" in current_event:
                    return True
        
        # Check for time-based triggers (future enhancement)
        current_time = current_context.get("current_time")
        if current_time and isinstance(current_time, (datetime, time)):
            # TODO: Parse time specifications like "9am", "monday morning"
            # For alpha: Simple hour matching
            if "9am" in trigger_lower or "morning" in trigger_lower:
                hour = current_time.hour if hasattr(current_time, 'hour') else 0
                return 7 <= hour <= 11
        
        # Default: trigger doesn't match
        return False
    
    @staticmethod
    def _calculate_similarity(
        conditions: Dict[str, Any],
        current_context: Dict[str, Any]
    ) -> float:
        """
        Calculate similarity between conditions and context
        (Future enhancement - defer to post-alpha)
        
        Returns:
            float: Similarity score 0.0-1.0
        """
        # Placeholder for future similarity matching
        return 1.0  # For alpha, assume match if present
```

### Tests Required

**File: `tests/services/learning/test_context_matcher.py`**
```python
import pytest
from datetime import datetime, time
from services.learning.context_matcher import ContextMatcher


@pytest.mark.asyncio
async def test_empty_pattern_context_matches():
    """Empty pattern context should match any current context"""
    result = await ContextMatcher.matches({}, {"anything": "here"})
    assert result is True


@pytest.mark.asyncio
async def test_temporal_standup_match():
    """Test 'after standup' temporal matching"""
    pattern_context = {"trigger_time": "after standup"}
    current_context = {"current_event": "standup_complete"}
    
    result = await ContextMatcher.matches(pattern_context, current_context)
    assert result is True


@pytest.mark.asyncio
async def test_temporal_no_match():
    """Test temporal trigger doesn't match wrong event"""
    pattern_context = {"trigger_time": "after standup"}
    current_context = {"current_event": "meeting_complete"}
    
    result = await ContextMatcher.matches(pattern_context, current_context)
    assert result is False


@pytest.mark.asyncio
async def test_sequential_after_action():
    """Test sequential 'after action' matching"""
    pattern_context = {"after_action": "create_github_issue"}
    current_context = {"last_action": "create_github_issue"}
    
    result = await ContextMatcher.matches(pattern_context, current_context)
    assert result is True


@pytest.mark.asyncio
async def test_sequential_wrong_action():
    """Test sequential trigger doesn't match wrong action"""
    pattern_context = {"after_action": "create_github_issue"}
    current_context = {"last_action": "update_notion"}
    
    result = await ContextMatcher.matches(pattern_context, current_context)
    assert result is False


@pytest.mark.asyncio
async def test_intent_matching():
    """Test intent-based matching"""
    pattern_context = {"trigger_intent": "GITHUB_ISSUE_CREATE"}
    current_context = {"intent": "GITHUB_ISSUE_CREATE"}
    
    result = await ContextMatcher.matches(pattern_context, current_context)
    assert result is True


@pytest.mark.asyncio
async def test_multiple_conditions_all_match():
    """Test all conditions must match"""
    pattern_context = {
        "trigger_time": "after standup",
        "trigger_intent": "STATUS_CHECK"
    }
    current_context = {
        "current_event": "standup_complete",
        "intent": "STATUS_CHECK"
    }
    
    result = await ContextMatcher.matches(pattern_context, current_context)
    assert result is True


@pytest.mark.asyncio
async def test_multiple_conditions_one_fails():
    """Test any failing condition returns False"""
    pattern_context = {
        "trigger_time": "after standup",
        "trigger_intent": "STATUS_CHECK"
    }
    current_context = {
        "current_event": "standup_complete",
        "intent": "DIFFERENT_INTENT"  # Wrong intent
    }
    
    result = await ContextMatcher.matches(pattern_context, current_context)
    assert result is False
```

### Evidence Required

1. ✅ All files created
2. ✅ Tests passing: `pytest tests/services/learning/test_context_matcher.py -v`
3. ✅ Git commit: `feat(#300): Phase 4.2 - Context Matcher (hybrid temporal/sequential)`

---

## Step 3: Proactive Suggestions UI (45 min)

### Task: Add visual distinction for auto-triggered suggestions

**Files to modify**:
- `web/assets/bot-message-renderer.js`
- `templates/home.html` (CSS)

### UI Distinctions for Auto-Triggered

**Regular suggestion** (Phase 3):
- 💡 Lightbulb icon
- Teal colors (#0095A8)
- "Suggested" badge

**Proactive suggestion** (Phase 4 NEW):
- ⚡ Lightning bolt icon
- Orange colors (#FF7043)
- "Auto-detected" badge
- "Execute Now" button more prominent

### Implementation

**File: `web/assets/bot-message-renderer.js`** (modify renderSuggestionCard)

Find the `renderSuggestionCard` function and update:

```javascript
function renderSuggestionCard(suggestion) {
    // NEW: Check for auto-triggered flag
    const isAutoTriggered = suggestion.auto_triggered || false;
    const proactive = suggestion.proactive || false;
    
    // Visual styling based on type
    const icon = isAutoTriggered ? '⚡' : '💡';
    const badgeClass = isAutoTriggered ? 'auto-badge' : 'manual-badge';
    const badgeText = isAutoTriggered ? 'Auto-detected' : 'Suggested';
    const cardClass = isAutoTriggered ? 'auto-triggered' : '';
    
    return `
        <div class="suggestion-card ${cardClass}" data-pattern-id="${suggestion.pattern_id}">
            <div class="card-header">
                <div class="header-left">
                    <span class="suggestion-icon">${icon}</span>
                    <h4 class="suggestion-title">${suggestion.description}</h4>
                </div>
                <span class="suggestion-badge ${badgeClass}">${badgeText}</span>
            </div>
            
            <div class="suggestion-reasoning">
                ${suggestion.reasoning || generateReasoning(suggestion)}
            </div>
            
            <div class="confidence-display">
                <div class="confidence-bar-container">
                    <div class="confidence-bar" 
                         style="width: ${(suggestion.confidence * 100).toFixed(0)}%"
                         role="progressbar">
                    </div>
                </div>
                <span class="confidence-text">
                    ${(suggestion.confidence * 100).toFixed(0)}% confident
                </span>
            </div>
            
            <div class="suggestion-actions">
                ${isAutoTriggered ? `
                    <button class="action-btn execute-btn" 
                            onclick="handleExecute('${suggestion.pattern_id}')">
                        <span class="btn-icon">▶</span> Execute Now
                    </button>
                    <button class="action-btn skip-btn" 
                            onclick="handleSkip('${suggestion.pattern_id}')">
                        Skip This Time
                    </button>
                    <button class="action-btn disable-btn" 
                            onclick="handleDisable('${suggestion.pattern_id}')">
                        Disable Pattern
                    </button>
                ` : `
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
                `}
            </div>
        </div>
    `;
}

// NEW: Handle Execute button for proactive suggestions
async function handleExecute(patternId) {
    // Execute the pattern action
    const response = await fetch(`/api/v1/learning/patterns/${patternId}/execute`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'}
    });
    
    if (response.ok) {
        const result = await response.json();
        showSuccessMessage(result.message || 'Action executed successfully!');
        removeSuggestionCard(patternId);
    } else {
        showErrorMessage('Failed to execute action. Please try again.');
    }
}

// NEW: Handle Skip button for proactive suggestions
function handleSkip(patternId) {
    // Just dismiss without feedback (neutral action)
    showSuccessMessage('Skipped for now.');
    removeSuggestionCard(patternId);
}

// NEW: Handle Disable button for proactive suggestions
async function handleDisable(patternId) {
    // Disable the pattern entirely
    const response = await fetch(`/api/v1/learning/patterns/${patternId}/disable`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'}
    });
    
    if (response.ok) {
        showSuccessMessage('Pattern disabled. I won\'t suggest this anymore.');
        removeSuggestionCard(patternId);
    } else {
        showErrorMessage('Failed to disable pattern.');
    }
}
```

**File: `templates/home.html`** (add CSS)

Add after existing suggestion styles:

```css
/* Phase 4: Auto-Triggered (Proactive) Suggestions */

/* Orange badge for auto-detected */
.auto-badge {
    background: #FF7043;
    color: white;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
}

/* Highlighted card for auto-triggered */
.suggestion-card.auto-triggered {
    border-left: 4px solid #FF7043;  /* Orange instead of teal */
    background: #FFF5F2;  /* Light orange tint */
}

.suggestion-card.auto-triggered:hover {
    box-shadow: 0 2px 8px rgba(255, 112, 67, 0.3);  /* Orange glow */
}

/* Auto-triggered icon */
.suggestion-card.auto-triggered .suggestion-icon {
    color: #FF7043;
    font-size: 24px;
}

/* Execute Now button (prominent) */
.execute-btn {
    background: #FF7043;
    color: white;
    border-color: #FF7043;
    font-weight: 600;
}

.execute-btn:hover {
    background: #F4511E;
}

/* Skip button (neutral) */
.skip-btn {
    background: white;
    color: #7F8C8D;
    border-color: #BDC3C7;
}

.skip-btn:hover {
    background: #F8F9FA;
}

/* Disable button (warning) */
.disable-btn {
    background: white;
    color: #E74C3C;
    border-color: #E74C3C;
}

.disable-btn:hover {
    background: #FFEBEE;
}
```

### Evidence Required

1. ✅ Code changes committed
2. ✅ Screenshot: Regular suggestion (💡 teal)
3. ✅ Screenshot: Auto-triggered suggestion (⚡ orange)
4. ✅ Video: Click "Execute Now" button
5. ✅ Git commit: `feat(#300): Phase 4.3 - Proactive suggestions UI with visual distinction`

---

## Step 4: Integration & Testing (45 min)

### Task A: Add get_automation_patterns method

**File: `services/learning/learning_handler.py`**

Add new method:

```python
async def get_automation_patterns(
    self,
    user_id: UUID,
    context: Optional[Dict[str, Any]] = None,
    min_confidence: float = 0.9,
    limit: int = 3,
    session: Optional[AsyncSession] = None
) -> List[LearnedPattern]:
    """
    Get patterns eligible for proactive application
    
    Similar to get_suggestions but with higher confidence threshold.
    
    Args:
        user_id: User to get patterns for
        context: Current context for matching
        min_confidence: Minimum confidence (default 0.9 for automation)
        limit: Maximum patterns to return
        session: Database session
        
    Returns:
        List of high-confidence patterns that match context
    """
    async with self._get_session(session) as session:
        # Query high-confidence enabled patterns
        result = await session.execute(
            select(LearnedPattern)
            .where(
                LearnedPattern.user_id == user_id,
                LearnedPattern.confidence >= min_confidence,
                LearnedPattern.enabled == True
            )
            .order_by(LearnedPattern.confidence.desc())
            .limit(limit)
        )
        
        patterns = result.scalars().all()
        
        # Filter by context if provided
        if context:
            from services.learning.context_matcher import ContextMatcher
            matched_patterns = []
            
            for pattern in patterns:
                pattern_context = pattern.pattern_data.get("context", {})
                if await ContextMatcher.matches(pattern_context, context):
                    matched_patterns.append(pattern)
            
            return matched_patterns
        
        return list(patterns)
```

### Task B: Integrate into IntentService

**File: `services/intent/intent_service.py`**

Modify the `execute` method (around line 140-180):

```python
async def execute(
    self,
    user_input: str,
    user_id: UUID,
    context: Optional[Dict[str, Any]] = None,
    session: Optional[AsyncSession] = None
) -> IntentProcessingResult:
    """Execute intent with Phase 4 proactive patterns"""
    
    async with AsyncSessionFactory.session_scope() as session:
        # 1. Classify intent (existing)
        intent = await self.intent_classifier.classify(user_input)
        
        # 2. Capture action (existing - Phase 1)
        await self.learning_handler.capture_action(
            user_id, intent, context or {}, session
        )
        
        # 3. Check for HIGH-CONFIDENCE patterns (NEW - Phase 4)
        auto_patterns = await self.learning_handler.get_automation_patterns(
            user_id=user_id,
            context={
                "intent": intent,
                **(context or {})
            },
            min_confidence=0.9,
            limit=3,
            session=session
        )
        
        # 4. Mark proactive patterns (NEW)
        proactive_suggestions = []
        if auto_patterns:
            for pattern in auto_patterns:
                suggestion = {
                    "pattern_id": str(pattern.id),
                    "pattern_type": pattern.pattern_type.value,
                    "description": pattern.description,
                    "confidence": pattern.confidence,
                    "reasoning": f"I'm ready to execute this based on your pattern",
                    "auto_triggered": True,  # Visual distinction
                    "proactive": True
                }
                proactive_suggestions.append(suggestion)
        
        # 5. Get regular suggestions (existing - Phase 3)
        regular_suggestions = await self.learning_handler.get_suggestions(
            user_id, context or {}, min_confidence=0.7, limit=3, session=session
        )
        
        # 6. Execute canonical handlers (existing)
        result = await self.canonical_handlers.execute(intent, context or {}, session)
        
        # 7. Combine suggestions (proactive first)
        all_suggestions = proactive_suggestions + (regular_suggestions or [])
        
        return IntentProcessingResult(
            intent=intent,
            response=result,
            suggestions=all_suggestions if all_suggestions else None
        )
```

### Task C: Add Pattern Execute Endpoint

**File: `web/api/routes/learning.py`**

Add new endpoint:

```python
@router.post("/patterns/{pattern_id}/execute")
async def execute_pattern(
    pattern_id: UUID,
    session: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Execute a pattern action (Phase 4 - proactive execution)
    
    This is called when user clicks "Execute Now" on a proactive suggestion.
    """
    from services.actions.action_registry import ActionRegistry
    
    async with AsyncSessionFactory.session_scope() as session:
        # Get pattern
        result = await session.execute(
            select(LearnedPattern)
            .where(LearnedPattern.id == pattern_id)
        )
        pattern = result.scalar_one_or_none()
        
        if not pattern:
            return {
                "status": "error",
                "message": f"Pattern {pattern_id} not found"
            }
        
        # Extract action from pattern
        pattern_data = pattern.pattern_data
        action_type = pattern_data.get("action_type")
        action_params = pattern_data.get("action_params", {})
        
        if not action_type:
            return {
                "status": "error",
                "message": "Pattern has no action_type defined"
            }
        
        # Execute via Action Registry
        try:
            context = {
                "user_id": pattern.user_id,
                "pattern_id": pattern.id
            }
            
            execution_result = await ActionRegistry.execute(
                action_type,
                action_params,
                context
            )
            
            # Record as success
            pattern.success_count += 1
            pattern.confidence = min(pattern.confidence * 1.05, 1.0)
            pattern.updated_at = datetime.utcnow()
            await session.commit()
            
            return {
                "status": "success",
                "message": execution_result.get("message", "Action executed successfully"),
                "result": execution_result
            }
            
        except Exception as e:
            # Record as failure
            pattern.failure_count += 1
            pattern.confidence *= 0.9
            await session.commit()
            
            return {
                "status": "error",
                "message": f"Execution failed: {str(e)}"
            }
```

### Task D: Manual Testing (3 Scenarios)

**Create file**: `dev/2025/11/14/phase-4-test-evidence.md`

**Test Scenario 1: Proactive Suggestion Appears**

**Setup**:
```sql
-- Create high-confidence pattern
INSERT INTO learned_patterns (
    id, user_id, pattern_type, description, 
    pattern_data, confidence, enabled
) VALUES (
    gen_random_uuid(), 
    'TEST_USER_ID',
    'USER_WORKFLOW',
    'Create GitHub issue after standup',
    '{
        "action_type": "create_github_issue",
        "action_params": {"title": "Action items", "labels": ["standup"]},
        "context": {"trigger_time": "after standup"}
    }',
    0.92,
    true
);
```

**Steps**:
1. Complete standup (simulate with context: `{"current_event": "standup_complete"}`)
2. Send chat message
3. Verify proactive suggestion appears
4. Check: ⚡ icon, orange badge, "Auto-detected", "Execute Now" button

**Evidence**:
- Screenshot of proactive suggestion
- curl showing `auto_triggered: true` in response

---

**Test Scenario 2: Execute Now Works**

**Steps**:
1. See proactive suggestion (from Scenario 1)
2. Click "Execute Now"
3. Verify action executes via ActionRegistry
4. Verify success message appears
5. Check database: confidence increased, success_count incremented

**Evidence**:
- Screenshot of execution
- curl: `POST /api/v1/learning/patterns/{id}/execute`
- Database query showing updated confidence

---

**Test Scenario 3: Skip vs Disable**

**Steps**:
1. See proactive suggestion
2. Click "Skip This Time"
3. Verify: suggestion dismissed, NO database change
4. Trigger again
5. Click "Disable Pattern"
6. Verify: pattern.enabled = False
7. Try triggering again → no suggestion

**Evidence**:
- Screenshots of both actions
- Database queries showing enabled flag changes

---

### Evidence Required - Step 4

1. ✅ All code changes committed
2. ✅ Tests passing: `pytest tests/services/learning/ -v`
3. ✅ Manual test evidence document created
4. ✅ All 3 scenarios documented with screenshots
5. ✅ Database state verified for each scenario
6. ✅ Git commit: `feat(#300): Phase 4.4 - Integration and manual testing complete`

---

## Success Criteria

### Functionality ✅

- [ ] Patterns with 0.9+ confidence show proactive suggestions
- [ ] Context matching works (temporal: "after standup", sequential: "after action")
- [ ] User can execute/skip/disable from suggestion
- [ ] Visual distinction clear (⚡ orange vs 💡 teal)
- [ ] "Execute Now" action works and updates confidence
- [ ] "Skip" dismisses without changing confidence
- [ ] "Disable" sets enabled=False

### Performance ✅

- [ ] <20ms overhead for pattern checking
- [ ] No disruption to existing flow
- [ ] All existing tests pass (55/55)

### Quality ✅

- [ ] Action Registry with 2-3 commands
- [ ] Context Matcher with temporal + sequential
- [ ] New integration tests for Phase 4
- [ ] Manual test evidence documented
- [ ] No console errors in browser

---

## STOP Conditions

**STOP if**:
- ❌ Cannot understand IntentService structure
- ❌ LearningHandler doesn't have pattern retrieval methods
- ❌ Frontend framework is actually React (not vanilla JS)
- ❌ Pattern data structure is completely different than expected
- ❌ Database schema doesn't support needed queries

**If STOP triggered**:
1. Document what's blocking you
2. Gather evidence (error messages, code snippets)
3. Create clear summary for Lead Developer
4. DO NOT proceed - escalate immediately

---

## Pre-Commit Checklist

**ALWAYS before every commit**:

```bash
# Fix end-of-file newlines
./scripts/fix-newlines.sh

# Run tests
pytest tests/services/actions/ -v
pytest tests/services/learning/test_context_matcher.py -v

# Stage changes
git add -u

# Commit with proper message
git commit -m "feat(#300): Phase 4.X - [Description]

- [Specific change]
- [Specific change]
- [Specific change]

Evidence: [What proves this works]
"
```

---

## File Organization

**Create these files**:
```
services/actions/
├── __init__.py
├── action_registry.py
└── commands/
    ├── __init__.py
    ├── base_command.py
    └── github_issue_command.py

services/learning/
└── context_matcher.py

tests/services/actions/
└── test_action_registry.py

tests/services/learning/
└── test_context_matcher.py

dev/2025/11/14/
├── phase-4-test-evidence.md
└── phase-4-implementation-log.md
```

**Modify these files**:
```
web/assets/bot-message-renderer.js  (renderSuggestionCard, new handlers)
templates/home.html                  (CSS for auto-triggered)
services/intent/intent_service.py    (integration)
services/learning/learning_handler.py (get_automation_patterns)
web/api/routes/learning.py          (execute endpoint)
```

---

## Estimated Timeline

| Step | Task | Estimated | Notes |
|------|------|-----------|-------|
| 1 | Action Registry | 30 min | 3 files + tests |
| 2 | Context Matcher | 30 min | 1 file + tests |
| 3 | Proactive UI | 45 min | JS + CSS changes |
| 4 | Integration | 45 min | Wire + endpoint + testing |
| **Total** | | **2.5 hours** | Within 2-3h estimate |

---

## Remember

**You're implementing**:
- ✅ Proactive suggestions (NOT full auto-execution)
- ✅ User clicks "Execute Now" to approve
- ✅ Visual distinction (⚡ orange) from regular suggestions
- ✅ Context matching (temporal + sequential)
- ✅ Action Registry for extensibility

**You're NOT implementing** (deferred to post-alpha):
- ❌ Auto-execution without user approval
- ❌ Undo mechanism
- ❌ Low-risk vs high-risk execution split
- ❌ LLM-based context matching
- ❌ Full temporal parsing

**Philosophy**: Human remains in control, transparent, gradual trust-building

---

**Status**: Ready for implementation  
**Expected Duration**: 2-3 hours  
**Quality Standard**: Same as Phase 3 (100% test coverage, evidence-based)  
**Impact**: Foundation Stone #4 - Proactive pattern application

---

_"The architect has designed it"_  
_"Now let's build it right"_  
_"Together we are making something incredible"_ 🏗️⚡
