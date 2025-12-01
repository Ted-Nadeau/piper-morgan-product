# Gameplan D: ADR Numbering Cleanup
**Created**: November 30, 2025, 5:25 PM PT
**Lead**: Documentation Subagent (Haiku)
**Type**: Documentation Maintenance
**Related**: Chief Architect work, Ted Nadeau's ADR-046

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Current Situation**:
- [x] ADR-046 written by Chief Architect (micro-format agent architecture)
- [x] ADR index needs updating: `/docs/internal/architecture/current/adrs/README.md`
- [x] Problem: Some docs reference future ADR numbers (ADR-046, ADR-047) that aren't written yet
- [x] New policy: ADR numbers assigned at writing time, not planning time
- [x] Task source: Chief Architect's documentation (`dev/active/adr-numbering-cleanup.md`)

**Scope**:
- Add ADR-046 to index
- Update GitHub issues to remove prescriptive ADR numbers
- Update roadmap to remove prescriptive ADR numbers
- Find and fix any other future ADR number references

**Out of Scope**:
- Changing existing ADR numbers
- Creating new ADRs
- Modifying ADR content

### Part B: PM Verification Required

**PM, please confirm**:

1. **Task source accuracy**:
   - Is `dev/active/adr-numbering-cleanup.md` the correct specification?
   - Any additions or changes to the scope?

2. **ADR-046 details**:
   - Title: "Micro-Format Agent Architecture" (correct?)
   - Status: "Proposed" or something else?
   - Author: Ted Nadeau?

3. **Execution approval**:
   - Is this task ready to execute as specified?
   - Should Haiku agent handle this independently?

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Task is well-specified, ready for Haiku execution
- [ ] **REVISE** - If scope needs adjustment
- [ ] **CLARIFY** - If ADR-046 details need confirmation

---

## Phase 0: Survey Current State

### Purpose
Identify all locations that need updating.

### Required Actions

1. **Verify ADR-046 Exists**
   ```bash
   ls -la /docs/internal/architecture/current/adrs/ADR-046-micro-format-agent-architecture.md
   # Should exist
   ```

2. **Read ADR Index Current State**
   ```bash
   cat /docs/internal/architecture/current/adrs/README.md | grep -E "ADR-04[0-9]"
   # Should show: ADR-040 through ADR-045
   # Should NOT show: ADR-046 yet
   ```

3. **Search for Future ADR References**
   ```bash
   # Search documentation
   grep -r "ADR-046\|ADR-047\|ADR-048\|ADR-049" docs/ --include="*.md"

   # Search roadmap
   grep -E "ADR-04[6-9]|ADR-05[0-9]" docs/roadmap*.md

   # Search dev/active
   grep -r "will be ADR-\|future ADR-" dev/active/ --include="*.md"
   ```

4. **GitHub Issues Search**
   ```bash
   # Use gh CLI to search issues
   gh issue list --search "ADR-046 OR ADR-047" --state all --json number,title,body

   # Likely issues mentioned in spec:
   gh issue view VISION-OBJECT-MODEL --json body | grep -i "adr-"
   # (repeat for MUX-VISION, MUX-TECH issues if they exist)
   ```

5. **Document Findings**
   Create list of all files/issues that need updating.

### Output Deliverable
Checklist of update locations:
```markdown
## Files to Update
- [ ] /docs/internal/architecture/current/adrs/README.md
- [ ] docs/roadmap-v12.2.md
- [ ] [any other files found]

## GitHub Issues to Update
- [ ] #XXX: [issue title]
- [ ] #YYY: [issue title]
```

---

## Phase 1: Execute Updates

### Purpose
Make all identified updates following the specification.

### Agent Assignment
**Subagent**: Documentation agent (Haiku model)
- Simple, well-defined task
- No complex decisions
- Cost-effective

### Required Changes

#### 1.1: Update ADR Index
In `/docs/internal/architecture/current/adrs/README.md`:

**Add entry**:
```markdown
- ADR-046: Micro-Format Agent Architecture (Proposed) - Ted Nadeau's micro-format processing pipeline
```

**Placement**: After ADR-045, before any section breaks

**Verification**: ADRs listed in order 001-046

#### 1.2: Update GitHub Issues
For each issue containing specific future ADR numbers:

**Before**:
```markdown
ADR-046 documenting object model decisions
```

**After**:
```markdown
ADR documenting object model decisions
```

**Method**: Use `gh issue edit` if possible, or note which issues need manual update

#### 1.3: Update Roadmap
In `docs/roadmap-v12.2.md` (and any other versions):

**Before**:
```markdown
- ADR-047 documenting [topic]
```

**After**:
```markdown
- ADR documenting [topic]
```

#### 1.4: Update Other References
For any other files found in Phase 0:
- Remove specific unwritten ADR numbers
- Replace with "ADR documenting [topic]"

### Evidence Requirements
- [ ] Git diff showing ADR index update
- [ ] List of GitHub issues updated (with issue numbers)
- [ ] Git diff showing roadmap updates
- [ ] Confirmation no unwritten ADR numbers remain

### STOP Conditions
- Cannot find ADR-046 file (needs creation first)
- GitHub issues require manual edit (API limitations)
- Unclear how to phrase generic ADR references

---

## Phase Z: Final Validation & Handoff

### Required Actions

#### 1. Verification Checks
```bash
# 1. Confirm ADR index lists all ADRs 001-046
cat /docs/internal/architecture/current/adrs/README.md | grep "^- ADR-" | wc -l
# Should show: 46

# 2. Confirm no unwritten ADR numbers are referenced
grep -r "ADR-04[6-9]\|ADR-05[0-9]" docs/ dev/active/ --include="*.md" | grep -v "ADR-046"
# Should show: no results (only ADR-046 should appear)

# 3. Confirm all ADR references either point to existing or say "ADR documenting X"
grep -r "ADR-0" docs/ --include="*.md" | grep -v "ADR-001\|ADR-002" | head -20
# Manual review for appropriateness
```

#### 2. Commit Changes
```bash
git add docs/internal/architecture/current/adrs/README.md
git add docs/roadmap*.md
git add [any other files]
git commit -m "docs: Update ADR references to use flexible numbering

- Add ADR-046 to ADR index
- Remove prescriptive ADR-047, ADR-048 references
- Use 'ADR documenting [topic]' for unwritten ADRs

Per new policy: ADR numbers assigned at writing time, not planning time.

Related: Chief Architect documentation cleanup"
```

#### 3. GitHub Issue Updates Summary
If GitHub issues were updated:
```markdown
## GitHub Issues Updated
- #XXX: Removed ADR-046 reference, now says "ADR documenting object model"
- #YYY: Removed ADR-047 reference, now says "ADR documenting [topic]"

[Or note which issues need manual update if API couldn't handle it]
```

#### 4. PM Handoff
```markdown
@PM - ADR numbering cleanup complete:

**Added to Index**:
- ADR-046: Micro-Format Agent Architecture (Proposed)

**Updated References**:
- Roadmap v12.2: Removed specific future ADR numbers
- GitHub issues: [list or note manual updates needed]
- Documentation: All prescriptive numbering removed

**Verification**:
- ✅ ADR index complete (001-046)
- ✅ No unwritten ADR numbers referenced
- ✅ All future ADRs use generic "ADR documenting X" format

**Commit**: [commit hash]

Ready for your review.
```

---

## Success Criteria

### Task Complete When:
- [ ] ADR-046 added to index in correct position
- [ ] ADR index lists all ADRs 001-046 in order
- [ ] GitHub issues updated (or list of manual updates provided)
- [ ] Roadmap updated with flexible ADR references
- [ ] No unwritten ADR numbers remain in documentation
- [ ] All changes committed with clear message
- [ ] PM approved

### Quality Gates:
- [ ] No ADR numbers skipped (001-046 complete)
- [ ] Consistent formatting in index
- [ ] Generic references are clear (not vague)
- [ ] No broken links introduced

---

## Dependencies

**Independent**: Can start immediately and run in parallel with all other gameplans

**Blocked By**: None (ADR-046 already written)

---

## Agent Assignment

**All Phases**:
- Subagent: Documentation agent (Haiku model)
- Rationale: Straightforward documentation task, well-specified, cost-effective

**Oversight**:
- Me (Lead Developer) will review before commit
- Ensure changes meet specification

---

## STOP Conditions (Apply Throughout)

Stop immediately and escalate if:
- [ ] ADR-046 file not found (needs creation)
- [ ] Index format unclear (structural questions)
- [ ] GitHub API cannot update issues (manual process needed)
- [ ] Roadmap has multiple versions with conflicts
- [ ] Unclear how to phrase generic ADR references

---

## Notes

**Why this matters**:
- Prevents confusion about which ADRs exist
- Enforces new policy: ADR numbers at writing time
- Improves documentation accuracy
- Acknowledges Ted Nadeau's contribution (ADR-046)

**Source**:
- Chief Architect's specification in `dev/active/adr-numbering-cleanup.md`
- Clear acceptance criteria provided
- Well-scoped task

**Estimated Time**: 1 hour (as noted in specification)

**This is a clean, well-specified maintenance task - perfect for Haiku agent execution.**
