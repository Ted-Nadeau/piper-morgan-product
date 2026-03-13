# Gameplan: Issue #453 - session_scope() vs session_scope_fresh() Audit
*Created: December 3, 2025*
*GitHub Issue: https://github.com/mediajunkie/piper-morgan-product/issues/453*

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI
- [x] CLI structure: Custom (main.py with subcommands via asyncio.run())
- [x] Database: PostgreSQL with asyncpg + SQLAlchemy async
- [x] Testing framework: pytest with pytest-asyncio
- [x] Existing patterns: `AsyncSessionFactory` with two methods - `session_scope()` and `session_scope_fresh()`

**My understanding of the task**:
- Audit all usages of `session_scope()` to identify any that should use `session_scope_fresh()`
- The pattern: code running via `asyncio.run()` from main.py creates a NEW event loop
- If `session_scope()` uses a db engine from a PREVIOUS `asyncio.run()` call → event loop mismatch
- Fix already applied to `scripts/setup_wizard.py` (16 instances) in commit 13b6cc3e

### Part B: PM Verification

**What actually exists**:
```bash
# session_scope_fresh is for different-event-loop contexts
# session_scope uses global db singleton (same event loop only)
grep -r "session_scope_fresh" . --include="*.py" | wc -l  # Count fresh usages
grep -r "session_scope()" . --include="*.py" | wc -l      # Count standard usages
```

**Actual task needed**:
- [x] Audit existing code for correctness
- [ ] Add lint rule or doc comment to prevent future regressions
- [ ] Document the pattern in ADR or Pattern catalog

### Part C: Proceed Decision

- [x] **PROCEED** - Understanding is correct, this is a code hygiene/audit task

---

## Phase 0: Investigation

### Purpose
Identify all usages of `session_scope()` and categorize by safety

### Actions

1. **Find all usages**:
```bash
grep -rn "session_scope()" . --include="*.py" | grep -v "session_scope_fresh"
grep -rn "session_scope_fresh()" . --include="*.py"
```

2. **Categorize by entry point**:
   - Entry via `asyncio.run()` from main.py → MUST use `session_scope_fresh()`
   - Entry via FastAPI request handler → OK to use `session_scope()`
   - Entry via pytest → safer with `session_scope_fresh()` but may work either way

3. **Files to check**:
   - [ ] `scripts/` - CLI scripts (FIXED: setup_wizard.py)
   - [ ] `scripts/status_checker.py` - Called via asyncio.run()
   - [ ] `scripts/preferences_questionnaire.py` - Called via asyncio.run()
   - [ ] `services/` - May be used from CLI or web
   - [ ] `tests/` - Test fixtures

### STOP Conditions
- Feature already audited/fixed
- Pattern doesn't exist in codebase
- Scope creep beyond session_scope patterns

---

## Phase 1: Audit Execution

**Deploy: Single Agent (Haiku)**
*Rationale: This is routine search/audit work - Haiku handles this efficiently*

### Agent Prompt (Checklist-Verified Against Template v10.2)

```markdown
# Claude Code Agent Prompt: session_scope() Audit (#453)

## Your Identity
You are Claude Code (Haiku), executing a code audit task for Piper Morgan.

## Mission
Audit all `session_scope()` usages in the codebase and categorize by event loop safety.

## Context
- **GitHub Issue**: #453 - session_scope() vs session_scope_fresh() audit
- **Background**: `session_scope()` uses global db singleton (bound to startup event loop).
  Code running via `asyncio.run()` from main.py creates NEW event loops, causing
  "Future attached to different loop" errors.
- **Already Fixed**: `scripts/setup_wizard.py` (16 instances → session_scope_fresh())
- **Session Log**: Append to existing daily log or create
  `dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-prog-haiku-log.md`

## Phase 0: Verification (MANDATORY)
```bash
# Verify GitHub issue exists
gh issue view 453

# Verify the pattern exists
grep -rn "session_scope" services/database/session_factory.py | head -5
```

## Implementation Steps

### Step 1: Find all usages
```bash
grep -rn "session_scope()" . --include="*.py" | grep -v session_scope_fresh | grep -v __pycache__
grep -rn "session_scope_fresh()" . --include="*.py" | grep -v __pycache__
```
**Evidence**: Paste complete grep output

### Step 2: Categorize each usage
For each file found, trace the entry point:
- ✅ SAFE: Called from FastAPI request handler (same event loop)
- ⚠️ RISKY: Called from service that could be used by CLI or web
- ❌ WRONG: Called from code invoked via `asyncio.run()` in main.py

**Evidence**: Markdown table with categorization

### Step 3: Fix any ❌ WRONG usages
Change `session_scope()` → `session_scope_fresh()`
**Evidence**: `git diff` and `git log --oneline -1`

### Step 4: Update docstring
Add event loop warning to `AsyncSessionFactory.session_scope()` in
`services/database/session_factory.py`
**Evidence**: Show updated docstring

## Constraints
- Do NOT modify web route handlers (they're SAFE)
- Do NOT modify test fixtures without PM approval
- PRESERVE existing functionality - only change session method
- RUN pre-commit after any changes

## Evidence Format Required
```markdown
## Audit Results

### Grep Output
[paste complete output]

### Categorization Table
| File | Line | Entry Point | Category | Action |
|------|------|-------------|----------|--------|
| ... | ... | ... | ✅/⚠️/❌ | None/Fix |

### Fixes Made
- Commit: [hash]
- Files: [list]

### Docstring Update
[show new docstring]
```

## Success Criteria
- [ ] Phase 0 verification passed (show gh issue view output)
- [ ] All usages found and categorized (show grep output)
- [ ] Any ❌ WRONG usages fixed (show commit hash)
- [ ] Docstring updated with event loop warning (show content)
- [ ] Findings table provided as evidence

## STOP Conditions
- If fixing breaks tests → STOP and report
- If unclear whether code runs via asyncio.run() → STOP and ask
- If >5 files need changes → STOP and confirm scope with PM
```

---

## Phase 2: Prevention (Future-Proofing)

### Options

A. **Doc Comment Approach** (Minimal)
   - Add detailed docstring to `session_scope()` explaining when NOT to use it
   - Pro: No tooling changes
   - Con: Easy to miss

B. **Naming Convention** (Medium)
   - Rename `session_scope()` → `session_scope_web()`
   - Make intent explicit in name
   - Pro: Self-documenting
   - Con: Breaking change, requires migration

C. **Lint Rule** (Robust)
   - Pre-commit hook that detects `session_scope()` in `scripts/` directory
   - Pro: Catches mistakes automatically
   - Con: May have false positives

D. **ADR Documentation** (Documentation)
   - Create ADR about event loop awareness patterns
   - Pro: Educational, explains "why"
   - Con: Doesn't prevent mistakes

### Recommendation
Combine A (Doc Comment) + D (ADR) for this issue.
Consider B (Naming) for future if pattern proves problematic.

---

## Phase Z: Completion Criteria

### Acceptance Criteria
- [ ] All `session_scope()` usages audited
- [ ] Any incorrect usages fixed
- [ ] Docstring updated on `session_scope()` with event loop warning
- [ ] ADR created: "Event Loop Awareness in Async Database Access"
- [ ] GitHub issue #453 updated with findings

### Evidence Required
- List of files audited with categorization
- Any fixes made (commits)
- ADR file location

### Evidence Format
```bash
# Terminal output showing audit results
grep -rn "session_scope()" . --include="*.py" | grep -v session_scope_fresh
# Categorized results in markdown table
```

### PM Approval Request
```markdown
@PM - Issue #453 complete and ready for review:
- All session_scope() usages audited ✓
- Categorization documented ✓
- Doc comment and ADR created ✓
- No new incorrect usages found ✓

Please review and close if satisfied.
```

---

## Notes

This is a **single-agent task** - search/audit work that doesn't benefit from multi-agent approaches.

This gameplan also establishes the **antipattern detection opportunity** you mentioned:
- Pattern: "Global singleton initialized in one async context, used in another"
- Detection: Look for singletons that store async resources (connections, locks, futures)
- Other potential instances: Redis connections, HTTP client sessions, etc.
