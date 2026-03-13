# Phase 2 Gameplan Revision Template

**Purpose**: Tag each test in original gameplan with priority classification based on Code's reality check
**Date**: Sunday, October 26, 2025, 9:00 AM PT
**Input**: Code's archaeological investigation report
**Output**: Updated Phase 2 gameplan ready for testing

---

## Priority Tag System

### [MUST WORK] - Alpha Blocker
**Criteria**: Core functionality that MUST work or Alpha release is blocked
- Onboarding flow
- Basic chat functionality
- API key storage
- Database connectivity
- System startup

**Test Behavior**: Any failure is P0 bug, stops testing immediately

---

### [IF EXISTS] - Discovery Mode
**Criteria**: Features we believe exist but need to verify
- Learning system components
- Integration capabilities
- Cost tracking interfaces
- Graph reasoning
- Multi-tool orchestration

**Test Behavior**: Try optimistically, document reality, not a bug if incomplete

---

### [FUTURE] - Out of Scope
**Criteria**: Known to be unimplemented, Alpha doesn't need them
- OAuth authentication
- Voice input
- Team/multi-user features
- Advanced ML adaptation
- Cross-user learning

**Test Behavior**: Skip test, note absence for documentation

---

## Revision Process

### Step 1: Map Reality Check to Gameplan

For each test in original gameplan, determine:
1. What does this test require to run?
2. Did Code find those components?
3. What's the appropriate priority tag?

**Example**:
```markdown
ORIGINAL:
### Journey 1: Alpha Onboarding

**Test Sequence**:
1. First run
2. Setup wizard
3. API key configuration
...

REVISED:
### Journey 1: Alpha Onboarding [MUST WORK]

**Test Sequence**:
1. First run [MUST WORK]
   - Status: READY (Code found main.py entry point)

2. Setup wizard [MUST WORK]
   - Status: READY (Code found setup command at [location])
   - Command: `python main.py setup`

3. API key configuration [MUST WORK]
   - Status: READY (Code found KeyValidator #268)
   - Command: `python main.py keys add --provider openai`
...
```

---

### Step 2: Add Status Annotations

For each test, add Code's findings:

**Status Types**:
- ✅ **READY** - Component exists, command works, ready to test
- ⚠️ **PARTIAL** - Component exists but may have gaps, test carefully
- ❌ **BLOCKED** - Component missing, cannot test
- 🔍 **DISCOVERY** - Unknown status, try and document
- ⏭️ **SKIP** - Out of scope, document absence

**Template**:
```markdown
### Test: [Name] [PRIORITY TAG]

**Status**: [READY/PARTIAL/BLOCKED/DISCOVERY/SKIP]
**Reason**: [From Code's report]
**Command**: [Actual command if exists]
**Location**: [File/module reference]

**Test Sequence**:
[original steps with annotations]
```

---

### Step 3: Update Test Matrix

Original test matrix:
```markdown
| Feature | Integration Points | Test Focus | Priority |
|---------|-------------------|------------|----------|
```

Add "Status" column:
```markdown
| Feature | Status | Integration Points | Test Focus | Priority | Notes |
|---------|--------|-------------------|------------|----------|-------|
| Preferences | ✅ READY | Database, Profile, LLM | Bridge works | HIGH | Found at [loc] |
| Cost Track | ⚠️ PARTIAL | LLMClient, DB, Analytics | Capture | HIGH | No CLI yet |
```

---

## Revision Template by Section

### Section 1: Infrastructure Verification

```markdown
## Phase -1: Infrastructure Verification [MUST WORK]

**Status**: [Assessment from Code's report]

**Working Commands** (from Code):
```bash
# System health check
[actual command Code found]

# Database status
[actual command Code found]

# Service status
[actual command Code found]
```

**Missing Commands** (if any):
```bash
# Need to create or workaround:
[list gaps]
```

**Blockers**:
- [List any P0 issues preventing testing]

**Go/No-Go**: CAN START TESTING / BLOCKED / NEEDS WORK
```

---

### Section 2: User Journey Testing

```markdown
## Phase 1: User Journey Testing

### Journey 1: Alpha Onboarding [MUST WORK]

**Overall Status**: READY / PARTIAL / BLOCKED
**Can Test**: YES / NO / WITH MODIFICATIONS

**Test Sequence** (updated with reality):

#### Step 1: First Run [MUST WORK]
**Status**: ✅ READY
**Found**: [location from Code]
**Command**: `[actual command]`
**Expected**: [behavior]
**Test**: [how to verify]

#### Step 2: Setup Wizard [MUST WORK]
**Status**: ✅ READY / ⚠️ PARTIAL / ❌ BLOCKED
**Found**: [location from Code]
**Command**: `[actual command]`
**Expected**: [behavior]
**Test**: [how to verify]
**Notes**: [any gaps or issues from Code's report]

[Repeat for each step...]

---

### Journey 2: Power Workflows [IF EXISTS]

**Overall Status**: READY / PARTIAL / BLOCKED
**Can Test**: YES / NO / WITH MODIFICATIONS
**Discovery Mode**: Try each, document reality

**Test Sequence** (updated with reality):

#### Step 1: Complex Query [IF EXISTS]
**Status**: 🔍 DISCOVERY
**Found**: [what Code discovered about GitHub integration]
**Command**: `[actual command if exists]`
**Expected**: [ideal behavior]
**Test**: Try it, see what happens, document reality
**Not a Bug**: If GitHub integration incomplete

[Repeat for each step...]

---

### Journey 3: Edge Cases [IF EXISTS]

**Overall Status**: READY / PARTIAL / BLOCKED
**Can Test**: YES / NO / WITH MODIFICATIONS

[Similar structure...]
```

---

### Section 3: Integration Testing

```markdown
## Phase 2: Integration Testing

### Updated Test Matrix

| Feature | Status | Location | Command | Priority | Notes |
|---------|--------|----------|---------|----------|-------|
| Preferences (#269) | [from Code] | [path] | [command] | [MUST WORK] | [notes] |
| Cost Tracking (#271) | [from Code] | [path] | [command] | [IF EXISTS] | [notes] |
| Knowledge Graph (#278) | [from Code] | [path] | [command] | [IF EXISTS] | [notes] |
| Key Validation (#268) | [from Code] | [path] | [command] | [MUST WORK] | [notes] |

### Integration Test Commands

**From Code's Report**:
```bash
# Preferences → Behavior
[actual command or "NOT FOUND"]

# Cost → Database
[actual command or "NOT FOUND"]

# Graph → Retrieval
[actual command or "NOT FOUND"]

# Full stack
[actual command or "NOT FOUND"]
```
```

---

### Section 4: Bug Documentation

```markdown
## Phase 3: Bug Documentation

**Updated Severity Classification**:

**P0 - BLOCKER**: [MUST WORK] features broken
- Prevents Alpha testing
- Examples: [from reality check]

**P1 - CRITICAL**: [MUST WORK] features degraded or [IF EXISTS] completely broken
- Major impact on Alpha
- Examples: [from reality check]

**P2 - MAJOR**: [IF EXISTS] features partially broken
- Workaround exists or feature incomplete
- Not a blocker if we document
- Examples: [from reality check]

**P3 - MINOR**: [IF EXISTS] edge cases or [FUTURE] noted
- Document for later
- Examples: [from reality check]

**DISCOVERY NOTE**: Features marked [IF EXISTS] that don't work fully are P2 at most, unless they're critical integrations.
```

---

### Section 5: Scope Adjustments

```markdown
## Scope Adjustments Based on Reality

### Remove from Testing (Confirmed [FUTURE])
**These were in gameplan but Code confirmed out of scope**:
- [List from Code's report]

### Add to Testing (Discovered Capabilities)
**Code found these working features not in gameplan**:
- [List surprises from Code's report]

### Modify Testing Approach (Partial Implementation)
**These need adjusted expectations**:
- [List features with gaps from Code's report]

### Known Limitations (Document, Don't Test)
**These are expected gaps for Alpha**:
- [List from Code's report]
```

---

## Quick Reference: Priority Decision Tree

```
Is this feature...

┌─ In onboarding flow? ──────► [MUST WORK]
│
├─ Basic chat functionality? ──► [MUST WORK]
│
├─ API key storage? ───────────► [MUST WORK]
│
├─ Sprint A8 Phase 1 feature? ─┬─ Core component? ───► [MUST WORK]
│                              └─ Enhancement? ──────► [IF EXISTS]
│
├─ Integration capability? ────► [IF EXISTS]
│
├─ Learning/adaptation? ───────► [IF EXISTS]
│
├─ Multi-user/OAuth/Voice? ────► [FUTURE]
│
└─ Unknown/Surprising? ────────► [IF EXISTS] (discovery mode)
```

---

## Output Format

**Deliver revised gameplan as**:
```
sprint-a8-phase-2-gameplan-e2e-testing-REVISED.md
```

**Include at top**:
```markdown
# Sprint A8 Phase 2 Gameplan: E2E Testing (REVISED)

**Original Date**: October 27, 2025
**Revised Date**: October 26, 2025, 9:20 AM PT
**Based On**: Code archaeological investigation report
**Philosophy**: Discovery testing with priority classification

## Revision Summary

**Changes from original**:
- Added [MUST WORK] / [IF EXISTS] / [FUTURE] tags
- Updated commands with actual paths
- Added status annotations
- Noted discovered capabilities
- Clarified scope boundaries

**Test Readiness**:
- [MUST WORK] tests: X ready, Y blocked
- [IF EXISTS] tests: X ready for discovery
- [FUTURE] tests: X skipped

**Can Begin Testing**: YES / NO / WITH MODIFICATIONS
```

---

## Success Criteria

Revised gameplan has:
- [ ] Every test tagged with priority
- [ ] Status annotations from Code's report
- [ ] Actual commands documented
- [ ] Scope boundaries clear
- [ ] Known gaps noted
- [ ] Go/no-go decision explicit

---

*Template Version: 1.0*
*Ready to apply Code's findings*
*Estimated revision time: 10-15 minutes*
