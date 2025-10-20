# CORE-LEARN-E Implementation: Intelligent Automation with Safety First

**Agent**: Claude Code (Programmer)
**Issue**: #225 CORE-LEARN-E - Intelligent Automation
**Sprint**: A5 - Learning System (Extended - Issue 5 of 6!)
**Date**: October 20, 2025, 2:50 PM
**Duration**: 6 hours estimated (based on discovery)

---

## 🎯 REALISTIC PREAMBLE: 80% COMPLETE (WE'VE BEEN SPOILED!)

Discovery found that CORE-LEARN-E infrastructure is **80% complete** (3,579 lines exist).

**Context check**: After seeing 90-98% on CORE-LEARN-A/B/C/D, 80% feels low. But 80% is EXCELLENT!
- 3.4:1 leverage ratio (3,579 existing : 1,050 new)
- 77% infrastructure exists
- Most new code is SAFETY-CRITICAL work (which SHOULD be done carefully!)

**What exists (the miracles from past days)**:
- ✅ PatternRecognitionService (543 lines) - 8 pattern types, prediction capable
- ✅ Slack Attention Model - Predictive intelligence already built!
- ✅ QueryLearningLoop (610 lines) - Confidence thresholds (≥ 0.8), feedback loops
- ✅ UserPreferenceManager (762 lines) - User approval preferences
- ✅ Chain-of-Draft (552 lines) - Gradual automation via A/B testing
- ✅ Learning API (511 lines) - Accuracy tracking (90%+ measurable!)
- ✅ CrossFeatureKnowledgeService (601 lines) - Cross-feature automation

**What's needed (today's work - ~1,050 lines)**:
- ⚠️ Field pre-population API (~150 lines)
- ⚠️ Autonomous execution framework (~200 lines)
- ⚠️ User approval system (~100 lines)
- 🔒 **Safety controls (~300 lines) - CRITICAL WORK!**
  - Action classification (safe vs destructive)
  - Emergency stop capability
  - Audit trail system
- ⚠️ Integration/wiring (~100 lines)
- ⚠️ Tests (~200 lines)

---

## 🔒 CRITICAL: SAFETY FIRST APPROACH

**BEFORE implementing autonomous execution, we MUST implement safety controls!**

**Non-negotiable safety requirements**:
1. **NEVER auto-execute destructive actions** (delete, publish, deploy, etc.)
2. **ALWAYS require confirmation for publishes**
3. **Audit trail for ALL automation**
4. **Emergency stop capability that WORKS**

**Implementation order**:
1. ✅ Phase 1: Safety Controls (2h) - DO THIS FIRST!
2. ✅ Phase 2: Predictive Assistance (2h) - Safe predictions
3. ✅ Phase 3: Autonomous Execution (3h) - ONLY after safety in place
4. ✅ Phase 4: Integration & Testing (1h) - Verify safety works

**This is the hill we die on!** 🔒

---

## CRITICAL: Post-Compaction Protocol

**If you just finished compacting**:

1. ⏸️ **STOP** - Do not continue working
2. 📋 **REPORT** - Summarize what was just completed
3. ❓ **ASK** - "Should I proceed to next task?"
4. ⏳ **WAIT** - For explicit instructions

---

## Mission

**Build intelligent automation with safety as PRIMARY concern!**

Discovery found 80% complete (3,579 lines). **We need ~1,050 lines of work**:
- Safety controls (CRITICAL!) (~300 lines)
- Predictive assistance (~150 lines)
- Autonomous execution (~200 lines)
- User approval system (~100 lines)
- Integration/wiring (~100 lines)
- Tests (~200 lines)

**Order matters**: Safety first, execution last!

**NOT in scope**:
- Machine learning (use existing patterns!)
- Complex prediction (use existing services!)
- Advanced analytics (use existing API!)

---

## Discovery Report

**YOU HAVE**: `core-learn-e-discovery-report.md` uploaded by PM

**CRITICAL FINDINGS**:
- 80% infrastructure exists (3,579 lines)
- PatternRecognitionService: 543 lines (prediction ready!)
- Slack Attention Model: exists! (predictive intelligence!)
- QueryLearningLoop: 610 lines (confidence, feedback loops!)
- Safety controls: 60% exists (needs completion!)
- Need ~1,050 lines: safety + execution + wiring + tests

**Read the discovery report first!** It contains complete assessment.

---

## STOP Conditions

If ANY of these occur, STOP and escalate to PM immediately:

1. **Safety controls cannot be implemented properly** - Critical requirement
2. **Pattern recognition doesn't exist** - Discovery said 543 lines
3. **Confidence thresholds don't exist** - Discovery said ≥ 0.8 in QueryLearningLoop
4. **Learning API doesn't work** - Discovery said 511 lines with accuracy tracking
5. **Cannot provide verification evidence** - Must show safety works
6. **Tests don't pass** - Must maintain zero regressions
7. **More than 1,200 lines needed** - Discovery said ~1,050 lines
8. **Tempted to skip safety controls** - STOP! Safety is non-negotiable!

---

## Evidence Requirements

### For EVERY Claim You Make:

- **"Safety controls added"** → Show action classification + tests
- **"Emergency stop works"** → Show stop mechanism + test results
- **"Audit trail complete"** → Show logging + verification
- **"Tests pass"** → Show test output
- **"Autonomous execution safe"** → Show safety checks + test results

### Working Files Location:

- ✅ dev/active/ - For test scripts, verification
- ✅ services/automation/ - For automation services (new!)
- ✅ services/learning/ - For wiring to learning system
- ✅ tests/integration/ - Integration tests
- ✅ docs/public/ - API documentation

---

## Implementation Plan (from Discovery)

### 🔒 Phase 1: Safety Controls (2 hours - DO THIS FIRST!)

**CRITICAL**: Implement safety BEFORE autonomous execution!

**Step 1: Create Action Classification System** (1 hour)

Create `services/automation/action_classifier.py`:

```python
"""
Action classification for intelligent automation safety.

Classifies actions as SAFE or DESTRUCTIVE to prevent auto-execution of
dangerous operations.
"""

from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass


class ActionSafetyLevel(Enum):
    """Safety classification for actions."""
    SAFE = "safe"                    # Auto-executable with high confidence
    REQUIRES_CONFIRMATION = "confirmation"  # Needs user approval
    DESTRUCTIVE = "destructive"      # NEVER auto-execute


@dataclass
class ActionClassification:
    """Classification result for an action."""
    action_type: str
    safety_level: ActionSafetyLevel
    reason: str
    requires_confirmation: bool


class ActionClassifier:
    """
    Classifies actions by safety level for automation decisions.

    CRITICAL SAFETY RULES:
    1. NEVER auto-execute destructive actions (delete, publish, deploy)
    2. ALWAYS require confirmation for publishes
    3. Only auto-execute truly safe operations
    """

    def __init__(self):
        # Destructive actions - NEVER auto-execute
        self._destructive_actions = {
            "delete", "remove", "destroy", "drop", "truncate",
            "publish", "deploy", "release", "merge", "push",
            "execute", "run", "start", "stop", "restart",
            "modify", "update", "change", "alter", "edit"
        }

        # Safe actions - Can auto-execute with high confidence
        self._safe_actions = {
            "read", "get", "fetch", "list", "search", "query",
            "view", "show", "display", "preview", "check",
            "validate", "verify", "test", "analyze"
        }

        # Confirmation actions - Need user approval
        self._confirmation_actions = {
            "create", "add", "insert", "post", "send",
            "assign", "label", "tag", "comment", "reply"
        }

    def classify_action(
        self,
        action_type: str,
        context: Optional[Dict] = None
    ) -> ActionClassification:
        """
        Classify action by safety level.

        Args:
            action_type: Type of action (e.g., "create_github_issue")
            context: Additional context for classification

        Returns:
            ActionClassification with safety level and requirements
        """
        action_lower = action_type.lower()

        # Check for destructive keywords
        for keyword in self._destructive_actions:
            if keyword in action_lower:
                return ActionClassification(
                    action_type=action_type,
                    safety_level=ActionSafetyLevel.DESTRUCTIVE,
                    reason=f"Contains destructive keyword: {keyword}",
                    requires_confirmation=True  # Actually, NEVER auto-execute
                )

        # Check for safe keywords
        for keyword in self._safe_actions:
            if keyword in action_lower:
                return ActionClassification(
                    action_type=action_type,
                    safety_level=ActionSafetyLevel.SAFE,
                    reason=f"Contains safe keyword: {keyword}",
                    requires_confirmation=False
                )

        # Check for confirmation keywords
        for keyword in self._confirmation_actions:
            if keyword in action_lower:
                return ActionClassification(
                    action_type=action_type,
                    safety_level=ActionSafetyLevel.REQUIRES_CONFIRMATION,
                    reason=f"Contains confirmation keyword: {keyword}",
                    requires_confirmation=True
                )

        # Default to requiring confirmation if unsure
        return ActionClassification(
            action_type=action_type,
            safety_level=ActionSafetyLevel.REQUIRES_CONFIRMATION,
            reason="Unknown action type - defaulting to safe",
            requires_confirmation=True
        )

    def is_safe_for_auto_execution(
        self,
        action_type: str,
        confidence: float,
        context: Optional[Dict] = None
    ) -> bool:
        """
        Determine if action is safe for autonomous execution.

        Args:
            action_type: Type of action
            confidence: Confidence score (0-1)
            context: Additional context

        Returns:
            True if safe for auto-execution, False otherwise

        CRITICAL: Returns False for ANY destructive action regardless of confidence!
        """
        classification = self.classify_action(action_type, context)

        # NEVER auto-execute destructive actions
        if classification.safety_level == ActionSafetyLevel.DESTRUCTIVE:
            return False

        # Only auto-execute if confidence is high enough AND action is safe
        if classification.safety_level == ActionSafetyLevel.SAFE and confidence >= 0.9:
            return True

        # Everything else requires confirmation
        return False
```

---

**Step 2: Create Emergency Stop System** (0.5 hours)

Add to `services/automation/emergency_stop.py`:

```python
"""
Emergency stop system for intelligent automation.

Provides immediate halt capability for all automation operations.
"""

import asyncio
from typing import Set
from datetime import datetime


class EmergencyStop:
    """
    Emergency stop system for automation.

    Provides global emergency stop capability to immediately halt
    all automation operations.
    """

    def __init__(self):
        self._stop_flag = False
        self._stopped_at: Optional[datetime] = None
        self._active_operations: Set[str] = set()

    def trigger_emergency_stop(self, reason: str = "Manual stop"):
        """
        Trigger emergency stop for all automation.

        Args:
            reason: Reason for emergency stop
        """
        self._stop_flag = True
        self._stopped_at = datetime.utcnow()

        # Log emergency stop
        print(f"🚨 EMERGENCY STOP TRIGGERED: {reason} at {self._stopped_at}")

        # Cancel all active operations
        self._active_operations.clear()

    def is_stopped(self) -> bool:
        """Check if emergency stop is active."""
        return self._stop_flag

    def reset(self):
        """Reset emergency stop (requires explicit action)."""
        self._stop_flag = False
        self._stopped_at = None
        self._active_operations.clear()

    def register_operation(self, operation_id: str):
        """Register an active automation operation."""
        if self._stop_flag:
            raise RuntimeError("Cannot start operation - emergency stop active!")
        self._active_operations.add(operation_id)

    def unregister_operation(self, operation_id: str):
        """Unregister completed automation operation."""
        self._active_operations.discard(operation_id)

    def get_status(self) -> Dict:
        """Get emergency stop status."""
        return {
            "stopped": self._stop_flag,
            "stopped_at": self._stopped_at.isoformat() if self._stopped_at else None,
            "active_operations": len(self._active_operations)
        }


# Global emergency stop instance
_emergency_stop = EmergencyStop()


def get_emergency_stop() -> EmergencyStop:
    """Get global emergency stop instance."""
    return _emergency_stop
```

---

**Step 3: Create Audit Trail System** (0.5 hours)

Add to `services/automation/audit_trail.py`:

```python
"""
Audit trail system for intelligent automation.

Logs all automation actions for accountability and review.
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import json


@dataclass
class AutomationEvent:
    """Record of an automation event."""
    timestamp: datetime
    event_type: str  # "prediction", "execution", "approval_request", etc.
    action_type: str
    confidence: float
    safety_level: str
    auto_executed: bool
    user_id: Optional[str]
    result: Optional[str]
    details: Dict


class AuditTrail:
    """
    Audit trail system for automation events.

    Records all automation actions for accountability, review, and debugging.
    """

    def __init__(self):
        self._events: List[AutomationEvent] = []

    def log_event(
        self,
        event_type: str,
        action_type: str,
        confidence: float,
        safety_level: str,
        auto_executed: bool,
        user_id: Optional[str] = None,
        result: Optional[str] = None,
        details: Optional[Dict] = None
    ):
        """
        Log an automation event.

        Args:
            event_type: Type of event (prediction, execution, etc.)
            action_type: Type of action being automated
            confidence: Confidence score for the action
            safety_level: Safety classification
            auto_executed: Whether action was auto-executed
            user_id: User who triggered or approved the action
            result: Result of the action
            details: Additional event details
        """
        event = AutomationEvent(
            timestamp=datetime.utcnow(),
            event_type=event_type,
            action_type=action_type,
            confidence=confidence,
            safety_level=safety_level,
            auto_executed=auto_executed,
            user_id=user_id,
            result=result,
            details=details or {}
        )

        self._events.append(event)

        # Also log to console for immediate visibility
        print(f"📝 AUDIT: {event.event_type} - {event.action_type} "
              f"(confidence: {event.confidence:.2f}, "
              f"safety: {event.safety_level}, "
              f"auto: {event.auto_executed})")

    def get_events(
        self,
        event_type: Optional[str] = None,
        action_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict]:
        """
        Get audit trail events.

        Args:
            event_type: Filter by event type
            action_type: Filter by action type
            limit: Maximum number of events to return

        Returns:
            List of event dictionaries
        """
        events = self._events

        # Filter by event type
        if event_type:
            events = [e for e in events if e.event_type == event_type]

        # Filter by action type
        if action_type:
            events = [e for e in events if e.action_type == action_type]

        # Limit results
        events = events[-limit:]

        # Convert to dictionaries
        return [
            {
                **asdict(event),
                "timestamp": event.timestamp.isoformat()
            }
            for event in events
        ]

    def get_automation_statistics(self) -> Dict:
        """Get statistics about automation usage."""
        total_events = len(self._events)
        auto_executed = sum(1 for e in self._events if e.auto_executed)

        return {
            "total_events": total_events,
            "auto_executed_count": auto_executed,
            "manual_count": total_events - auto_executed,
            "auto_execution_rate": auto_executed / total_events if total_events > 0 else 0
        }


# Global audit trail instance
_audit_trail = AuditTrail()


def get_audit_trail() -> AuditTrail:
    """Get global audit trail instance."""
    return _audit_trail
```

---

### Phase 2: Predictive Assistance (2 hours)

**Step 1: Create Field Pre-population API** (1 hour)

Add to `services/automation/predictive_assistance.py`:

```python
"""
Predictive assistance for intelligent automation.

Uses pattern recognition to anticipate next actions and provide smart defaults.
"""

from typing import Dict, List, Optional
from services.knowledge.pattern_recognition_service import PatternRecognitionService
from services.domain.user_preference_manager import UserPreferenceManager


class PredictiveAssistant:
    """
    Provides predictive assistance using learned patterns.

    Capabilities:
    - Next action prediction
    - Field pre-population
    - Smart defaults
    - Auto-fill suggestions
    """

    def __init__(self):
        self.pattern_service = PatternRecognitionService()
        self.preference_manager = UserPreferenceManager()

    async def predict_next_action(
        self,
        user_id: str,
        current_context: Dict
    ) -> List[Dict]:
        """
        Predict likely next actions based on workflow patterns.

        Args:
            user_id: User ID
            current_context: Current workflow context

        Returns:
            List of predicted actions with confidence scores
        """
        # Use pattern recognition to find workflow patterns
        patterns = await self.pattern_service.get_patterns_by_type("WORKFLOW_PATTERN")

        # Filter patterns relevant to current context
        relevant_patterns = [
            p for p in patterns
            if self._is_pattern_relevant(p, current_context)
        ]

        # Sort by confidence
        relevant_patterns.sort(key=lambda p: p.confidence, reverse=True)

        # Generate predictions
        predictions = []
        for pattern in relevant_patterns[:5]:  # Top 5 predictions
            predictions.append({
                "action": pattern.pattern_data.get("next_action", "unknown"),
                "confidence": pattern.confidence,
                "reason": f"Based on pattern {pattern.id}"
            })

        return predictions

    async def get_smart_defaults(
        self,
        user_id: str,
        field_name: str,
        context: Dict
    ) -> Optional[Dict]:
        """
        Get smart default value for a field based on user preferences and patterns.

        Args:
            user_id: User ID
            field_name: Name of field to pre-populate
            context: Current context

        Returns:
            Smart default with confidence, or None
        """
        # Check user preferences first
        pref_value = await self.preference_manager.get_preference(
            key=f"default_{field_name}",
            user_id=user_id
        )

        if pref_value:
            return {
                "value": pref_value,
                "confidence": 0.95,  # High confidence for explicit preferences
                "source": "user_preference"
            }

        # Fall back to pattern-based defaults
        patterns = await self.pattern_service.get_patterns_by_type("USER_PREFERENCE_PATTERN")

        for pattern in patterns:
            if pattern.pattern_data.get("field_name") == field_name:
                return {
                    "value": pattern.pattern_data.get("default_value"),
                    "confidence": pattern.confidence,
                    "source": "learned_pattern"
                }

        return None

    async def suggest_field_values(
        self,
        user_id: str,
        field_name: str,
        partial_input: str,
        context: Dict
    ) -> List[Dict]:
        """
        Suggest field values based on partial input and patterns.

        Args:
            user_id: User ID
            field_name: Name of field
            partial_input: Partial user input
            context: Current context

        Returns:
            List of suggestions with confidence scores
        """
        # Implementation for auto-fill suggestions
        # Example: GitHub label suggestions

        suggestions = []

        # Get patterns for this field
        patterns = await self.pattern_service.get_patterns_by_type("USER_PREFERENCE_PATTERN")

        for pattern in patterns:
            if pattern.pattern_data.get("field_name") == field_name:
                value = pattern.pattern_data.get("value", "")
                if partial_input.lower() in value.lower():
                    suggestions.append({
                        "value": value,
                        "confidence": pattern.confidence,
                        "usage_count": pattern.usage_count
                    })

        # Sort by confidence and usage
        suggestions.sort(key=lambda s: (s["confidence"], s["usage_count"]), reverse=True)

        return suggestions[:10]  # Top 10 suggestions

    def _is_pattern_relevant(self, pattern: Dict, context: Dict) -> bool:
        """Check if pattern is relevant to current context."""
        # Simple relevance check - can be enhanced
        pattern_context = pattern.pattern_data.get("context", {})

        # Check if any context keys match
        for key in context:
            if key in pattern_context:
                if context[key] == pattern_context[key]:
                    return True

        return False
```

---

### Phase 3: Autonomous Execution (3 hours - ONLY AFTER SAFETY!)

**Step 1: Create Autonomous Execution Framework** (1.5 hours)

Create `services/automation/autonomous_executor.py`:

```python
"""
Autonomous execution framework for intelligent automation.

CRITICAL: Only executes actions that pass safety checks!
"""

from typing import Dict, Optional
from services.automation.action_classifier import ActionClassifier, ActionSafetyLevel
from services.automation.emergency_stop import get_emergency_stop
from services.automation.audit_trail import get_audit_trail
from services.learning.query_learning_loop import QueryLearningLoop


class AutonomousExecutor:
    """
    Executes actions autonomously when confidence and safety allow.

    CRITICAL SAFETY RULES:
    1. NEVER execute if emergency stop active
    2. NEVER execute destructive actions (regardless of confidence)
    3. ONLY execute if confidence >= 0.9 AND action is SAFE
    4. ALWAYS log to audit trail
    """

    def __init__(self):
        self.classifier = ActionClassifier()
        self.emergency_stop = get_emergency_stop()
        self.audit_trail = get_audit_trail()
        self.learning_loop = QueryLearningLoop()

    async def should_auto_execute(
        self,
        action_type: str,
        confidence: float,
        user_id: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Determine if action should be auto-executed.

        Args:
            action_type: Type of action
            confidence: Confidence score (0-1)
            user_id: User ID
            context: Action context

        Returns:
            Decision dict with should_execute, reason, requires_approval
        """
        # Check emergency stop FIRST
        if self.emergency_stop.is_stopped():
            return {
                "should_execute": False,
                "reason": "Emergency stop active",
                "requires_approval": True,
                "safety_level": "STOPPED"
            }

        # Classify action safety
        classification = self.classifier.classify_action(action_type, context)

        # Check if safe for auto-execution
        is_safe = self.classifier.is_safe_for_auto_execution(
            action_type,
            confidence,
            context
        )

        # Log decision to audit trail
        self.audit_trail.log_event(
            event_type="auto_execute_decision",
            action_type=action_type,
            confidence=confidence,
            safety_level=classification.safety_level.value,
            auto_executed=is_safe,
            user_id=user_id,
            details={
                "classification_reason": classification.reason,
                "context": context or {}
            }
        )

        return {
            "should_execute": is_safe,
            "reason": classification.reason,
            "requires_approval": classification.requires_confirmation,
            "safety_level": classification.safety_level.value
        }

    async def execute_if_safe(
        self,
        action_type: str,
        action_function,
        confidence: float,
        user_id: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Execute action if safety checks pass.

        Args:
            action_type: Type of action
            action_function: Async function to execute
            confidence: Confidence score
            user_id: User ID
            context: Action context

        Returns:
            Execution result with status
        """
        # Check if should auto-execute
        decision = await self.should_auto_execute(
            action_type,
            confidence,
            user_id,
            context
        )

        if not decision["should_execute"]:
            return {
                "executed": False,
                "reason": decision["reason"],
                "requires_approval": decision["requires_approval"]
            }

        # Register operation with emergency stop
        operation_id = f"{action_type}_{user_id}_{datetime.utcnow().timestamp()}"
        self.emergency_stop.register_operation(operation_id)

        try:
            # Execute action
            result = await action_function()

            # Log successful execution
            self.audit_trail.log_event(
                event_type="auto_execute_success",
                action_type=action_type,
                confidence=confidence,
                safety_level=decision["safety_level"],
                auto_executed=True,
                user_id=user_id,
                result="success",
                details={"result": result}
            )

            # Learn from successful execution (feedback loop!)
            await self._record_success(action_type, confidence)

            return {
                "executed": True,
                "result": result,
                "confidence": confidence
            }

        except Exception as e:
            # Log failed execution
            self.audit_trail.log_event(
                event_type="auto_execute_failure",
                action_type=action_type,
                confidence=confidence,
                safety_level=decision["safety_level"],
                auto_executed=True,
                user_id=user_id,
                result="failure",
                details={"error": str(e)}
            )

            # Learn from failure (adjust confidence!)
            await self._record_failure(action_type, confidence)

            return {
                "executed": False,
                "error": str(e),
                "confidence": confidence
            }

        finally:
            # Unregister operation
            self.emergency_stop.unregister_operation(operation_id)

    async def _record_success(self, action_type: str, confidence: float):
        """Record successful execution for learning."""
        # Feedback loop: Success increases confidence for similar actions
        # Implementation uses QueryLearningLoop feedback mechanisms
        pass

    async def _record_failure(self, action_type: str, confidence: float):
        """Record failed execution for learning."""
        # Feedback loop: Failure decreases confidence for similar actions
        # Implementation uses QueryLearningLoop feedback mechanisms
        pass
```

---

**Step 2: User Approval System** (1 hour)

Add to `services/automation/user_approval.py`:

```python
"""
User approval system for automation actions.

Manages user preferences for autonomous execution and approval workflows.
"""

from typing import Dict, Optional
from services.domain.user_preference_manager import UserPreferenceManager


class UserApprovalSystem:
    """
    Manages user approval preferences for autonomous execution.

    Allows users to control automation comfort levels and approval requirements.
    """

    def __init__(self):
        self.preference_manager = UserPreferenceManager()

    async def get_user_automation_preference(
        self,
        user_id: str,
        action_type: str
    ) -> Dict:
        """
        Get user's automation preference for action type.

        Args:
            user_id: User ID
            action_type: Type of action

        Returns:
            Preference dict with allow_auto_execute, requires_approval
        """
        # Check action-specific preference
        action_pref = await self.preference_manager.get_preference(
            key=f"automation_{action_type}",
            user_id=user_id
        )

        if action_pref is not None:
            return {
                "allow_auto_execute": action_pref.get("allow", False),
                "requires_approval": action_pref.get("requires_approval", True)
            }

        # Fall back to general automation preference
        general_pref = await self.preference_manager.get_preference(
            key="automation_general",
            user_id=user_id
        )

        if general_pref is not None:
            return {
                "allow_auto_execute": general_pref.get("allow", False),
                "requires_approval": general_pref.get("requires_approval", True)
            }

        # Default: Require approval
        return {
            "allow_auto_execute": False,
            "requires_approval": True
        }

    async def set_automation_preference(
        self,
        user_id: str,
        action_type: Optional[str],
        allow_auto_execute: bool,
        requires_approval: bool = True
    ):
        """
        Set user's automation preference.

        Args:
            user_id: User ID
            action_type: Specific action type, or None for general preference
            allow_auto_execute: Whether to allow autonomous execution
            requires_approval: Whether approval is required
        """
        key = f"automation_{action_type}" if action_type else "automation_general"

        await self.preference_manager.set_preference(
            key=key,
            value={
                "allow": allow_auto_execute,
                "requires_approval": requires_approval
            },
            user_id=user_id
        )
```

---

**Step 3: Rollback Capability** (0.5 hours)

Add rollback to `autonomous_executor.py`:

```python
async def rollback_action(
    self,
    action_id: str,
    user_id: str
) -> Dict:
    """
    Rollback a previously executed action.

    Args:
        action_id: ID of action to rollback
        user_id: User ID requesting rollback

    Returns:
        Rollback result
    """
    # Get action from audit trail
    events = self.audit_trail.get_events(action_type=action_id, limit=1)

    if not events:
        return {
            "success": False,
            "reason": "Action not found in audit trail"
        }

    event = events[0]

    # Determine rollback strategy based on action type
    # Implementation depends on action types

    # Log rollback
    self.audit_trail.log_event(
        event_type="rollback",
        action_type=event["action_type"],
        confidence=0.0,
        safety_level="SAFE",
        auto_executed=False,
        user_id=user_id,
        result="rollback_success",
        details={"original_action_id": action_id}
    )

    return {
        "success": True,
        "rolled_back_action": action_id
    }
```

---

### Phase 4: Integration & Testing (1 hour)

**Step 1: Create Integration Tests** (0.5 hours)

Create `tests/integration/test_intelligent_automation.py`:

```python
"""
Integration tests for intelligent automation system.

Tests safety controls, predictive assistance, and autonomous execution.
"""

import pytest
from services.automation.action_classifier import ActionClassifier, ActionSafetyLevel
from services.automation.emergency_stop import EmergencyStop
from services.automation.audit_trail import AuditTrail
from services.automation.predictive_assistance import PredictiveAssistant
from services.automation.autonomous_executor import AutonomousExecutor


class TestActionClassifier:
    """Test action safety classification."""

    def test_destructive_actions_never_safe(self):
        """Destructive actions are NEVER safe for auto-execution."""
        classifier = ActionClassifier()

        destructive_actions = [
            "delete_file", "remove_user", "drop_table",
            "publish_release", "deploy_prod", "merge_pr"
        ]

        for action in destructive_actions:
            # Even with high confidence, should NOT be safe
            is_safe = classifier.is_safe_for_auto_execution(
                action_type=action,
                confidence=0.99  # Very high confidence
            )

            assert is_safe is False, f"{action} should NEVER be safe for auto-execution"

    def test_safe_actions_with_high_confidence(self):
        """Safe actions with high confidence can be auto-executed."""
        classifier = ActionClassifier()

        safe_actions = [
            "read_file", "get_data", "list_items",
            "search_issues", "view_pr", "check_status"
        ]

        for action in safe_actions:
            # With high confidence, should be safe
            is_safe = classifier.is_safe_for_auto_execution(
                action_type=action,
                confidence=0.95
            )

            assert is_safe is True, f"{action} should be safe with high confidence"

    def test_confirmation_actions_require_approval(self):
        """Actions requiring confirmation need user approval."""
        classifier = ActionClassifier()

        confirmation_actions = [
            "create_issue", "add_comment", "assign_user"
        ]

        for action in confirmation_actions:
            classification = classifier.classify_action(action)

            assert classification.requires_confirmation is True
            assert classification.safety_level == ActionSafetyLevel.REQUIRES_CONFIRMATION


class TestEmergencyStop:
    """Test emergency stop functionality."""

    def test_emergency_stop_prevents_execution(self):
        """Emergency stop prevents all automation execution."""
        stop = EmergencyStop()

        # Trigger emergency stop
        stop.trigger_emergency_stop("Test stop")

        assert stop.is_stopped() is True

        # Should not allow operation registration
        with pytest.raises(RuntimeError):
            stop.register_operation("test_op")

    def test_emergency_stop_reset(self):
        """Emergency stop can be reset."""
        stop = EmergencyStop()

        stop.trigger_emergency_stop("Test")
        assert stop.is_stopped() is True

        stop.reset()
        assert stop.is_stopped() is False


class TestAuditTrail:
    """Test audit trail logging."""

    def test_audit_trail_logs_events(self):
        """Audit trail logs all automation events."""
        audit = AuditTrail()

        # Log an event
        audit.log_event(
            event_type="test_execution",
            action_type="create_issue",
            confidence=0.85,
            safety_level="REQUIRES_CONFIRMATION",
            auto_executed=False,
            user_id="test_user"
        )

        # Retrieve events
        events = audit.get_events()

        assert len(events) > 0
        assert events[-1]["event_type"] == "test_execution"
        assert events[-1]["action_type"] == "create_issue"


class TestPredictiveAssistance:
    """Test predictive assistance capabilities."""

    @pytest.mark.asyncio
    async def test_next_action_prediction(self):
        """Test next action prediction using patterns."""
        assistant = PredictiveAssistant()

        predictions = await assistant.predict_next_action(
            user_id="test_user",
            current_context={"action": "create_issue"}
        )

        # Should return list of predictions
        assert isinstance(predictions, list)

        # Each prediction should have confidence
        for pred in predictions:
            assert "confidence" in pred
            assert 0 <= pred["confidence"] <= 1


class TestAutonomousExecution:
    """Test autonomous execution with safety."""

    @pytest.mark.asyncio
    async def test_safe_execution_with_high_confidence(self):
        """Safe actions with high confidence auto-execute."""
        executor = AutonomousExecutor()

        decision = await executor.should_auto_execute(
            action_type="read_file",
            confidence=0.95,
            user_id="test_user"
        )

        assert decision["should_execute"] is True
        assert decision["safety_level"] == "safe"

    @pytest.mark.asyncio
    async def test_destructive_never_auto_executes(self):
        """Destructive actions NEVER auto-execute."""
        executor = AutonomousExecutor()

        decision = await executor.should_auto_execute(
            action_type="delete_file",
            confidence=0.99,  # Even with very high confidence!
            user_id="test_user"
        )

        assert decision["should_execute"] is False
        assert decision["requires_approval"] is True
```

---

**Step 2: End-to-End Testing** (0.5 hours)

Create manual test in `dev/active/test_intelligent_automation_flow.py`:

```python
"""
Manual test for intelligent automation end-to-end flow.

Tests: Prediction → Safety Check → Autonomous Execution → Audit
"""

import asyncio
from services.automation.predictive_assistance import PredictiveAssistant
from services.automation.autonomous_executor import AutonomousExecutor
from services.automation.audit_trail import get_audit_trail


async def main():
    print("Testing Intelligent Automation Flow...")

    assistant = PredictiveAssistant()
    executor = AutonomousExecutor()
    audit = get_audit_trail()

    # Test 1: Predictive assistance
    print("\n1. Testing next action prediction...")
    predictions = await assistant.predict_next_action(
        user_id="test_user",
        current_context={"action": "create_issue", "repo": "piper-morgan"}
    )
    print(f"Predictions: {len(predictions)} actions predicted")

    # Test 2: Safety classification
    print("\n2. Testing safety classification...")
    safe_decision = await executor.should_auto_execute(
        action_type="read_file",
        confidence=0.95,
        user_id="test_user"
    )
    print(f"Safe action decision: {safe_decision}")

    destructive_decision = await executor.should_auto_execute(
        action_type="delete_file",
        confidence=0.99,
        user_id="test_user"
    )
    print(f"Destructive action decision: {destructive_decision}")

    # Test 3: Audit trail
    print("\n3. Testing audit trail...")
    stats = audit.get_automation_statistics()
    print(f"Automation statistics: {stats}")

    events = audit.get_events(limit=5)
    print(f"Recent events: {len(events)}")

    print("\n✅ All intelligent automation tests passed!")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## Verification Steps

### Step 1: Verify Safety Controls

```bash
# Check action classifier
python -c "
from services.automation.action_classifier import ActionClassifier
classifier = ActionClassifier()

# Test destructive action
print('Delete safe?', classifier.is_safe_for_auto_execution('delete_file', 0.99))
# Should print: False

# Test safe action
print('Read safe?', classifier.is_safe_for_auto_execution('read_file', 0.95))
# Should print: True
"
```

---

### Step 2: Run Integration Tests

```bash
# Run intelligent automation tests
pytest tests/integration/test_intelligent_automation.py -v

# Should pass all safety tests!
```

---

### Step 3: Test Emergency Stop

```bash
python -c "
from services.automation.emergency_stop import EmergencyStop
stop = EmergencyStop()

print('Initial:', stop.is_stopped())  # False
stop.trigger_emergency_stop('Test')
print('After trigger:', stop.is_stopped())  # True

try:
    stop.register_operation('test')
except RuntimeError as e:
    print('Correctly blocked:', str(e))
"
```

---

### Step 4: Run End-to-End Test

```bash
python dev/active/test_intelligent_automation_flow.py
```

---

## Success Criteria

CORE-LEARN-E is complete when:

- [ ] Action classification system complete (~150 lines)
- [ ] Emergency stop system working (~50 lines)
- [ ] Audit trail system logging (~100 lines)
- [ ] Predictive assistance API complete (~150 lines)
- [ ] Autonomous execution framework complete (~200 lines)
- [ ] User approval system integrated (~100 lines)
- [ ] Integration tests passing (5+ tests)
- [ ] All existing tests still passing (zero regressions)
- [ ] Manual end-to-end test demonstrates safe automation
- [ ] Safety controls VERIFIED to prevent destructive auto-execution
- [ ] Code committed with evidence
- [ ] Session log updated

---

## Files to Create/Modify

### Create (New Automation Infrastructure)

- `services/automation/action_classifier.py` (~150 lines) - Safety classification
- `services/automation/emergency_stop.py` (~50 lines) - Emergency stop
- `services/automation/audit_trail.py` (~100 lines) - Audit logging
- `services/automation/predictive_assistance.py` (~150 lines) - Predictions
- `services/automation/autonomous_executor.py` (~200 lines) - Safe execution
- `services/automation/user_approval.py` (~100 lines) - User preferences
- `tests/integration/test_intelligent_automation.py` (~300 lines) - Tests
- `dev/active/test_intelligent_automation_flow.py` (~100 lines) - Manual test

### Session Log

- Continue in existing log or create: `dev/2025/10/20/HHMM-prog-code-log.md`

---

## Expected Timeline

**Total**: 6 hours (from discovery)

**Phase-by-Phase**:
- 2h: Safety controls (CRITICAL - do first!)
- 2h: Predictive assistance (wiring existing services)
- 3h: Autonomous execution (framework + approval + rollback)
- 1h: Integration & testing

---

## Remember

**SAFETY IS NON-NEGOTIABLE!**

**Critical principles**:
1. ✅ Implement safety controls FIRST (Phase 1)
2. ✅ NEVER auto-execute destructive actions
3. ✅ ALWAYS require confirmation for publishes
4. ✅ Audit trail for ALL automation
5. ✅ Emergency stop MUST work

**Implementation order matters**:
1. Safety controls (Phase 1)
2. Predictive assistance (Phase 2)
3. Autonomous execution (Phase 3) - ONLY after safety!
4. Integration & testing (Phase 4)

**This is the hill we die on!** 🔒

---

**Ready to build intelligent automation safely!** 🚀

*Discovery found 80% complete (3,579 lines). Implementation is ~1,050 lines of careful, safety-first work. Issue 5 of 6 in Extended Sprint A5!*

**SAFETY FIRST. ALWAYS.** 🔒✨
