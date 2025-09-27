# Claude Code Agent Prompt: Commit Documentation Work

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first in docs/briefing/:
- PROJECT.md - What Piper Morgan is
- CURRENT-STATE.md - Current epic and focus
- role/PROGRAMMER.md - Your role requirements
- METHODOLOGY.md - Inchworm Protocol

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Check Current Working State FIRST
**Before doing ANYTHING else, verify current repository state**:

```bash
# Verify we're in the main working directory (not the /tmp fresh clone)
pwd
git status
git log --oneline -3

# Check for uncommitted documentation work
git status --porcelain | grep docs/
ls -la docs/guides/orchestration-setup-guide.md
ls -la docs/testing/performance-enforcement.md
```

**Current Context**: Fresh clone verification revealed documentation deployment gap - comprehensive setup guide created today exists only in working directory, not committed to repository.

## Session Log Management (CRITICAL)

**Continue existing session log**: Use your existing session log from Phase 1A
- Update with Phase 1.5 documentation commitment task
- Do NOT create new session log

## Mission
**Commit all documentation work created today to repository**

**Scope Boundaries**:
- This prompt covers ONLY: Git commit of today's documentation work
- NOT in scope: Creating new documentation or fixing code issues
- Target: Enable fresh clone to access comprehensive setup guide

## Context
- **GitHub Issue**: GREAT-1C (#187) - Verification Phase
- **Current State**: Documentation exists in working directory but not committed
- **Target State**: All today's documentation work committed and available in fresh clones
- **Critical Finding**: Fresh clone tested outdated docs/internal/development/tools/setup.md instead of docs/guides/orchestration-setup-guide.md
- **User Data Risk**: None - documentation commit only
- **Infrastructure Verified**: [Verify current state per above]

## Evidence Requirements (CRITICAL)

### For EVERY Claim You Make:
- **"Added files to git"** → Show `git add` output and `git status`
- **"Committed changes"** → Show `git commit` output with commit hash
- **"Pushed to repository"** → Show `git push` output
- **"Documentation accessible"** → Show files exist in fresh clone test

### Git Workflow Discipline:
```bash
# Systematic commit process
git status  # Show current state
git add [files]  # Add documentation files
git status  # Verify staged changes
git commit -m "descriptive message"  # Commit with evidence
git log --oneline -1  # Show commit hash
git push origin main  # Push to repository
```

## Constraints & Requirements

### For This Agent
1. **Working directory only**: Stay in main project directory, not /tmp
2. **Documentation focus**: Commit documentation files, avoid code changes
3. **Verification preparation**: Enable fresh clone to access today's work
4. **Evidence collection**: Terminal output for every git command

## Documentation Commit Instructions

### Step 1: Assess Uncommitted Documentation
```bash
# Check what documentation work needs committing
git status --porcelain

# Specifically check for today's key documentation:
ls -la docs/guides/orchestration-setup-guide.md
ls -la docs/testing/performance-enforcement.md
ls -la docs/architecture/initialization-sequence.md
ls -la docs/NAVIGATION.md

# Check git status for each
git status | grep docs/
```

### Step 2: Stage Documentation Files
```bash
# Add documentation files created/updated today
git add docs/guides/orchestration-setup-guide.md
git add docs/testing/performance-enforcement.md
git add docs/architecture/initialization-sequence.md
git add docs/NAVIGATION.md
git add docs/README.md

# Verify staged correctly
git status
git diff --cached --stat
```

### Step 3: Commit with Clear Message
```bash
# Commit with descriptive message
git commit -m "docs: Add comprehensive setup guide and verification documentation

- Add docs/guides/orchestration-setup-guide.md (264 lines)
- Add docs/testing/performance-enforcement.md with troubleshooting
- Add docs/architecture/initialization-sequence.md
- Update docs/NAVIGATION.md and docs/README.md
- Support GREAT-1C verification phase fresh clone testing

Resolves documentation deployment gap found in fresh clone verification."

# Verify commit created
git log --oneline -1
git show --stat HEAD
```

### Step 4: Push to Repository
```bash
# Push to make available for fresh clone testing
git push origin main

# Verify push successful
git status
git log --oneline -3
```

### Step 5: Verification Test
```bash
# Quick verification that documentation is now in repository
git ls-tree HEAD docs/guides/
git show HEAD:docs/guides/orchestration-setup-guide.md | head -10
```

## Expected Outcomes

### Success Criteria
- [ ] All today's documentation work committed to repository
- [ ] Clear commit message describing changes
- [ ] Push successful to remote repository
- [ ] Documentation accessible in fresh clones
- [ ] Git history shows documentation deployment

### Evidence Package to Provide
1. **Git status before/after**: Show uncommitted → committed state
2. **Commit hash and message**: Show successful commit creation
3. **Push confirmation**: Show successful push to remote
4. **File verification**: Show documentation accessible in repository

## Handoff Preparation
Once documentation committed, prepare for fresh clone re-test:
- **Repository state**: All documentation work available in fresh clones
- **Setup guide location**: docs/guides/orchestration-setup-guide.md now accessible
- **Fresh clone ready**: New /tmp environment can access comprehensive documentation

## STOP Conditions
- If git repository in unstable state
- If merge conflicts prevent clean commit
- If documentation files missing or corrupted
- If unable to push to remote repository

## Success Definition
**Documentation deployment gap resolved**: Fresh clone can access comprehensive setup guide created today, enabling accurate verification of new developer experience.

---

**Mission**: Commit today's documentation work to repository, resolving deployment gap found in fresh clone verification.

**Evidence Standard**: Complete git workflow with terminal output, verified remote accessibility.
