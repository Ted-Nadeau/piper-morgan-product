# Code Agent Prompt: PROOF Phase -1 - Pre-Reconnaissance Verification

**Date**: October 13, 2025, 2:25 PM
**Phase**: PROOF Phase -1 (Pre-Reconnaissance Check)
**Duration**: 15-20 minutes
**Priority**: CRITICAL (blocks PROOF-0 deployment)
**Agent**: Code Agent

---

## Mission

Verify that all infrastructure and tools needed for CORE-CRAFT-PROOF are operational and accessible. Report current state without attempting fixes.

**This is a verification mission, not a fix mission.** Just tell us what you find.

---

## Investigation Areas

### 1. Serena MCP Operational Status (5 minutes)

**What we need to know**:
- Is Serena MCP currently connected and working?
- What tools/capabilities does it provide?
- Can you successfully invoke a simple Serena tool?

**How to investigate**:
- You have access to Serena tools in your environment
- Try a simple, safe operation (like listing tools or searching for a known file)
- Report what works and what doesn't

**Report format**:
```markdown
### Serena Status
**Connected**: [Yes/No]
**Available Tools**: [List of tools you can see]
**Test Query**: [What you tried]
**Result**: [What happened]
**Assessment**: [Ready/Blocked/Partial]
```

---

### 2. Documentation Structure (5 minutes)

**What we need to know**:
- Where are the GREAT epic documentation files?
- Where are the ADRs located?
- What's the current state of the documentation tree?

**How to investigate**:
- Look for documentation directories
- Find GREAT-related markdown files
- Locate ADR directory
- Count rough numbers (don't need exact yet)

**Report format**:
```markdown
### Documentation Structure
**GREAT Docs Location**: [Path or paths found]
**ADR Location**: [Path]
**GREAT Files Found**: [Approximate count]
**ADR Files Found**: [Approximate count]
**Accessibility**: [Can we read these files easily? Any issues?]
```

---

### 3. CI/CD Current State (3 minutes)

**What we need to know**:
- What's the current workflow status?
- Are we still at 7/9 passing (from GAP-2)?
- What are the 2 failing workflows?

**How to investigate**:
- Use whatever tools you have to check GitHub Actions status
- Or look at recent workflow runs in the repository
- We documented this in GAP-2, so you could also check those docs

**Report format**:
```markdown
### CI/CD Status
**Current State**: [X/9 workflows passing]
**Passing Workflows**: [List if available]
**Failing Workflows**: [List if available]
**Changes Since GAP-2**: [Any differences from 7/9 status?]
**Assessment**: [Same as GAP-2 / Better / Worse]
```

---

### 4. Test Infrastructure Baseline (5 minutes)

**What we need to know**:
- How many tests do we currently have?
- Are they all passing?
- Where are the test files located?

**How to investigate**:
- Look for test directories and files
- Count test files (rough is fine)
- Check if we have recent test run results
- From GAP-2 we know we had 278/278 passing - is that still true?

**Report format**:
```markdown
### Test Infrastructure
**Test Directories**: [Locations found]
**Approximate Test File Count**: [Number]
**Last Known Status**: [From GAP: 278/278 passing]
**Current Status**: [If you can determine it]
**Test Framework**: [pytest/unittest/other]
**Assessment**: [Stable/Unknown/Issues]
```

---

### 5. Code Repository State (2 minutes)

**What we need to know**:
- Are we on main branch?
- Is the working directory clean?
- Any uncommitted changes from GAP work?

**How to investigate**:
- Check git status
- See what branch we're on
- Look for uncommitted files

**Report format**:
```markdown
### Repository State
**Current Branch**: [Name]
**Working Directory**: [Clean/Has changes]
**Uncommitted Files**: [List if any, or "None"]
**Last Commit**: [Recent commit message or hash]
**Assessment**: [Ready for work / Needs cleanup]
```

---

## Critical Notes

### What NOT To Do
- ❌ Don't attempt to fix anything you find
- ❌ Don't run the full test suite (just check status)
- ❌ Don't modify any files
- ❌ Don't invent syntax for tools you're unsure about
- ❌ Don't make assumptions - report what you actually observe

### What TO Do
- ✅ Report exactly what you find
- ✅ Use whatever tools/methods work for you
- ✅ Say "I don't know" if you can't determine something
- ✅ Flag anything unexpected or concerning
- ✅ Be honest about limitations

---

## Investigation Questions

As you investigate, keep these questions in mind:

1. **Serena**: Can we actually use it for automated documentation auditing?
2. **Documentation**: Can we easily locate and read all GREAT epic docs?
3. **CI/CD**: Are we starting from the same 7/9 state GAP-2 left us in?
4. **Tests**: Is our 278/278 passing baseline still stable?
5. **Repository**: Is the environment clean and ready for PROOF work?

---

## Output Format

Create a single report file: `dev/2025/10/13/proof-phase-minus1-verification.md`

Use this structure:

```markdown
# PROOF Phase -1: Pre-Reconnaissance Verification

**Date**: October 13, 2025, 2:25 PM
**Agent**: Code Agent
**Duration**: [Actual time taken]

---

## Executive Summary

**Overall Assessment**: [Ready / Blocked / Partial]

**Key Findings**:
- [Finding 1]
- [Finding 2]
- [Finding 3]

**Recommendation**: [Proceed with PROOF-0 / Fix blockers first / Other]

---

## Detailed Findings

[Include all 5 investigation areas as documented above]

---

## Blockers Identified

[List anything that would prevent PROOF-0 from succeeding]

---

## Unknowns

[List anything you couldn't determine]

---

## Ready State Checklist

- [ ] Serena MCP operational
- [ ] Documentation accessible
- [ ] CI/CD status known
- [ ] Test baseline confirmed
- [ ] Repository clean

**Pass Count**: X/5

---

## Recommendation

[Your assessment: Can we proceed with PROOF-0 today?]

---

**Verification Complete**: [Timestamp]
```

---

## Time Budget

- **Serena check**: 5 minutes
- **Documentation structure**: 5 minutes
- **CI/CD status**: 3 minutes
- **Test baseline**: 5 minutes
- **Repository state**: 2 minutes
- **Report creation**: 5 minutes
- **Total**: 25 minutes (with buffer)

---

## Success Criteria

**Minimum Acceptable**:
- We know if Serena works (Yes/No/Partially)
- We know where documentation lives
- We know current CI/CD state
- We have a baseline for comparison
- We know if anything is blocking PROOF-0

**Ideal**:
- All 5 areas verified
- No unexpected blockers
- Clear "go/no-go" for PROOF-0
- Confidence in infrastructure readiness

---

## Context for Code Agent

**Why This Matters**:
- PROOF-0 reconnaissance depends on Serena MCP
- Can't audit documentation if we can't find it
- Need to know if GAP-2's 7/9 CI state is still stable
- Don't want surprises when we start PROOF-0

**What Comes Next**:
- If this check passes → Deploy PROOF-0 today (2-3 hours)
- If blockers found → Fix tomorrow, start PROOF-0 fresh
- If uncertain → Review findings with PM and decide

**PM Context**: "Start now. Break when sensible. Continue tomorrow as needed."

**Expected Outcome**: Quick verification report that tells us we're ready (or not) for PROOF-0.

---

**Phase -1 Start Time**: 2:25 PM
**Expected Completion**: 2:45 PM (20 minutes)
**Status**: Ready for Code Agent investigation

**LET'S VERIFY READINESS! 🔍**
