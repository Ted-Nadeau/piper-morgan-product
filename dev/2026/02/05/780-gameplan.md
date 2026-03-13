# Gameplan: API Endpoint Prefix Standardization

**Issue**: #780 (expanded scope)
**Date**: 2026-02-05
**Effort**: Medium (~1-2 hours)

---

## Phase -1: Infrastructure Verification

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI
- [x] Router pattern: `APIRouter(prefix="...")` in `web/api/routes/*.py`
- [x] Frontend: Jinja2 templates + vanilla JS with `fetch()` calls
- [x] Pre-commit hooks: Exist in `.pre-commit-config.yaml`

**My understanding of the task**:
- Fix 5 frontend files calling wrong API paths
- Migrate `/api/personality` router to `/api/v1/personality`
- Update all frontend calls to personality endpoints
- Add documentation to CLAUDE.md
- Add pre-commit hook to enforce convention

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**
- [x] Single agent, sequential work
- [x] Tightly coupled files (router + all callers must change together)
- [ ] Multiple agents working in parallel

**Assessment**: **SKIP WORKTREE** - Sequential work, atomic changes needed

---

## Phase 0: Audit & Inventory

### 0.1: Frontend calls to fix (wrong prefix)

| File | Line | Current | Target |
|------|------|---------|--------|
| `templates/home.html` | 1897 | `/api/conversations` | `/api/v1/conversations` |
| `web/assets/standup.html` | 407 | `/api/standup` | `/api/v1/standup` |
| `tests/fixtures/test_standup_output.html` | 50 | `/api/standup` | `/api/v1/standup` |
| `tests/fixtures/test_fixed_ui.html` | 50 | `/api/standup` | `/api/v1/standup` |
| `tests/fixtures/test_ui.html` | 50 | `/api/standup` | `/api/v1/standup` |

### 0.2: Personality router migration

**Router file**: `web/api/routes/personality.py`
- Current: `APIRouter(prefix="/api/personality", ...)`
- Target: `APIRouter(prefix="/api/v1/personality", ...)`

**Frontend callers to update**:

| File | Lines | Current | Target |
|------|-------|---------|--------|
| `templates/personality-preferences.html` | 448, 580, 619 | `/api/personality/...` | `/api/v1/personality/...` |
| `web/assets/personality-preferences.html` | 397, 525, 561 | `/api/personality/...` | `/api/v1/personality/...` |

### 0.3: Verify no other callers

Need to grep for any other `/api/personality` references before migration.

---

## Phase 1: Fix Wrong Endpoint Paths

### 1.1: Fix history sidebar (#780 original bug)
- File: `templates/home.html`
- Change: `/api/conversations` → `/api/v1/conversations`

### 1.2: Fix standup endpoints
- Files: `web/assets/standup.html`, 3 test fixtures
- Change: `/api/standup` → `/api/v1/standup`

### Verification
- Start server
- Load home page, check console for 404 errors
- Verify history sidebar loads

---

## Phase 2: Migrate Personality Router

### 2.1: Update router prefix
- File: `web/api/routes/personality.py`
- Change: `prefix="/api/personality"` → `prefix="/api/v1/personality"`

### 2.2: Update all frontend callers
- `templates/personality-preferences.html` (3 locations)
- `web/assets/personality-preferences.html` (3 locations)

### 2.3: Search for any other callers
```bash
grep -r "/api/personality" --include="*.html" --include="*.js" --include="*.py"
```

### Verification
- Load personality preferences page
- Verify API calls succeed (no 404)
- Check all 3 operations: load, save, enhance

---

## Phase 3: Documentation Update

### 3.1: Update CLAUDE.md

Add to "CRITICAL PATHS" or create new "API Conventions" section:

```markdown
## API Conventions

- **All API endpoints use `/api/v1/` prefix**
- When adding new routes: `APIRouter(prefix="/api/v1/yourroute", ...)`
- When calling from frontend: `fetch('/api/v1/...')`
- Exceptions (no /api prefix): `/auth`, `/setup`, `/loading`
```

---

## Phase 4: Pre-commit Hook

### 4.1: Create hook script

Create `scripts/check-api-paths.sh`:
```bash
#!/bin/bash
# Check for fetch() calls to /api/ without v1 prefix
# Allowlist: /api/v1/ (correct), /api/personality (if not migrated)

ERRORS=$(grep -rn "fetch(['\"]\/api\/[^v]" --include="*.html" --include="*.js" \
  | grep -v "/api/v1/" \
  | grep -v "node_modules" \
  | grep -v ".git")

if [ -n "$ERRORS" ]; then
  echo "ERROR: Found fetch() calls to /api/ without v1 prefix:"
  echo "$ERRORS"
  echo ""
  echo "All API calls should use /api/v1/ prefix."
  exit 1
fi
exit 0
```

### 4.2: Add to .pre-commit-config.yaml

```yaml
- repo: local
  hooks:
    - id: check-api-paths
      name: Check API endpoint paths use /api/v1/
      entry: scripts/check-api-paths.sh
      language: script
      files: \.(html|js)$
```

### Verification
- Run `pre-commit run check-api-paths --all-files`
- Should pass after all fixes applied
- Should fail if wrong path introduced

---

## Phase Z: Final Verification

### Checklist
- [ ] All 5 original wrong paths fixed
- [ ] Personality router migrated to `/api/v1/personality`
- [ ] All personality frontend callers updated
- [ ] No 404 errors in browser console on:
  - [ ] Home page (history sidebar)
  - [ ] Personality preferences page
- [ ] CLAUDE.md updated with API convention
- [ ] Pre-commit hook added and passing
- [ ] All changes committed with clear message

### Test Commands
```bash
# Verify no remaining wrong paths
grep -rn "fetch(['\"]\/api\/[^v]" --include="*.html" --include="*.js" | grep -v "/api/v1/"

# Run pre-commit
pre-commit run check-api-paths --all-files

# Start server and manually verify
python main.py
# Browse to localhost:8001, check console
# Browse to personality preferences, check console
```

---

## STOP Conditions

- Any endpoint returns 404 after migration
- Pre-commit hook has false positives on legitimate patterns
- Discovered additional callers not in inventory

---

## Rollback Plan

If issues discovered after commit:
1. `git revert HEAD` to undo changes
2. Investigate which caller was missed
3. Re-do with complete inventory

---

## Files to Modify (Summary)

| File | Change |
|------|--------|
| `templates/home.html` | Fix `/api/conversations` |
| `web/assets/standup.html` | Fix `/api/standup` |
| `tests/fixtures/test_standup_output.html` | Fix `/api/standup` |
| `tests/fixtures/test_fixed_ui.html` | Fix `/api/standup` |
| `tests/fixtures/test_ui.html` | Fix `/api/standup` |
| `web/api/routes/personality.py` | Migrate prefix |
| `templates/personality-preferences.html` | Update 3 paths |
| `web/assets/personality-preferences.html` | Update 3 paths |
| `CLAUDE.md` | Add API convention |
| `scripts/check-api-paths.sh` | NEW: Hook script |
| `.pre-commit-config.yaml` | Add hook |

**Total**: 11 files (10 modified, 1 new)
