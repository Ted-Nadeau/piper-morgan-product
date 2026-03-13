# Phase 0: CORE-LEARN-B Discovery - Pattern Recognition Infrastructure Survey

**Agent**: Cursor (Chief Architect)
**Issue**: #222 CORE-LEARN-B - Pattern Recognition
**Sprint**: A5 - Learning System
**Phase**: 0 - Discovery & Assessment
**Date**: October 20, 2025, 12:38 PM
**Duration**: 4-10 minutes (based on CORE-LEARN-A pattern)

---

## CRITICAL CONTEXT

**CORE-LEARN-A Pattern**: 90% infrastructure existed, 4-minute discovery, 1h 20min implementation!

**Expected for CORE-LEARN-B**:
- Pattern recognition service found in CORE-LEARN-A discovery (543 lines)
- QueryLearningLoop likely has pattern detection (610 lines)
- Similar high leverage pattern expected
- Fast discovery + wiring approach

**Previous Discovery** (CORE-LEARN-A findings):
- PatternRecognitionService exists (543 lines)
- QueryLearningLoop exists (610 lines) with pattern learning
- Knowledge infrastructure exists (2,994 lines)
- Privacy-compliant design already in place

**New Focus**: Pattern TYPES - temporal, workflow, communication, error patterns

---

## Mission

**FIND EXISTING PATTERN RECOGNITION INFRASTRUCTURE!** Then assess:
1. What pattern types already exist
2. What pattern detection logic is present
3. What confidence scoring exists
4. What visualization/reporting exists
5. What needs to be added vs wired

**DO NOT IMPLEMENT** - Just discover, assess, document!

---

## Discovery Process

### Step 1: Find Pattern Recognition Code (5 minutes)

**Search for existing pattern services** (found in CORE-LEARN-A):

```bash
# We know these exist from CORE-LEARN-A:
ls -la services/knowledge/pattern_recognition_service.py  # 543 lines
ls -la services/learning/query_learning_loop.py  # 610 lines

# Check what's inside them
head -100 services/knowledge/pattern_recognition_service.py
head -100 services/learning/query_learning_loop.py
```

**Use Serena MCP for pattern type search**:

```python
# Search for pattern types
mcp__serena__search_project("temporal.*pattern|workflow.*pattern|communication.*pattern|error.*pattern", file_pattern="services/**/*.py")

# Search for confidence scoring
mcp__serena__search_project("confidence.*score|pattern.*confidence|confidence.*threshold", file_pattern="services/**/*.py")

# Search for pattern detection methods
mcp__serena__find_symbol("detect_pattern|recognize_pattern|identify_pattern|pattern_type", scope="services")

# Search for pattern models
mcp__serena__search_project("PatternType|TemporalPattern|WorkflowPattern|CommunicationPattern", file_pattern="models/**/*.py")
```

**Look for pattern visualization**:

```bash
# Search for reporting/visualization
grep -r "pattern.*report\|pattern.*visual\|pattern.*display" services/ --include="*.py"

# Search for analytics
grep -r "pattern.*analytics\|pattern.*stats\|pattern.*metrics" services/ --include="*.py"
```

---

### Step 2: Assess Pattern Types (3 minutes)

**Required Pattern Types** (from issue #222):

1. **Temporal Patterns** ⏰
   - Time-of-day preferences
   - Day-of-week patterns
   - Recurring tasks
   - Example: "User creates standups every Monday at 9am"

2. **Workflow Patterns** 🔄
   - Common command sequences
   - Frequently used parameters
   - Integration preferences
   - Example: "User always adds label 'bug' to GitHub issues"

3. **Communication Patterns** 💬
   - Preferred response length
   - Formality level
   - Detail preferences
   - Example: "User prefers bullet points over paragraphs"

4. **Error Patterns** ⚠️
   - Common mistakes
   - Retry patterns
   - Correction preferences
   - Example: "User often forgets to specify repo"

**For each pattern type, document**:

```markdown
### [Pattern Type Name]

**Status**:
- [ ] Exists and complete
- [ ] Exists but incomplete
- [ ] Partially exists (needs extension)
- [ ] Missing - needs creation

**Found in**: [file path and line range]

**Current Capabilities**:
- Feature 1
- Feature 2

**Missing Capabilities**:
- Need 1
- Need 2

**Work Required**: [estimate]
```

---

### Step 3: Assess Confidence Scoring (2 minutes)

**Look for existing confidence mechanisms**:

```python
# Search for confidence scoring
mcp__serena__search_project("confidence|score|threshold|probability", file_pattern="services/learning/**/*.py")

# Check QueryLearningLoop for confidence tracking
grep -A 20 "confidence" services/learning/query_learning_loop.py
```

**Document**:
- Does confidence scoring exist?
- How is confidence calculated?
- What thresholds are used?
- Is confidence tracked per pattern?

---

### Step 4: Assess Observation Requirements (2 minutes)

**Requirement**: "Minimum 10 observations before pattern confirmed"

**Look for observation tracking**:

```python
# Search for observation/sample counting
mcp__serena__search_project("observation|sample.*count|frequency|occurrence", file_pattern="services/learning/**/*.py")

# Check for threshold logic
grep -r "min.*observation\|minimum.*sample\|threshold.*count" services/learning/
```

**Document**:
- Does observation counting exist?
- What are current thresholds?
- How are observations tracked?

---

### Step 5: Assess Visualization/Reporting (2 minutes)

**Requirement**: "Pattern visualization/reporting"

**Look for reporting capabilities**:

```python
# Search for reporting/analytics
mcp__serena__search_project("report|analytics|visualize|display|summary", file_pattern="services/learning/**/*.py")

# Check API endpoints from CORE-LEARN-A
cat web/api/routes/learning.py | grep -A 10 "analytics\|report\|stats"
```

**Document**:
- What reporting exists?
- What visualization exists?
- What needs to be added?

---

### Step 6: Gap Analysis (3 minutes)

**Compare requirements vs existing infrastructure**:

**Required** (from issue #222):
- [ ] Identifies 5+ pattern types
- [ ] Pattern confidence scoring
- [ ] Pattern visualization/reporting
- [ ] Minimum 10 observations before pattern confirmed
- [ ] Tests for each pattern type

**For each item**: Mark as ✅ Exists / ⚠️ Partial / ❌ Missing

---

## Deliverable: Discovery Report

**File**: `dev/2025/10/20/core-learn-b-discovery-report.md`

### Report Structure

```markdown
# CORE-LEARN-B Discovery Report

**Date**: October 20, 2025
**Agent**: Cursor (Chief Architect)
**Issue**: #222
**Duration**: [X] minutes

---

## Executive Summary

[What exists, what's missing, leverage ratio, revised estimate]

---

## Component Inventory

### PatternRecognitionService (543 lines)

**Status**: [Assessment]

**Current Capabilities**:
- [List what it does]

**Pattern Types Supported**:
- [List which of 4 types exist]

**Missing Capabilities**:
- [List gaps]

**Work Required**: [estimate]

---

### QueryLearningLoop (610 lines)

**Status**: [Assessment]

**Current Pattern Detection**:
- [What patterns it detects]

**Confidence Scoring**:
- [Does it exist? How does it work?]

**Observation Tracking**:
- [Does it track observation counts?]

**Work Required**: [estimate]

---

## Pattern Type Assessment

### 1. Temporal Patterns ⏰

**Status**: [Exists / Partial / Missing]
**Found in**: [file:line]
**Capabilities**: [what works]
**Gaps**: [what's missing]
**Estimate**: [hours]

### 2. Workflow Patterns 🔄

**Status**: [Exists / Partial / Missing]
**Found in**: [file:line]
**Capabilities**: [what works]
**Gaps**: [what's missing]
**Estimate**: [hours]

### 3. Communication Patterns 💬

**Status**: [Exists / Partial / Missing]
**Found in**: [file:line]
**Capabilities**: [what works]
**Gaps**: [what's missing]
**Estimate**: [hours]

### 4. Error Patterns ⚠️

**Status**: [Exists / Partial / Missing]
**Found in**: [file:line]
**Capabilities**: [what works]
**Gaps**: [what's missing]
**Estimate**: [hours]

### 5. Additional Pattern Types

[Any other pattern types found that aren't in the 4 required]

---

## Feature Assessment

### Confidence Scoring

**Status**: [Exists / Partial / Missing]
**Current Implementation**: [description]
**Gaps**: [what's needed]
**Estimate**: [hours]

### Observation Threshold (10+ required)

**Status**: [Exists / Partial / Missing]
**Current Implementation**: [description]
**Threshold**: [current value]
**Gaps**: [what's needed]
**Estimate**: [hours]

### Visualization/Reporting

**Status**: [Exists / Partial / Missing]
**Current Capabilities**: [what exists]
**Gaps**: [what's needed]
**Estimate**: [hours]

### Testing

**Existing Tests**: [file locations]
**Test Coverage**: [assessment]
**Gaps**: [tests needed]
**Estimate**: [hours]

---

## Integration Opportunities

### API Endpoints (from CORE-LEARN-A)

**Existing** (web/api/routes/learning.py):
- GET /patterns (can this filter by type?)
- GET /analytics (does this show pattern breakdowns?)

**Needed**:
- [Additional endpoints for pattern-specific queries]

**Estimate**: [hours]

### User Preferences (from CORE-LEARN-A)

**Existing** (UserPreferenceManager):
- learning_enabled
- learning_min_confidence
- learning_features

**Could Add**:
- pattern_types_enabled (List[str])
- pattern_min_observations (int)

**Estimate**: [hours]

---

## Leverage Analysis

**Existing Code**:
- PatternRecognitionService: 543 lines
- QueryLearningLoop: 610 lines
- Knowledge Infrastructure: 2,994 lines
- API Routes (CORE-LEARN-A): 538 lines
- User Preferences (CORE-LEARN-A): 114 lines
- **Total existing**: [X] lines

**New Code Needed**:
- Pattern type implementations: [X] lines
- Confidence enhancements: [X] lines
- Visualization/reporting: [X] lines
- Tests: [X] lines
- **Total new**: [Y] lines

**Leverage Ratio**: [X:Y] (existing:new)

---

## Revised Implementation Plan

**Original Estimate**: [from gameplan]

**Revised Breakdown**:

**Phase 1: Pattern Types** ([X] hours)
- Temporal patterns: [estimate]
- Workflow patterns: [estimate]
- Communication patterns: [estimate]
- Error patterns: [estimate]

**Phase 2: Features** ([X] hours)
- Confidence scoring: [estimate]
- Observation thresholds: [estimate]
- Visualization/reporting: [estimate]

**Phase 3: Testing** ([X] hours)
- Pattern type tests: [estimate]
- Integration tests: [estimate]

**Total Revised**: [X] hours (vs [Y] hours gameplan)
**Confidence**: [High/Medium/Low]

---

## Recommendations

### Approach

1. [First priority]
2. [Second priority]
3. [Third priority]

### Quick Wins

[Things that are nearly complete and easy to finish]

### Risks

- [Risk 1 and mitigation]
- [Risk 2 and mitigation]

---

## Next Steps

**Immediate**:
1. [First action for Code agent]
2. [Second action]

**Then**:
- [Follow-up actions]

---

_Discovery complete - ready for implementation!_
```

---

## Search Strategy Summary

**Phase 1: Known Services** (from CORE-LEARN-A)
```bash
# Examine existing services
services/knowledge/pattern_recognition_service.py  # 543 lines - what does it do?
services/learning/query_learning_loop.py  # 610 lines - what patterns does it learn?
```

**Phase 2: Pattern Type Search** (Serena MCP)
```python
# Find pattern type implementations
mcp__serena__search_project("temporal|workflow|communication|error", file_pattern="services/**/*.py")
mcp__serena__find_symbol("TemporalPattern|WorkflowPattern|CommunicationPattern|ErrorPattern")
```

**Phase 3: Feature Search**
```python
# Confidence scoring
mcp__serena__search_project("confidence.*scor|pattern.*confidence")

# Observation tracking
mcp__serena__search_project("observation.*count|min.*observation|threshold")

# Visualization
mcp__serena__search_project("visualiz|report|analytics|display")
```

**Phase 4: Test Search**
```bash
# Find existing tests
find tests/ -name "*pattern*" -o -name "*learning*"
grep -r "test.*pattern\|pattern.*test" tests/
```

---

## Success Criteria

Discovery is complete when you can answer:

1. **What pattern types exist?**
   - [ ] Which of 4 required types are implemented?
   - [ ] What additional types exist?
   - [ ] What's the completeness of each?

2. **What features exist?**
   - [ ] Confidence scoring present?
   - [ ] Observation thresholds present?
   - [ ] Visualization/reporting present?

3. **What's the leverage ratio?**
   - [ ] How much existing code?
   - [ ] How much new code needed?
   - [ ] What's the ratio?

4. **What's the real estimate?**
   - [ ] Revised time estimates by phase
   - [ ] Confidence level in estimates
   - [ ] Risk assessment

---

## Expected Findings (Hypothesis)

Based on CORE-LEARN-A pattern:

**Likely to find** (75-90% infrastructure):
- ✅ Pattern recognition service exists
- ✅ Some pattern types implemented
- ✅ Confidence scoring exists
- ✅ Basic observation tracking
- ⚠️ May need pattern type extensions
- ⚠️ Visualization may be basic
- ⚠️ Tests may need extension

**Unlikely to find**:
- ❌ All 4 pattern types complete
- ❌ Full visualization dashboard
- ❌ Complete test coverage

**Similar to CORE-LEARN-A**: Discover → Assess → Wire → Build gaps

---

## Time Tracking

**Start Time**: 12:38 PM
**Target Duration**: 4-10 minutes (based on CORE-LEARN-A)
**Target Completion**: 12:42-12:48 PM

**Stay focused!** Quick discovery, thorough assessment, clear recommendations.

---

## Remember

**YOU ARE DISCOVERING, NOT IMPLEMENTING!**

- ✅ Find existing pattern code
- ✅ Assess pattern types
- ✅ Check features (confidence, observations, visualization)
- ✅ Document findings
- ✅ Revise estimates
- ❌ Don't implement patterns
- ❌ Don't create tests
- ❌ Don't build features

**Save implementation for Code agent after discovery!**

---

**Ready to find the pattern recognition infrastructure!** 🔍

*CORE-LEARN-A showed 90% existed in 4 minutes. Let's see what CORE-LEARN-B reveals!*
