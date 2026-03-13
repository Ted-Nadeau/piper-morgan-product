# Gameplan: #795 - uvloop Windows PEP 508 Fix

**Issue**: [SETUP] uvloop fails to install on Windows - use PEP 508 environment markers
**Priority**: BLOCKER
**Estimated Time**: 15 minutes
**Type**: Simple dependency fix

---

## Phase -1: Infrastructure Verification

### Current Understanding
- **File to modify**: `requirements.txt`
- **Change**: Add PEP 508 platform marker to uvloop line
- **Risk**: Low - only affects which platforms install uvloop

### Verification
```bash
grep uvloop requirements.txt
# Expected: uvloop==0.21.0 (without platform marker)
```

### Work Characteristics
- [x] Single agent, sequential work
- [x] Small fix (<15 min)
- [x] Single file change
- **Assessment**: SKIP WORKTREE - trivial fix

---

## Phase 0: Investigation

### Verify Current State
1. Confirm uvloop in requirements.txt without marker
2. Verify uvloop is used in codebase (to confirm it's needed on non-Windows)

### Root Cause
uvloop is a Unix-only high-performance event loop. It's imported conditionally at runtime but unconditionally required at install time.

---

## Phase 1: Implementation

### Change Required
```
# Before:
uvloop==0.21.0

# After:
uvloop==0.21.0; sys_platform != 'win32'
```

### Verification
1. Syntax check: pip can parse the modified requirements.txt
2. Codebase check: Confirm uvloop usage is also platform-conditional

---

## Phase Z: Completion

### Acceptance Criteria (from issue)
- [ ] requirements.txt updated with platform marker
- [ ] Windows user can complete `pip install -r requirements.txt`
- [ ] Linux/Mac installs still get uvloop

### Evidence Required
- Modified requirements.txt content
- `pip install -r requirements.txt --dry-run` on non-Windows shows uvloop
- Code path check showing uvloop is conditionally imported

---

## Phases NOT Applicable

The following gameplan phases are N/A for this fix:
- Phase 0.5 (Frontend-Backend Contract): No UI involved
- Phase 0.6 (Data Flow): No data propagation
- Phase 0.7 (Conversation Design): No conversation flow
- Phase 0.8 (Post-Completion Integration): No state changes

---

## STOP Conditions
- If uvloop is unconditionally imported at startup → need code changes too
- If other Windows-incompatible dependencies exist → file new issue
