# Memo: API Serialization Pattern Decision

**From**: Lead Developer
**To**: Chief Architect
**Date**: 2026-01-27
**Re**: API route serialization pattern - situational awareness

---

## Context

During #708 (MUX-LIFECYCLE-UI-TODOS) planning, I discovered an architectural pattern worth your awareness.

## Discovery

Both `todos.py` and `projects.py` API routes use **inline dict construction** rather than calling the domain model's `to_dict()` method:

```python
# Current pattern in list_todos() - lines 246-258
return {
    "todos": [
        {
            "id": t.id,
            "text": t.title,
            "status": t.status,
            "priority": t.priority,
            "owner_id": t.owner_id,
            "created_at": t.created_at.isoformat() if t.created_at else None,
        }
        for t in todos
    ],
}
```

Meanwhile, `Todo.to_dict()` exists and returns 30+ fields with full serialization.

## Decision Made

For #708, PM and I chose **Option A** (minimal change):
- Add `lifecycle_state` to the inline dict in the API
- Don't refactor to use `to_dict()`

**Rationale**:
1. Todos use a hybrid model (simple status + optional lifecycle) - novel adaptation
2. Keep #708 focused on lifecycle wiring, not API refactoring
3. `projects.py` uses same inline pattern - changing one creates inconsistency
4. Larger refactor should be a separate, deliberate decision

## Question for Future

Is the inline dict pattern intentional (selective field exposure, performance) or technical debt?

If we want to standardize on `to_dict()` for API responses:
- Would need to cover both `todos.py` and `projects.py`
- May affect frontend expectations (field names, field count)
- Would align with how `personality.py` uses `config.to_dict()`

No action required now - just wanted you to have visibility on this pattern divergence.

---

*Reference: Session log `dev/active/2026-01-27-0708-lead-code-opus-log.md`*
