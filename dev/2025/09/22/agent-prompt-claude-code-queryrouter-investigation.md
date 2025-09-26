# Claude Code Agent Prompt: QueryRouter Investigation & Root Cause Analysis

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You excel at broad investigation, pattern discovery, and deploying subagents for parallel work. You follow systematic methodology and provide evidence for all claims.

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
# - QueryRouter in services/orchestration/engine.py (lines 78-101)
# - services/queries/query_router.py exists
# - OrchestrationEngine class with disabled initialization
# - TODO comment about "complex dependency chain"

# Verify reality:
ls -la services/orchestration/
ls -la services/queries/
grep -n "QueryRouter" services/orchestration/engine.py
grep -n "TODO.*QueryRouter" services/orchestration/engine.py
```

**If reality doesn't match gameplan**:
1. **STOP immediately**
2. **Report the mismatch with evidence**
3. **Wait for revised gameplan**

## Session Log Management
Create session log at: `dev/2025/09/22/2025-09-22-1204-claude-code-queryrouter-log.md`

## Mission
Conduct broad investigation to discover WHY QueryRouter was disabled and identify the root cause that led to the "complex dependency chain" comment. Focus on git history, pattern discovery, and comprehensive codebase analysis.

**Scope Boundaries**:
- This prompt covers: Investigation and root cause analysis
- NOT in scope: Actual fixing (that's Phase 2)
- Cursor agent handles: Focused file analysis of engine.py

## Context
- **GitHub Issue**: #185 - CORE-GREAT-1A: QueryRouter Investigation & Fix
- **Current State**: QueryRouter 75% complete but disabled with TODO comment
- **Target State**: Understanding of root cause and fix approach
- **Dependencies**: Part of CORE-GREAT-1 epic, blocks 80% of MVP features
- **Infrastructure Verified**: [Complete during Phase 0]

## GitHub Progress Discipline (MANDATORY)

### Checkbox Updates Required
**You MUST update GitHub issue #185 DESCRIPTION (not comments) as you complete each task:**

```markdown
## Investigation Phase
- [x] Located disabled QueryRouter code (found in engine.py lines 78-101)
- [x] Reviewed git history (disabled in commit abc123 on date X)
- [ ] Identified root cause
- [ ] Documented dependencies/blockers
- [ ] Found all QueryRouter references
```

### Update Process:
1. **Complete a verification step** with evidence
2. **Immediately update GitHub issue** with checkbox ✓
3. **Include brief evidence summary** in parentheses
4. **Use issue DESCRIPTION, never just comments**

**This is how we track progress and maintain accountability!**

## Evidence Requirements

### For EVERY Claim You Make:
- **"Found in git history"** → Provide `git log` output showing actual commits
- **"QueryRouter referenced in X files"** → Show `grep -r` results with line numbers
- **"Dependency chain involves Y"** → Show import statements and error messages
- **"Pattern exists in Z locations"** → Show exact file paths and line numbers
- **"TODO comment says X"** → Quote exact text with file:line reference

### Completion Bias Prevention:
- **Never guess! Always verify first!**
- **NO "probably caused by"** - only "evidence shows"
- **NO "likely the issue"** - only "git history reveals"
- **NO assumptions** - only verified findings

## Constraints & Requirements

### For Claude Code (Broad Investigation)
1. **Infrastructure verified**: Check gameplan assumptions first
2. **Git history focus**: When was QueryRouter disabled and why?
3. **Pattern discovery**: Find ALL QueryRouter references across codebase
4. **Dependency analysis**: What is the "complex dependency chain"?
5. **Subagent deployment**: Use if needed for parallel investigation
6. **Cross-codebase search**: Find similar patterns or related TODOs
7. **Session log**: 2025-09-22-1204-claude-code-queryrouter-log.md

## Multi-Agent Coordination

You are working alongside Cursor Agent who is doing focused file analysis.

### Your Focus (Claude Code):
- **Broad investigation** across entire codebase
- **Git history analysis** to understand timeline
- **Pattern discovery** of similar disabled components
- **Dependency mapping** across services
- **Deploy subagents** for parallel work if available
- **Update GitHub issue** with investigation findings

### Cursor Agent's Focus:
- Focused analysis of services/orchestration/engine.py
- Import dependency verification
- Class structure analysis
- Specific error analysis

### Coordination:
- Update GitHub issue #185 with your findings
- Check for Cursor's updates before major conclusions
- Flag any conflicts between broad vs focused findings

## Phase 0: Mandatory Verification

```bash
# 1. INFRASTRUCTURE CHECK
ls -la services/orchestration/engine.py
ls -la services/queries/query_router.py
grep -n "QueryRouter" services/orchestration/engine.py

# 2. Verify GitHub issue exists
gh issue view 185

# 3. Check current git state
git status
git log --oneline -5

# 4. Find all QueryRouter references
grep -r "QueryRouter" . --include="*.py" | head -20

# 5. Check for related TODOs
grep -r "TODO.*QueryRouter" . --include="*.py"
```

## Investigation Approach

### Step 1: Git History Deep Dive
**Objective**: Understand when and why QueryRouter was disabled
```bash
# Check git history for QueryRouter changes
cd services/orchestration/
git log -p --follow engine.py | grep -A 10 -B 10 "QueryRouter"
git blame engine.py | grep "QueryRouter"

# Look for related commits
git log --grep="QueryRouter" --oneline
git log --grep="query" --oneline | head -10
```
**Evidence**: Capture git log output showing disable commit
**Validation**: Find exact commit hash and message

### Step 2: Comprehensive Reference Mapping
**Objective**: Find every QueryRouter reference in codebase
```bash
# Find all references
grep -r "QueryRouter" . --include="*.py" | grep -v ".pyc"
find . -name "*.py" -exec grep -l "QueryRouter" {} \;

# Check imports
grep -r "from.*QueryRouter" . --include="*.py"
grep -r "import.*QueryRouter" . --include="*.py"

# Check for related classes
grep -r "query_router" . --include="*.py"
```
**Evidence**: Complete list of files and line numbers
**Validation**: Verify each reference is real (not comment/string)

### Step 3: Dependency Chain Analysis
**Objective**: Understand the "complex dependency chain"
```bash
# Check QueryRouter class itself
cat services/queries/query_router.py | head -50

# Find its dependencies
grep -r "import" services/queries/query_router.py
grep -r "from" services/queries/query_router.py

# Check what depends on QueryRouter
grep -r "QueryRouter" services/ --include="*.py" | grep -v "queries/query_router.py"
```
**Evidence**: Dependency tree showing circular or complex dependencies
**Validation**: Try importing QueryRouter to see actual errors

### Step 4: Pattern Discovery
**Objective**: Find similar 75% patterns in codebase
```bash
# Look for other disabled components
grep -r "TODO.*disabled" . --include="*.py"
grep -r "TODO.*temporarily" . --include="*.py"
grep -r "# TODO:" . --include="*.py" | grep -i "complex\|dependency\|disabled"

# Check for None placeholders
grep -r "= None" services/ --include="*.py" | grep -i "router\|engine\|service"
```
**Evidence**: List of other disabled/incomplete components
**Validation**: Verify each is actually disabled, not legitimate None

## Success Criteria (With Evidence)
- [ ] Infrastructure matches expectations (verified with ls/grep)
- [ ] Git history analyzed (commit hashes and messages shown)
- [ ] All QueryRouter references mapped (complete grep results)
- [ ] Dependency chain understood (import tree documented)
- [ ] Root cause identified (evidence-backed conclusion)
- [ ] Similar patterns found (other 75% components listed)
- [ ] GitHub issue #185 updated with findings
- [ ] Cursor coordination completed (findings compared)

## Deliverables
1. **Git History Report**: When/why QueryRouter was disabled
2. **Reference Map**: All QueryRouter usages across codebase
3. **Dependency Analysis**: What makes the chain "complex"
4. **Root Cause**: Evidence-backed explanation of the real problem
5. **Pattern Report**: Other similar disabled components found
6. **GitHub Update**: Issue #185 updated with investigation results

## Cross-Validation Preparation
Leave clear markers for Cursor Agent:
- File paths analyzed (with specific findings)
- Git commit hashes discovered (for verification)
- Dependency errors found (exact error messages)
- Any assumptions made (none should exist!)
- Questions for focused file analysis

## STOP Conditions
If ANY of these occur, STOP and escalate:
1. Infrastructure doesn't match gameplan expectations
2. QueryRouter completely missing (not just disabled)
3. Git history shows it never worked
4. Complex dependency involves major architectural changes
5. Can't provide evidence for investigation claims

---

**Focus**: Broad investigation, git history, pattern discovery
**Evidence**: Required for every claim
**Coordination**: Work with Cursor on focused analysis
**Goal**: Understand WHY before attempting to fix
