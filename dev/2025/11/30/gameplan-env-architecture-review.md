# Gameplan A: Environment Variable Architecture Review
**Created**: November 30, 2025, 5:10 PM PT
**Lead**: Claude Code Sonnet 4.5 (Lead Developer)
**Type**: Investigation → Decision → Implementation
**Related Threads**: Thread 1 (.env.example audit), Thread 2 (alpha setup), Thread 4 (post-pull docs)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Environment management: python-dotenv (verified in requirements.txt:154)
- [x] Secrets management: keyring library (secure keychain storage)
- [x] Configuration: .env files (gitignored, local only)
- [x] Setup wizard: scripts/setup_wizard.py (interactive setup)
- [x] Main entry point: main.py (now loads .env automatically as of v0.8.1.2)
- [x] Alpha docs: ALPHA_QUICKSTART.md (6-step setup including .env)

**My understanding of the task**:
- I believe we have TWO environment systems: .env files AND keyring/keychain storage
- I think these may be serving different purposes OR one is legacy from pre-keychain design
- I assume .env is for non-secret config (ports, debug flags) and keyring is for secrets (API keys, JWT)
- Current problem: .env.example doesn't include JWT_SECRET_KEY section → alpha testers confused
- Deeper problem: Unclear what SHOULD go in .env vs keyring

**My understanding of current state**:
- .env loading: NOW automatic (added in v0.8.1.2, commit c2f58743)
- .env.example: EXISTS but incomplete (missing JWT_SECRET_KEY guidance)
- Setup wizard: Creates keyring entries for API keys
- JWT_SECRET_KEY: Required in .env but not documented in .env.example
- Alpha tester experience: Confusion about environment setup, especially post-pull

### Part B: PM Verification Required

**PM, please correct/confirm the above and provide**:

1. **What is the INTENDED architecture?**
   - Should .env be temporary staging for wizard → keyring flow?
   - Should .env be permanent for non-secret config?
   - Should secrets EVER be in .env or ONLY in keyring?
   - Is the dual system intentional or legacy?

2. **Current behavior verification needed**:
   ```bash
   # On PM's alpha laptop
   ls -la .env .env.example
   cat .env.example  # What sections exist?
   python -c "import keyring; print(keyring.get_password('piper_morgan', 'jwt_secret_key'))"
   ```

3. **Setup wizard behavior**:
   - Does wizard create .env file?
   - Does wizard write to .env or only to keyring?
   - Does wizard prompt for JWT_SECRET_KEY?
   - Should wizard handle ALL environment setup?

4. **Alpha tester workflow intent**:
   - Should testers manually create .env? Or wizard handles it?
   - Should testers run wizard on every git pull? Or once at setup?
   - What SHOULD persist across git operations?

### Part C: Proceed/Revise Decision

**AWAITING PM ANSWERS** before proceeding to Phase 0.

Depending on answers, this gameplan may need:
- [ ] **PROCEED** - Current approach is correct, just need to complete .env.example
- [ ] **REVISE** - Need to refactor .env → keyring migration strategy
- [ ] **CLARIFY** - Need architectural decision on .env vs keyring boundaries

---

## Phase 0: Initial Investigation (AFTER PM Approval)

### Purpose
Map current state of environment variable usage across codebase and documentation.

### Required Actions

1. **Map .env Usage**
   ```bash
   # Find all references to environment variables
   grep -r "os.getenv\|os.environ" . --include="*.py" | tee /tmp/env-getenv-usage.txt
   grep -r "load_dotenv" . --include="*.py" | tee /tmp/env-dotenv-usage.txt

   # Find all .env file operations
   grep -r "\.env" docs/ --include="*.md" | tee /tmp/env-doc-references.txt
   ```

2. **Map Keyring Usage**
   ```bash
   # Find all keyring operations
   grep -r "keyring\." . --include="*.py" | tee /tmp/keyring-usage.txt

   # Analyze setup wizard keyring flow
   cat scripts/setup_wizard.py | grep -A 5 -B 5 "keyring"
   ```

3. **Read Current .env.example**
   ```bash
   cat .env.example
   ```

4. **Analyze Setup Wizard Flow**
   ```bash
   # Read full setup wizard to understand current behavior
   cat scripts/setup_wizard.py
   ```

5. **Create Findings Document**
   Create `/dev/2025/11/30/env-architecture-findings.md` with:
   - What's currently stored in .env vs keyring
   - How setup wizard handles environment setup
   - What's documented vs what's implemented
   - Gaps and inconsistencies
   - Security concerns (if any)

### STOP Conditions
- Discover secrets being stored in .env files (security issue)
- Find evidence of broken keyring flow
- Discover .env and keyring storing same values (redundancy issue)

### Output Deliverable
Complete findings document with **questions for PM** before proposing any solutions.

---

## Phase 1: PM Decision Point (MANDATORY STOP)

### Purpose
Present findings to PM and get architectural decisions before proceeding.

### Required Actions

1. **Present Findings Document**
   - Current state analysis
   - Discovered issues
   - Security concerns (if any)

2. **Get PM Decisions On**:
   - What belongs in .env vs keyring?
   - Should .env → keyring be one-time migration or permanent dual system?
   - Should setup wizard manage .env creation?
   - Should secrets ever touch .env files?
   - What's the alpha tester ideal workflow?

3. **Document Decisions**
   Add PM's decisions to findings document under "## Architectural Decisions" section.

### STOP Condition
**DO NOT PROCEED TO PHASE 2 WITHOUT EXPLICIT PM APPROVAL AND DECISIONS**

---

## Phase 2: Implementation (ONLY After PM Approval)

### Purpose
Implement approved changes to .env.example, setup wizard, and documentation.

### Subtasks (Specific tasks depend on Phase 1 decisions)

**Likely tasks** (adjust based on PM decisions):

#### 2.1: Update .env.example
- [ ] Add JWT_SECRET_KEY section with clear instructions
- [ ] Add generation command: `openssl rand -hex 32`
- [ ] Clarify what goes in .env vs keyring
- [ ] Add comments explaining purpose of each section
- [ ] Remove any legacy/unused sections
- [ ] Test: Can alpha tester follow instructions?

#### 2.2: Update Setup Wizard (if needed)
- [ ] Ensure wizard creates .env file (if decided)
- [ ] Ensure wizard prompts for JWT_SECRET_KEY (if decided)
- [ ] Ensure wizard explains .env vs keyring (if decided)
- [ ] Test: Does wizard behavior match documentation?

#### 2.3: Update ALPHA_QUICKSTART.md
- [ ] Revise Step 2 (environment setup) to match new flow
- [ ] Clarify wizard behavior
- [ ] Update troubleshooting section
- [ ] Test: Can new alpha tester follow instructions?

#### 2.4: Update AFTER-GIT-PULL.md
- [ ] Add .env verification step
- [ ] Add "what should persist" section
- [ ] Add "when to re-run wizard" guidance
- [ ] Test: Does post-pull workflow make sense?

### Evidence Requirements
- [ ] Terminal output showing wizard creating .env (if applicable)
- [ ] Diff of .env.example changes
- [ ] Diff of documentation changes
- [ ] Fresh-eyes test: Can someone follow updated instructions?

### STOP Conditions
- Changes break existing alpha tester setups
- Security regressions (secrets in .env)
- Wizard errors during testing

---

## Phase Z: Final Validation & Handoff

### Required Actions

#### 1. Testing Validation
- [ ] Clean environment test: Follow ALPHA_QUICKSTART.md from scratch
- [ ] Existing environment test: Follow AFTER-GIT-PULL.md procedure
- [ ] Wizard test: Run setup wizard, verify .env handling
- [ ] Document results in session log

#### 2. Documentation Completeness
- [ ] .env.example updated and clear
- [ ] ALPHA_QUICKSTART.md reflects new flow
- [ ] AFTER-GIT-PULL.md reflects new flow
- [ ] No conflicting instructions across docs

#### 3. Security Review
- [ ] No secrets in .env.example
- [ ] Clear warnings about not committing .env
- [ ] Keyring usage correct and secure
- [ ] Document security boundaries

#### 4. Evidence Compilation
- [ ] Terminal outputs from all test scenarios
- [ ] Diffs of all changed files
- [ ] Before/after workflow comparison
- [ ] Session log updated with findings

#### 5. PM Approval Request
```markdown
@PM - Environment architecture review complete:

**Findings Summary**:
- [Summary of current state]
- [Decisions made based on your guidance]

**Changes Implemented**:
- .env.example: [changes]
- Setup wizard: [changes]
- Documentation: [changes]

**Testing Results**:
- Fresh setup: [evidence]
- Post-pull workflow: [evidence]
- Security validation: [evidence]

All changes aligned with your Phase 1 decisions.
Ready for your review and approval.
```

---

## Success Criteria

### Investigation Phase Complete When:
- [ ] All .env usage mapped
- [ ] All keyring usage mapped
- [ ] Current state documented with evidence
- [ ] Questions prepared for PM
- [ ] Findings document ready for review

### Implementation Phase Complete When:
- [ ] All PM-approved changes implemented
- [ ] .env.example complete and clear
- [ ] Setup wizard behavior matches documentation
- [ ] Alpha docs updated and consistent
- [ ] Fresh setup tested successfully
- [ ] Post-pull workflow tested successfully
- [ ] No security regressions
- [ ] PM approval received

---

## Dependencies

**Blocks**:
- Gameplan B (Thread 2): Alpha setup instructions - depends on this gameplan's decisions
- Gameplan D (Thread 4): Post-pull docs - depends on this gameplan's decisions

**Blocked By**:
- PM decisions in Phase 1

**Runs in Parallel With**:
- Gameplan C (Thread 3): .env forensics investigation
- Gameplan E (Thread 6): Release notes and ADR cleanup

---

## Agent Assignment

**Phase 0 (Investigation)**:
- Lead: Claude Code Sonnet 4.5 (me)
- Subagent: Explore agent (Sonnet) for pattern discovery
- Model rationale: Investigation requires synthesis and judgment

**Phase 1 (Decisions)**:
- PM only (human decisions required)

**Phase 2 (Implementation)**:
- Lead: Claude Code Sonnet 4.5 (me)
- Rationale: Needs context from investigation, UX sensitivity

**Phase Z (Validation)**:
- Lead: Claude Code Sonnet 4.5 (me)
- Rationale: End-to-end understanding required

---

## STOP Conditions (Apply Throughout)

Stop immediately and escalate if:
- [ ] Secrets found in .env files (security issue)
- [ ] Keyring flow broken or inaccessible
- [ ] Changes would break existing alpha testers
- [ ] Documentation conflicts cannot be resolved
- [ ] PM decisions needed before proceeding
- [ ] Evidence contradicts assumptions

---

## Notes

**Why this is critical**:
- Alpha testers currently confused about environment setup
- .env mysteriously disappeared from PM's alpha laptop
- .env.example incomplete
- Unclear boundary between .env and keyring
- Risk of security anti-patterns if not architected correctly

**Success means**:
- Clear, documented architecture for environment variables
- Alpha testers can set up without confusion
- Environment persists correctly across git operations
- Security boundaries enforced
- Wizard automates what it should

**This gameplan follows Investigation → Decision → Implementation pattern with mandatory PM stop point before solutions.**
