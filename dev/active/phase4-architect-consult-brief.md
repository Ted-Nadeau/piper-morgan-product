# Chief Architect Consult: Phase 4 Pattern Application
## Quick Architectural Clarity Needed

**Date**: November 13, 2025, 7:25 PM PT
**From**: Lead Developer
**To**: Chief Architect
**Duration**: 30 minutes
**Purpose**: Clarify architectural approach before implementing Phase 4

---

## Context (2 minutes)

### What We've Built

**Phase 1-3 Complete** ✅:
- Real-time pattern detection and confidence tracking
- User controls API (7 endpoints for pattern management)
- Web UI for suggestions (badge, cards, accept/reject/dismiss)
- Manual feedback loop working (confidence updates based on user response)

**Current Flow**:
```
User action → Capture pattern → Build confidence over time
If confidence > 0.7 → Show suggestion in UI
User accepts/rejects → Confidence adjusts
```

---

### What Phase 4 Is

**Gameplan scope**: When pattern confidence >= 0.9, **auto-apply** the pattern

**Example**:
- User creates GitHub issue after standup 10 times
- Pattern confidence reaches 0.92
- Next standup: **Piper automatically creates issue** (no asking)
- User notified: "I created issue #456 based on your workflow pattern"

**Question**: How to architect this properly?

---

## Core Questions (15 minutes)

### Question 1: Action Execution Architecture

**Context**: Patterns capture "what user did" but Phase 4 needs to "do the thing"

**Example pattern data**:
```json
{
  "pattern_type": "USER_WORKFLOW",
  "description": "Create GitHub issue after standup",
  "context": {
    "trigger": "after standup",
    "action": "create_github_issue",
    "typical_params": {
      "labels": ["standup", "action-item"],
      "assignee": "self"
    }
  }
}
```

**How do we execute this?**

**Option A: Direct execution**
```python
if action == "create_github_issue":
    await github_service.create_issue(params)
```
- Pro: Simple, direct
- Con: Hard-coded action types, doesn't scale

**Option B: Action registry**
```python
action_registry = {
    "create_github_issue": github_service.create_issue,
    "update_notion": notion_service.update,
    # ...
}
await action_registry[action](params)
```
- Pro: Extensible, clean
- Con: Need to build registry

**Option C: Intent-based**
```python
# Re-route through IntentService
await intent_service.execute(
    user_input=pattern.description,
    auto_execute=True
)
```
- Pro: Reuses existing handlers
- Con: Circular dependency risk

**Option D: Command pattern**
```python
# Patterns store executable commands
command = pattern.create_command()
await command.execute()
```
- Pro: Flexible, testable
- Con: More abstraction

**Your recommendation**: Which approach or hybrid?

---

### Question 2: Safety & Consent Model

**Context**: Auto-execution is powerful but risky

**Safety concerns**:
1. What if pattern is wrong for this specific instance?
2. What if user doesn't want it executed right now?
3. How does user undo or roll back?
4. What actions need explicit consent vs. implicit?

**Possible models**:

**Model A: Execute then notify**
```
Pattern applies → Execute action → Notify user → Undo available
```
- Pro: Fast, autonomous
- Con: User sees after-the-fact

**Model B: Preview then execute**
```
Pattern applies → Show preview → User approves → Execute
```
- Pro: User control, safer
- Con: Not truly "auto", more like proactive suggestion

**Model C: Two-tier consent**
```
Low-risk actions (read, draft): Execute then notify
High-risk actions (create, delete, send): Preview first
```
- Pro: Balanced risk/automation
- Con: Need to classify risk levels

**Model D: Sliding automation**
```
0.7-0.8: Show suggestion (Phase 3 - done)
0.8-0.9: Show proactive suggestion
0.9-0.95: Execute draft, notify, require approval
0.95+: Execute final, notify, undo available
```
- Pro: Gradual trust-building
- Con: Complex thresholds

**Your recommendation**: Which model fits Piper's philosophy?

---

### Question 3: Context Matching Strategy

**Context**: Pattern has context like "after standup" or "Monday 9am" - how to match?

**Pattern context types**:

1. **Temporal**: "Monday at 9am", "End of day", "After standup"
2. **Sequential**: "After creating issue", "Before sending message"
3. **Conditional**: "When project is active", "If calendar has meetings"
4. **Event-based**: "On GitHub PR merge", "On Slack mention"

**Matching approaches**:

**Approach A: Explicit triggers**
```python
# Patterns define specific trigger events
if current_event in pattern.triggers:
    apply_pattern()
```

**Approach B: Context similarity**
```python
# Compare current context dict to pattern context
if context_similarity(current, pattern.context) > 0.8:
    apply_pattern()
```

**Approach C: LLM-based**
```python
# Ask LLM if context matches
prompt = f"Does '{current_context}' match pattern context '{pattern.context}'?"
if await llm_check(prompt):
    apply_pattern()
```

**Approach D: Hybrid**
```python
# Explicit triggers for time/events
# Similarity for sequential/conditional
# LLM for ambiguous cases
```

**Your recommendation**: Which approach or combination?

---

### Question 4: Integration Point in Flow

**Context**: IntentService orchestrates user requests - where to check for auto-application?

**Current flow**:
```python
async def execute(user_input, user_id, context):
    # 1. Classify intent (TEMPORAL, GITHUB, etc.)
    intent = await intent_classifier.classify(user_input)

    # 2. Capture action for learning (Phase 1)
    await learning_handler.capture_action(user_id, intent, context)

    # 3. Get suggestions for UI (Phase 3)
    suggestions = await learning_handler.get_suggestions(user_id, context)

    # 4. ?????? WHERE TO CHECK AUTO-APPLICATION (Phase 4)

    # 5. Execute canonical handlers (standup, issue creation, etc.)
    result = await canonical_handlers.execute(intent, context)

    # 6. Return result + suggestions
    return IntentProcessingResult(response=result, suggestions=suggestions)
```

**Options**:

**Option A: Before canonical handlers**
```python
# 4. Check for auto-application
auto_applied = await learning_handler.apply_patterns(user_id, context)
if auto_applied:
    return early_with_notification(auto_applied)
# 5. Otherwise, execute canonical handlers
```
- Pro: Clean separation
- Con: Might miss canonical handler logic

**Option B: Parallel to canonical handlers**
```python
# 4. Check and prepare auto-application
auto_applied = await learning_handler.apply_patterns(user_id, context)
# 5. Execute canonical handlers
result = await canonical_handlers.execute(intent, context)
# 6. Merge results
return combined(result, auto_applied)
```
- Pro: Both systems work
- Con: Potential conflicts

**Option C: Replace canonical handlers**
```python
# 4. Check for high-confidence pattern
patterns = await get_automation_patterns(user_id, context)
if patterns:
    result = await apply_pattern(patterns[0])
else:
    # 5. Fall back to canonical handlers
    result = await canonical_handlers.execute(intent, context)
```
- Pro: Patterns take precedence
- Con: May bypass important logic

**Your recommendation**: Where and how to integrate?

---

### Question 5: Scope Decision for Alpha

**Context**: Phase 4 could be simple or complex depending on scope

**Scope options**:

**Full Auto (Original)**:
- Execute actions without asking
- Notify after execution
- Undo mechanism
- 4-5 hours work, higher risk

**Simplified (Proactive Suggestions)**:
- Show suggestion when confidence >= 0.9 AND context matches
- User still approves before execution
- Reuses Phase 3 UI
- 2-3 hours work, lower risk

**Your recommendation**:
- Full auto for alpha? (more impressive, riskier)
- Simplified for alpha, full post-alpha? (safer, faster)
- Something in between?

---

## Decision Tree (10 minutes)

**Based on your answers, we'll know**:

1. **Q1 (Execution)** → Implementation approach for applying patterns
2. **Q2 (Safety)** → User consent model and undo mechanism
3. **Q3 (Context)** → How to trigger auto-application
4. **Q4 (Integration)** → Where in code to add Phase 4
5. **Q5 (Scope)** → Full or simplified for alpha

**Output**: Clear Phase 4 implementation plan

---

## What We Need From You

**Not asking for**:
- Detailed design (we'll do that)
- Code review (not written yet)
- Implementation decisions (Lead Dev handles)

**Asking for**:
- Architectural direction (which approach fits system?)
- Risk assessment (what could go wrong?)
- Philosophy guidance (what fits Piper's values?)
- Scope recommendation (alpha-appropriate?)

**Your expertise**: System architecture, risk/benefit trade-offs, strategic direction

---

## If Short on Time

**Priority ranking** (if we only have 15 minutes):

1. **Q5 (Scope)** - Most critical: full or simplified for alpha?
2. **Q2 (Safety)** - Second: what consent model?
3. **Q1 (Execution)** - Third: how to execute actions?
4. **Q4 (Integration)** - Fourth: where to integrate?
5. **Q3 (Context)** - Fifth: can be solved during implementation

We can proceed with just Q5 + Q2 if needed.

---

## Success Criteria

**After this consult, Lead Developer should**:
- Know which Phase 4 scope to implement
- Have clear architectural direction
- Understand safety/risk considerations
- Be able to create confident agent prompt
- Estimate realistic implementation time

**After implementation, PM should**:
- Have working auto-application (full or simplified)
- Feel confident about alpha user experience
- Know what's deferred vs. delivered

---

## Next Steps

**After consult**:
1. Lead Dev creates Phase 4 agent prompt (15 min)
2. Deploy to Code agent (2-5 hours depending on scope)
3. Test and validate
4. Ready for Phase 5 (integration tests) or other priorities

---

## Appendices

### A. Current Pattern Structure

```python
@dataclass
class LearnedPattern:
    id: UUID
    user_id: UUID
    pattern_type: PatternType  # USER_WORKFLOW, COMMAND_SEQUENCE, etc.
    description: str  # Human-readable
    pattern_data: dict  # JSONB with action details
    confidence: float  # 0.0-1.0
    success_count: int
    failure_count: int
    enabled: bool
    created_at: datetime
    updated_at: datetime
```

### B. Example Pattern Data

```json
{
  "intent": "GITHUB_ISSUE_CREATE",
  "trigger_context": {
    "after": "standup",
    "time_pattern": "weekday_morning",
    "typical_time": "09:15"
  },
  "action_params": {
    "labels": ["standup", "action-item"],
    "assignee": "self",
    "project": "current"
  },
  "success_signals": [
    "issue_created",
    "user_viewed_issue"
  ]
}
```

### C. Related ADRs

- ADR-001: MCP Integration Pattern
- ADR-024: Persistent Context Architecture
- ADR-029: Domain Service Mediation

---

**Status**: Ready for 30-minute architect consult
**Scheduling**: Tonight (brief) or tomorrow morning?
**Output**: Clear direction for Phase 4 implementation

---

_"Measure twice, cut once"_
_"30 minutes of architecture saves 2 hours of refactoring"_
_"The PM decides scope. The architect decides approach."_
