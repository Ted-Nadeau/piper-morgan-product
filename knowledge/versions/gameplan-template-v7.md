# Gameplan Template v7.0 - Full Methodology Enforcement
*Incorporates all lessons from September 2025*

## 🛑 INFRASTRUCTURE VERIFICATION CHECKPOINT (MANDATORY) 🛑

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

## Multi-Agent Deployment Strategy (MANDATORY)

### Default: Always Deploy Multiple Agents
**Single-agent deployment requires explicit justification**

### Agent Division Template
```markdown
## Phase [X]: [Phase Name] - Multi-Agent Deployment

### Claude Code - Investigation & Broad Work
- Discovery tasks using subagents when available
- Pattern finding across codebase
- Architecture mapping
- GitHub bookending responsibility

### Cursor Agent - Implementation & Testing
- Specific file modifications
- Test creation and execution
- UI/UX adjustments
- Cross-validation of Code's work

### Coordination Points
- Share findings via GitHub issue
- Cross-validate at logical junctures (not arbitrary times)
- Handoff document if sequential work
```

---

## GitHub Tracking Requirements (MANDATORY)

### Before Starting Work
```bash
# Update issue description with starting status
gh issue edit [ISSUE#] --body "
## Status: Starting Investigation
- [ ] Phase 0: Investigation
- [ ] Phase 1: [Next phase]
- [ ] Phase 2: [Next phase]

Starting: [timestamp]
Agent: [Claude Code/Cursor]
"
```

### During Work (At Logical Checkpoints)
```bash
# Update checkboxes in DESCRIPTION (not comments!)
gh issue edit [ISSUE#] --body "
## Status: Phase 1 in Progress
- [x] Phase 0: Investigation ✅ [evidence link]
- [ ] Phase 1: Implementation [in progress]
- [ ] Phase 2: Verification

Last Update: [timestamp]
Current: [what's being done]
"
```

### After Completion
```bash
# Final update with all evidence
gh issue edit [ISSUE#] --body "
## Status: Complete
- [x] Phase 0: Investigation ✅ [terminal output]
- [x] Phase 1: Implementation ✅ [test results]
- [x] Phase 2: Verification ✅ [cross-validation]

Completed: [timestamp]
Evidence: [links to all proof]
"
```

---

## Phase -1: MANDATORY EXISTING ARCHITECTURE CHECK

**BEFORE CREATING THIS GAMEPLAN, VERIFY:**

```bash
# 1. Search project knowledge for existing solutions
project_knowledge_search: "[feature name]"

# 2. Check conversation history
conversation_search: "[feature] implementation"

# 3. Review specifications
ls -la specs/
grep -r "[feature]" specs/

# 4. Check for existing implementations
grep -r "[functionality]" services/ --include="*.py"
find . -name "*[feature]*" -type f

# 5. Review configuration files
cat config/PIPER.user.md
cat config/*.yaml config/*.json 2>/dev/null

# 6. Consult TDD guidance
# Reference: tdd-pragmatic-approach.md in project knowledge
```

**Document What Already Exists**:
- Existing architecture for this feature: ___________
- Previous implementations found: ___________
- Configuration already available: ___________
- Related ADRs or patterns: ___________

**STOP if significant existing architecture found** - Don't reinvent!

---

## System Context Assessment

**CRITICAL: Is this a LIVE SYSTEM or GREENFIELD?**

### Live System Checklist
- [ ] User data currently exists that must be preserved
- [ ] Existing configuration files in use
- [ ] Active integrations that can't break
- [ ] Production data that needs migration
- [ ] Server processes currently running

### If Live System:
```bash
# MANDATORY: Check running processes
ps aux | grep python
ps aux | grep piper

# MANDATORY: Backup existing configuration
cp config/PIPER.user.md config/PIPER.user.md.backup.$(date +%Y%m%d)
cp -r config/ config.backup.$(date +%Y%m%d)/

# Document current state
echo "Current user config:" > current_state.md
cat config/PIPER.user.md >> current_state.md
```

**User Data Preservation Requirements**:
- Files that must not be deleted: ___________
- Settings that must be preserved: ___________
- Integrations that must continue working: ___________

---

## MANDATORY METHODOLOGY REQUIREMENTS
Before creating any gameplan, verify:
- [ ] Infrastructure verification checkpoint completed with PM
- [ ] Multi-agent deployment strategy defined
- [ ] GitHub bookending instructions included for all phases
- [ ] Phase -1 existing architecture check complete
- [ ] System context (live vs greenfield) assessed
- [ ] Test strategy selected (TDD preferred, see below)
- [ ] Verification Pyramid: All 3 tiers specified below
- [ ] Handoff Protocol: Evidence requirements defined
- [ ] Cross-Validation: Independent agent verification planned
- [ ] STOP Conditions: At least 12 specified
- [ ] Resource awareness: ADRs and patterns referenced

---

## Mission Statement
[Clear, specific objective that can be verified as complete]

**GitHub Issue**: #[NUMBER] - [TITLE]

---

## Phase 0: Investigation & Setup (ALWAYS REQUIRED)

### Multi-Agent Deployment
- **Claude Code**: Broad investigation using subagents when available
- **Cursor Agent**: Test infrastructure setup in parallel

### GitHub Bookending - Start
```bash
gh issue edit [ISSUE#] --body "
## Starting Phase 0: Investigation
- [ ] Infrastructure verified with PM
- [ ] Check existing architecture
- [ ] Review patterns
- [ ] Investigate current state

Agent: [Claude Code/Cursor]
Started: $(date)
"
```

### Investigation Commands
```bash
# 0. FIRST - Check resource locations
cat docs/development/methodology-core/resource-map.md

# 1. GitHub Verification
gh issue view [ISSUE_NUMBER]

# 2. Pattern Discovery
grep -r "[relevant_pattern]" services/ --include="*.py"
cat docs/patterns/README.md | grep -i "[feature]"

# 3. ADR Review (34+ exist in docs/architecture/decisions/)
ls -la docs/architecture/decisions/
grep -r "[feature]" docs/architecture/decisions/

# 4. Configuration Check
cat config/settings.py | grep "[relevant_setting]"
cat config/PIPER.user.md  # Check user configuration

# 5. Existing Implementation Search
find services/ -name "*[feature]*" -type f

# 6. Server State Check (NEW)
ps aux | grep python
ps aux | grep piper
```

### GitHub Bookending - Phase 0 Complete
```bash
gh issue edit [ISSUE#] --body "
## Phase 0: Investigation ✅
- [x] Infrastructure verified with PM
- [x] Existing architecture checked
- [x] Patterns reviewed
- [x] Current state documented

Findings: [summary]
Next: Phase 1
"
```

**STOP CONDITIONS for Phase 0**:
- If infrastructure doesn't match gameplan → Report immediately
- If pattern already exists → Use it, don't duplicate
- If ADR conflicts with approach → Follow ADR
- If configuration unclear → Escalate for clarification
- If user data at risk → Stop and preserve first

---

## Phase 1: Test Strategy Selection (MANDATORY)

### Choose Testing Approach:

#### Option A: Test-Driven Development (Preferred)
```markdown
Multi-Agent Deployment:
- Claude Code: Write failing test suites
- Cursor: Set up test infrastructure

Steps:
- [ ] Write failing test that defines requirement
- [ ] Implement minimal code to pass test
- [ ] Verify test passes with evidence
- [ ] Refactor while keeping tests green
```

**Use when**: Requirements clear, building new features, fixing bugs

#### Option B: Exploratory Then Test (When Appropriate)
```markdown
Multi-Agent Deployment:
- Claude Code: Explore approach with subagents
- Cursor: Document findings and patterns

Steps:
- [ ] Explore solution approach
- [ ] Document discoveries in session log
- [ ] Write comprehensive tests immediately
- [ ] Verify all behaviors covered
```

**Use when**: API behavior unknown, UI prototyping, spike investigations
**Justification required**: [Why TDD not appropriate for this case]

### Testing Requirements (Regardless of Approach)
- [ ] Unit tests for core logic
- [ ] Integration tests for component interactions
- [ ] Error case handling tests
- [ ] Edge case boundary tests
- [ ] End-to-end browser tests for UI claims (NEW)

**Reference**: See `tdd-pragmatic-approach.md` in project knowledge for detailed guidance

---

## Verification Pyramid (MANDATORY FOR ALL WORK)

### Tier 1: Basic Validation ✓
- [ ] Unit tests pass with output
- [ ] Terminal output captured
- [ ] Session logs created and updated (.md format)
- [ ] No errors in implementation
- [ ] GitHub checkboxes updated
- [ ] Git commits verified with `git log --oneline -1` (NEW)

### Tier 2: Integration Testing ✓✓
- [ ] Cross-feature validation performed
- [ ] Performance metrics captured (actual numbers)
- [ ] Error handling verified with test cases
- [ ] Dependencies properly integrated
- [ ] GitHub evidence linked
- [ ] Server state verified with `ps aux | grep python` (NEW)

### Tier 3: System Validation ✓✓✓
- [ ] End-to-end testing complete
- [ ] User workflow works in UI (browser testing required)
- [ ] Production readiness verified
- [ ] No regressions introduced
- [ ] User data preserved (if live system)
- [ ] GitHub issue fully documented
- [ ] Screenshots/visual proof for UI claims (NEW)

---

## Implementation Phases

### Phase 2: Implementation (Multi-Agent Required)

#### GitHub Bookending - Start Phase 2
```bash
gh issue edit [ISSUE#] --body "
## Status: Phase 2 Starting
- [x] Phase 0: Investigation ✅
- [x] Phase 1: Test Development ✅
- [ ] Phase 2: Implementation [in progress]

Current: Multi-agent implementation
Claude Code: [specific tasks]
Cursor Agent: [specific tasks]
"
```

#### Multi-Agent Division
- **Claude Code**: Core implementation, services, orchestration
- **Cursor**: UI, tests, documentation

[Implementation approach details]

#### GitHub Bookending - Complete Phase 2
```bash
gh issue edit [ISSUE#] --body "
## Status: Phase 2 Complete
- [x] Phase 0: Investigation ✅
- [x] Phase 1: Test Development ✅
- [x] Phase 2: Implementation ✅ [link to code]

Implementation complete
Ready for verification
"
```

### Phase 3: Verification (Cross-Agent Validation)

#### Multi-Agent Cross-Validation
- **Claude Code**: Validates Cursor's implementation
- **Cursor**: Validates Code's implementation
- **Both**: Report findings in GitHub

[Verification approach]

---

## Evidence Requirements (STRENGTHENED)

### For ALL Claims:
- **"Created file X"** → Show `cat X` output + update GitHub
- **"Implemented method Y"** → Show it running + link in GitHub
- **"Fixed issue Z"** → Show before/after + checkbox in GitHub
- **"Integration works"** → Show end-to-end test + final GitHub update
- **"Committed changes"** → Show `git log --oneline -1` output (NEW)
- **"Server updated"** → Show `ps aux | grep python` output (NEW)
- **"UI works"** → Provide screenshot or browser test output (NEW)

### NO Acceptances Without:
- Terminal output proving functionality
- File diffs showing changes
- Test results with pass counts
- Independent verification
- GitHub issue updated with evidence
- Git commit verification (NEW)
- Server state confirmation (NEW)

### Completion Bias Prevention (NEW)
- **Never guess! Always verify first!**
- **No "should work" - only "here's proof it works"**
- **No "probably fixed" - only "here's evidence it's fixed"**
- **No assumptions - only verified facts**

---

## Handoff Protocol Requirements

Before ANY handoff between agents or sessions:
- [ ] GitHub issue updated with evidence (in DESCRIPTION, not comments!)
- [ ] All checkboxes reflect current state
- [ ] Evidence links added to checkboxes
- [ ] Terminal outputs provided in session log
- [ ] Test results documented with pass/fail counts
- [ ] Session log current with latest status (.md format)
- [ ] Next steps clearly defined in GitHub
- [ ] Blockers identified and escalated
- [ ] User data preservation verified (if applicable)
- [ ] Git status clean (all changes committed)
- [ ] Server state documented

---

## Cross-Validation Framework (NOW MANDATORY)

### Required for:
- Multi-scope implementations
- Configuration or architecture changes
- Any integration between systems
- Claims of file creation or method implementation

### Independent Verification Protocol
1. **Claude Code implements** → updates GitHub → provides evidence
2. **Cursor Agent independently verifies** → checks GitHub → provides counter-evidence
3. **Both must agree** on:
   - Core functionality works
   - Tests actually pass (not just claim they do)
   - Performance meets requirements
   - GitHub properly updated (checkboxes in description!)
   - User data preserved (if applicable)

### Discrepancy Resolution
If agents disagree:
- Document specific discrepancy in GitHub
- Provide evidence from both sides
- Escalate to Lead Developer
- Do not proceed until resolved

### Validation Timing (UPDATED)
- At logical junctures, not arbitrary 30-minute intervals
- After completing major phases
- Before significant architectural changes
- When encountering unexpected behavior

---

## Agent-Specific Instructions

### Claude Code
- **Multi-Agent Capabilities**:
  - Use subagents when available for parallel work
  - Coordinate parallel investigations
  - Share findings for Cursor implementation
- **GitHub Responsibilities**:
  - Update issue description at logical checkpoints
  - Check boxes as tasks complete (IN DESCRIPTION!)
  - Add evidence links to checkboxes
  - Never just comment - always edit description
- **Resources to Check**:
  - ADRs in `docs/architecture/decisions/` (34+ exist!)
  - Pattern Catalog: `docs/patterns/README.md`
  - TDD guidance: `tdd-pragmatic-approach.md`
  - Existing services: `services/` directory
  - User configuration: `config/PIPER.user.md`
- **Infrastructure Verification**:
  - If gameplan assumptions seem wrong, verify immediately
  - Ask PM for filesystem confirmation rather than guessing
- **Session Log**:
  - Create as YYYY-MM-DD-HHMM-claude-code-log.md (not .txt!)
- **Focus Areas**: [Specific to this task]

### Cursor Agent
- **Multi-Agent Coordination**:
  - Work in parallel with Claude Code
  - Implement based on Code's discoveries
  - Cross-validate Code's work
- **GitHub Responsibilities**:
  - Verify Code's GitHub updates are accurate
  - Add own evidence to checkboxes
  - Report if checkboxes don't match reality
  - Keep description current with progress
- **Constraints**:
  - Work only in these files: [explicit list]
  - Check `services/shared_types.py` for enums
  - Stay in assigned lane (no scope creep)
  - Preserve user configuration
- **Verification Role**:
  - Independently verify Code's work
  - Report discrepancies immediately
  - Provide counter-evidence
- **Infrastructure Verification**:
  - If filesystem doesn't match expectations, report immediately
  - Don't proceed on assumptions
- **Session Log**:
  - Create as YYYY-MM-DD-HHMM-cursor-log.md (not .txt!)
- **Focus Areas**: [Specific to this task]

---

## STOP Conditions (MANDATORY - EXPANDED)

Agents must STOP and request guidance if:
1. ❌ **Infrastructure doesn't match gameplan** - Reality check failed
2. ❌ **Pattern might already exist** - Check catalog first
3. ❌ **Tests fail for any reason** - Don't proceed with "acceptable" failures
4. ❌ **Configuration assumptions needed** - Never assume, always verify
5. ❌ **GitHub issue doesn't exist** - Don't create ad-hoc
6. ❌ **Verification evidence cannot be provided** - No evidence = not done
7. ❌ **ADR conflicts with approach** - ADRs are authoritative
8. ❌ **Resource not found after searching** - Escalate before creating new
9. ❌ **User data at risk** - Preserve before proceeding
10. ❌ **Completion bias detected** - Evidence required, not claims
11. ❌ **GitHub not updating properly** - Fix before continuing
12. ❌ **Single agent seems sufficient** - Justify why multi-agent not needed
13. ❌ **Git commits failing** - Don't proceed without version control (NEW)
14. ❌ **Server state unclear** - Verify what's actually running (NEW)
15. ❌ **UI behavior not visually confirmed** - Need screenshot/test (NEW)

---

## Success Criteria

- [ ] Infrastructure verified with PM before planning
- [ ] Multi-agent deployment utilized effectively
- [ ] All three tiers of Verification Pyramid complete
- [ ] GitHub issue shows completed checkboxes WITH evidence IN DESCRIPTION
- [ ] Progressive bookending performed throughout
- [ ] Test strategy followed (TDD or justified alternative)
- [ ] Cross-validation performed and documented
- [ ] No assumptions made (all verified)
- [ ] Session logs complete with handoff ready (.md format)
- [ ] Documentation updated where needed
- [ ] End-to-end testing confirms functionality
- [ ] User data preserved (if live system)
- [ ] Evidence provided for every claim
- [ ] Git commits verified with log output
- [ ] Server state confirmed with process checks
- [ ] UI claims backed by visual evidence

---

## Configuration Considerations

### Piper Core vs User Config
- **Piper Capability**: [Generic capability that any user could use]
- **User Configuration**: [User-specific implementation details]
- **Hardcoding Risks**: [What should NOT be hardcoded]
- **Config Location**: [Where configuration should live]

Example:
- Piper: "Add issues to tracking systems"
- User Config: "xian uses GitHub with PM-XXX format"

---

## Time Estimates
- Infrastructure Verification: ___ minutes (with PM)
- Phase -1: ___ minutes (existing architecture check)
- Phase 0: ___ minutes (investigation) + GitHub updates
- Phase 1: ___ minutes (test strategy) + GitHub updates
- Phase 2: ___ minutes (implementation) + GitHub updates
- Phase 3: ___ minutes (verification) + GitHub updates
- Phase 4: ___ minutes (documentation) + GitHub updates
- **Total**: ___ minutes (including bookending)

---

## Notes for Lead Developer

### Emergency Infrastructure Check
If gameplan lacks infrastructure verification:
- **STOP immediately**
- Run 5-minute filesystem check
- Report discrepancies to Chief Architect
- Get revised gameplan before proceeding

### Multi-Agent Deployment Enforcement
- **DEFAULT TO MULTI-AGENT** - Single agent requires justification
- Deploy agents in parallel when possible
- Use Code's subagent capability for broad work
- Coordinate through GitHub issue updates

### GitHub Tracking Enforcement
- **CRITICAL**: Ensure agents update issue description, not comments
- Monitor for checkbox updates at logical checkpoints
- Verify evidence links are added to checkboxes
- Escalate if GitHub tracking falls behind

### Deployment Strategy
- Check infrastructure verification completed
- Deploy agents only AFTER Phase 0 complete
- Verify GitHub bookending started
- Use parallel deployment when tasks are independent
- Cross-validate at logical junctures
- Escalate STOP conditions immediately

### Resource Awareness Check
Before deploying agents, verify they know:
- [ ] Infrastructure verified with PM
- [ ] Multi-agent coordination requirements
- [ ] GitHub bookending requirements
- [ ] TDD guidance location (tdd-pragmatic-approach.md)
- [ ] Where ADRs are located
- [ ] How to search pattern catalog
- [ ] Where to find existing services
- [ ] How to check for existing implementations
- [ ] User data preservation requirements
- [ ] Session log format (.md not .txt)
- [ ] Git workflow discipline requirements
- [ ] Server state verification needs

### Quality Gates
- ✅ Infrastructure verification complete with PM
- ✅ Phase -1 shows no conflicting architecture
- ✅ Phase 0 investigation shows no conflicts
- ✅ Multi-agent strategy defined
- ✅ GitHub bookending started properly
- ✅ Test strategy selected and justified
- ✅ All tests written before implementation (or justification provided)
- ✅ Implementation passes all three pyramid tiers
- ✅ Cross-validation confirms both agents agree
- ✅ Documentation and GitHub updated
- ✅ User data preserved (if applicable)
- ✅ Final GitHub update complete with all evidence
- ✅ Git commits verified
- ✅ Server state documented
- ✅ UI claims have visual proof

---

## Session Completion

### Session Satisfaction Check (For PM)
At session end, add to session log:

```markdown
## Session Satisfaction

**Value**: [What shipped?]
**Process**: [Methodology smooth?]
**Feel**: [Energizing/OK/Draining]
**Learned**: [Key insight]
**Tomorrow**: [Next steps clear?]

**Overall**: 😊 / 🙂 / 😐 / 😕 / 😞
```

---

*Template Version: 7.0*
*Major Updates: Incorporated all September 2025 learnings*
*Last Updated: September 16, 2025*
*Key Additions: Git workflow, server state, UI evidence, completion bias prevention*
