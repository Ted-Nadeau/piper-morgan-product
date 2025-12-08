# Gameplan Template v9.2 - Complete Phase Documentation
*Last Updated: December 4, 2025*
*Key Addition: Worktree Assessment in Phase -1 (Issue #463 learning)*

---

## Phase Structure Overview

### Complete Phase Sequence
- **Phase -1**: Infrastructure Verification (with PM)
- **Phase 0**: Initial Bookending (GitHub investigation)
- **Phase 0.5**: Frontend-Backend Contract Verification (MANDATORY for UI work)
- **Phases 1-N**: Development Work (progressive bookending)
- **Phase Z**: Final Bookending & Handoff

---

## Phase -1: Infrastructure Verification Checkpoint (MANDATORY)

### STOP! Complete This Section WITH PM Before Writing Rest of Gameplan

**Purpose**: Prevent wrong gameplans based on incorrect assumptions

### Part A: Chief Architect's Current Understanding

Based on available context, I believe:

**Infrastructure Status**:
- [ ] Web framework: ____________ (I think: FastAPI/Flask/None/Unknown)
- [ ] CLI structure: ____________ (I think: Click/Argparse/Custom/Unknown)
- [ ] Database: ____________ (I think: PostgreSQL/SQLite/None/Unknown)
- [ ] Testing framework: ____________ (I think: pytest/unittest/None/Unknown)
- [ ] Existing endpoints: ____________ (I think these exist: _______)
- [ ] Missing features: ____________ (I think we need: _______)

**My understanding of the task**:
- I believe we need to: ____________
- I think this involves: ____________
- I assume the current state is: ____________

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?** (Check all that apply)

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel on different files/features
- [ ] Task duration >30 minutes (main branch may advance)
- [ ] Multi-component work (e.g., frontend + backend by different agents)
- [ ] Exploratory/risky changes where easy rollback is valuable
- [ ] Coordination queue prompt being claimed

Worktrees ADD overhead when:
- [ ] Single agent, sequential work
- [ ] Small fixes (<15 min)
- [ ] Tightly coupled files requiring atomic commits
- [ ] Time-critical work where setup overhead matters

**Assessment:**
- [ ] **USE WORKTREE** - 2+ parallel criteria checked
- [ ] **SKIP WORKTREE** - Overhead criteria dominate
- [ ] **PM DECISION** - Mixed signals, escalate

**If USE WORKTREE:**
```bash
# Agent claims prompt with worktree
./scripts/worktree-setup.sh <prompt-id> <session-id>
cd .trees/<prompt-id>-<session>/
```

**If SKIP WORKTREE:**
Document rationale: ____________
(e.g., "Single agent, 5 files, 15 min estimate - worktree overhead exceeds benefit")

### Part B: PM Verification Required

**PM, please correct/confirm the above and provide**:

1. **What actually exists in the filesystem?**
   ```bash
   ls -la web/
   ls -la services/
   ls -la cli/
   find . -name "*[relevant_feature]*"
   ```

2. **Recent work in this area?**
   - Last changes to this feature: ____________
   - Known issues/quirks: ____________
   - Previous attempts: ____________

3. **Actual task needed?**
   - [ ] Create new feature from scratch
   - [ ] Add to existing application
   - [ ] Fix broken functionality
   - [ ] Refactor existing code
   - [ ] Other: ____________

4. **Critical context I'm missing?**
   - ____________

### Part C: Proceed/Revise Decision

After PM verification:
- [ ] **PROCEED** - Understanding is correct, gameplan appropriate
- [ ] **REVISE** - Major assumptions wrong, need different approach
- [ ] **CLARIFY** - Need more context on: ____________

**If REVISE or CLARIFY checked, STOP and create new gameplan**

---

## Phase 0: Initial Bookending - GitHub Investigation

### Purpose
Establish context, verify issue exists, understand current state

### Required Actions

1. **GitHub Issue Verification**
   ```bash
   gh issue view [ISSUE_NUMBER]
   ```

2. **Codebase Investigation**
   ```bash
   # Find existing patterns
   grep -r "[pattern]" . --include="*.py"

   # Check git history
   git log --grep="[feature]" --oneline

   # Verify current state
   python main.py  # or appropriate test
   ```

3. **Update GitHub Issue**
   ```bash
   gh issue edit [ISSUE_NUMBER] --body "
   ## Status: Investigation Started
   - [ ] Current state documented
   - [ ] Root cause identified
   - [ ] Fix approach determined
   "
   ```

### STOP Conditions
- Issue doesn't exist or is wrong number
- Feature already implemented
- Different problem than described

---

## Phase 0.5: Frontend-Backend Contract Verification (MANDATORY for UI work)

### Purpose
Prevent path mismatches between backend routes and frontend API calls. This phase is REQUIRED when the issue involves both backend API routes AND frontend JavaScript/templates.

### When to Apply
- ✅ Creating new API endpoints + UI that calls them
- ✅ Modifying existing API paths
- ✅ Adding JavaScript that makes fetch() calls
- ❌ Backend-only changes (skip this phase)
- ❌ Frontend-only styling changes (skip this phase)

### Required Actions

#### 1. After Backend Routes Created, BEFORE Frontend Work
```bash
# Get all endpoint paths from new route file
grep -n "@router\." web/api/routes/[new_file].py

# Get the mount prefix from app.py or router_initializer.py
grep -n "include_router\|mount_router" web/app.py | grep [module_name]
# OR
grep -n "[module_name]" web/router_initializer.py
```

#### 2. Calculate Full Paths
```markdown
| Endpoint | Route Path | Mount Prefix | Full Path |
|----------|------------|--------------|-----------|
| status   | /status    | /setup       | /setup/status |
| create   | /create    | /api/v1/todos | /api/v1/todos/create |
```

#### 3. Verify Paths Work (Server Running)
```bash
# Test each endpoint BEFORE writing frontend
curl -s http://localhost:8001/[full-path]
# Must NOT return {"detail":"Not Found"}
```

#### 4. Static File Verification
```bash
# Verify where static files are served from
grep -n "StaticFiles" web/app.py
# Note the directory path (e.g., web/static vs static)

# If creating JS/CSS files, verify location matches
ls -la web/static/js/  # or wherever app.py points
```

### STOP Conditions
- If ANY endpoint returns 404 → fix backend before frontend
- If static file path is wrong → fix mount before creating files
- If mount prefix unclear → verify in app.py or ask PM

### Evidence Required
```bash
# Document verified paths in gameplan or session log
echo "Verified paths:"
echo "  /setup/status → HTTP 200"
echo "  /setup/check-system → HTTP 200"
echo "  Static files: web/static/ → /static/"
```

---

## Phases 1-N: Development Work with Progressive Bookending

### Multi-Agent Deployment (DEFAULT)

#### Phase [X]: [Specific Work Description]

**Deploy: Both Agents (Different Approaches)**

##### Claude Code Instructions
```markdown
[Broad investigation/implementation approach]
- Use subagents for parallel discovery
- Check patterns across codebase
- Find all related code
```

##### Cursor Instructions
```markdown
[Focused implementation approach]
- Specific files to modify
- Exact changes needed
- Targeted testing
```

### Progressive Bookending
After each subtask completion:
```bash
gh issue comment [ISSUE_NUMBER] -b "✓ Completed: [subtask]
Evidence: [link or output]"
```

## GitHub Progress Discipline (MANDATORY)
- Agents UPDATE progress descriptions
- PM VALIDATES by checking boxes
- Include "(PM will validate)" in criteria

## Test Scope Requirements in Acceptance Criteria
- [ ] Unit tests: [what components they test]
- [ ] Integration tests: [what flows they verify]
- [ ] Performance tests: [what metrics required]
- [ ] Regression tests: [what they prevent]

### Cross-Validation Points
- Agents share findings via GitHub
- Different approaches validate each other
- Evidence required from both

### Evidence Format
- Terminal output: paste key lines
- Test results: link to full output
- Commits: include hash
- Performance: include metrics

---

## Phase Z: Final Bookending & Handoff

### Purpose
Complete final verification, update all documentation, prepare for PM approval

### Required Actions

#### 1. GitHub Final Update
```bash
gh issue edit [ISSUE_NUMBER] --body "
## Status: Complete - Awaiting PM Approval

### Evidence Summary
- [x] All acceptance criteria met
- [x] Tests passing: [evidence]
- [x] No regressions: [evidence]
- [x] Documentation updated

### Ready for PM Review
"
```

## GitHub Closeout Discipline (MANDATORY)
- Agents provide evidence issue is completed
- PM VALIDATES and closes issue or identifies incomplete work or completed work claims without sufficient evidence

#### 2. Documentation Updates
- [ ] Update relevant ADRs if decisions made
- [ ] Update architecture.md if flow changed
- [ ] Remove/update misleading TODO comments
- [ ] Update CURRENT-STATE.md if significant

#### 3. Evidence Compilation
- [ ] All terminal outputs in session log
- [ ] Key code changes documented
- [ ] Before/after behavior captured
- [ ] Performance metrics if relevant

#### 4. Handoff Preparation (if part of sequence)
- [ ] Document discoveries for next issue
- [ ] Note unexpected complexities
- [ ] Flag architectural concerns
- [ ] Prepare context for next phase

#### 5. Session Completion
- [ ] Run satisfaction assessment
- [ ] Complete session log
- [ ] Note process improvements

#### 6. PM Approval Request
```markdown
@PM - Issue #[NUMBER] complete and ready for review:
- All acceptance criteria met ✓
- Evidence provided ✓
- Documentation updated ✓
- No regressions confirmed ✓

Please review and close if satisfied.
```

### CRITICAL: Agents Do NOT Close Issues
**Only PM closes issues after review and approval**

---

## STOP Conditions (Apply Throughout)

Stop immediately and escalate if:
- Infrastructure doesn't match gameplan
- Critical features break
- Performance degrades unacceptably
- Security issues discovered
- Assumptions prove wrong

---

## Evidence Requirements

### What Counts as Evidence
✅ Terminal output showing success
✅ Test results with full output
✅ Performance metrics
✅ Git commits/diffs
✅ Before/after screenshots

❌ "Should work"
❌ "Tests pass" without output
❌ "Fixed" without proof

---

## Success Criteria Template

### Issue Completion Requires
- [ ] All acceptance criteria met
- [ ] Evidence provided for each criterion
- [ ] Tests passing (with output)
- [ ] No regressions introduced
- [ ] Documentation updated
- [ ] GitHub issue fully updated
- [ ] PM approval received

---

## Session Patterns

### Starting a Session
1. Check BRIEFING-CURRENT-STATE
2. Review GitHub issue
3. Verify infrastructure (Phase -1)
4. Begin Phase 0

### During Work
- Progressive bookending
- Evidence collection
- Cross-validation
- GitHub updates

### Ending a Session
- Phase Z completion
- Satisfaction assessment
- Session log finalized
- Clear handoff if incomplete

---

## Remember

- **Inchworm Protocol**: Complete each phase 100% before moving
- **Evidence Required**: No claims without proof
- **75% Pattern**: Complete existing work, don't replace
- **Multi-Agent Default**: Single agent needs justification
- **PM Closes Issues**: Agents request approval only

---

*This template ensures systematic, complete execution following all methodology learnings*
