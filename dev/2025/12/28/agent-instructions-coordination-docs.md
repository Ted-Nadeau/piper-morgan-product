# Instructions: Update Multi-Agent Coordination Documentation

**Agent Type Needed**: Code Agent or Lead Developer
**Estimated Time**: 30 minutes
**GitHub Issue**: Create new issue "Update multi-agent coordination protocols"

## Your Mission

Update Piper Morgan's documentation to establish rigorous multi-agent coordination protocols, addressing the "75% completion pattern" where work gets done but tracking/evidence/closure gets abandoned.

## Files to Update

### 1. CLAUDE.md

**Location**: `CLAUDE.md` (root directory)

**Find Section**: Multi-agent coordination or similar

**Add/Update With**:
```markdown
## Multi-Agent Coordination Protocol

### Core Principle
"Done" means:
- ✅ User can actually use the feature
- ✅ Tests exist and pass
- ✅ Evidence documented in GitHub issue
- ✅ Session log updated

NOT "Done":
- ❌ Code written but not tested
- ❌ Tests pass but no documentation
- ❌ Works locally but not verified

### When Deploying Subagents

ALWAYS provide:
1. GitHub issue number and link
2. Specific acceptance criteria (checkboxes)
3. Required evidence format:
   - Test count and location
   - Files modified
   - Verification commands
4. Handoff instructions (what to report back)

### Evidence Requirements

Every issue closure MUST include:
```
## Implementation Evidence
- Tests: X tests added/modified in [file]
- Verification: `pytest path/to/tests -v` (all passing)
- Files: [list of modified files]
- User verification: [how to test as user]
```

### Anti-Patterns to Avoid

1. **The 75% Pattern**: Implementing feature without closing loop
2. **Evidence-Free Closure**: Closing issues without proof
3. **Test Theatre**: Writing tests that don't verify user experience
4. **Role Drift**: Lead Dev implementing instead of coordinating
```

### 2. Lead Developer Briefing

**Location**: `docs/briefings/BRIEFING-ESSENTIAL-LEAD-DEV.md` or similar

**Find Section**: Role responsibilities

**Add/Update With**:
```markdown
## Critical: Multi-Agent Coordination Discipline

### Your Role When Using Claude Code
- You COORDINATE agents, not implement
- You VERIFY completion, not trust assertions
- You DOCUMENT evidence, not assume it exists
- You CLOSE issues properly, not abandon at 75%

### Subagent Deployment Checklist
Before deploying any agent:
- [ ] Issue number ready
- [ ] Acceptance criteria defined as checkboxes
- [ ] Test requirements specified ("add 10 tests covering X")
- [ ] Evidence format specified ("provide test output")
- [ ] Integration point identified ("update session log")

### Handoff Protocol
When receiving work from subagent:
1. Verify ALL acceptance criteria met
2. Run tests independently
3. Document evidence in issue
4. Update session log with:
   - What was requested
   - What was delivered
   - What was verified
5. ONLY THEN close issue
```

### 3. Gameplan Template

**Location**: `templates/gameplan-template.md` or `docs/templates/gameplan-template.md`

**Add New Section** (after Phase definitions):
```markdown
## Multi-Agent Coordination Plan

### Agent Deployment Map
| Phase | Agent Type | Issue | Evidence Required | Handoff |
|-------|------------|-------|------------------|---------|
| 1 | Code Agent | #XXX | 10 tests, coverage report | Test locations |
| 2 | Cursor Agent | #XXY | File modifications | Diff summary |
| 3 | Lead Dev | #XXZ | Integration verified | User test |

### Verification Gates
- [ ] Phase 1: Unit tests passing
- [ ] Phase 2: Integration tests passing
- [ ] Phase 3: User verification complete
- [ ] Phase 4: Documentation updated

### Evidence Collection Points
1. After each subagent returns: Collect evidence
2. Before phase transition: Verify accumulated evidence
3. Before issue closure: Compile all evidence
4. At session end: Update omnibus log
```

### 4. Agent Prompt Template

**Location**: `templates/agent-prompt-template.md`

**Add New Section** (at the beginning):
```markdown
## CRITICAL: Evidence and Handoff Requirements

You are being deployed to complete GitHub Issue #[NUMBER].

### Your Acceptance Criteria
- [ ] [Specific criterion 1]
- [ ] [Specific criterion 2]
- [ ] [Test requirement]

### Evidence You MUST Provide
1. Test count: "Added X tests in [file]"
2. Test verification: "All tests passing (output below)"
3. Files modified: Complete list with line counts
4. How to verify: Step-by-step for user testing

### Your Handoff Format
Return your work with:
```
## Issue #XXX Completion Report
**Status**: Complete/Partial/Blocked
**Tests**: X added in [location]
**Verification**: [paste test output]
**Files Modified**: [list]
**User Testing**: [steps]
**Blockers**: [if any]
```

### Remember
- You're part of a coordination chain
- Your output enables the next step
- Incomplete handoff = failed task
- Evidence > assertions
```

## Verification of Your Work

After updating all files:
1. Confirm each file has new sections
2. Check that protocols are consistent across files
3. Create a summary of changes
4. Report back with:
   - Files updated (with line counts)
   - Sections added/modified
   - Any conflicts or concerns found

## Success Criteria

- [ ] CLAUDE.md has multi-agent protocol section
- [ ] Lead Dev briefing has coordination discipline section
- [ ] Gameplan template has coordination plan section
- [ ] Agent prompt template has evidence requirements
- [ ] All updates consistent with each other
- [ ] No duplicate or contradictory instructions

## Why This Matters

We've observed the "75% completion pattern" where sophisticated work gets done but tracking/closure fails. These updates will ensure:
- Every agent knows their evidence obligations
- Lead Developer maintains coordination discipline
- Work products are properly handed off
- Issues close only with proof

---

*Note: If any of these files don't exist or have different names/locations, use your judgment to find the equivalent files and update them accordingly. The key is establishing consistent multi-agent coordination protocols across all relevant documentation.*
