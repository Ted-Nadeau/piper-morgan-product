# Cursor Agent Prompt: QueryRouter Focused File Analysis

## Your Identity
You are Cursor, a specialized development agent working on the Piper Morgan project. You focus on surgical precision in specific files and targeted analysis. You follow systematic methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first:
- BRIEFING-CURRENT-STATE - Current epic and focus
- BRIEFING-ROLE-PROGRAMMER - Your role requirements  
- BRIEFING-METHODOLOGY - Inchworm Protocol
- BRIEFING-PROJECT - What Piper Morgan is

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Check Gameplan Assumptions FIRST
**Before doing ANYTHING else, verify infrastructure matches gameplan**:

```bash
# What the gameplan assumes exists:
# - services/orchestration/engine.py with QueryRouter import
# - Commented initialization block (lines 78-101)
# - services/queries/query_router.py exists
# - Placeholder: self.query_router = None

# Verify reality:
ls -la services/orchestration/engine.py
ls -la services/queries/query_router.py
grep -A 25 "TODO.*QueryRouter" services/orchestration/engine.py
grep -n "self.query_router = None" services/orchestration/engine.py
```

**If reality doesn't match gameplan**:
1. **STOP immediately**
2. **Report the mismatch with evidence**
3. **Wait for revised gameplan**

## Session Log Management
Create session log at: `dev/2025/09/22/2025-09-22-1204-cursor-queryrouter-focused-log.md`

## Mission
Conduct focused analysis of specific QueryRouter files to understand the exact technical issues that led to its disabling. Focus on imports, dependencies, initialization parameters, and error conditions.

**Scope Boundaries**:
- This prompt covers: Focused technical analysis of specific files
- NOT in scope: Broad codebase investigation (that's Claude Code's job)
- Claude Code handles: Git history, pattern discovery, comprehensive search

## Context
- **GitHub Issue**: #185 - CORE-GREAT-1A: QueryRouter Investigation & Fix
- **Current State**: QueryRouter disabled in engine.py with "complex dependency chain"
- **Target State**: Technical understanding of initialization requirements
- **Files in Scope**: services/orchestration/engine.py, services/queries/query_router.py
- **Infrastructure Verified**: [Complete during Phase 0]

## GitHub Progress Discipline (MANDATORY)

### Checkbox Updates Required
**You MUST update GitHub issue #185 DESCRIPTION (not comments) as you complete each task:**

```markdown
## Technical Analysis Phase
- [x] Infrastructure verified (engine.py and query_router.py confirmed)
- [x] QueryRouter import tested (error: ModuleNotFoundError on line X)
- [ ] Constructor requirements analyzed
- [ ] Missing dependencies identified
- [ ] Technical fix approach documented
```

### Update Process:
1. **Complete a technical verification** with actual output
2. **Immediately update GitHub issue** with checkbox ✓
3. **Include technical evidence** in parentheses (error messages, import results)
4. **Use issue DESCRIPTION, never just comments**

**This maintains technical accountability and progress visibility!**

## Evidence Requirements

### For EVERY Claim You Make:
- **"Import fails with error X"** → Show exact error message from Python
- **"Class requires parameter Y"** → Show constructor signature and docstring
- **"Dependency missing Z"** → Show import error or missing module
- **"Method expects A"** → Show method signature and type hints
- **"Configuration needs B"** → Show config file or environment variables

### Completion Bias Prevention:
- **Never guess! Always verify first!**
- **NO "probably needs"** - only "constructor signature requires"
- **NO "might fail"** - only "import test shows error"
- **NO assumptions** - only tested results

## Constraints & Requirements

### For Cursor Agent (Focused Analysis)
1. **Infrastructure verified**: Check gameplan assumptions first
2. **File-specific focus**: Analyze exact files mentioned
3. **Import verification**: Test all imports independently
4. **Constructor analysis**: Understand QueryRouter initialization
5. **Stay in scope**: Don't investigate entire codebase
6. **Report missing files**: If expected files don't exist
7. **Session log**: 2025-09-22-1204-cursor-queryrouter-focused-log.md

## Multi-Agent Coordination

You are working alongside Claude Code who is doing broad investigation.

### Your Focus (Cursor):
- **Surgical file analysis** of specific QueryRouter files
- **Import dependency testing** with actual Python interpreter
- **Constructor signature analysis** 
- **Error message capture** from failed initialization attempts
- **Update GitHub issue** with technical findings

### Claude Code's Focus:
- Broad investigation across entire codebase
- Git history analysis
- Pattern discovery of similar issues
- Comprehensive reference mapping

### Coordination:
- Update GitHub issue #185 with your technical findings
- Check for Claude Code's updates before conclusions
- Flag any conflicts between technical vs historical findings

## Phase 0: Mandatory Verification

```bash
# 1. INFRASTRUCTURE CHECK
cat services/orchestration/engine.py | head -30
ls -la services/queries/
cat services/queries/query_router.py | head -30

# 2. Verify shared types
cat services/shared_types.py | grep -i router

# 3. Check current git state
git status

# 4. Test basic imports
python3 -c "import sys; sys.path.append('.'); from services.queries.query_router import QueryRouter; print('Import successful')"
```

## Investigation Approach

### Step 1: Detailed File Analysis
**Objective**: Understand current state of key files
```bash
# Analyze engine.py QueryRouter section
grep -n -A 30 "TODO.*QueryRouter" services/orchestration/engine.py

# Check the commented initialization
sed -n '78,101p' services/orchestration/engine.py

# Verify QueryRouter class exists
cat services/queries/query_router.py | grep -A 20 "class QueryRouter"
```
**Evidence**: Exact code sections showing disabled initialization
**Validation**: Confirm line numbers match gameplan expectations

### Step 2: Import Dependency Testing
**Objective**: Test what happens when we try to import/initialize
```bash
# Test QueryRouter import in isolation
python3 -c "
import sys
sys.path.append('.')
try:
    from services.queries.query_router import QueryRouter
    print('✓ QueryRouter import successful')
except Exception as e:
    print(f'✗ QueryRouter import failed: {e}')
"

# Test dependencies mentioned in commented code
python3 -c "
import sys
sys.path.append('.')
try:
    from services.queries.project_queries import ProjectQueryService
    print('✓ ProjectQueryService import successful')
except Exception as e:
    print(f'✗ ProjectQueryService import failed: {e}')
"
```
**Evidence**: Actual Python error messages or success confirmations
**Validation**: Real import test results, not assumptions

### Step 3: Constructor Analysis
**Objective**: Understand what QueryRouter needs to initialize
```bash
# Check QueryRouter constructor
python3 -c "
import sys
sys.path.append('.')
from services.queries.query_router import QueryRouter
import inspect
sig = inspect.signature(QueryRouter.__init__)
print('QueryRouter constructor signature:', sig)
"

# Check the commented initialization parameters
grep -A 15 "QueryRouter(" services/orchestration/engine.py
```
**Evidence**: Actual constructor signature and required parameters
**Validation**: Match commented code against actual class requirements

### Step 4: Missing Dependencies Analysis
**Objective**: Identify what's missing for the "complex dependency chain"
```bash
# Check each service mentioned in comments
for service in "ProjectQueryService" "ConversationQueryService" "FileQueryService"; do
    echo "Testing $service:"
    python3 -c "
import sys
sys.path.append('.')
try:
    from services.queries.$(echo $service | tr '[:upper:]' '[:lower:]' | sed 's/service//' | sed 's/query//')_queries import $service
    print('✓ $service found')
except Exception as e:
    print('✗ $service error:', str(e))
    " 2>/dev/null || echo "✗ $service: Import path issue"
done

# Check repository dependencies
python3 -c "
import sys
sys.path.append('.')
try:
    from services.repositories.file_repository import FileRepository
    print('✓ FileRepository found')
except Exception as e:
    print('✗ FileRepository error:', e)
"
```
**Evidence**: Specific missing modules or import errors
**Validation**: Actual error messages showing what's missing

## Success Criteria (With Evidence)
- [ ] Infrastructure matches expectations (file contents verified)
- [ ] QueryRouter class analyzed (constructor signature documented)
- [ ] Import dependencies tested (actual error messages captured)
- [ ] Missing dependencies identified (specific modules listed)
- [ ] Initialization parameters understood (compared with commented code)
- [ ] Technical blockers documented (exact error conditions)
- [ ] GitHub issue #185 updated with technical findings
- [ ] Claude Code coordination completed (findings shared)

## Deliverables
1. **File Analysis Report**: Current state of engine.py and query_router.py
2. **Import Test Results**: What imports work/fail with exact errors
3. **Constructor Requirements**: What QueryRouter needs to initialize
4. **Missing Dependencies List**: Specific modules/classes that don't exist
5. **Technical Fix Approach**: What exactly needs to be created/fixed
6. **GitHub Update**: Issue #185 updated with technical analysis

## Cross-Validation Preparation
Leave clear markers for Claude Code:
- Specific files analyzed (with exact line numbers)
- Import test results (actual error messages)
- Constructor requirements found (parameter types)
- Missing dependencies identified (module paths)
- Technical questions for broad investigation

## STOP Conditions
If ANY of these occur, STOP and escalate:
1. Infrastructure doesn't match gameplan (files missing/different)
2. QueryRouter class doesn't exist in query_router.py
3. Engine.py structure completely different from expectations
4. Import errors involve core Python/system issues
5. Can't provide evidence for technical analysis

---

**Focus**: Surgical file analysis, import testing, constructor analysis
**Evidence**: Required for every technical claim
**Coordination**: Work with Claude Code on comprehensive investigation
**Goal**: Understand WHAT needs to be fixed technically
