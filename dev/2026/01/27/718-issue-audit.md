# Audit: Issue #718 against bug_report_alpha.md

**Issue**: BUG: lifecycle_state columns missing from database tables
**Template**: `.github/ISSUE_TEMPLATE/bug_report_alpha.md`

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Bug Description | ✅ | Clear problem statement with table showing affected models |
| Steps to Reproduce | ⚠️ | Missing - no explicit steps to reproduce |
| Expected Behavior | ⚠️ | Implicit (columns should exist) but not explicit section |
| Actual Behavior | ✅ | Clear: "none of the corresponding database tables have the column" |
| Environment | N/A | Internal bug, not user-facing - environment not relevant |
| Screenshots/Logs | ⚠️ | No evidence of missing columns (e.g., `\d table_name` output) |
| Severity | ✅ | P2, blocks manual testing - functionally "Major" |
| Additional Context | ✅ | Root cause analysis via Five Whys |

## Additional Quality Checks (Beyond Template)

| Element | Status | Notes |
|---------|--------|-------|
| Priority specified | ✅ | P2 |
| Labels appropriate | ✅ | bug, component: database |
| Milestone set | ✅ | MVP |
| Related issues linked | ✅ | #433, #708, #709 |
| Root cause analysis | ✅ | Five Whys completed |
| Requirements clear | ✅ | Two phases with checkboxes |
| Acceptance criteria | ✅ | 5 criteria |
| STOP conditions | ✅ | 3 conditions specified |

## Items Requiring Fix

### 1. Steps to Reproduce (⚠️)
**Current**: Missing
**Required**: Add explicit steps showing how the bug manifests

**Suggested addition**:
```markdown
## Steps to Reproduce

1. Apply all current migrations: `alembic upgrade head`
2. Connect to database: `docker exec -it piper-postgres psql -U piper -d piper_morgan`
3. Check for column: `\d projects`
4. Observe: no `lifecycle_state` column exists
5. Try to set lifecycle_state on a Project in Python
6. Observe: value not persisted to database
```

### 2. Expected Behavior (⚠️)
**Current**: Implicit
**Required**: Explicit statement

**Suggested addition**:
```markdown
## Expected Behavior

- All four tables (features, work_items, projects, todo_items) should have a `lifecycle_state` column
- Setting `model.lifecycle_state = LifecycleState.ACTIVE` should persist to database
- UI lifecycle indicators should display correctly
```

### 3. Evidence/Logs (⚠️)
**Current**: Missing
**Recommended**: Add database inspection output

**Suggested addition**:
```markdown
## Evidence

```sql
piper_morgan=# \d projects
                                      Table "public.projects"
    Column     |           Type           | ...
---------------+--------------------------+-----
 id            | uuid                     |
 name          | character varying(200)   |
 description   | text                     |
 ...
-- NOTE: No lifecycle_state column present
```
```

## Summary

**Overall Assessment**: Issue is well-structured with good root cause analysis and clear requirements. Missing 3 template sections that should be added for completeness.

**Action Required**:
1. Add Steps to Reproduce section
2. Add Expected Behavior section
3. Add Evidence section with `\d table_name` output

**Recommendation**: These are documentation gaps, not blockers. The issue is clear enough to implement. Suggest updating issue description to add missing sections, OR proceed with implementation since requirements are unambiguous.

---

*Audit completed: 2026-01-27*
*Auditor: Lead Developer*
