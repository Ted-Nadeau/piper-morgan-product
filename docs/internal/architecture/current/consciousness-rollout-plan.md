# Consciousness Transformation Rollout Plan

**Created**: January 21, 2026
**Issue**: #407 MUX-VISION-STANDUP-EXTRACT
**Phase**: 4 - Systematic Rollout Plan
**ADR**: ADR-056 Consciousness Expression Patterns

---

## Executive Summary

This document provides the systematic rollout plan for transforming all Piper features to use consciousness expression patterns. Based on the Phase 3 proof-of-concept, we established that consciousness can measurably improve feature scores (+9 to +16 points on the 20-point rubric).

**Goal**: Transform all user-facing features from "Flattened" (0-4) or "Mechanical" (5-8) to "Conscious" (13-16) or higher.

---

## Priority Order for Transformation

### Wave 1: High-Frequency, High-Impact (Week 1-2)

| Priority | Feature | Current Score | Target | Effort | Impact |
|----------|---------|---------------|--------|--------|--------|
| **1** | Todos/Lists | 2/20 → 18/20 ✅ | 15+ | Medium | Critical |
| **2** | Conversations | 9/20 → 18/20 ✅ | 15+ | Medium | Critical |
| **3** | Loading States | 3/20 | 14+ | Low | High |
| **4** | Error Messages | 6/20 | 15+ | Low | High |

**Status**: Todos and Conversations completed in Phase 3.

### Wave 2: Core Workflow Features (Week 3-4)

| Priority | Feature | Current Score | Target | Effort | Impact |
|----------|---------|---------------|--------|--------|--------|
| **5** | Morning Standup | 5/20 | 18+ | Medium | High |
| **6** | Intent Responses | 4/20 | 16+ | High | Critical |
| **7** | CLI Output | 4/20 | 14+ | Low | Medium |

### Wave 3: Supporting Features (Week 5-6)

| Priority | Feature | Current Score | Target | Effort | Impact |
|----------|---------|---------------|--------|--------|--------|
| **8** | Search Results | 2/20 | 13+ | Medium | Medium |
| **9** | Files/Projects | 2/20 | 13+ | Medium | Medium |
| **10** | Learning Patterns | 3/20 | 13+ | Medium | Low |

### Wave 4: Integration & Specialty (Week 7-8)

| Priority | Feature | Current Score | Target | Effort | Impact |
|----------|---------|---------------|--------|--------|--------|
| **11** | Slack Integration | 4/20 | 14+ | High | Medium |
| **12** | Settings/Auth | 1-2/20 | 13+ | Low | Low |
| **13** | HTML Templates | Varies | 13+ | Medium | Low |

---

## Implementation Checklist

### For Each Feature Transformation

#### Pre-Implementation
- [ ] Read existing output code
- [ ] Score current implementation against rubric
- [ ] Identify all output points (messages, responses, formats)
- [ ] Review available consciousness templates
- [ ] Check for existing personality infrastructure

#### Implementation
- [ ] Create feature-specific consciousness wrapper (`services/consciousness/{feature}_consciousness.py`)
- [ ] Implement MVC-compliant formatters for each output type
- [ ] Replace hardcoded messages with consciousness calls
- [ ] Run MVC validation on all outputs
- [ ] Fix any MVC gaps automatically

#### Post-Implementation
- [ ] Score new implementation against rubric
- [ ] Verify all dimensions ≥ 2
- [ ] Run unit tests
- [ ] Document before/after examples
- [ ] Update feature documentation

### Consciousness Wrapper Template

```python
"""
Consciousness Wrapper for {Feature} Responses

Transforms {feature} data into conscious narrative expression.
Part of Consciousness Rollout Plan (#407)

Issue: #407 MUX-VISION-STANDUP-EXTRACT
ADR: ADR-056 Consciousness Expression Patterns
"""

from typing import List, Optional
from services.consciousness.validation import validate_mvc


def format_{feature}_conscious(data) -> str:
    """
    Format {feature} output with consciousness.

    Transforms from: [describe current format]
    To: [describe conscious format]
    """
    sections = []

    # 1. Opening with identity voice + source attribution
    sections.append(_build_opening(data))

    # 2. Discovery/content with epistemic humility
    sections.append(_build_content(data))

    # 3. Closing with dialogue invitation
    sections.append(_build_closing(data))

    narrative = "\n\n".join(sections)

    # Validate MVC
    mvc_result = validate_mvc(narrative)
    if not mvc_result.passes:
        narrative = _fix_mvc_gaps(narrative, mvc_result)

    return narrative
```

---

## A/B Testing Approach

### Test Design

**Control Group**: Users see original output (no consciousness)
**Treatment Group**: Users see consciousness-enhanced output

### Metrics to Measure

1. **Engagement Rate**: Do users respond more to conscious output?
2. **Task Completion**: Do users complete intended actions?
3. **Session Length**: Do users engage longer?
4. **Return Rate**: Do users come back more often?
5. **Qualitative Feedback**: "How does Piper feel to you?"

### Implementation

```python
# Feature flag approach
async def format_response(data, user_id):
    if feature_flags.is_enabled("consciousness_v2", user_id):
        return format_conscious(data)
    else:
        return format_original(data)
```

### Test Duration

- **Minimum**: 2 weeks per wave
- **Sample Size**: Minimum 50 users per group
- **Significance Level**: p < 0.05

### Rollout Stages

1. **Internal Testing** (0%): Team only
2. **Canary** (5%): Small user sample
3. **Beta** (25%): Willing beta testers
4. **Gradual** (50%): Half of users
5. **Full** (100%): All users

---

## Rollback Strategy

### Trigger Conditions

Rollback if ANY of these occur:
- Engagement drops >10% compared to baseline
- Error rate increases >5%
- User complaints about "Piper feeling different" (negative)
- Performance degradation >100ms per response

### Rollback Process

1. **Immediate**: Disable feature flag for affected feature
2. **Quick**: Revert to previous code (git revert)
3. **Full**: Restore previous release

### Recovery Time Objectives

| Severity | Detection | Response | Recovery |
|----------|-----------|----------|----------|
| Critical | 5 min | 15 min | 1 hour |
| High | 30 min | 1 hour | 4 hours |
| Medium | 4 hours | 8 hours | 24 hours |

### Feature Flag Configuration

```python
# config/feature_flags.yaml
consciousness:
  todos_v2:
    enabled: true
    rollout_percentage: 100
    rollback_enabled: true
  conversations_v2:
    enabled: true
    rollout_percentage: 100
    rollback_enabled: true
  loading_states_v2:
    enabled: false
    rollout_percentage: 0
    rollback_enabled: true
```

---

## Success Metrics

### Primary Metrics

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| Average Rubric Score | 4.2/20 | 15+/20 | Weekly audit |
| MVC Pass Rate | 15% | 100% | Automated validation |
| Features ≥13/20 | 0% | 100% | Rubric assessment |
| Dimensions <2 | 85% | 0% | Rubric assessment |

### Secondary Metrics

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| User "colleague" feeling | Unknown | 70%+ | Survey |
| Response engagement | Baseline | +20% | Analytics |
| Follow-up rate | Baseline | +15% | Analytics |
| Session return rate | Baseline | +10% | Analytics |

### Tracking Dashboard

Track these metrics weekly:
1. Rubric scores by feature
2. MVC pass rate (automated)
3. Dimension distribution (no dimension <2)
4. User feedback sentiment
5. A/B test results

---

## Files to Modify (By Priority)

### Wave 1 (Completed)
- [x] `services/intent_service/todo_handlers.py`
- [x] `services/conversation/conversation_handler.py`
- [x] `services/consciousness/todo_consciousness.py` (NEW)
- [x] `services/consciousness/conversation_consciousness.py` (NEW)

### Wave 1 (Remaining)
- [ ] `services/ui_messages/loading_states.py`
- [ ] `services/ui_messages/user_friendly_errors.py`

### Wave 2
- [ ] `web/api/routes/standup.py` (formatters)
- [ ] `services/intent/intent_service.py` (response formatting)
- [ ] `cli/commands/standup.py`

### Wave 3
- [ ] `web/api/routes/todos.py` (API responses)
- [ ] `web/api/routes/lists.py` (API responses)
- [ ] `web/api/routes/files.py`
- [ ] `web/api/routes/projects.py`
- [ ] `web/api/routes/learning.py`

### Wave 4
- [ ] `services/integrations/slack/response_handler.py`
- [ ] `services/integrations/slack/reminder_formatter.py`
- [ ] `web/api/routes/auth.py`
- [ ] `web/api/routes/preferences.py`
- [ ] `templates/*.html` (22 files)

---

## Quick Wins (Low Effort, High Impact)

### 1. Loading States Enhancement
**File**: `services/ui_messages/loading_states.py`
**Effort**: 2 hours
**Impact**: Visible during every async operation

**Current**:
```python
LoadingState.STARTING: "Starting workflow execution..."
```

**After**:
```python
LoadingState.STARTING: "I'm starting the workflow now..."
```

### 2. Error Message Enhancement
**File**: `services/ui_messages/user_friendly_errors.py`
**Effort**: 2 hours
**Impact**: Shown on every error

**Current**:
```python
"Hmm, {message.lower()} {recovery}"
```

**After**:
```python
"I ran into something: {message.lower()}. Let me suggest: {recovery}. Does that help?"
```

### 3. CLI Print Methods
**File**: `cli/commands/standup.py`
**Effort**: 1 hour
**Impact**: Every CLI interaction

**Current**:
```python
def print_success(self, message: str):
    self.print_colored(f"✅ {message}", "green")
```

**After**:
```python
def print_success(self, message: str):
    self.print_colored(f"✅ {message}. What's next?", "green")
```

---

## Validation Checklist

### Before Release

- [ ] All transformed features score ≥13/20
- [ ] No dimension scores <2
- [ ] 100% MVC pass rate on automated validation
- [ ] Before/after documentation complete
- [ ] A/B test infrastructure ready
- [ ] Rollback procedure tested
- [ ] Feature flags configured

### After Release

- [ ] Monitor engagement metrics for 48 hours
- [ ] Review user feedback
- [ ] Check error rates
- [ ] Validate performance impact
- [ ] Conduct user interviews (sample of 5)

---

## Anti-Patterns to Avoid

### 1. Over-Consciousness
**Problem**: Making every message too verbose
**Solution**: Use consciousness for key moments, not every micro-interaction

### 2. Inconsistent Voice
**Problem**: "I" in some places, "Piper" in others, impersonal elsewhere
**Solution**: Always use "I" for Piper's voice

### 3. Fake Hedging
**Problem**: Adding "maybe" to facts (e.g., "You maybe have 5 todos")
**Solution**: Hedge on inferences, not facts

### 4. Empty Invitations
**Problem**: "What do you think?" after irrelevant information
**Solution**: Make invitations contextually meaningful

### 5. Source Fabrication
**Problem**: Claiming to have "checked" something that wasn't checked
**Solution**: Only attribute sources that were actually consulted

---

## Timeline

| Week | Wave | Focus | Deliverables |
|------|------|-------|--------------|
| 1 | Wave 1 | Todos, Conversations | ✅ Complete |
| 2 | Wave 1 | Loading, Errors | Wrappers + Integration |
| 3 | Wave 2 | Standup | Formatter enhancement |
| 4 | Wave 2 | Intent, CLI | Response wrapping |
| 5 | Wave 3 | Search, Files | API response wrappers |
| 6 | Wave 3 | Projects, Learning | API response wrappers |
| 7 | Wave 4 | Slack | Integration messages |
| 8 | Wave 4 | Auth, Templates | Final touches |

---

## Success Definition

**Phase 4 Complete When**:
1. ✅ Priority order documented
2. ✅ Implementation checklist created
3. ✅ A/B testing approach designed
4. ✅ Rollback strategy defined
5. ✅ Success metrics documented

**Full Rollout Complete When**:
1. All 22 output points transformed
2. Average rubric score ≥15/20
3. 100% MVC pass rate
4. Zero dimensions <2
5. User survey: 70%+ report "colleague" feeling

---

*Created as part of #407 MUX-VISION-STANDUP-EXTRACT Phase 4*
