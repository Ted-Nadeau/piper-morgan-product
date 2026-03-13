# Phase 0: CORE-LEARN-C Discovery - Preference Learning Infrastructure Survey

**Agent**: Cursor (Chief Architect)
**Issue**: #223 CORE-LEARN-C - Preference Learning
**Sprint**: A5 - Learning System
**Phase**: 0 - Discovery & Assessment
**Date**: October 20, 2025, 1:20 PM
**Duration**: 4-10 minutes (based on CORE-LEARN-A/B pattern)

---

## CRITICAL CONTEXT

**PATTERN ESTABLISHED** (CORE-LEARN-A & B):
- 90-95% infrastructure exists
- 4-minute discoveries
- Simple extensions, not rebuilds
- Fast implementations (17 min to 1h 20min)

**Previous Discoveries**:
- **CORE-LEARN-A**: Found QueryLearningLoop (610 lines), learning API (538 lines), UserPreferenceManager (114 lines)
- **CORE-LEARN-B**: Found 8 pattern types, confidence scoring, observation tracking

**Expected for CORE-LEARN-C**: High likelihood that preference infrastructure exists from Sprint A4!

---

## Mission

**FIND EXISTING PREFERENCE LEARNING INFRASTRUCTURE!** Then assess:
1. What explicit preference storage exists
2. What implicit preference derivation exists
3. What conflict resolution exists
4. What preference API exists
5. What privacy controls exist
6. What needs to be added vs wired

**DO NOT IMPLEMENT** - Just discover, assess, document!

---

## Discovery Process

### Step 1: Find Preference Infrastructure (5 minutes)

**Known starting points** (from CORE-LEARN-A):

```bash
# We know UserPreferenceManager exists from CORE-LEARN-A
ls -la services/domain/user_preference_manager.py  # 114 lines + CORE-LEARN-A additions

# Check what's inside
cat services/domain/user_preference_manager.py

# Look for preference-related services
ls -la services/*preference* services/*/*preference*
```

**Use Serena MCP for preference search**:

```python
# Search for preference storage/learning
mcp__serena__search_project("preference.*learning|learn.*preference|derive.*preference|infer.*preference", file_pattern="services/**/*.py")

# Search for explicit vs implicit preference handling
mcp__serena__search_project("explicit.*preference|implicit.*preference|stated.*preference|derived.*preference", file_pattern="services/**/*.py")

# Search for conflict resolution
mcp__serena__find_symbol("resolve_conflict|preference_conflict|conflict_resolution", scope="services")

# Search for preference models
mcp__serena__search_project("PreferenceModel|UserPreference|PreferenceData", file_pattern="models/**/*.py")
```

**Look for preference API**:

```bash
# Check if preference endpoints exist
grep -r "preference" web/api/routes/ --include="*.py"

# Look for preference handlers
grep -r "get_preference\|set_preference\|update_preference" services/ --include="*.py"
```

---

### Step 2: Assess Explicit Preferences (3 minutes)

**Requirement**: User-stated preferences, configuration choices, direct feedback

**Search for explicit preference storage**:

```python
# Find preference storage mechanisms
mcp__serena__search_project("store.*preference|save.*preference|persist.*preference", file_pattern="services/**/*.py")

# Check UserPreferenceManager from CORE-LEARN-A
grep -A 20 "class UserPreferenceManager" services/domain/user_preference_manager.py

# Look for preference keys/configuration
grep -r "preference.*key\|preference.*config" services/ models/
```

**Document**:
```markdown
### Explicit Preferences

**Status**:
- [ ] Exists and complete
- [ ] Exists but incomplete
- [ ] Partially exists (needs extension)
- [ ] Missing - needs creation

**Found in**: [file path and line range]

**Current Capabilities**:
- User-stated preferences
- Configuration storage
- Direct feedback handling

**Missing Capabilities**:
- [List gaps]

**Work Required**: [estimate]
```

---

### Step 3: Assess Implicit Preferences (3 minutes)

**Requirement**: Derived from behavior, inferred from patterns, statistical analysis

**Search for implicit preference derivation**:

```python
# Find pattern-to-preference logic
mcp__serena__search_project("derive.*from.*pattern|infer.*from.*behavior|statistical.*preference", file_pattern="services/**/*.py")

# Check if QueryLearningLoop does implicit learning
grep -A 30 "learn_pattern\|detect_pattern" services/learning/query_learning_loop.py

# Look for behavior analysis
mcp__serena__search_project("analyze.*behavior|user.*behavior|behavior.*pattern", file_pattern="services/**/*.py")
```

**Document**:
```markdown
### Implicit Preferences

**Status**: [Exists / Partial / Missing]
**Found in**: [file path]

**Current Capabilities**:
- Derived from patterns
- Inferred from behavior
- Statistical analysis

**Missing Capabilities**:
- [List gaps]

**Work Required**: [estimate]
```

---

### Step 4: Assess Conflict Resolution (2 minutes)

**Requirement**: Resolution strategy (Explicit > Implicit, Recent > Historical, Context-aware)

**Search for conflict resolution**:

```python
# Find conflict resolution logic
mcp__serena__search_project("resolve.*conflict|preference.*priority|explicit.*implicit", file_pattern="services/**/*.py")

# Look for precedence rules
grep -r "precedence\|priority\|override" services/*preference* --include="*.py"
```

**Document**:
```markdown
### Conflict Resolution

**Status**: [Exists / Partial / Missing]
**Found in**: [file path]

**Current Strategy**:
- Explicit > Implicit priority
- Recent > Historical priority
- Context-aware resolution

**Missing Capabilities**:
- [List gaps]

**Work Required**: [estimate]
```

---

### Step 5: Assess Preference API (2 minutes)

**Requirement**: API to get/set/apply preferences

**Search for preference API**:

```python
# Check existing API routes
cat web/api/routes/learning.py | grep -A 10 "preference"

# Look for preference service methods
mcp__serena__find_symbol("get_preferences|set_preferences|apply_preferences", scope="services")

# Check if UserPreferenceManager has API
grep -A 20 "def get\|def set\|def update" services/domain/user_preference_manager.py
```

**Document**:
```markdown
### Preference API

**Status**: [Exists / Partial / Missing]
**Found in**: [file paths]

**Current Endpoints/Methods**:
- get_preferences(user_id)
- set_preference(key, value)
- apply_to_response(data, preferences)

**Missing Capabilities**:
- [List gaps]

**Work Required**: [estimate]
```

---

### Step 6: Assess Privacy Controls (2 minutes)

**Requirement**: Privacy controls for preference data

**Search for privacy mechanisms**:

```python
# Find privacy controls
mcp__serena__search_project("privacy.*preference|preference.*privacy|pii.*preference", file_pattern="services/**/*.py")

# Check existing privacy infrastructure (from CORE-LEARN-A)
grep -r "privacy\|anonymize\|sanitize" services/learning/ services/knowledge/
```

**Document**:
```markdown
### Privacy Controls

**Status**: [Exists / Partial / Missing]
**Found in**: [file paths]

**Current Controls**:
- PII filtering
- Data anonymization
- User consent tracking
- Data retention policies

**Missing Controls**:
- [List gaps]

**Work Required**: [estimate]
```

---

### Step 7: Gap Analysis (3 minutes)

**Compare requirements vs existing infrastructure**:

**Required** (from issue #223):
- [ ] Stores explicit preferences
- [ ] Derives implicit preferences
- [ ] Resolves conflicts consistently
- [ ] Preferences affect system behavior
- [ ] Privacy controls for preference data

**For each item**: Mark as ✅ Exists / ⚠️ Partial / ❌ Missing

---

## Deliverable: Discovery Report

**File**: `dev/2025/10/20/core-learn-c-discovery-report.md`

### Report Structure

```markdown
# CORE-LEARN-C Discovery Report

**Date**: October 20, 2025
**Agent**: Cursor (Chief Architect)
**Issue**: #223
**Duration**: [X] minutes

---

## Executive Summary

[What exists, what's missing, leverage ratio, revised estimate]

**Key Finding**: [90-95% exists / 50-75% exists / mostly missing]

---

## Component Inventory

### UserPreferenceManager (from CORE-LEARN-A)

**Status**: [Assessment]
**Current Lines**: 114 lines + CORE-LEARN-A additions

**Current Capabilities**:
- [List what it does]
- [List preference types supported]
- [List storage mechanisms]

**Missing Capabilities**:
- [List gaps]

**Work Required**: [estimate]

---

### PreferenceLearningService (if exists)

**Status**: [Found / Not found]
**Found in**: [file:line]

**Current Capabilities**:
- [What exists]

**Missing Capabilities**:
- [What's needed]

**Work Required**: [estimate]

---

## Feature Assessment

### 1. Explicit Preferences

**Status**: [Exists / Partial / Missing]
**Found in**: [file:line]
**Capabilities**: [what works]
**Gaps**: [what's missing]
**Estimate**: [hours]

**Examples**:
- User-stated preferences (e.g., "I prefer concise responses")
- Configuration choices
- Direct feedback

### 2. Implicit Preferences

**Status**: [Exists / Partial / Missing]
**Found in**: [file:line]
**Capabilities**: [what works]
**Gaps**: [what's missing]
**Estimate**: [hours]

**Examples**:
- Derived from behavior (e.g., "User always chooses option A")
- Inferred from patterns
- Statistical analysis

### 3. Preference Conflicts

**Status**: [Exists / Partial / Missing]
**Found in**: [file:line]
**Capabilities**: [what works]
**Gaps**: [what's missing]
**Estimate**: [hours]

**Resolution Strategy**:
- Explicit > Implicit priority
- Recent > Historical priority
- Context-aware preferences

### 4. Preference API

**Status**: [Exists / Partial / Missing]
**Found in**: [file:line]
**Capabilities**: [what works]
**Gaps**: [what's missing]
**Estimate**: [hours]

**Example Usage**:
```python
# Get user preferences
preferences = learning_service.get_preferences(user_id)

# Apply to response
response = format_response(data, preferences)
```

### 5. Privacy Controls

**Status**: [Exists / Partial / Missing]
**Found in**: [file:line]
**Capabilities**: [what works]
**Gaps**: [what's missing]
**Estimate**: [hours]

**Controls Needed**:
- PII protection
- User consent
- Data anonymization
- Retention policies

---

## Integration Assessment

### With QueryLearningLoop (from CORE-LEARN-A)

**Connection**: [How preferences integrate with pattern learning]

**Opportunities**:
- Patterns can inform implicit preferences
- Preferences can guide pattern application
- Cross-feature preference learning

### With UserPreferenceManager (from CORE-LEARN-A)

**Current State**: [What UserPreferenceManager provides]

**Extension Needs**:
- [What needs to be added]

### With API Layer (from CORE-LEARN-A)

**Existing Endpoints**: [List relevant endpoints]

**New Endpoints Needed**: [List gaps]

---

## Leverage Analysis

**Existing Code**:
- UserPreferenceManager: 114+ lines (from CORE-LEARN-A)
- QueryLearningLoop: 610 lines (from CORE-LEARN-A)
- Pattern recognition: 543 lines (from CORE-LEARN-B)
- API layer: 511 lines (from CORE-LEARN-A)
- [Other components found]
- **Total existing**: [X] lines

**New Code Needed**:
- Implicit preference derivation: [X] lines
- Conflict resolution: [X] lines
- Privacy controls: [X] lines
- API extensions: [X] lines
- Tests: [X] lines
- **Total new**: [Y] lines

**Leverage Ratio**: [X:Y] (existing:new)

---

## Revised Implementation Plan

**Original Estimate**: [from gameplan]

**Revised Breakdown**:

**Phase 1: Explicit Preferences** ([X] hours)
- Storage mechanism: [estimate]
- API endpoints: [estimate]
- Tests: [estimate]

**Phase 2: Implicit Preferences** ([X] hours)
- Pattern-to-preference derivation: [estimate]
- Behavior analysis: [estimate]
- Statistical inference: [estimate]

**Phase 3: Conflict Resolution** ([X] hours)
- Priority system: [estimate]
- Context awareness: [estimate]
- Tests: [estimate]

**Phase 4: Privacy Controls** ([X] hours)
- PII filtering: [estimate]
- User controls: [estimate]
- Tests: [estimate]

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

_Discovery complete - ready for implementation planning!_
```

---

## Search Strategy Summary

**Phase 1: Known Services** (from CORE-LEARN-A)
```bash
# Check UserPreferenceManager
services/domain/user_preference_manager.py  # 114+ lines - what does it do?

# Check QueryLearningLoop for preference learning
services/learning/query_learning_loop.py  # 610 lines - does it learn preferences?
```

**Phase 2: Preference-Specific Search** (Serena MCP)
```python
# Find preference services
mcp__serena__search_project("preference.*learning|learn.*preference|derive.*preference")

# Find explicit/implicit handling
mcp__serena__search_project("explicit.*preference|implicit.*preference")

# Find conflict resolution
mcp__serena__find_symbol("resolve_conflict|preference_conflict")
```

**Phase 3: API Search**
```bash
# Check for preference endpoints
grep -r "preference" web/api/routes/ --include="*.py"

# Check for preference methods
grep -r "get_preference\|set_preference" services/ --include="*.py"
```

**Phase 4: Privacy Search**
```python
# Find privacy controls
mcp__serena__search_project("privacy.*preference|pii.*preference|anonymize.*preference")
```

---

## Success Criteria

Discovery is complete when you can answer:

1. **What preference storage exists?**
   - [ ] Explicit preference storage?
   - [ ] Implicit preference derivation?
   - [ ] Where are preferences stored?

2. **What preference features exist?**
   - [ ] Conflict resolution present?
   - [ ] Privacy controls present?
   - [ ] API for preferences present?

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

Based on CORE-LEARN-A/B pattern:

**Likely to find** (75-90% infrastructure):
- ✅ UserPreferenceManager exists (from CORE-LEARN-A)
- ✅ Some preference storage exists
- ✅ Basic preference API exists
- ✅ Privacy infrastructure exists (from CORE-LEARN-A)
- ⚠️ May need implicit preference derivation
- ⚠️ May need conflict resolution
- ⚠️ May need behavior analysis

**Unlikely to find**:
- ❌ Complete implicit preference system
- ❌ Full conflict resolution strategy
- ❌ Complete behavior analysis

**Similar to CORE-LEARN-A/B**: Discover → Assess → Wire → Build gaps

---

## Time Tracking

**Start Time**: 1:20 PM
**Target Duration**: 4-10 minutes (based on CORE-LEARN-A/B)
**Target Completion**: 1:24-1:30 PM

**Stay focused!** Quick discovery, thorough assessment, clear recommendations.

---

## Remember

**YOU ARE DISCOVERING, NOT IMPLEMENTING!**

- ✅ Find existing preference code
- ✅ Assess explicit preference storage
- ✅ Check implicit preference derivation
- ✅ Check conflict resolution
- ✅ Check privacy controls
- ✅ Document findings
- ✅ Revise estimates
- ❌ Don't implement preferences
- ❌ Don't create APIs
- ❌ Don't build features

**Save implementation for Code agent after discovery!**

---

**Ready to find the preference learning infrastructure!** 🔍

*CORE-LEARN-A/B showed 90-95% existed in 4 minutes. Let's see what CORE-LEARN-C reveals!*
