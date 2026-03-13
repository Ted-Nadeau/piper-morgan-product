# Phase 4 Implementation Plan
## Based on Chief Architect Recommendations

**Date**: Friday, November 14, 2025, 8:05 AM PT
**Architect Consult**: Completed 7:00-7:20 AM
**Status**: Ready to implement

---

## Executive Summary

**Architect's Core Recommendation**: **Simplified scope for Alpha** (proactive suggestions, not full auto-execution)

**Implementation Approach**:
- Action Registry + Command Pattern for extensibility
- Two-tier consent model (low-risk vs high-risk actions)
- Hybrid context matching (explicit triggers + similarity)
- Integration before canonical handlers with fallback
- **2-3 hours estimated effort**

**Philosophy**: Human remains in control, transparent automation, gradual trust-building

---

## Detailed Recommendations

### Q1: Action Execution Architecture ✅

**Architect chose**: **Option B (Action Registry) with Command Pattern elements**

**Implementation**:
```python
class ActionRegistry:
    """Central registry for executable actions"""

    _actions = {
        "create_github_issue": GithubIssueCommand,
        "update_notion": NotionUpdateCommand,
        "send_slack_message": SlackMessageCommand,
    }

    @classmethod
    async def execute(cls, action_type: str, params: dict, context: dict):
        command_class = cls._actions.get(action_type)
        if not command_class:
            raise ValueError(f"Unknown action: {action_type}")

        command = command_class(params, context)
        return await command.execute()
```

**Rationale**:
- ✅ Extensible without modifying core
- ✅ Each command encapsulates its logic
- ✅ Testable in isolation
- ✅ Can add undo() methods later
- ✅ Avoids circular dependencies

**Rejected**: Option C (Intent-based) - circular dependency risk

---

### Q2: Safety & Consent Model ✅

**Architect chose**: **Model C (Two-Tier Consent) for Alpha**

**Implementation**:
```python
# Risk classification
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

async def apply_pattern(pattern, context):
    if pattern.action_type in LOW_RISK_ACTIONS:
        # Execute then notify
        result = await execute_action(pattern)
        notify_user(f"I've {pattern.description} based on your pattern")
        return result

    elif pattern.action_type in HIGH_RISK_ACTIONS:
        # Preview and wait for approval (reuse Phase 3 UI)
        await show_auto_suggestion(
            f"Ready to {pattern.description}",
            pattern,
            auto_triggered=True
        )
```

**Rationale**:
- ✅ Balances automation with safety
- ✅ Builds trust gradually
- ✅ Alpha users won't be surprised
- ✅ Aligns with "human-AI collaboration" philosophy

**For Post-Alpha**: Consider sliding automation (Model D) once we have usage data

---

### Q3: Context Matching Strategy ✅

**Architect chose**: **Approach D (Hybrid) - Start Simple**

**Implementation**:
```python
class ContextMatcher:
    """Match current context to pattern triggers"""

    @classmethod
    async def matches(cls, pattern_context: dict, current_context: dict) -> bool:
        # 1. Temporal triggers (explicit)
        if pattern_context.get("trigger_time"):
            if not cls._check_temporal(...):
                return False

        # 2. Sequential triggers (explicit)
        if pattern_context.get("after_action"):
            if current_context.get("last_action") != pattern_context["after_action"]:
                return False

        # 3. Conditional (similarity-based)
        if pattern_context.get("conditions"):
            similarity = cls._calculate_similarity(...)
            if similarity < 0.8:
                return False

        # 4. Event-based (exact match)
        if pattern_context.get("trigger_event"):
            if current_context.get("event") != pattern_context["trigger_event"]:
                return False

        return True  # All conditions met
```

**Rationale**:
- ✅ Predictable for users
- ✅ No LLM latency/cost for alpha
- ✅ Can add LLM later for ambiguous cases
- ✅ "Explicit is better than implicit"

**Rejected**: Option C (LLM-based) - too slow/costly for alpha

---

### Q4: Integration Point in Flow ✅

**Architect chose**: **Option A (Before canonical handlers) with fallback**

**Implementation**:
```python
async def execute(user_input, user_id, context):
    # 1. Classify intent
    intent = await intent_classifier.classify(user_input)

    # 2. Capture for learning
    await learning_handler.capture_action(user_id, intent, context)

    # 3. Check for HIGH-CONFIDENCE auto-application (NEW)
    auto_patterns = await learning_handler.get_automation_patterns(
        user_id, context, min_confidence=0.9
    )

    # 4. Apply pattern if found
    if auto_patterns and context_matches(auto_patterns[0], context):
        result = await apply_pattern(auto_patterns[0], context)

        # Still run canonical for side effects
        canonical_result = await canonical_handlers.execute(intent, context)

        return IntentProcessingResult(
            response=result.response or canonical_result.response,
            pattern_applied=auto_patterns[0],
            suggestions=[]  # No suggestions when auto-applied
        )

    # 5. Otherwise, normal flow
    suggestions = await learning_handler.get_suggestions(user_id, context)
    result = await canonical_handlers.execute(intent, context)

    return IntentProcessingResult(
        response=result,
        suggestions=suggestions
    )
```

**Rationale**:
- ✅ Patterns take precedence (user's learned behavior)
- ✅ Still runs canonical for logging/side effects
- ✅ Clean separation of concerns
- ✅ Easy to disable if issues

---

### Q5: Scope Decision for Alpha ✅

**Architect chose**: **SIMPLIFIED (Proactive Suggestions)** - NOT full auto

**Alpha Scope** (2-3 hours):
```python
# When confidence >= 0.9 AND context matches:
# Show PROACTIVE suggestion (different from regular suggestions)

if pattern.confidence >= 0.9 and context_matches(pattern, context):
    suggestion = ProactiveSuggestion(
        title=f"Ready to {pattern.description}",
        message="I'm ready to execute this based on your pattern",
        pattern=pattern,
        auto_triggered=True,  # Visual distinction
        actions=["Execute Now", "Skip This Time", "Disable Pattern"]
    )
    return suggestion
```

**Why NOT Full Auto for Alpha**:
- ⚠️ Risk of surprising users
- ⚠️ No undo mechanism yet
- ⚠️ Need user feedback first
- ⚠️ Can always upgrade to full auto

**Benefits of Simplified**:
- ✅ Faster to implement (2-3 hours vs 4-5)
- ✅ Reuses Phase 3 UI
- ✅ User maintains control
- ✅ Still feels "smart"
- ✅ Gather data on what users want

**Post-Alpha Evolution**:
- See which patterns users always approve → make those full auto
- See which patterns users skip → lower confidence
- Build undo mechanism based on real usage

---

## Risk Assessment

### Simplified Approach Risks (Low) ✅

**Low Risks**:
- User annoyance (they control it)
- System errors (preview before execute)
- Privacy concerns (same as Phase 3)

**Medium Risks**:
- Users want MORE automation (good problem!)
- Patterns fire too often (tune thresholds)

### Full Auto Risks (High) ❌

**Why we're NOT doing full auto**:
- ❌ Execute wrong action (no undo yet)
- ❌ User loses trust (one bad auto-execution)
- ❌ Compliance issues (auto-sending messages)

---

## Implementation Plan (2-3 Hours)

### Step 1: Action Registry (Small - 30 min)

**What**: Create registry with 2-3 actions

**Files to create**:
- `services/actions/action_registry.py`
- `services/actions/commands/base_command.py`
- `services/actions/commands/github_issue_command.py` (example)

**Start with LOW_RISK only**:
- `read_github_issue`
- `draft_document`
- `search_slack`

**Test in isolation**: Unit tests for each command

---

### Step 2: Context Matcher (Small - 30 min)

**What**: Implement hybrid matcher

**Files to create**:
- `services/learning/context_matcher.py`

**Matching types to implement**:
- Temporal (time-based)
- Sequential (after-action)
- (Defer conditional/event for post-alpha)

**Test with real patterns**: Integration test

---

### Step 3: Proactive Suggestions UI (Small - 45 min)

**What**: Modify Phase 3 UI for auto-triggered suggestions

**Files to modify**:
- `web/assets/bot-message-renderer.js`
- `templates/home.html` (CSS)

**Changes**:
```javascript
// Add auto_triggered flag handling
function renderSuggestionCard(suggestion) {
    const isAutoTriggered = suggestion.auto_triggered;
    const badgeClass = isAutoTriggered ? 'auto-badge' : 'manual-badge';

    return `
        <div class="suggestion-card ${isAutoTriggered ? 'auto-triggered' : ''}">
            <span class="suggestion-badge ${badgeClass}">
                ${isAutoTriggered ? '⚡ Auto-detected' : '💡 Suggested'}
            </span>
            <!-- rest of card -->
        </div>
    `;
}
```

**Visual distinction**:
- Different color (orange instead of teal for auto-triggered)
- Lightning bolt icon (⚡) instead of lightbulb (💡)
- "Execute Now" button more prominent

---

### Step 4: Integration (Small - 45 min)

**What**: Wire into IntentService

**Files to modify**:
- `services/intent/intent_service.py`
- `services/learning/learning_handler.py`

**New method in LearningHandler**:
```python
async def get_automation_patterns(
    self,
    user_id: UUID,
    context: dict,
    min_confidence: float = 0.9,
    session: AsyncSession = None
) -> List[LearnedPattern]:
    """Get patterns eligible for auto-application"""
    # Similar to get_suggestions but confidence >= 0.9
```

**Integration in IntentService**:
```python
# After capture_action, before canonical handlers
auto_patterns = await learning_handler.get_automation_patterns(...)
if auto_patterns and context_matcher.matches(...):
    # Show proactive suggestion
```

**Test end-to-end flow**:
- Create pattern with 0.9 confidence
- Trigger context match
- Verify proactive suggestion appears
- Click "Execute Now"
- Verify action executes

---

## Success Criteria

**Functionality** ✅:
- [ ] Patterns with 0.9+ confidence show proactive suggestions
- [ ] Context matching works (temporal, sequential)
- [ ] User can execute/skip/disable from suggestion
- [ ] Visual distinction for auto-triggered suggestions
- [ ] "Execute Now" action works

**Performance** ✅:
- [ ] <20ms overhead maintained
- [ ] No disruption to existing flow

**Quality** ✅:
- [ ] All existing tests still pass (55/55)
- [ ] New integration test for auto-application
- [ ] Manual testing: 3 scenarios
- [ ] Evidence documented

---

## Manual Testing Scenarios

### Scenario 1: Proactive Suggestion Appears

**Setup**: Pattern with 0.92 confidence, temporal trigger "after standup"

**Steps**:
1. Complete standup
2. Navigate to chat
3. Verify proactive suggestion appears
4. Check visual distinction (⚡ icon, orange badge)

**Evidence**: Screenshot

---

### Scenario 2: Execute Now Works

**Steps**:
1. See proactive suggestion
2. Click "Execute Now"
3. Verify action executes
4. Verify user notification
5. Check database: pattern applied

**Evidence**: Screenshot + curl output

---

### Scenario 3: Skip This Time

**Steps**:
1. See proactive suggestion
2. Click "Skip This Time"
3. Verify suggestion dismissed
4. Check database: NO confidence change

**Evidence**: Screenshot + database state

---

## Philosophy Alignment

**Architect's Assessment**: ✅ Aligned with Piper's values

- ✅ **Human remains in control** (can execute/skip)
- ✅ **Transparent about automation** (shows what will happen)
- ✅ **Gradual trust building** (not full auto yet)
- ✅ **Quality over features** (simplified but solid)

**Building-in-public**: Shows transparent learning progression

**User-controlled**: User makes final execution decision

**Teachable**: Can explain to users how it works

---

## Comparison to Yesterday's Options

**Yesterday we identified 4 options**:

| Option | Effort | Risk | Architect Chose |
|--------|--------|------|-----------------|
| A: Full auto | 4-5h | Medium | ❌ Not for alpha |
| B: Architect review first | +30m + 3-4h | Low | ✅ Done! |
| C: Defer to post-alpha | 0h | Low | ❌ |
| D: Simplified proactive | 2-3h | Low | ✅ YES |

**Architect validated Option D** (simplified) as the right choice for alpha

---

## Next Steps

### Immediate (Now - 8:15 AM)

1. ✅ Synthesize architect recommendations (this document)
2. ⏭️ Create Phase 4 agent prompt (15 min)
3. ⏭️ Deploy to Code agent (2-3 hours)

### After Implementation (11:00 AM - 12:00 PM)

4. Review and test Phase 4
5. Manual testing (3 scenarios)
6. Document evidence
7. Ready for Phase 5/6 or other priorities

---

## Summary of Architect Decisions

| Question | Recommendation | Rationale |
|----------|----------------|-----------|
| **Q1: Execution** | Registry + Command Pattern | Extensible, testable, clean |
| **Q2: Safety** | Two-tier consent | Balance automation & safety |
| **Q3: Context** | Hybrid matching | Predictable, no LLM cost |
| **Q4: Integration** | Before canonical w/ fallback | Patterns take precedence |
| **Q5: Scope** | **SIMPLIFIED for alpha** | Faster, safer, user-controlled |

**Bottom line**: Proactive suggestions (0.9+ confidence), user approves, 2-3 hours work

---

## Questions Answered

**Do we have action execution infrastructure?** → Will build Action Registry

**How to handle safety?** → Two-tier consent model (low-risk vs high-risk)

**How to match context?** → Hybrid (temporal + sequential for now)

**Where to integrate?** → Before canonical handlers with fallback

**Full or simplified?** → **SIMPLIFIED for alpha** ✅

---

**Status**: Ready to create Phase 4 agent prompt
**Estimated implementation**: 2-3 hours
**Philosophy**: Aligned with Piper's values
**Risk**: Low

---

_"Measure twice, cut once"_ ✅
_"The architect has spoken"_
_"Let's build it right"_
