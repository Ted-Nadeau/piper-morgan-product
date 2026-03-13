# Lead Developer Prompt: #419 MUX-NAV-HOME Implementation

## Your Identity
You are the Lead Developer (Claude Code), implementing #419 MUX-NAV-HOME - Home State Design. You follow systematic methodology and provide evidence for all claims.

## Essential Context
- **GitHub Issue**: #419 MUX-NAV-HOME - Home State Design
- **Current State**: Implementation exists from prior session (needs verification)
- **Target State**: Trust-gated, consciousness-aware home page
- **Dependencies**: TrustComputationService (exists), ADR-053 (approved)
- **User Data Risk**: None - read-only feature
- **Infrastructure Verified**: Yes (Phase -1 gameplan)

---

## CRITICAL: Evidence and Handoff Requirements

### Acceptance Criteria (from issue)

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
- [ ] No regressions introduced (baseline: 4364 tests)
- [ ] Code follows existing patterns
- [ ] Per ADR-053: Trust stage invisible to users, effects noticeable
- [ ] Anti-flattening test: Can describe using "Piper notices/shows" language

**Documentation**
- [ ] Code documentation (docstrings) complete
- [ ] Session log documents implementation decisions
- [ ] Issue updated with evidence before closure

### Handoff Format Required
```markdown
## Issue #419 Completion Report
**Status**: Complete/Partial/Blocked

**Tests**:
- X tests added in [location]
- `pytest [path] -v` output: [paste actual output]

**Verification**:
[Actual command output showing success]

**Files Modified**:
- [file1.py] (+X/-Y lines)
- [file2.py] (+X/-Y lines)

**User Testing Steps**:
1. [Step 1]
2. [Step 2]
3. [Expected result]

**Blockers** (if any):
- [Blocker description and why it prevents completion]
```

---

## Mission
Verify existing implementation against acceptance criteria and complete any gaps. Provide evidence for 100% completion.

**Scope Boundaries**:
- This prompt covers: Phases 1-4 + Phase Z from gameplan
- NOT in scope: #420, #421, #684 (separate issues)
- Separate prompts handle: N/A (single-agent work)

---

## Infrastructure Verification (MANDATORY FIRST ACTION)

```bash
# 1. Verify existing implementation exists
ls -la services/home/
# Expected: __init__.py, home_state_service.py

# 2. Verify HardnessLevel enum exists
grep -n "class HardnessLevel" services/shared_types.py
# Expected: IntEnum definition

# 3. Verify trust_stage in home route
grep -n "trust_stage" web/api/routes/ui.py
# Expected: Added to template context

# 4. Verify template has trust-gated greeting
grep -n "trust_stage" templates/home.html
# Expected: Jinja conditionals for greeting subtext

# 5. Verify tests exist
ls -la tests/unit/services/home/
ls -la tests/unit/services/test_hardness_level.py
ls -la tests/unit/web/api/routes/test_ui_home.py
```

**If infrastructure differs from expected**: STOP and document gaps.

---

## Phase 0: Mandatory Verification

```bash
# 1. GitHub issue exists
gh issue view 419

# 2. Check existing patterns (trust service usage)
grep -rn "TrustComputationService" services/intent_service/canonical_handlers.py | head -5

# 3. Check ADR for trust visibility rules
grep -n "invisible" docs/internal/architecture/current/adrs/adr-053*

# 4. Verify server can start
python -c "from web.app import app; print('Import OK')"

# 5. Run existing tests for baseline
python -m pytest tests/unit/services/home/ tests/unit/services/test_hardness_level.py tests/unit/web/api/routes/test_ui_home.py -v --tb=short
```

---

## Implementation Approach

### Step 1: Verify Phase 1 (Trust Stage in Route)

**Expected Files**:
- `web/api/routes/ui.py` - Contains trust_stage in home route

**Verification**:
```bash
# Check imports
grep -n "TrustComputationService\|UserTrustProfileRepository" web/api/routes/ui.py

# Check context contains trust_stage
grep -A 20 "def home" web/api/routes/ui.py | grep "trust_stage"

# Run route tests
python -m pytest tests/unit/web/api/routes/test_ui_home.py -v
```

**Evidence Required**:
- [ ] Import statements present
- [ ] trust_stage and trust_stage_name in template context
- [ ] Error handling defaults to TrustStage.NEW
- [ ] Tests pass

### Step 2: Verify Phase 2 (HardnessLevel Enum)

**Expected Files**:
- `services/shared_types.py` - Contains HardnessLevel IntEnum

**Verification**:
```bash
# Check enum exists with 5 levels
python -c "from services.shared_types import HardnessLevel; print([(h.name, h.value) for h in HardnessLevel])"
# Expected: [('HARDEST', 5), ('HARD', 4), ('MEDIUM', 3), ('SOFT', 2), ('SOFTEST', 1)]

# Check docstring documents visibility rules
grep -A 10 "class HardnessLevel" services/shared_types.py

# Run enum tests
python -m pytest tests/unit/services/test_hardness_level.py -v
```

**Evidence Required**:
- [ ] 5 levels: HARDEST=5, HARD=4, MEDIUM=3, SOFT=2, SOFTEST=1
- [ ] Docstring explains trust-stage visibility
- [ ] Tests pass

### Step 3: Verify Phase 3 (HomeStateService)

**Expected Files**:
- `services/home/__init__.py`
- `services/home/home_state_service.py`

**Verification**:
```bash
# Check dataclasses exist
python -c "from services.home import HomeStateContext, HomeStateResult, HomeStateItem, HomeStateService; print('All imports OK')"

# Check Pattern-050 compliance (Context/Result pair)
grep -n "class HomeStateContext\|class HomeStateResult" services/home/home_state_service.py

# Check lens items are HARDEST
grep -n "HARDEST" services/home/home_state_service.py

# Check greeting generation
grep -n "def.*greeting\|greeting" services/home/home_state_service.py

# Run service tests
python -m pytest tests/unit/services/home/test_home_state_service.py -v
```

**Evidence Required**:
- [ ] HomeStateContext dataclass (Pattern-050 input)
- [ ] HomeStateResult dataclass (Pattern-050 output)
- [ ] HomeStateItem with hardness field
- [ ] Trust-gated filtering logic
- [ ] Always-present lens items (HARDEST)
- [ ] 4 greeting variations by trust stage
- [ ] Tests pass

### Step 4: Verify Phase 4 (Template Integration)

**Expected Files**:
- `templates/home.html` - Trust-gated greeting subtext

**Verification**:
```bash
# Check greeting variations
grep -A 20 "greeting-subtext" templates/home.html | head -30

# Check 4 distinct messages for trust stages
grep -c "trust_stage\|default(1)" templates/home.html

# Verify Jinja syntax is valid
python -c "from jinja2 import Environment, FileSystemLoader; env = Environment(loader=FileSystemLoader('templates')); t = env.get_template('home.html'); print('Template syntax OK')"
```

**Evidence Required**:
- [ ] 4 distinct greeting subtext messages
- [ ] Stage 1: "What can I help you with?"
- [ ] Stage 2: "I'm here to help."
- [ ] Stage 3: "I noticed a few things while you were away."
- [ ] Stage 4: "I've been thinking about your priorities."
- [ ] Template renders without syntax errors

### Step 5: Full Test Suite Verification (Phase Z)

**Run all new tests**:
```bash
# Run all #419 related tests
python -m pytest tests/unit/services/home/ tests/unit/services/test_hardness_level.py tests/unit/web/api/routes/test_ui_home.py -v

# Count new tests
python -m pytest tests/unit/services/home/ tests/unit/services/test_hardness_level.py tests/unit/web/api/routes/test_ui_home.py --collect-only | grep "test session starts" -A 100 | grep "<Function" | wc -l
```

**Run full unit test suite for regression check**:
```bash
python -m pytest tests/unit/ -v --tb=line | tail -20
# Verify: baseline is 4364, should be 4364 + new tests
```

---

## Success Criteria (With Evidence)

- [ ] Infrastructure matches expectations (verification output)
- [ ] Phase 1 complete: trust_stage in route (test output)
- [ ] Phase 2 complete: HardnessLevel enum (test output)
- [ ] Phase 3 complete: HomeStateService (test output)
- [ ] Phase 4 complete: Template integration (syntax check)
- [ ] 30+ new tests added (count output)
- [ ] No regressions (full suite output)
- [ ] GitHub issue updated (issue link)

---

## Deliverables

1. **Code Changes**: Verified existing implementation
2. **Test Coverage**: 30+ new unit tests confirmed
3. **Evidence Report**: All verification commands with output
4. **GitHub Update**: Issue #419 updated with evidence
5. **Completion Report**: Using handoff format above

---

## STOP Conditions

STOP immediately and escalate if:
- [ ] Infrastructure doesn't match (files missing)
- [ ] Tests fail for any reason
- [ ] TrustComputationService unavailable
- [ ] Trust stage query errors
- [ ] Template syntax errors
- [ ] Regressions detected in full suite
- [ ] Cannot verify any acceptance criterion

---

## Self-Check Before Claiming Complete

1. Did I run ALL verification commands?
2. Did I capture ALL output as evidence?
3. Are ALL acceptance criteria checked off with evidence?
4. Did I run the full test suite for regressions?
5. Is the GitHub issue updated with evidence?
6. Can another agent verify my work independently?

---

*Template Version: 10.2*
*Issue: #419 MUX-NAV-HOME*
*Agent: Lead Developer*
*Date: 2026-01-25*
