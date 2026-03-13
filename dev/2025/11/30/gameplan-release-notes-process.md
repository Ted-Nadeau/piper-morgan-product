# Gameplan C: Release Notes v0.8.1.3 + Mandatory Process
**Created**: November 30, 2025, 5:20 PM PT
**Lead**: Documentation Subagent (Haiku) for drafting, Lead Developer (Sonnet) for process
**Type**: Documentation + Process Design
**Related Thread**: Thread 6 (release notes)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Current Situation**:
- [x] v0.8.1.3 deployed to production today (Nov 30, 2025, ~3:45 PM PT)
- [x] NO release notes created for v0.8.1.3 (gap)
- [x] Previous release notes exist: RELEASE-NOTES-v0.8.1.2.md
- [x] Release notes directory: `/dev/2025/11/30/`
- [x] Version tracking: `pyproject.toml`

**What v0.8.1.3 included**:
- Login UI restoration (templates/login.html, static/css/auth.css, static/js/auth.js)
- Setup detection merge (feat/setup-detection-388)
- Venv docs merge (fix/version-and-venv-docs)
- Commits: dced0d6a (UI restoration), d192f159 (version bump), fae04751 (merge to production)

**Process gap**:
- Released to production without release notes (should be mandatory)
- Need mechanism to enforce release notes before production deployment

**My understanding of the task**:
- Part 1: Write release notes for v0.8.1.3 (retroactive documentation)
- Part 2: Design process to make release notes mandatory for future releases

### Part B: PM Verification Required

**PM, please confirm**:

1. **Release notes format**: Should v0.8.1.3 follow same format as v0.8.1.2?
   - Location: `/dev/2025/11/30/RELEASE-NOTES-v0.8.1.3.md`
   - Format: Same sections as v0.8.1.2?

2. **Key content for v0.8.1.3**:
   - Login UI restoration (critical fix)
   - Setup detection (alpha tester UX improvement)
   - Venv documentation (alpha tester guidance)
   - Anything else you want highlighted?

3. **Mandatory process**: What's your preferred enforcement mechanism?
   - [ ] Pre-push git hook (technical enforcement)
   - [ ] Checklist in deployment protocol (process enforcement)
   - [ ] Both (belt and suspenders)
   - [ ] Other approach?

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - PM confirmed this gap needs addressing
- [ ] **REVISE** - If PM wants different approach
- [ ] **CLARIFY** - If format or process needs discussion

---

## Phase 0: Gather Context for v0.8.1.3

### Purpose
Collect all information needed to write accurate release notes.

### Required Actions

1. **Review Commits in v0.8.1.3**
   ```bash
   # Get commit range for v0.8.1.3
   git log --oneline production --since="2025-11-30 14:00" --until="2025-11-30 16:00"

   # Detailed view of key commits
   git show dced0d6a --stat  # Login UI restoration
   git show d192f159 --stat  # Version bump
   git show fae04751 --stat  # Production merge
   ```

2. **Review Merged Branches**
   ```bash
   # Setup detection branch
   git log --oneline feat/setup-detection-388 ^main

   # Venv docs branch
   git log --oneline fix/version-and-venv-docs ^main
   ```

3. **Read Previous Release Notes for Template**
   ```bash
   cat /dev/2025/11/30/RELEASE-NOTES-v0.8.1.2.md
   ```

4. **Gather Deployment Timeline**
   From session log:
   - Login UI deletion discovered: ~3:38 PM
   - Files restored: ~3:40 PM (commit dced0d6a)
   - Branches merged: ~3:42 PM
   - Production deployment: ~3:45 PM (fae04751)

5. **Document Files Changed**
   - Login UI: templates/login.html, static/css/auth.css, static/js/auth.js
   - Setup detection: main.py, scripts/setup_wizard.py
   - Venv docs: docs/dev-tips/version-bump-and-venv-fix.md
   - Version: pyproject.toml

### Output Deliverable
Context document with all facts needed for release notes.

---

## Phase 1: Draft Release Notes for v0.8.1.3

### Purpose
Create comprehensive, accurate release notes following v0.8.1.2 format.

### Agent Assignment
**Subagent**: Documentation agent (Haiku model)
- Cost-effective for structured writing
- Fast turnaround
- Follows template well

### Required Sections (Based on v0.8.1.2 Format)

1. **Release Date and Version**
   - Date: November 30, 2025
   - Previous version: v0.8.1.2
   - Branch: production

2. **Summary**
   - Critical fix: Login UI restoration
   - Alpha tester improvements: Setup detection, venv docs

3. **What Changed**
   - Login UI restoration (with backstory about deletion)
   - Setup detection merge
   - Venv docs merge

4. **For Alpha Testers**
   - Action required: git pull origin production
   - New features available: Login UI, setup detection
   - Documentation available: Venv management guide

5. **Files Changed**
   - Complete list with change counts

6. **Technical Details**
   - Deployment process
   - Rollback path

7. **Commits in This Release**
   - Full list with hashes and descriptions

### Quality Criteria
- [ ] Accurate commit references
- [ ] Clear action items for alpha testers
- [ ] Explains WHY changes were made
- [ ] Includes rollback instructions
- [ ] Matches v0.8.1.2 format and tone
- [ ] No errors or omissions

### Output Deliverable
`/dev/2025/11/30/RELEASE-NOTES-v0.8.1.3.md` ready for PM review.

---

## Phase 2: Design Mandatory Release Notes Process

### Purpose
Prevent future production deployments without release notes.

### Agent Assignment
**Lead**: Claude Code Sonnet 4.5 (me)
- Requires process design thinking
- Needs to understand deployment workflow
- Must balance rigor with practicality

### Investigation Required

1. **Current Deployment Workflow**
   ```bash
   # How do we currently deploy to production?
   # Steps: version bump → commit → merge → push

   # Read current deployment docs (if they exist)
   find docs/ -name "*deploy*" -o -name "*release*" | xargs grep -l "production"
   ```

2. **Git Hook Options**
   ```bash
   # Check existing hooks
   ls -la .git/hooks/

   # Pre-push hook could check for release notes
   # Example logic:
   # - If pushing to production branch
   # - Check if version bumped in pyproject.toml
   # - Verify release notes exist for that version
   # - Block push if missing
   ```

3. **Checklist Options**
   - Add to CLAUDE.md deployment protocol
   - Add to session closing checklist
   - Add to gameplan template

### Design Options

#### Option A: Git Pre-Push Hook (Technical Enforcement)
**Pros**:
- Automatic, can't bypass without --no-verify
- Catches issue before push reaches remote
- Consistent enforcement

**Cons**:
- Requires hook installation on each machine
- Can be bypassed with --no-verify
- May frustrate if false positives

#### Option B: Deployment Checklist (Process Enforcement)
**Pros**:
- Flexible, human judgment
- Easy to understand and follow
- No technical setup required

**Cons**:
- Can be forgotten
- Relies on discipline
- Easier to skip under pressure

#### Option C: Both (Recommended)
**Pros**:
- Belt and suspenders approach
- Hook catches accidental skips
- Checklist ensures intentional thought

**Cons**:
- More initial setup work
- Redundant if always followed

### Deliverables

1. **Pre-Push Hook Script** (if Option A or C chosen)
   `/scripts/hooks/pre-push-release-notes-check.sh`:
   ```bash
   #!/bin/bash
   # Check if pushing to production branch
   # Check if version changed in pyproject.toml
   # Verify release notes exist for that version
   # Exit 1 if missing, 0 if present
   ```

2. **Installation Instructions**
   ```bash
   # How to install the hook
   ln -s ../../scripts/hooks/pre-push-release-notes-check.sh .git/hooks/pre-push
   chmod +x .git/hooks/pre-push
   ```

3. **Updated CLAUDE.md Deployment Section**
   Add release notes to mandatory deployment steps:
   ```markdown
   ## Production Deployment Protocol
   1. Version bump in pyproject.toml
   2. **Create release notes** (MANDATORY)
   3. Safety tag
   4. Merge to production
   5. Push to origin
   ```

4. **Updated Gameplan Template**
   Add "Release notes" to Phase Z requirements.

---

## Phase Z: Final Validation & Handoff

### Required Actions

#### 1. Release Notes Validation
- [ ] v0.8.1.3 release notes written
- [ ] PM reviewed and approved content
- [ ] File created in correct location
- [ ] Format matches v0.8.1.2
- [ ] All commits accounted for
- [ ] Action items clear for alpha testers

#### 2. Process Design Validation
- [ ] Pre-push hook written (if applicable)
- [ ] Hook tested (catches missing release notes)
- [ ] Installation instructions clear
- [ ] CLAUDE.md updated with deployment protocol
- [ ] Gameplan template updated with release notes requirement

#### 3. Testing
- [ ] Hook test: Try pushing version bump without release notes (should block)
- [ ] Hook test: Try pushing with release notes (should succeed)
- [ ] Checklist test: Can PM follow updated deployment protocol?

#### 4. Documentation
- [ ] Session log updated with process changes
- [ ] Deployment protocol documented
- [ ] Hook usage documented
- [ ] Rationale explained

#### 5. PM Approval Request
```markdown
@PM - Release notes and mandatory process complete:

**v0.8.1.3 Release Notes**: [link to file]
- Covers login UI restoration
- Covers setup detection and venv docs
- Includes alpha tester action items
- Ready for your review

**Mandatory Process**: [chosen option]
- Pre-push hook: [Yes/No]
- Deployment checklist: [Updated]
- Enforcement mechanism: [description]

**Testing**:
- Hook tested: [results]
- Protocol validated: [results]

Ready for your approval.
```

---

## Success Criteria

### Release Notes Complete When:
- [ ] v0.8.1.3 release notes written
- [ ] All sections complete (summary, changes, action items, commits)
- [ ] Accurate and clear
- [ ] PM approved

### Process Complete When:
- [ ] Enforcement mechanism chosen (hook, checklist, or both)
- [ ] Implementation complete and tested
- [ ] Documentation updated (CLAUDE.md, gameplan template)
- [ ] PM can follow new protocol easily
- [ ] Future releases will include release notes

---

## Dependencies

**Independent**: Can start immediately and run in parallel

**Informs**:
- All future releases will follow new process
- Improves documentation discipline project-wide

---

## Agent Assignment

**Phase 0 (Gather Context)**:
- Lead: Claude Code Sonnet 4.5 (me)
- Quick git investigation, straightforward

**Phase 1 (Draft Release Notes)**:
- Subagent: Documentation agent (Haiku model)
- Rationale: Cost-effective, fast, good at structured writing

**Phase 2 (Process Design)**:
- Lead: Claude Code Sonnet 4.5 (me)
- Rationale: Requires architectural thinking, workflow design

**Phase Z (Validation)**:
- Lead: Claude Code Sonnet 4.5 (me)
- Rationale: End-to-end validation, PM interface

---

## STOP Conditions (Apply Throughout)

Stop immediately and escalate if:
- [ ] Cannot determine what went into v0.8.1.3
- [ ] Conflicting information about deployment timeline
- [ ] PM wants different release notes format
- [ ] Hook implementation would break existing workflow
- [ ] Process too burdensome for team

---

## Notes

**Why this matters**:
- Release notes are critical for alpha testers
- Tracking what changed in each version
- Audit trail for production deployments
- Professional project management

**Gap identified**:
- v0.8.1.3 shipped without release notes (rushed deployment)
- Need process to prevent future occurrences

**This gameplan addresses both immediate gap (retroactive notes) and systemic issue (mandatory process).**

**Can start immediately - all context available from today's session.**
