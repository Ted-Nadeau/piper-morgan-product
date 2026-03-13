# Audit: #749 Issue against bug_report_alpha.md

**Date**: 2026-02-01
**Issue**: #749 - BUG: Knowledge graph entity query fails with type mismatch
**Template**: `.github/ISSUE_TEMPLATE/bug_report_alpha.md`

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Bug Description | ✅ | Clear description with error message |
| Steps to Reproduce | ❌ | Missing - not specified how to trigger |
| Expected Behavior | ❌ | Missing - not stated explicitly |
| Actual Behavior | ⚠️ | Partially covered in "Impact" section |
| Environment (Browser/OS/Version) | ❌ | Missing - not specified |
| Screenshots/Logs | ✅ | Error log included in body |
| Severity | ⚠️ | "Medium" stated but not using template checkbox format |
| Additional Context | ⚠️ | "Observed In" and "Likely Fix" partially cover this |
| Labels | ❌ | No labels applied (should have bug, alpha-testing) |

## Summary

- ✅ Present: 2
- ⚠️ Partial: 3
- ❌ Missing: 4

## Required Fixes

### 1. Add Steps to Reproduce
Need to specify how to trigger this error:
- What user action causes entity query?
- Is it during specific intent types?
- How to observe the error (terminal output)?

### 2. Add Expected Behavior
"Entity queries should return matching knowledge graph nodes to enrich intent context"

### 3. Add Actual Behavior (explicit)
"Entity query fails with type mismatch error. Processing continues but without entity context."

### 4. Add Environment
- Server-side bug, so browser/OS less relevant
- Should note: PostgreSQL version, SQLAlchemy version

### 5. Fix Severity Format
Use template checkbox format:
- [ ] Blocker
- [ ] Major
- [x] Minor (workaround: processing continues without entity context)
- [ ] Enhancement

### 6. Add Labels
Should apply: `bug` (at minimum)

---

## Updated Issue Body (Proposed)

```markdown
## Bug Description

During intent processing, an entity query fails with a PostgreSQL type mismatch error:

```
Entity query failed: (sqlalchemy.dialects.postgresql.asyncpg.ProgrammingError)
<class 'asyncpg.exceptions.UndefinedFunctionError'>: operator does not exist: character varying = nodetype
HINT: No operator matches the given name and argument types. You might need to add explicit type casts.
[SQL: SELECT ... FROM knowledge_nodes WHERE knowledge_nodes.node_type = $1::nodetype LIMIT $2::INTEGER]
[parameters: ('PERSON', 5)]
```

## Steps to Reproduce

1. Start the server with `python main.py`
2. Send any message that triggers intent processing (e.g., "add todo: test task")
3. Observe terminal output - entity query error appears during processing
4. Note: The main operation succeeds, but entity enrichment fails silently

## Expected Behavior

Entity queries should successfully return matching knowledge graph nodes to enrich intent context with relevant entities (people, projects, etc.).

## Actual Behavior

Entity query fails with type mismatch error. The SQLAlchemy model defines `node_type` as an enum (`nodetype`), but the query passes a string value `'PERSON'` without proper type casting. PostgreSQL can't compare `character varying` with the custom `nodetype` enum.

Processing continues but without entity context enrichment.

## Environment

- **PostgreSQL**: (version from docker-compose)
- **SQLAlchemy**: 2.x with asyncpg
- **Server-side**: Python 3.12

## Screenshots/Logs

See error message in Bug Description above.

## Severity

- [ ] Blocker - Can't continue testing
- [ ] Major - Significant impact on functionality
- [x] Minor - Workaround exists (processing continues without entity context)
- [ ] Enhancement - Not really a bug, but could be improved

## Additional Context

- Observed during todo creation testing, but unrelated to todo functionality
- Knowledge graph features that depend on entity context are affected
- Graceful degradation is working (no crash, just missing enrichment)

## Likely Fix

Either:
1. Cast the parameter to the enum type in the query
2. Use the SQLAlchemy enum properly in the filter
3. Ensure the model's enum type matches the database enum
```

---

## Status: NEEDS FIXES BEFORE GAMEPLAN

Apply fixes above, then this issue is ready for gameplan phase.
