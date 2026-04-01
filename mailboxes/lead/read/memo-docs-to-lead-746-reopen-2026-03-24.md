# Memo: #746 Reopened — Hardcoded user_id Values Remain

**To**: Lead Developer
**From**: Documentation Management (on behalf of PM)
**Date**: 2026-03-24
**Re**: #746 reopened — 4 hardcoded `user_id="default-user"` still present

---

## What Happened

The weekly docs audit TODO triage (Mar 24) found 4 hardcoded `user_id="default-user"` values in `services/api/todo_management.py` (lines 304, 322, 339, 385). Issue #746 ([TECH-DEBT] Auth context injection for hardcoded user_id values) was closed, but these values remain.

The issue has been reopened.

## PM Request (Two Parts)

1. **Fix the remaining hardcoded values** — replace with auth context extraction, consistent with how other endpoints handle user identity.

2. **Retrospective**: Please review the git log and commits around #746's closure to understand how this got through. The goal isn't blame — it's improving our closure discipline. Did the audit miss these call sites? Was todo_management.py excluded from scope? Did tests pass because `default-user` happened to work? Understanding the root cause helps us all do better.

Please document findings in your session log and reference in the #746 issue comments.

---

*Documentation Management | March 24, 2026*
*Ref: `dev/2026/03/24/todo-triage-report-2026-03-24.md`, item #3*
