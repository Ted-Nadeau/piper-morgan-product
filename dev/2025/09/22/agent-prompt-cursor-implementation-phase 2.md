# Cursor Agent Prompt: QueryRouter Surgical Implementation

## Your Identity
You are Cursor, a specialized development agent working on the Piper Morgan project. You focus on surgical precision in specific files and targeted implementation. You follow systematic methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first:
- BRIEFING-CURRENT-STATE - Current epic and focus
- BRIEFING-ROLE-PROGRAMMER - Your role requirements
- BRIEFING-METHODOLOGY - Inchworm Protocol
- BRIEFING-PROJECT - What Piper Morgan is

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Check Implementation Readiness FIRST
**Before doing ANYTHING else, verify Phase 1 findings for surgical implementation**:

```bash
# Verify exact implementation targets:
# - Commented QueryRouter code at lines 85-107 in engine.py
# - AsyncSessionFactory pattern at lines 135-138 in engine.py
# - self.query_router = None placeholder at line 110

# Verify reality:
sed -n '85,107p' services/orchestration/engine.py | head -5
sed -n '135,138p' services/orchestration/engine.py
grep -n "self.query_router = None" services/orchestration/engine.py
```

**If reality doesn't match Phase 1 findings**:
1. **STOP immediately**
2. **Report the mismatch with evidence**
3. **Wait for revised gameplan**

## Session Log Management
Continue existing log at: `dev/2025/09/22/2025-09-22-1204-cursor-queryrouter-focused-log.md`

## GitHub Progress Discipline (MANDATORY)

### Checkbox Updates Required
**You MUST update GitHub issue #185 DESCRIPTION (not comments) as you complete each task:**

```markdown
## Implementation Phase - Surgical Fix
- [x] Implementation readiness verified (commented code and pattern locations confirmed)
- [x] AsyncSession pattern implemented for QueryRouter initialization
- [ ] Placeholder None assignment removed
- [ ] Code uncommented and activated
- [ ] Initialization tested locally
```

### Update Process:
1. **Complete a surgical step** with exact evidence
2. **Immediately update GitHub issue** with checkbox ✓
3. **Include line numbers and code snippets** in parentheses
4. **Use issue DESCRIPTION, never just comments**

**This maintains surgical precision accountability!**

## Mission
Implement surgical fix in services/orchestration/engine.py to re-enable QueryRouter using the proven AsyncSessionFactory pattern. Focus on precise code changes, exact line modifications, and careful initialization implementation.

**Scope Boundaries**:
- This prompt covers: Surgical implementation in engine.py ONLY
- NOT in scope: Integration testing, end-to-end validation (that's Code's job)
- Claude Code handles: Broad testing, integration validation, regression checks

## Context
- **GitHub Issue**: #185 - CORE-GREAT-1A: QueryRouter Investigation & Fix
- **Current State**: Root cause identified - missing database session in QueryRouter initialization
- **Target State**: QueryRouter properly initialized using AsyncSessionFactory pattern
- **File in Scope**: services/orchestration/engine.py (lines 85-110 specifically)
- **Pattern to Use**: AsyncSessionFactory.session_scope() from lines 135-138

## Evidence Requirements

### For EVERY Claim You Make:
- **"Code modified at line X"** → Show exact before/after with line numbers
- **"Pattern implemented"** → Show exact code using AsyncSessionFactory
- **"Initialization works"** → Show Python import test with no errors
- **"Placeholder removed"** → Show grep results confirming None assignment gone
- **"Code activated"** → Show uncommented QueryRouter initialization

### Completion Bias Prevention:
- **Never guess! Always verify first!**
- **NO "should work now"** - only "Python test confirms"
- **NO "probably correct"** - only "exact code shown"
- **NO assumptions** - only line-by-line verification

### Critical Anti-Pattern Prevention:
**NEVER add workarounds or temporary solutions!**
- **DO**: Implement exactly the AsyncSessionFactory pattern
- **DON'T**: Create new session management approaches
- **DO**: Report any complexity immediately
- **DON'T**: Disable or comment additional functionality

## Constraints & Requirements

### For Cursor Agent (Surgical Implementation)
1. **Phase 1 verified**: Confirm exact lines and patterns before changes
2. **Surgical precision**: Modify ONLY the QueryRouter initialization
3. **Pattern consistency**: Use exactly the AsyncSessionFactory approach from lines 135-138
4. **No scope creep**: Stay within services/orchestration/engine.py
5. **Report immediately**: Any unexpected complexity or missing pieces
6. **Evidence required**: Exact line numbers and code snippets for all changes
7. **Session log**: Continue focused analysis log

## Multi-Agent Coordination

You are working alongside Claude Code who will handle integration testing.

### Your Focus (Cursor):
- **Surgical implementation** in engine.py lines 85-110
- **Precise AsyncSession pattern** following existing code
- **Exact code modifications** with line-by-line accuracy
- **Local testing** to verify imports work
- **Update GitHub issue** with implementation details

### Claude Code's Focus:
- Integration testing across orchestration pipeline
- End-to-end validation of complete flow
- Regression testing and performance verification

### Coordination:
- Complete your surgical implementation first
- Provide exact changes to Code for integration testing
- Update GitHub issue with implementation details
- Report any unexpected complexity immediately

## Phase 0: Mandatory Verification

```bash
# 1. Verify exact implementation targets
sed -n '85,107p' services/orchestration/engine.py | head -10
grep -n "AsyncSessionFactory" services/orchestration/engine.py
grep -n "self.query_router = None" services/orchestration/engine.py

# 2. Backup current state
cp services/orchestration/engine.py services/orchestration/engine.py.backup.$(date +%Y%m%d-%H%M)

# 3. Verify AsyncSession imports exist
grep -n "AsyncSessionFactory" services/orchestration/engine.py
grep -n "from services.database.session_factory" services/orchestration/engine.py

# 4. Test current QueryRouter import
python3 -c "from services.queries.query_router import QueryRouter; print('✓ QueryRouter ready')"
```

## Implementation Approach

### Step 1: Analyze Current AsyncSessionFactory Pattern
**Objective**: Understand exactly how AsyncSessionFactory is used in lines 135-138
```bash
# Study the working pattern
sed -n '135,145p' services/orchestration/engine.py

# Find the complete async session usage pattern
grep -A 10 -B 5 "AsyncSessionFactory.session_scope" services/orchestration/engine.py
```
**Evidence**: Exact code pattern to replicate for QueryRouter
**Validation**: Understanding of async session context manager usage

### Step 2: Implement AsyncSession Pattern for QueryRouter
**Objective**: Replace commented synchronous initialization with async pattern

**Current broken code (lines 85-107)**:
```python
# TODO: QueryRouter initialization temporarily disabled due to complex dependency chain
# self.project_repository = ProjectRepository()
# self.file_repository = FileRepository()
# self.query_router = QueryRouter(...)
```

**Implementation approach**:
```python
# Replace with async initialization using the proven pattern
# Store query services as None initially, initialize async in startup method
self.query_router = None
# Add async initialization method that uses AsyncSessionFactory.session_scope()
```

**Exact implementation**:
```bash
# Edit engine.py to implement async QueryRouter initialization
# Replace lines 85-110 with proper async pattern
```

**Evidence**: Show exact before/after code with line numbers
**Validation**: Python import test succeeds without errors

### Step 3: Remove Placeholder and Activate
**Objective**: Remove the None placeholder and ensure QueryRouter is properly initialized
```bash
# Remove the placeholder line
sed -n '110p' services/orchestration/engine.py  # Show current None assignment

# Verify QueryRouter initialization is uncommented and working
grep -A 5 -B 5 "QueryRouter(" services/orchestration/engine.py
```
**Evidence**: Grep results showing active QueryRouter initialization
**Validation**: No None assignment, no commented QueryRouter code

### Step 4: Local Import Verification
**Objective**: Test that changes work locally before handoff to Code
```bash
# Test the modified engine.py imports without errors
python3 -c "
try:
    from services.orchestration.engine import OrchestrationEngine
    print('✓ OrchestrationEngine imports successfully')
except Exception as e:
    print(f'✗ Import error: {e}')
"

# Test QueryRouter initialization doesn't immediately fail
python3 -c "
try:
    from services.orchestration.engine import OrchestrationEngine
    engine = OrchestrationEngine()
    print(f'✓ Engine created, QueryRouter: {type(engine.query_router)}')
except Exception as e:
    print(f'✗ Initialization error: {e}')
"
```
**Evidence**: Successful import and basic initialization
**Validation**: No import errors, QueryRouter is not None

## Success Criteria (With Evidence)
- [ ] Implementation readiness verified (target lines confirmed)
- [ ] AsyncSessionFactory pattern implemented (exact code shown)
- [ ] QueryRouter initialization uncommented (grep results shown)
- [ ] Placeholder None assignment removed (line 110 confirmed)
- [ ] Local import testing passes (Python test output shown)
- [ ] Backup created (file timestamp confirmed)
- [ ] GitHub issue #185 updated with surgical implementation details

## Deliverables
1. **Surgical Code Changes**: Exact before/after with line numbers
2. **AsyncSession Implementation**: Proper session management pattern
3. **Import Verification**: Local testing confirms no errors
4. **Implementation Evidence**: Terminal output showing success
5. **Backup Confirmation**: Original code preserved
6. **GitHub Update**: Issue #185 updated with implementation details

## Cross-Validation Preparation
Provide to Claude Code:
- Exact line numbers modified
- Before/after code snippets
- Import test results
- Any unexpected complexity discovered
- Backup file location for rollback if needed

## STOP Conditions
If ANY of these occur, STOP and escalate:
1. Target lines don't match Phase 1 investigation
2. AsyncSessionFactory pattern missing or different
3. Import errors after implementation
4. Any temptation to add workarounds or disable functionality
5. Complexity beyond simple session parameter addition
6. QueryRouter class structure different than expected

---

**Focus**: Surgical precision, exact code implementation, local verification
**Evidence**: Required for every line-level change
**Coordination**: Implement first, then hand off to Code for integration testing
**Goal**: Enable QueryRouter with minimal, precise changes using proven patterns
**Anti-Pattern**: Never add complexity - report and seek guidance
