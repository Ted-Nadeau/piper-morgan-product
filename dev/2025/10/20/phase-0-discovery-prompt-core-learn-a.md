# Phase 0: CORE-LEARN-A Discovery - Learning System Infrastructure Survey

**Agent**: Cursor (Chief Architect)
**Issue**: #221 CORE-LEARN-A - Learning Infrastructure Foundation
**Sprint**: A5 - Learning System
**Phase**: 0 - Discovery & Assessment
**Date**: October 20, 2025, 10:48 AM
**Duration**: 30-45 minutes

---

## CRITICAL CONTEXT

**PM Insight**: "I know we built a learning system in the early days and never wired it up. It may not be fully DDD compliant or finished but we should expect that 75% pattern to hold."

**Historical Pattern** (from Sprint A4):
- Reminder system: 95% infrastructure existed
- Just needed wiring + integration
- 30 min discovery saved 5+ hours
- Discovery phase was CRITICAL

**Expected for Learning System**:
- ~75% likely exists but unwired
- May need DDD compliance updates
- May need integration with current architecture
- Discovery will reveal what's salvageable vs what needs rebuilding

---

## Mission

**FIND THE LEARNING SYSTEM!** Then assess:
1. What exists and where
2. What's salvageable vs needs rebuild
3. What's missing from gameplan requirements
4. How to integrate with current DDD architecture
5. Revised time estimates based on findings

**DO NOT IMPLEMENT** - Just discover, assess, document!

---

## Discovery Process

### Step 1: Find Learning Components (15 minutes)

**Search for learning services**:
```bash
# Look for learning-related services
find . -type f -name "*learn*.py" -not -path "*/node_modules/*" -not -path "*/.venv/*"
find . -type f -name "*pattern*.py" -not -path "*/node_modules/*" -not -path "*/.venv/*"
find . -type f -name "*preference*.py" -not -path "*/node_modules/*" -not -path "*/.venv/*"
find . -type f -name "*workflow*.py" -not -path "*/node_modules/*" -not -path "*/.venv/*"
```

**Use Serena MCP for deep search**:
```python
# Search project for learning keywords
mcp__serena__search_project("learning|pattern|preference|workflow", file_pattern="services/**/*.py")

# Look for learning models
mcp__serena__search_project("UserPattern|WorkflowPattern|LearningData", file_pattern="models/**/*.py")

# Find learning-related classes
mcp__serena__find_symbol("PatternRecognizer|PreferenceTracker|LearningService|WorkflowOptimizer", scope="services")
```

**Expected locations**:
- `services/learning/` (if it exists)
- `services/pattern/` (alternative naming)
- `services/domain/` (might be integrated)
- `handlers/` (might have learning handlers)

---

### Step 2: Assess What Exists (10 minutes)

For each discovered component, document:

**Component Assessment Template**:
```markdown
### [Component Name] - [File Path]

**Status**:
- [ ] Exists and complete
- [ ] Exists but incomplete
- [ ] Exists but needs DDD compliance
- [ ] Missing - needs creation

**Lines of Code**: [X] lines

**Key Features**:
- Feature 1
- Feature 2
- Feature 3

**Integration Status**:
- [ ] Wired into main application
- [ ] Has tests
- [ ] Has API endpoints
- [ ] Connected to storage
- [ ] Privacy-compliant

**DDD Compliance**:
- [ ] Domain service structure
- [ ] Repository pattern
- [ ] Entity/Value objects
- [ ] Follows current patterns

**Salvageable**: [Yes/No/Partial]
**Work Required**: [None/Minor/Moderate/Major/Rebuild]
**Estimate**: [X hours]

**Notes**:
- Key observations
- Integration challenges
- Recommendations
```

---

### Step 3: Gap Analysis (10 minutes)

**Compare gameplan requirements vs what exists**:

**Required Components** (from gameplan):

1. **Learning Service Framework**:
   - [ ] `services/learning/learning_service.py` - Core service
   - [ ] `services/learning/pattern_recognizer.py` - Pattern detection
   - [ ] `services/learning/preference_tracker.py` - User preferences
   - [ ] `services/learning/workflow_optimizer.py` - Optimization engine

2. **Data Models**:
   - [ ] `services/learning/models/user_pattern.py`
   - [ ] `services/learning/models/workflow_pattern.py`
   - [ ] `services/learning/models/optimization_rule.py`

3. **Storage Layer**:
   - [ ] Pattern storage (SQLite/JSON)
   - [ ] Preference persistence
   - [ ] Privacy-compliant design
   - [ ] Anonymization utilities

4. **Learning Loop**:
   - [ ] Action observer
   - [ ] Pattern detection pipeline
   - [ ] API endpoints

5. **Integration Points**:
   - [ ] UserPreferenceManager integration (from A4)
   - [ ] Privacy utilities (from ethics work)
   - [ ] Application startup wiring
   - [ ] API router registration

**For each item**: Mark as "Exists", "Partial", or "Missing"

---

### Step 4: Integration Assessment (5 minutes)

**Check existing integration points**:

**UserPreferenceManager** (extended in Sprint A4):
```bash
# Find UserPreferenceManager
grep -r "UserPreferenceManager" services/domain/

# Check what preferences exist
grep -r "set_.*preference\|get_.*preference" services/domain/user_preference_manager.py
```

**Privacy Utilities** (from ethics implementation):
```bash
# Find privacy/anonymization code
find . -type f -name "*privacy*.py" -o -name "*anonymize*.py" -o -name "*compliance*.py"

# Search for privacy-related functions
grep -r "anonymize\|remove_pii\|privacy_compliant" services/
```

**Application Startup** (where to wire in):
```bash
# Check main.py for service initialization
grep -r "service.*init\|start.*service" main.py

# Check for dependency injection setup
grep -r "get_.*service\|provide_.*service" services/
```

---

### Step 5: Revised Estimates (5 minutes)

**Calculate work required**:

**For each component**, estimate:
- **Exists & ready**: 0 hours
- **Exists, needs minor updates**: 0.5 hours
- **Exists, needs DDD compliance**: 1-2 hours
- **Exists, needs major refactor**: 2-4 hours
- **Missing, needs creation**: From gameplan estimates

**Total revised estimate**: Sum of all components

**Confidence level**: Based on findings
- High: 75%+ exists and salvageable
- Medium: 50-75% exists
- Low: <50% exists

---

## Deliverable: Discovery Report

**File**: `dev/2025/10/20/core-learn-a-discovery-report.md`

### Report Structure

```markdown
# CORE-LEARN-A Discovery Report

**Date**: October 20, 2025
**Agent**: Cursor (Chief Architect)
**Issue**: #221
**Duration**: [X] minutes

---

## Executive Summary

[2-3 sentences: What exists, what's missing, revised estimate]

---

## Component Inventory

### Existing Components

[For each found component, use assessment template]

### Missing Components

[List components that need creation]

---

## Integration Opportunities

### UserPreferenceManager Integration
[Assessment of how to leverage A4 work]

### Privacy Utilities Integration
[Assessment of existing privacy code]

### Application Wiring
[Where and how to wire in learning system]

---

## DDD Compliance Assessment

**Current State**:
- [Observations about architectural compliance]

**Required Updates**:
- [List of DDD updates needed]

**Effort Estimate**: [X] hours

---

## Gap Analysis

### What We Have
- [List of salvageable components]
- [Line counts and status]

### What We Need
- [Missing components from gameplan]
- [Required new development]

### Leverage Ratio
- Existing: [X]%
- New: [Y]%
- Ratio: [X:Y]

---

## Revised Implementation Plan

**Original Estimate**: 2-3 days (16-24 hours)

**Revised Breakdown**:

**Phase 1: Core Services** ([X] hours)
- Component A: [X]h (exists, needs [work])
- Component B: [X]h (missing, create)
- [etc.]

**Phase 2: Storage Layer** ([X] hours)
- [Breakdown]

**Phase 3: Learning Loop** ([X] hours)
- [Breakdown]

**Phase 4: Testing** ([X] hours)
- [Breakdown]

**Total Revised**: [X] hours (vs 8-10 hours gameplan)
**Confidence**: [High/Medium/Low]

---

## Recommendations

### Approach
1. [Strategic recommendation #1]
2. [Strategic recommendation #2]
3. [Strategic recommendation #3]

### Priorities
1. [What to do first]
2. [What to do second]
3. [What to defer]

### Risks
- [Risk 1 and mitigation]
- [Risk 2 and mitigation]

---

## Next Steps

**Immediate**:
1. [First action]
2. [Second action]

**Then**:
- [Follow-up actions]

---

_Discovery complete, ready for implementation!_
```

---

## Search Commands Reference

**For Cursor to use**:

### File System Searches
```bash
# Find all learning-related files
find . -type f \( -name "*learn*.py" -o -name "*pattern*.py" -o -name "*preference*.py" \) -not -path "*/node_modules/*" -not -path "*/.venv/*" | head -20

# Search for specific classes
grep -r "class.*Learning\|class.*Pattern\|class.*Preference" services/ --include="*.py" | head -20

# Find model definitions
grep -r "class.*Pattern\|@dataclass" models/ --include="*.py" | head -20

# Check for storage implementations
find . -type f -name "*storage*.py" -o -name "*repository*.py" | grep -i learn
```

### Serena MCP Searches
```python
# Comprehensive learning search
mcp__serena__search_project("learning|pattern|preference|workflow|optimize", file_pattern="**/*.py", max_results=50)

# Find learning models
mcp__serena__search_project("UserPattern|WorkflowPattern|LearningData|PatternType", file_pattern="models/**/*.py")

# Find learning services
mcp__serena__find_symbol("LearningService|PatternRecognizer|PreferenceTracker|WorkflowOptimizer", scope="services")

# Check for privacy utilities
mcp__serena__search_project("anonymize|privacy|pii|compliant", file_pattern="services/**/*.py")
```

### Code Analysis
```bash
# Count lines in discovered files
wc -l services/learning/*.py 2>/dev/null || echo "No learning service found"

# Check for tests
find tests/ -type f -name "*learn*.py" -o -name "*pattern*.py"

# Check API endpoints
grep -r "@router\|@app\|@api" web/ --include="*.py" | grep -i "learn\|pattern"
```

---

## Success Criteria

Discovery is complete when you can answer:

1. **What exists?**
   - [ ] Found all learning-related code
   - [ ] Assessed each component's status
   - [ ] Counted lines of code

2. **What's salvageable?**
   - [ ] Identified DDD compliance issues
   - [ ] Determined what needs updates vs rebuild
   - [ ] Found integration opportunities

3. **What's the real estimate?**
   - [ ] Revised time estimates based on findings
   - [ ] Identified leverage ratio (existing:new)
   - [ ] Set confidence level

4. **How do we proceed?**
   - [ ] Clear recommendations
   - [ ] Prioritized next steps
   - [ ] Risk mitigation strategies

---

## Remember

**YOU ARE DISCOVERING, NOT IMPLEMENTING!**

- ✅ Find code
- ✅ Assess status
- ✅ Document findings
- ✅ Revise estimates
- ❌ Don't implement
- ❌ Don't refactor
- ❌ Don't test

**Save implementation for Code agent after discovery!**

---

## Expected Findings (Hypothesis)

Based on PM's insight and Sprint A4 pattern:

**Likely to find**:
- ✅ ~75% of learning infrastructure
- ✅ Pattern recognition code (94 lines mentioned)
- ✅ Some models and data structures
- ✅ Basic storage implementation
- ⚠️ Not wired into main application
- ⚠️ May need DDD compliance updates
- ⚠️ Tests may be missing or outdated

**Unlikely to find**:
- ❌ Complete API endpoints
- ❌ Full integration with current architecture
- ❌ Privacy-compliant storage
- ❌ Recent updates (built in early days)

**This is the pattern from A4!** Discover → Wire → Test → Ship

---

## Time Tracking

**Start Time**: 10:48 AM
**Target Duration**: 30-45 minutes
**Target Completion**: 11:20-11:30 AM

**Stay focused!** Discovery only, then hand off to implementation.

---

**Ready to discover the hidden learning system!** 🔍

*Let's see what past-you built that present-you can leverage!*
