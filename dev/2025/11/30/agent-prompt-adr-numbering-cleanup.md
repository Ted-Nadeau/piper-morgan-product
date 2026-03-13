# Agent Prompt: ADR Numbering Cleanup
**Created**: November 30, 2025, 5:40 PM PT
**For**: Haiku Documentation Agent
**Gameplan**: Gameplan D
**Model**: Haiku (cost-effective, straightforward task)

---

## Context

You are a documentation agent tasked with updating ADR (Architecture Decision Record) references across the codebase. The Chief Architect has established a new policy: **ADR numbers are assigned at writing time, not planning time**.

### The Problem

Some documentation currently references specific future ADR numbers (like "ADR-046", "ADR-047") that haven't been written yet. Additionally, ADR-046 HAS now been written (micro-format agent architecture by Ted Nadeau) and needs to be added to the index.

### The Solution

1. Add ADR-046 to the ADR index
2. Remove prescriptive future ADR numbers from docs
3. Replace with flexible references: "ADR documenting [topic]"

---

## Your Task

Complete the ADR numbering cleanup as specified in `/dev/active/adr-numbering-cleanup.md`.

### Specification Source

**READ THIS FIRST**:
```bash
cat /dev/active/adr-numbering-cleanup.md
```

This document contains:
- Complete task specification
- Acceptance criteria
- Specific changes needed
- Verification steps

---

## Required Actions

### 1. Add ADR-046 to Index

**File**: `/docs/internal/architecture/current/adrs/README.md`

**Action**: Add this entry after ADR-045:
```markdown
- ADR-046: Micro-Format Agent Architecture (Proposed) - Ted Nadeau's micro-format processing pipeline
```

**Verification**:
```bash
# Should show 46 ADRs total
cat /docs/internal/architecture/current/adrs/README.md | grep "^- ADR-" | wc -l
```

### 2. Update GitHub Issues

**Search for issues mentioning specific future ADR numbers**:
```bash
gh issue list --search "ADR-046 OR ADR-047" --state all --json number,title,body
```

**Change pattern**:
- **Before**: "ADR-046 documenting object model decisions"
- **After**: "ADR documenting object model decisions"

**Method**:
- Try `gh issue edit` if possible
- If API limitations, create list of issues needing manual update

**Likely issues** (from spec):
- VISION-OBJECT-MODEL
- MUX-VISION issues
- MUX-TECH issues

### 3. Update Roadmap

**File**: `docs/roadmap-v12.2.md` (and any other versions)

**Change pattern**:
- **Before**: "ADR-047 documenting [topic]"
- **After**: "ADR documenting [topic]"

**Verification**:
```bash
# Should show NO results after update
grep -E "ADR-04[7-9]|ADR-05[0-9]" docs/roadmap*.md
```

### 4. Search for Other References

**Find all prescriptive ADR numbering**:
```bash
# Search documentation
grep -r "ADR-046\|ADR-047\|ADR-048\|ADR-049" docs/ --include="*.md"

# Search dev/active
grep -r "will be ADR-\|future ADR-" dev/active/ --include="*.md"
```

**Update** any files found following the same pattern:
- Remove specific unwritten ADR numbers
- Replace with "ADR documenting [topic]"

---

## Tools You Can Use

**Git commands**:
```bash
# Verify ADR-046 file exists
ls -la /docs/internal/architecture/current/adrs/ADR-046-micro-format-agent-architecture.md

# Check current index
cat /docs/internal/architecture/current/adrs/README.md | grep "ADR-04"

# Search for problematic references
grep -r "ADR-04[6-9]" docs/ dev/active/ --include="*.md"
```

**GitHub CLI**:
```bash
# Search issues
gh issue list --search "ADR-" --state all --json number,title

# View specific issue
gh issue view <number> --json body

# Edit issue (if possible)
gh issue edit <number> --body "new body text"
```

---

## Constraints

**DO**:
- Read `/dev/active/adr-numbering-cleanup.md` completely first
- Verify ADR-046 file exists before adding to index
- Use git grep/GitHub search to find all references
- Make changes systematically
- Verify no unwritten ADR numbers remain

**DON'T**:
- Change existing ADR numbers (001-046 are correct)
- Create new ADRs
- Modify ADR content (only index/references)
- Skip verification steps
- Leave any unwritten ADR numbers in docs

---

## Acceptance Criteria

From the specification, your work is complete when:

- [ ] ADR-046 added to `/docs/internal/architecture/current/adrs/README.md`
- [ ] GitHub issues updated (or list of manual updates provided)
- [ ] Roadmap v12.2 updated with flexible ADR references
- [ ] Any other prescriptive numbering found and fixed
- [ ] All changes committed with clear message

### Verification Steps

**Run these before committing**:

```bash
# 1. Confirm ADR index lists all ADRs 001-046
cat /docs/internal/architecture/current/adrs/README.md | grep "^- ADR-" | wc -l
# Expected: 46

# 2. Confirm no unwritten ADR numbers are referenced (except ADR-046)
grep -r "ADR-04[6-9]\|ADR-05[0-9]" docs/ dev/active/ --include="*.md" | grep -v "ADR-046"
# Expected: no results

# 3. Manual review
grep -r "ADR-0" docs/ --include="*.md" | head -20
# Check all references are appropriate
```

---

## Commit Message Format

When you're done, use this commit message:

```
docs: Update ADR references to use flexible numbering

- Add ADR-046 to ADR index
- Remove prescriptive ADR-047, ADR-048 references
- Use 'ADR documenting [topic]' for unwritten ADRs

Per new policy: ADR numbers assigned at writing time, not planning time.

Related: Chief Architect documentation cleanup
```

---

## Success Criteria

Task is complete when:
- [ ] ADR-046 in index (correct position, correct format)
- [ ] ADR index has all ADRs 001-046 in order
- [ ] GitHub issues updated or manual update list provided
- [ ] Roadmap has flexible ADR references
- [ ] No unwritten ADR numbers in documentation
- [ ] Changes committed with clear message
- [ ] Verification steps pass

---

## Quality Gates

Before marking complete:
- [ ] No ADR numbers skipped (001-046 complete sequence)
- [ ] Consistent formatting in index
- [ ] Generic references are clear (not vague like "an ADR")
- [ ] No broken links introduced
- [ ] All files syntax-valid markdown

---

## STOP Conditions

If you encounter any of these, STOP and report:
- [ ] ADR-046 file not found (needs creation first)
- [ ] Index format unclear (structural questions)
- [ ] GitHub API cannot update issues (need manual process)
- [ ] Roadmap has multiple conflicting versions
- [ ] Unclear how to phrase generic ADR references
- [ ] Breaking changes to existing ADR links

---

## Example Changes

### Good Generic References

✅ "We will document this in an ADR covering database migration strategy"
✅ "See ADR documenting spatial integration architecture"
✅ "Pending: ADR documenting multi-workspace support"

### Bad Generic References

❌ "See future ADR" (too vague)
❌ "ADR-047 will cover this" (prescriptive numbering)
❌ "An ADR exists for this" (unclear which one)

---

## Timeline

**Estimated Time**: 1 hour (from specification)
**Priority**: P1 - Immediate

---

## Start Here

1. Read `/dev/active/adr-numbering-cleanup.md` completely
2. Verify ADR-046 file exists
3. Update ADR index
4. Search for prescriptive numbering (docs, roadmap, issues)
5. Make updates following the pattern
6. Run verification steps
7. Commit changes
8. Report completion

**Begin when ready. This is a straightforward task with clear specifications!**
