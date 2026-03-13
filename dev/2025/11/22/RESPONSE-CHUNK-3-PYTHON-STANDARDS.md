# Python Code Standards Action Plan

**To**: Development Team + Chief Architect
**From**: Claude Code (research assistant)
**Re**: Ted Nadeau's Code Review Findings
**Date**: November 22, 2025

---

## Executive Summary

Ted's code review identified **6 categories of Python standards gaps** in Piper Morgan. This plan provides:
- Current state assessment (371 files, 563 functions analyzed)
- Prioritized remediation roadmap (Quick wins + foundational work)
- Effort estimates and success criteria
- Process improvements to prevent regression

**Key Finding**: Code quality is "very high" overall, but 5 specific discipline areas need systematic improvement.

---

## Current State Assessment

### Compliance Matrix

| Category | Status | Count | Severity | Quick Win |
|----------|--------|-------|----------|-----------|
| **Type Safety** (PEP 484) | 77% compliant | 22 dict→TypedDict | HIGH | 2-3h |
| **File Headers** | 0% compliant | 371 files | HIGH | 4-5h (top 10) |
| **Docstrings** (PEP 257) | 60-75% present | ~120 incomplete | MEDIUM | 1-2h (critical 5) |
| **Comments** | 0.5-2% density | ~300 files | MEDIUM | 10-15h (full sprint) |
| **Conditionals** (if/elif/else) | 55% explicit else | ~8 critical | LOW-MEDIUM | 1-2h |
| **Function Naming** | Generic names | 23 instances | LOW | 30-60 min |

---

## Detailed Findings

### 1. TYPE SAFETY (PEP 484) - HIGH PRIORITY

**Problem**: 22 functions return untyped `dict` instead of specific types

**Examples**:
```python
# BAD - Loses type information
def get_config() -> dict:
    return {"timeout": 30, "retries": 3}

# GOOD - Type-safe
class ConfigDict(TypedDict):
    timeout: int
    retries: int

def get_config() -> ConfigDict:
    return {"timeout": 30, "retries": 3}
```

**Files Affected** (Priority Order):
1. `services/config_validator.py:21` - ValidationResult dict
2. `services/personality/cache.py:113` - CacheStats dict
3. `services/infrastructure/errors/mcp_error_handler.py` (4 methods) - ErrorResponse dict
4. 19 more across integrations, domain, monitoring modules

**Impact**:
- ❌ IDE autocomplete broken for dict consumers
- ❌ Breaking changes undetected at type-check time
- ❌ `mypy` can't help
- ✅ Easy to fix (create TypedDict, update return type)

**Solution**:
1. Create 5 TypedDict definitions (2-3 hours)
2. Update 22 function signatures (1-2 hours)
3. Add to AGENTS.md guidelines

**Success Criteria**:
- ✅ All 22 functions have typed returns
- ✅ `mypy --strict` passes on core modules
- ✅ TypedDict patterns documented in code style guide

---

### 2. FILE HEADERS - HIGH PRIORITY (Quick Win)

**Problem**: 371 files (100%) lack proper headers

**Current State**:
```python
# services/ui_messages/action_humanizer.py
# File starts directly with imports
from typing import Optional
from ...
```

**Recommended Template**:
```python
"""
Module: services/ui_messages/action_humanizer.py
Purpose: Convert domain action objects to human-readable strings
Authors: [Claude Code agent], [list original authors]
Copyright: © 2025 Piper Morgan. Licensed under [LICENSE].

Key Classes:
  - ActionHumanizer: Main conversion logic

Key Functions:
  - humanize(action, category) -> str
"""
```

**Why It Matters**:
- Helps new readers understand file purpose in 30 seconds
- Documents authorship (important for code review accountability)
- Legal/compliance requirement (copyright tracking)
- Supports IDE tooltips and documentation generation

**Quick Win Target** (4-5 hours):
Add headers to 10 core services:
1. `services/intent_service/classifier.py`
2. `services/intent_service/canonical_handlers.py`
3. `services/slack/webhook_router.py`
4. `services/domain/models.py`
5. `services/llm/clients.py`
6. `services/auth/jwt_service.py`
7. `services/config.py`
8. `services/container/service_container.py`
9. `services/analytics/cost_estimator.py`
10. `services/integrations/github/github_integration_router.py`

Then roll out to remaining 361 files in phases.

**Success Criteria**:
- ✅ Top 10 files have complete headers
- ✅ Header template documented in AGENTS.md
- ✅ Pre-commit hook verifies new files have headers

---

### 3. DOCSTRINGS & COMMENTS (PEP 257) - MEDIUM PRIORITY

**Problem**: Docstrings often incomplete; Comments extremely sparse (0.5-2% density)

**Example of Current Gap**:
```python
async def humanize(self, action: str, category: Optional[str] = None) -> str:
    """Convert action to human-readable string."""  # ← Missing Args, Returns
    parts = action.split("_")
    if len(parts) == 2:
        # ...
    # No comments on logic, why these magic numbers exist, etc.
```

**Fixed Version**:
```python
async def humanize(self, action: str, category: Optional[str] = None) -> str:
    """Convert action to human-readable string.

    Transforms underscored action names into readable format for UI display.
    Example: "create_list" → "Create List"

    Args:
        action: Underscore-separated action name (e.g., "create_list")
        category: Optional category for context-specific formatting

    Returns:
        Human-readable action string suitable for UI labels

    Raises:
        ValueError: If action contains <2 parts (malformed)
    """
    parts = action.split("_")
    # Handle underscore-separated names: split on _ and format each part
    # This pattern matches our action naming convention in IntentHandler
    if len(parts) == 2:
        # Most common case: action only (no category)
        return " ".join(p.capitalize() for p in parts)
    elif len(parts) == 3:
        # Less common: category_action_subaction
        return " ".join(p.capitalize() for p in parts[1:])
    else:
        # Defensive: unknown format, log and return original
        logger.warning(f"Unexpected action format: {action}")
        return action.replace("_", " ")
```

**Missing Docstring Cases**:
- ~120 functions missing Args/Returns sections
- Complex logic lacking explanation
- Lazy imports unexplained
- Fallback strategies undocumented

**Quick Win Target** (1-2 hours):
Complete docstrings for 5 critical functions:
1. `intent_service/canonical_handlers.py:handle()`
2. `analysis/document_analyzer.py:analyze()`
3. `infrastructure/errors/mcp_error_handler.py:handle_mcp_error()`
4. `llm/clients.py:create_client()`
5. `config.py:load_config()`

**Full Remediation** (10-15 hours):
- Add Args/Returns to ~120 functions
- Add explanatory comments to complex logic
- Document non-obvious design choices
- Flag assumptions that should be confirmed

**Success Criteria**:
- ✅ All public functions have complete docstrings (Args, Returns, Raises)
- ✅ Complex functions (>15 lines) have explanatory comments
- ✅ Ratio of comments:code ≥ 5% (currently 0.5-2%)
- ✅ `docformatter` check passes

---

### 4. CONDITIONAL LOGIC COMPLETENESS - LOW-MEDIUM PRIORITY

**Problem**: ~8 functions have if/elif chains without explicit else clause

**Example Gap**:
```python
# RISKY - Falls through silently if len(parts) < 2
if len(parts) == 2:
    return fmt_two_part(parts)
elif len(parts) == 3:
    return fmt_three_part(parts)
elif len(parts) > 3:
    return fmt_many_part(parts)
# What if len(parts) == 1 or 0? Silent failure.
```

**Fixed Version**:
```python
# SAFE - Handles all cases
if len(parts) == 2:
    return fmt_two_part(parts)
elif len(parts) == 3:
    return fmt_three_part(parts)
elif len(parts) > 3:
    return fmt_many_part(parts)
else:
    # Handle edge case: malformed action
    logger.warning(f"Action has {len(parts)} parts, expected 2+: {action}")
    return action.replace("_", " ")  # Fallback to simple space replacement
```

**Alternative for Input Validation**:
```python
# Or prevent invalid inputs upfront with assertion
assert len(parts) >= 2, f"Action must have 2+ parts, got: {action}"
if len(parts) == 2:
    return fmt_two_part(parts)
# ... rest of logic
```

**Affected Functions** (8 total):
- Most in `intent_service`, `domain/models.py`, `config.py`

**Effort**: 1-2 hours (add else clauses + logging)

**Success Criteria**:
- ✅ All if/elif chains have else clause (explicit or assertion)
- ✅ Else clause logs unhandled case
- ✅ Assertion messages include context

---

### 5. FUNCTION NAMING - LOW PRIORITY

**Problem**: 23 instances of generic names like `decorator()`, `execute()`, `handle()`

**Critical Issue** (2 functions actually named "decorator"):
```python
# services/ui_messages/loading_states.py:417
def decorator(func):  # ← Too generic, what does it decorate?
    # ...

# Should be:
def time_execution_decorator(func):  # ← Clear purpose
    # ...
```

**Impact**: Low (standard patterns like handle/execute are acceptable in context)

**Effort**: 30-60 minutes to rename 2 critical "decorator" functions

**Success Criteria**:
- ✅ No function literally named "decorator"
- ✅ Generic names like "execute", "handle" are only in contexts where convention is clear

---

## Remediation Roadmap

### Phase 1: Quick Wins (2-3 Days)
**Time**: 8-10 hours
**Effort Level**: Easy
**Impact**: High

- [ ] Create 5 TypedDict definitions (2-3h)
- [ ] Update 22 function signatures (1-2h)
- [ ] Add headers to 10 core files (4-5h)
- [ ] Complete docstrings for 5 critical functions (1-2h)
- [ ] Rename 2 "decorator" functions (30 min)

**Outcome**: Quick wins completed, can declare "visible progress"

### Phase 2: Foundational Work (1-2 Weeks)
**Time**: 30-40 hours
**Effort Level**: Moderate
**Impact**: High

- [ ] Add headers to remaining 361 files (20-25h)
- [ ] Complete docstrings for ~120 more functions (8-12h)
- [ ] Fix 8 if/elif chains with else clauses (2-3h)
- [ ] Add explanatory comments to complex functions (5-8h)

**Outcome**: "Standards compliant" status achieved

### Phase 3: Continuous Improvement (Ongoing)
**Time**: 2-3 hours per month
**Effort Level**: Low (baked into review process)

- [ ] Pre-commit hooks enforce:
  - All new functions have return types
  - All new files have headers
  - All public functions have docstrings
- [ ] Code review checklist includes:
  - Docstring completeness (Args, Returns, Raises)
  - Comments on complex logic
  - Complete if/elif/else chains

**Outcome**: Standards maintained automatically going forward

---

## Implementation Strategy

### Who Does This?
- **Phase 1**: Any developer (good first task for new team members)
- **Phase 2**: Assign by service (intent_service, domain, integrations, etc.)
- **Phase 3**: Built into normal code review + pre-commit hooks

### How to Track?
- [ ] Create GitHub issues for each phase
- [ ] Use `beads` for fine-grained task tracking
- [ ] Metrics: "Files compliant" %, "Functions with complete docstrings" %

### How to Prevent Regression?
1. **Pre-commit hooks**:
   - `docformatter` checks PEP 257 compliance
   - `mypy --strict` checks type completeness
   - Custom hook checks for file headers

2. **Code review checklist**:
   - Docstrings with Args, Returns, Raises?
   - Comments on non-obvious logic?
   - If/elif/else completeness?

3. **AGENTS.md Updates**:
   - Document Python code style requirements
   - Link to examples (good/bad)
   - Provide templates for headers, docstrings

---

## Success Metrics

**Short-term** (2 weeks):
- ✅ Phase 1 complete: Quick wins visible
- ✅ Team familiar with new standards
- ✅ First 50 files compliant

**Medium-term** (4 weeks):
- ✅ 90% of files have proper headers
- ✅ All public functions have complete docstrings
- ✅ Type safety at 95%+
- ✅ Pre-commit hooks in place

**Long-term** (ongoing):
- ✅ 100% of new code meets standards
- ✅ Automated enforcement prevents regression
- ✅ Code reviews consistently check standards

---

## Ted's Feedback - Acknowledgment

**What Ted Praised**:
> "Generally looks of high quality. (even very high)"

**What Needs Improvement** (this plan addresses):
1. ✅ Type hints for return types → TypedDict pattern
2. ✅ File headers → Template provided
3. ✅ Docstrings (PEP 257) → Checklist for completeness
4. ✅ Comments → Explicit targets (0.5% → 5%+)
5. ✅ Generic function names → Rename checklist
6. ✅ Incomplete if/elif logic → Assertion strategy

**Our Response**: Not reactive patches, but systematic improvement with measurement and prevention.

---

## Appendix: Quick Reference

### TypedDict Template
```python
from typing import TypedDict

class MyDictType(TypedDict):
    """Type definition for my_function returns."""
    field1: str
    field2: int
    field3: bool | None  # Optional
```

### File Header Template
```python
"""
Module: services/my_service/module.py
Purpose: [Brief description of what this module does]
Authors: [Original authors], [Claude Code]
Copyright: © 2025 Piper Morgan. Licensed under MIT.

Key Classes:
  - MyClass: [Brief description]

Key Functions:
  - my_function: [Brief description]
"""
```

### Docstring Template
```python
def my_function(arg1: str, arg2: int = None) -> MyReturnType:
    """[Brief description - one line].

    [Extended description if needed - explain what it does
     and why it exists, edge cases, special behaviors].

    Args:
        arg1: Description of arg1
        arg2: Description of arg2, defaults to None

    Returns:
        MyReturnType: Description of return value

    Raises:
        ValueError: If arg1 is empty
        TypeError: If arg2 is not int or None

    Example:
        >>> my_function("test", 42)
        MyReturnType(...)
    """
```

---

**Claude Code (research assistant)**
For: Development Team + Chief Architect
Date: Nov 22, 2025
