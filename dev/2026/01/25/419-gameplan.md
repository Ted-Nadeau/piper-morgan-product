# Gameplan: #419 MUX-NAV-HOME - Home State Design

**Issue**: #419
**Priority**: P1
**Sprint**: P1 (Navigation Paradigm)
**Epic**: #418 MUX-IMPLEMENT
**Created**: 2026-01-25

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (confirmed via `web/app.py`)
- [x] CLI structure: Click (confirmed via `main.py`)
- [x] Database: PostgreSQL on port 5433 (confirmed via docker-compose)
- [x] Testing framework: pytest (confirmed via pytest.ini)
- [x] Existing endpoints: `/` home route in `web/api/routes/ui.py`
- [x] Missing features: Trust-gated home state content

**My understanding of the task**:
- I believe we need to: Transform the home page from a static greeting to a trust-gated, consciousness-aware experience
- I think this involves: Adding trust_stage to home route, creating HardnessLevel enum, creating HomeStateService, updating template
- I assume the current state is: Home page has time-based greeting but no trust awareness

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel on different files/features
- [ ] Task duration >30 minutes (main branch may advance)
- [ ] Multi-component work (e.g., frontend + backend by different agents)
- [ ] Exploratory/risky changes where easy rollback is valuable
- [ ] Coordination queue prompt being claimed

Worktrees ADD overhead when:
- [x] Single agent, sequential work
- [ ] Small fixes (<15 min)
- [x] Tightly coupled files requiring atomic commits
- [ ] Time-critical work where setup overhead matters

**Assessment:**
- [x] **SKIP WORKTREE** - Overhead criteria dominate
- Document rationale: Single Lead Dev implementing, tightly coupled service + template changes requiring atomic commits, previous implementation already exists (may reuse)

### Part B: PM Verification Required

**PM, please correct/confirm the above and provide**:

1. **What actually exists in the filesystem?**
   ```bash
   # Home route
   ls -la web/api/routes/ui.py  # Contains home route at /

   # Trust service (VERIFIED EXISTS)
   ls -la services/trust/trust_computation_service.py  # TrustComputationService

   # Existing implementation from earlier session (VERIFIED EXISTS)
   ls -la services/home/  # HomeStateService already created
   ls -la services/shared_types.py  # HardnessLevel already added
   ```

2. **Recent work in this area?**
   - Last changes: Earlier today - full implementation created before proper audit cascade
   - Known issues: Implementation done without gameplan audit
   - Previous attempts: Complete implementation exists, needs verification against requirements

3. **Actual task needed?**
   - [ ] Create new feature from scratch
   - [x] Add to existing application
   - [ ] Fix broken functionality
   - [ ] Refactor existing code
   - Note: May need to verify/adjust existing implementation against audited requirements

4. **Critical context I'm missing?**
   - None identified - infrastructure verified in earlier session

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Understanding is correct, existing implementation may satisfy requirements
- [ ] **REVISE** - Major assumptions wrong
- [ ] **CLARIFY** - Need more context

---

## Phase 0: Initial Bookending - GitHub Investigation

### Required Actions

1. **GitHub Issue Verification**
   ```bash
   gh issue view 419
   ```
   - Issue exists and was updated with restructured content today
   - Status: Not Started (per issue description)

2. **Codebase Investigation**
   ```bash
   # Check existing implementation
   cat services/home/home_state_service.py  # HomeStateService exists
   cat services/shared_types.py | grep -A 20 "class HardnessLevel"  # Enum exists
   grep -n "trust_stage" web/api/routes/ui.py  # Check if trust added to route

   # Find patterns
   grep -r "TrustComputationService" services/ --include="*.py"  # Usage patterns
   ```

3. **Existing Implementation Inventory**
   - `services/home/__init__.py` - Module init
   - `services/home/home_state_service.py` - HomeStateService with context/result dataclasses
   - `services/shared_types.py` - HardnessLevel enum added
   - `web/api/routes/ui.py` - Trust stage added to home route
   - `templates/home.html` - Trust-gated greeting subtext
   - `tests/unit/services/home/test_home_state_service.py` - Tests exist
   - `tests/unit/services/test_hardness_level.py` - Tests exist
   - `tests/unit/web/api/routes/test_ui_home.py` - Tests exist

4. **Update GitHub Issue**
   ```bash
   gh issue edit 419 --body "$(cat dev/2026/01/25/419-issue-restructured.md)"
   # Status update to "Investigation Complete"
   ```

### STOP Conditions Check
- [x] Issue exists: #419 confirmed
- [x] Feature not already complete: Implementation exists but needs verification
- [x] Problem matches description: Yes - home page trust awareness

---

## Phase 0.5: Frontend-Backend Contract Verification

### When to Apply
- [x] Creating new API endpoints + UI that calls them - NO (using existing home route)
- [ ] Modifying existing API paths - NO
- [x] Adding JavaScript that makes fetch() calls - MINIMAL (window.trustStage global only)

### Required Actions

#### 1. Verify Home Route Path
```bash
# Get endpoint path
grep -n "@router\." web/api/routes/ui.py | grep home
# Expected: @router.get("/") for home

# Get mount prefix
grep -n "include_router" web/app.py | grep ui
# Expected: /api/v1 prefix or similar
```

#### 2. Path Verification
| Endpoint | Route Path | Mount Prefix | Full Path |
|----------|------------|--------------|-----------|
| home | / | /api/v1 | / (special case - root) |

#### 3. Template Data Verification
```bash
# Verify template receives trust_stage
grep -n "trust_stage" templates/home.html
# Should show usage in Jinja template
```

### STOP Conditions
- [ ] If trust_stage not in template context → fix route before template work
- [ ] If template syntax errors → fix before proceeding

---

## Phase 0.6: Data Flow & Integration Verification

### Part A: Data Flow Requirements

#### User Context Propagation

| Layer | Needs user_id? | Needs session_id? | Source of value |
|-------|----------------|-------------------|-----------------|
| Home route handler | [x] Yes | [ ] No | `get_current_user` dependency |
| TrustComputationService | [x] Yes | [ ] No | Parameter from route |
| HomeStateService | [x] Yes | [ ] No | Parameter from route |

**Verification Commands**:
```bash
# Check if route has user dependency
grep -n "get_current_user\|current_user" web/api/routes/ui.py

# Check if TrustComputationService accepts user_id
grep -n "get_trust_stage" services/trust/trust_computation_service.py

# Check if HomeStateService receives user context
grep -n "def generate" services/home/home_state_service.py
```

#### State Persistence
- [x] Where is state stored? Database (user_trust_profile table)
- [x] Key for lookup: `user_id`
- [x] How is state retrieved? TrustComputationService.get_trust_stage(user_id)
- [x] What happens if lookup fails? Default to TrustStage.NEW

### Part B: Integration Points Checklist

| Caller | Callee | Import Path Verified? | Method Name Verified? | Parameters Available? |
|--------|--------|----------------------|----------------------|----------------------|
| ui.py home route | TrustComputationService | [x] | [x] get_trust_stage | [x] user_id from JWT |
| ui.py home route | HomeStateService | [x] | [x] generate | [x] context from user |

### Part C: Pattern Adaptation Notes

**Reference Pattern**: Trust service usage in `services/intent_service/canonical_handlers.py:4212-4216`

| Aspect | Source Pattern | This Implementation | Why Different? |
|--------|---------------|---------------------|----------------|
| Service instantiation | Within session scope | Same | Consistency |
| User ID source | JWT claims | Same | Consistency |
| Error handling | Default to basic | Default to TrustStage.NEW | Graceful degradation |

### STOP Conditions
- [ ] If TrustComputationService import fails → verify path
- [ ] If get_trust_stage signature differs → verify parameters

---

## Phase 0.7: Conversation Design

**Not applicable** - This feature is not conversational. It's a page load state determination.
- [ ] Skip this phase: HOME STATE IS NOT A CONVERSATION FLOW

---

## Phase 0.8: Post-Completion Integration

### When to Apply
- [ ] Features that change user state - NO (read-only of trust state)
- [ ] Features that create/modify database records - NO
- [ ] Features that should affect other feature behavior - MINOR

### Completion Side-Effects

This feature is primarily read-only. It reads trust state, it does not modify it.

| Side Effect | Table/Field | Value | Verified? |
|-------------|-------------|-------|-----------|
| None - read only | N/A | N/A | [x] |

### Downstream Behavior Changes

| Feature | Before Completion | After Completion |
|---------|-------------------|------------------|
| Home greeting | Generic time-based | Trust-aware subtext |
| Home lens items | Not present | Always-present lenses |
| Home content | Static | Trust-gated by hardness |

---

## Phase 1: Trust Stage in Home Route

### Objective
Pass trust_stage to template context from home route.

### Deploy: Lead Developer (Single Agent)

**Justification**: Simple service integration, pattern already established in codebase.

### Tasks
- [ ] Import TrustComputationService in ui.py
- [ ] Import UserTrustProfileRepository
- [ ] Query trust stage within existing session scope
- [ ] Add trust_stage (int) and trust_stage_name (string) to template context
- [ ] Handle errors gracefully (default to TrustStage.NEW)

### Verification Commands
```bash
# Run unit tests
python -m pytest tests/unit/web/api/routes/test_ui_home.py -xvs

# Verify imports work
python -c "from services.trust.trust_computation_service import TrustComputationService; print('Import OK')"
```

### Evidence Required
- [ ] Test output: `pytest tests/unit/web/api/routes/test_ui_home.py -v`
- [ ] Import verification output
- [ ] Modified file: `web/api/routes/ui.py`

### STOP Conditions
- If TrustComputationService unavailable → verify service exists
- If import errors → check module structure

---

## Phase 2: HardnessLevel Enum

### Objective
Define object hardness classification for trust-gated visibility.

### Deploy: Lead Developer (Single Agent)

### Tasks
- [ ] Add HardnessLevel enum to shared_types.py (if not exists)
- [ ] Document trust-stage visibility rules in docstring
- [ ] Define 5 levels: HARDEST=5, HARD=4, MEDIUM=3, SOFT=2, SOFTEST=1
- [ ] Add visibility_for_stage() helper method

### Verification Commands
```bash
# Run unit tests
python -m pytest tests/unit/services/test_hardness_level.py -xvs

# Verify enum works
python -c "from services.shared_types import HardnessLevel; print(list(HardnessLevel))"
```

### Evidence Required
- [ ] Test output: `pytest tests/unit/services/test_hardness_level.py -v`
- [ ] Enum verification output
- [ ] Modified file: `services/shared_types.py`
- [ ] New test file: `tests/unit/services/test_hardness_level.py`

---

## Phase 3: HomeStateService

### Objective
Service to compose trust-gated home state content.

### Deploy: Lead Developer (Single Agent)

### Tasks
- [ ] Create `services/home/` module (if not exists)
- [ ] Implement HomeStateContext dataclass (Pattern-050 input)
- [ ] Implement HomeStateResult dataclass (Pattern-050 output)
- [ ] Implement HomeStateItem for individual items with hardness
- [ ] Implement HomeStateService with trust-gated filtering
- [ ] Add always-present lens items (HARDEST level)
- [ ] Add trust-appropriate greeting generation (4 variations)

### Pattern Compliance
- Pattern-050: Context/Result dataclass pair ✓
- ADR-053: Trust invisible to users, effects noticeable ✓

### Verification Commands
```bash
# Run unit tests
python -m pytest tests/unit/services/home/test_home_state_service.py -xvs

# Verify service instantiation
python -c "from services.home import HomeStateService; print('Service import OK')"
```

### Evidence Required
- [ ] Test output: `pytest tests/unit/services/home/test_home_state_service.py -v`
- [ ] Service verification output
- [ ] New files: `services/home/__init__.py`, `services/home/home_state_service.py`
- [ ] New test file: `tests/unit/services/home/test_home_state_service.py`

---

## Phase 4: Template Integration

### Objective
Update home.html with trust-gated content.

### Deploy: Lead Developer (Single Agent)

### Tasks
- [ ] Add trust_stage data attribute to greeting area
- [ ] Add trust-stage-aware greeting subtext (4 variations)
- [ ] Add CSS for consciousness-aware styling (if needed)
- [ ] Add window.trustStage JavaScript global for adaptive UI
- [ ] Verify template renders correctly at all trust stages

### Greeting Variations (from ADR-053 design)
| Trust Stage | Greeting Subtext |
|-------------|------------------|
| 1 (NEW) | "What can I help you with?" |
| 2 (BUILDING) | "I'm here to help." |
| 3 (ESTABLISHED) | "I noticed a few things while you were away." |
| 4 (TRUSTED) | "I've been thinking about your priorities." |

### Verification Commands
```bash
# Visual verification (requires server running)
python main.py &
curl -s http://localhost:8001/ | grep -A 5 "greeting-subtext"

# Template syntax check
python -c "from jinja2 import Environment, FileSystemLoader; env = Environment(loader=FileSystemLoader('templates')); t = env.get_template('home.html'); print('Template OK')"
```

### Evidence Required
- [ ] Template syntax verification
- [ ] Greeting subtext renders for each trust stage (manual or test)
- [ ] Modified file: `templates/home.html`

---

## Phase Z: Final Bookending & Handoff

### Required Actions

#### 1. Full Test Suite Verification
```bash
# Run all unit tests
python -m pytest tests/unit/ -v

# Verify no regressions
# Baseline: 4364 tests
```

#### 2. Acceptance Criteria Verification

**Functionality**
- [ ] Trust stage is queried from TrustComputationService on home page load
- [ ] Trust stage is passed to template as both int and name
- [ ] Greeting subtext varies by trust stage (4 distinct messages)
- [ ] HardnessLevel enum has 5 levels with documented visibility rules
- [ ] HomeStateService filters items by trust-gated hardness
- [ ] Lens items (HARDEST) are always present regardless of trust stage
- [ ] Error handling defaults to TrustStage.NEW gracefully

**Testing**
- [ ] Unit tests for trust stage in home route context
- [ ] Unit tests for HardnessLevel enum and comparisons
- [ ] Unit tests for HomeStateService (context, result, filtering, greetings)
- [ ] Template render test with all 4 trust stages
- [ ] Full unit test suite passes with no regressions

**Quality**
- [ ] No regressions introduced (baseline: 4364 tests passing)
- [ ] Code follows existing patterns
- [ ] Per ADR-053: Trust stage invisible to users, effects noticeable
- [ ] Anti-flattening test: Can describe using "Piper notices/shows" language

**Documentation**
- [ ] Code documentation (docstrings) complete
- [ ] Session log documents implementation decisions
- [ ] Issue updated with evidence before closure

#### 3. Evidence Compilation

All evidence to be added to GitHub issue #419:
- Test output for each phase
- Modified files list
- Commit hashes
- Verification commands and output

#### 4. GitHub Final Update
```bash
gh issue edit 419 --body "
## Status: Complete - Awaiting PM Approval

### Evidence Summary
- [x] All acceptance criteria met
- [x] Tests passing: [evidence link]
- [x] No regressions: [baseline comparison]
- [x] Documentation updated

### Ready for PM Review
"
```

### PM Approval Request

After all evidence compiled:
```markdown
@PM - Issue #419 complete and ready for review:
- All acceptance criteria met ✓
- Evidence provided ✓
- Documentation updated ✓
- No regressions confirmed ✓

Please review and close if satisfied.
```

---

## Multi-Agent Coordination Plan

### Agent Deployment Map

| Phase | Agent Type | Issue | Evidence Required | Handoff |
|-------|------------|-------|------------------|---------|
| 1-4 | Lead Developer | #419 | Tests, modified files | Phase Z |
| Z | Lead Developer | #419 | Full verification | PM Review |

**Single agent justified**: Sequential phases, tightly coupled changes, existing implementation to verify.

### Verification Gates
- [ ] Phase 1: Route tests passing
- [ ] Phase 2: Enum tests passing
- [ ] Phase 3: Service tests passing
- [ ] Phase 4: Template renders correctly
- [ ] Phase Z: Full suite, no regressions

---

## STOP Conditions (Apply Throughout)

Stop immediately and escalate if:
- Infrastructure doesn't match gameplan
- TrustComputationService unavailable or broken
- Trust stage query causes performance degradation (>500ms)
- Template changes break existing functionality
- Tests fail for any reason
- Cannot verify trust stage is actually computed (not hardcoded)
- User data exposure risk (trust stage leaking sensitive info)
- Completion bias detected (claiming done without all criteria met)

---

## Success Criteria

### Issue Completion Requires
- [ ] All acceptance criteria met
- [ ] Evidence provided for each criterion
- [ ] Tests passing (with output)
- [ ] 30+ new unit tests
- [ ] No regressions (4364 baseline)
- [ ] Documentation updated
- [ ] GitHub issue fully updated
- [ ] PM approval received

---

## Notes

### Existing Implementation
Implementation from earlier session exists and may satisfy requirements:
- Verify against audited acceptance criteria
- Run all tests to confirm functionality
- May need minimal adjustments

### Key References
- Trust service pattern: `services/intent_service/canonical_handlers.py:4212-4216`
- ADR-053: Trust computation architecture
- Pattern-050: Context/Result dataclass pair
- consciousness-philosophy.md: Greeting language guidelines

---

*Gameplan created: 2026-01-25*
*Template version: v9.3*
