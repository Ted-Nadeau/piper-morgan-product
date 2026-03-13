# Five Whys Analysis: Wrong API Endpoint Prefix (#780)

**Date**: 2026-02-05
**Problem**: History sidebar calls `/api/conversations` instead of `/api/v1/conversations`

---

## The Five Whys

### Why #1: Why is the endpoint path wrong in the history sidebar?

The developer wrote `/api/conversations` instead of `/api/v1/conversations`.

### Why #2: Why did the developer use the wrong path?

**Finding**: There's inconsistency in the codebase itself. Router prefixes are inconsistent:

| Pattern | Count | Examples |
|---------|-------|----------|
| `/api/v1/*` | 17 | conversations, standup, todos, projects, etc. |
| `/api/*` (no v1) | 1 | personality |
| `/*` (no api) | 4 | /auth, /setup, /conversation, /loading |

The developer may have looked at `/api/personality` as a reference and assumed no v1 was needed, OR just guessed without checking.

### Why #3: Why is there inconsistency in the router prefixes?

**Finding**: The API specification clearly states `Base URL: http://localhost:8001/api/v1` but:
1. The personality router was created without v1: `/api/personality`
2. Some utility routes intentionally skip it: `/auth`, `/setup`, `/loading`
3. No pre-commit hook or linter enforces the convention

### Why #4: Why wasn't the convention enforced?

1. **No automated check**: No pre-commit hook validates API path conventions
2. **No code review caught it**: The release commit (e93479b6) bundled many changes
3. **Documentation exists but isn't referenced**: `api-specification.md` says `/api/v1` but developers don't always check

### Why #5: Why don't developers check the documentation/existing patterns?

1. **Time pressure**: Bug fixes during alpha testing prioritize speed
2. **No explicit instruction**: CLAUDE.md and briefings don't mention "always use /api/v1"
3. **Inconsistent examples**: When developers DO look at existing code, they may find `/api/personality` (wrong) instead of `/api/v1/conversations` (right)

---

## Root Causes Identified

1. **Inconsistent existing code** - `/api/personality` router doesn't follow the convention
2. **No automated enforcement** - No hook/lint to catch wrong prefixes
3. **Documentation not surfaced** - API spec exists but isn't in agent briefings

---

## Bugs Found (Same Root Cause)

| File | Line | Wrong | Correct |
|------|------|-------|---------|
| `templates/home.html` | 1897 | `/api/conversations` | `/api/v1/conversations` |
| `web/assets/standup.html` | 407 | `/api/standup` | `/api/v1/standup` |
| `tests/fixtures/test_standup_output.html` | 50 | `/api/standup` | `/api/v1/standup` |
| `tests/fixtures/test_fixed_ui.html` | 50 | `/api/standup` | `/api/v1/standup` |
| `tests/fixtures/test_ui.html` | 50 | `/api/standup` | `/api/v1/standup` |

**Note**: The `/api/personality` calls are actually correct because that router genuinely uses `/api/personality` (though this is itself inconsistent with the spec).

---

## Recommended Fixes

### Immediate (Fix the bugs)
1. Fix all 5 wrong endpoint paths listed above

### Short-term (Prevent recurrence)
2. Add to CLAUDE.md or agent briefings: "All API endpoints use `/api/v1/` prefix"
3. Consider: Should `/api/personality` be migrated to `/api/v1/personality` for consistency?

### Medium-term (Automated enforcement)
4. Add pre-commit hook to flag `fetch('/api/` without `v1` (with allowlist for exceptions)

---

## Decision Needed from PM

1. **Scope of this fix**: Just the 5 bugs, or also migrate `/api/personality` to `/api/v1/personality`?
2. **Documentation update**: Should we add API convention to CLAUDE.md?
3. **Pre-commit hook**: Worth the effort for a ~20 endpoint codebase?
