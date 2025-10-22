# Architectural Review: Standup API DDD Compliance

**Agent**: Cursor (Chief Architect)
**Issue**: #162 (CORE-STAND-MODES-API)
**Date**: October 19, 2025, 8:33 PM
**Priority**: CRITICAL - Blocks Task 6 (Testing)

---

## Mission

Investigate whether the Phase 2 standup API implementation follows Piper Morgan's Domain-Driven Design (DDD) principles, or if business logic has drifted into the web layer.

**Context**: You researched the Standup epic last night during refactoring. Use that recent context plus Serena for current state.

---

## Critical Question

**Has business logic been placed in `web/` instead of `services/`?**

This would violate our core architectural principle: **thin routes, fat services**.

---

## What to Investigate

### 1. Locate All Standup-Related Files

**Use Serena to find**:
```
Find all files related to standup functionality:
- web/api/routes/standup.py (if exists)
- services/domain/*standup*
- services/orchestration/*standup*
- services/api/*standup*
- Any other standup-related files
```

**Map the structure**: What files exist and where?

---

### 2. Analyze web/api/routes/standup.py

**If this file exists, determine**:

**A. How much code is in it?**
- Line count
- Complexity assessment

**B. What does it contain?**
- Just FastAPI route definitions? ✅ (good)
- Request validation only? ✅ (good)
- Business logic embedded? ❌ (bad)
- Standup generation logic? ❌ (bad)
- Mode handling logic? ❌ (bad)
- Format conversion logic? ❌ (bad)

**C. Does it delegate to services?**
- Does it call domain services?
- Or does it implement logic itself?

**Example of GOOD (thin) route**:
```python
@router.post("/generate")
async def generate_standup(request: StandupRequest):
    # Minimal - just HTTP handling
    service = StandupService()  # Or injected
    result = await service.generate(request)
    return result
```

**Example of BAD (fat) route**:
```python
@router.post("/generate")
async def generate_standup(request: StandupRequest):
    # 200+ lines of business logic here
    if mode == "standard":
        # Generate standup logic
        # GitHub calls
        # Data processing
    elif mode == "issues":
        # More business logic
    # Format conversion
    # etc...
```

---

### 3. Analyze services/ Structure

**Check for domain services**:

**A. Does StandupOrchestrationService exist?**
- Location: `services/orchestration/standup_orchestration_service.py`?
- Or: `services/domain/standup_service.py`?
- What does it do?
- Is it being used by web routes?

**B. Where is business logic?**
- Standup generation
- Mode handling (standard, issues, documents, calendar, trifecta)
- Format conversion (json, slack, markdown, text)
- Integration orchestration

**C. How are modes implemented?**
- Separate service classes?
- Strategy pattern?
- Switch/if statements in routes? (bad)
- Proper domain service delegation? (good)

---

### 4. Check Against Architectural Patterns

**Compare against these patterns from knowledge**:

**Pattern: Domain Service Mediation (ADR-029)**
```
✅ Domain services contain business logic
✅ Web layer is thin (just HTTP concerns)
✅ Clean separation of concerns
❌ Business logic in web/api/routes/
```

**Pattern: Plugin Wrapper (Pattern-031)**
```
✅ Router contains business logic (~300-500 lines)
✅ Web routes delegate to router/service
❌ Web routes implement logic directly
```

**Architecture.md - Web Layer**:
```
✅ FastAPI routes only
✅ Request/response handling
✅ HTTP concerns
❌ Business logic
❌ Domain logic
```

---

### 5. Integration with Existing Services

**Check how standup integrates**:

**A. GitHub integration**
- Does it use GitHubDomainService?
- Or direct GitHub calls?

**B. Slack integration**
- Does it use SlackDomainService?
- Or direct Slack calls?

**C. Calendar integration**
- Does it use existing calendar service?
- Or implement its own?

**D. Document integration**
- Does it use document service?
- Or implement its own?

---

## Deliverable: Gap Analysis

### Part 1: Current State

**File Structure**:
```
[List all standup-related files with paths and line counts]
```

**Business Logic Location**:
```
Where is standup generation logic?
Where is mode handling?
Where is format conversion?
Where is integration orchestration?
```

**Architecture Pattern**:
```
Does it follow: [pattern name]
Or: Custom implementation
```

### Part 2: What SHOULD Exist (Per DDD)

**Ideal structure per our patterns**:

```
services/domain/standup_service.py (or similar):
  - StandupGenerationService
  - Business logic
  - Mode coordination
  - Format handling
  - Delegates to integration domain services

services/orchestration/standup_orchestration_service.py:
  - High-level workflow coordination
  - Calls domain services
  - Manages multi-integration workflows

web/api/routes/standup.py:
  - THIN routes (~50-100 lines total)
  - FastAPI endpoint definitions only
  - Request validation
  - Call orchestration service
  - Return responses
  - NO business logic
```

### Part 3: Gap Assessment

**If gaps exist, categorize**:

**Critical Gaps** (must fix before testing):
- Business logic in web layer
- No domain service layer
- Direct integration calls from routes

**Moderate Gaps** (document as tech debt):
- Some logic in routes, but not extensive
- Domain service exists but underutilized
- Mixed delegation patterns

**Minor Gaps** (acceptable for MVP):
- Structure is sound
- Minor refactoring opportunities
- Documentation improvements

---

## Recommendations

**For each gap identified, recommend**:

**A. Continue as-is**
- If: Architecture is sound
- If: Follows DDD principles
- Action: Proceed with Task 6 (testing)

**B. Document as tech debt**
- If: Minor gaps, but functional
- If: Refactor would be disruptive now
- Action: Create tech debt issue, proceed with testing

**C. Refactor before testing**
- If: Critical architectural violations
- If: Business logic in web layer
- Action: Extract to domain services before Task 6

**D. Hybrid approach**
- If: Some parts good, some parts need work
- Action: Specify what to fix vs document

---

## Use Serena Efficiently

**Serena queries to run**:

1. **Find files**:
   ```
   List all files containing "standup" in services/ and web/
   ```

2. **Check imports**:
   ```
   What does web/api/routes/standup.py import from services/?
   ```

3. **Find domain services**:
   ```
   Does StandupOrchestrationService or StandupService exist?
   ```

4. **Check integration usage**:
   ```
   How does standup code use GitHubDomainService, SlackDomainService?
   ```

5. **Code complexity**:
   ```
   How many lines in web/api/routes/standup.py?
   What functions/classes are defined there?
   ```

---

## Output Format

### Summary

**One sentence**: Architecture [compliant/non-compliant] with DDD principles

**Recommendation**: [Continue/Refactor/Document debt]

### Detailed Findings

**Current Architecture**:
- [File structure]
- [Where business logic lives]
- [Pattern being followed]

**Gaps Identified**:
1. [Gap 1 with severity]
2. [Gap 2 with severity]
3. [etc.]

**Evidence**:
- [Code snippets showing issues]
- [File locations]
- [Import patterns]

### Action Items

**Immediate** (before Task 6):
- [ ] Action 1
- [ ] Action 2

**Tech Debt** (document for later):
- [ ] Debt 1
- [ ] Debt 2

**None** (if architecture is sound):
- ✅ Proceed with Task 6

---

## Context for Efficiency

**You investigated standup last night** during epic refactoring:
- You know the intended architecture
- You know the mode structure
- You have recent familiarity

**Use that context** plus Serena to:
- Quickly locate relevant files
- Assess against what you expected
- Identify any drift from plan

---

## Success Criteria

This investigation is complete when PM can answer:

1. **Is business logic in web/ or services/?**
2. **Does architecture follow DDD principles?**
3. **Can we continue Task 6, or must we refactor?**
4. **If gaps exist, what's the severity and recommendation?**

---

## Timeline

**This is blocking Task 6** (testing) which is waiting.

**Target**: 30-45 minutes for thorough investigation

**Deliverable**: Clear architectural assessment with specific recommendation

---

## Remember

**We've built outside DDD principles before** - PM's "(once again)" comment.

**Better to catch now** than:
- After testing locks in architecture
- After Task 7 builds on wrong foundation
- After it's harder to refactor

**Be thorough but honest**: If there are gaps, we need to know!

---

*This investigation determines whether we continue Task 6 or need architectural refactoring first.*

**Ready when you are!** 🏗️
